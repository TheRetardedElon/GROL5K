# M1-B2 boot polish

Evidence from Build #7 booted in VirtualBox:

- GRUB timeout was 1 second, so `Grol5k.png` was effectively invisible
- systemd printed the full HAOS unit list on VGA
- console was taken by `ha-cli@` which execs `hassio_cli`
- that container still prints the upstream Home Assistant ASCII banner

## This tranche changes

- GRUB timeout 1 → 8 seconds
- explicit `gfxmode=1024x768,800x600,auto` for VirtualBox
- menu titles prefixed `GROL5000` (slot logic / PARTUUIDs unchanged)
- kernel cmdline `quiet loglevel=3 systemd.show_status=auto`
- systemd `ShowStatus=auto`
- `haos-cli` wait screen is GROL-branded

## Intentionally not changed

- `hassio_cli` container artwork (plugin-cli, pulled at runtime)
- `ha-cli@.service` still owns the VGA console (appliance behavior)
- RAUC A/B, Supervisor, OS Agent, `HAOS_ID`

The HA cow on `ha >` goes away only when we ship a GROL-owned CLI plugin or stop auto-attaching VGA to `hassio_cli`. That is M5, not M1-B2.
