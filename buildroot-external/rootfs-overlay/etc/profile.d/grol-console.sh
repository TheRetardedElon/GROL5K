#!/bin/sh
# GROL5000 appliance console helpers.
[ -n "$PS1" ] || return
PS1='grol > '

ha() {
    if ! command -v docker >/dev/null 2>&1; then
        echo 'docker is not available.'
        return 1
    fi
    if [ -z "$(docker ps -q -f name=hassio_cli 2>/dev/null)" ]; then
        echo 'hassio_cli is not running yet.'
        return 1
    fi
    docker container exec -ti hassio_cli /usr/bin/cli.sh
}

status() {
    ipaddr=$(ip -4 -o addr show scope global 2>/dev/null | awk '{print $4}' | cut -d/ -f1 | head -n1)
    [ -n "$ipaddr" ] || ipaddr=waiting
    printf '\n'
    printf '  GROL5000 OS\n'
    printf '  Global Robotic Overlord Logic\n'
    printf '\n'
    printf '  Network:     %s\n' "$ipaddr"
    if [ "$ipaddr" != waiting ]; then
        printf '  Web UI:      http://%s:8123\n' "$ipaddr"
    else
        printf '  Web UI:      http://<ip>:8123\n'
    fi
    printf '\n'
    printf '  ha      inherited Home Assistant CLI\n'
    printf '  status  reprint this card\n'
    printf '\n'
}
