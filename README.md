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
