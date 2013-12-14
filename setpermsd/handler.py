from os.path import dirname, isdir, join as path_join
from pyinotify import ProcessEvent
from grp import getgrnam as get_group_entry_by_name, getgrgid
from pwd import getpwnam as get_passwd_entry_by_name, getpwuid
import os
import sys

class FixPermsHandler(ProcessEvent):
    _path_rules = {}
    _log_handle = None
    _debug_enabled = False

    def process_default(self, event):
        fn = path_join(event.path, event.name)
        found_rule, path, chown, chmod, recursive = self._find_rule(fn)
        is_file = True

        if fn[-1] == '/':
            self._log_write('Deleted directory? %s' % (fn,), debug=True)
            return

        if not found_rule:
            self._log_write('No rule for %s' % (fn,))
            return

        needs_recursion = len(fn.split('/')) - len(path.split('/')) != 1

        if needs_recursion:
            if not recursive:
                self._log_write('Not setting due to recursive being set to '
                                'False', debug=True)
                return

            self._log_write('recursive = True, setting for %s' % (fn,),
                            debug=True)
        else:
            self._log_write('Not recursive, using rule', debug=True)

        if not isdir(fn):
            self._log_write('%s is a file' % (fn,), debug=True)
            chmod_rule = chmod['files']
        else:
            self._log_write('%s is a directory' % (fn,), debug=True)
            chmod_rule = chmod['directories']
            is_file = False

        chmod_rule_str = oct(chmod_rule).replace('0o', '0')

        self._log_write('chmod = %s, chown = %s' % (chmod_rule_str, chown,),
                        debug=True)

        if chown is not None:
            uid = gid = None
            name = group = 'none'

            try:
                user_entry = get_passwd_entry_by_name(chown['name'])
                uid = user_entry[2]
                name = user_entry[0]
            except KeyError:
                self._log_write('No entry for user name %s in /etc/passwd' % (
                    chown['name'],
                ), debug=True)
                uid = os.stat(fn).st_uid

            try:
                group_entry = get_group_entry_by_name(chown['group'])
                gid = group_entry[2]
                group = group_entry[0]
            except KeyError:
                self._log_write('No group entry for group %s in /etc/group' % (
                    chown['group'],
                ), debug=True)

                if uid:
                    self._log_write('Using user\'s GID')
                    gid = user_entry[3]
                    group = getgrgid(gid)[0]

            self._log_write('Setting ownership to %d:%d' % (
                uid,
                gid,
            ), debug=True)
            self._log_write('chown %s:%s %s' % (name, group, fn,))
            os.chown(fn, uid, gid)
        else:
            self._log_write('No user/group setting for %s' % (fn,), debug=True)

        if type(chmod_rule) is not int:
            self._log_write('Not setting mode because rule is not numeric', debug=True)
            return

        if is_file and os.access(fn, os.X_OK):
            self._log_write('Not setting mode rule because file is executable', debug=True)
            return

        self._log_write('Setting mode to %s' % (chmod_rule_str,), debug=True)
        self._log_write('chmod %s %s' % (chmod_rule_str, fn,))
        os.chmod(fn, chmod_rule)

    def _find_rule(self, dir_name):
        default_return = (False, None, None, False,)
        back_counts = 0

        while True:
            try:
                chown, chmod, recursive = self._path_rules[dir_name]
                self._log_write('Found rule for %s (recursive = %s)'  % (dir_name, recursive,), debug=True)

                return (
                    True,
                    dir_name,
                    chown,
                    chmod,
                    recursive,
                )
            except KeyError:
                last_dir = dir_name
                dir_name = dirname(dir_name)
                back_counts += 1

                if dir_name == '/':
                    break

                self._log_write('New directory name (.. count = %d): %s' % (back_counts, dir_name), debug=True)

        return default_return

    def _log_write(self, string, debug=False):
        if debug and not self._debug_enabled:
            return

        if not self._log_handle:
            print('No log handle')
            return

        string += '\n'
        self._log_handle.write(string)
        self._log_handle.flush()

    def add_path_rule(self, path, chown, chmod, recursive):
        self._path_rules[path] = (chmod, chown, recursive,)

    def reset(self):
        self._path_rules = []

    def set_log_handle(self, log_handle):
        self._log_handle = log_handle
