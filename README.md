# Deprecated

This utility is deprecated/abandoned in favour of "better planning" (deployment, etc). Please do not use.

# Notes

* This will never modify files that are already executable
* This is better run as root to ensure no errors
* Be very careful with what paths you put in configuration and the `recursive` option!

# Example configuration

## `/etc/setpermsd/conf.yml`

```yaml
log_file: /var/log/setpermsd.log
pid_file: /var/run/setpermsd.pid
```

## `/etc/setpermsd/paths.yml`

```yaml
'/home/tatsh/dev/sutra-cc':
    recursive: true
'/home/tatsh/nginx-needs-access':
    recursive: true
    chown:
        name: tatsh
        group: nginx
'/home/tatsh/should-be-executable.file':
    chmod: 0755
```
