# M1-B2 boot polish

Evidence from Build #7 booted in VirtualBox:

- GRUB timeout was 1 second, so `Grol5k.png` was effectively invisible
- systemd printed the full HAOS unit list on VGA
- console was taken by `ha-cli@` which auto-exec'd `hassio_cli`
- that container prints the upstream Home Assistant ASCII banner

## This tranche changes

- GRUB timeout 1 → 3 seconds (long enough to see the splash, short enough for QEMU)
- explicit `gfxmode=1024x768,800x600,auto` for VirtualBox
- menu titles prefixed `GROL5000` (slot logic / PARTUUIDs unchanged)
- kernel cmdline `quiet loglevel=3 systemd.show_status=auto`
- systemd `ShowStatus=auto`
- tty1 is a GROL status card + `grol >` prompt
- inherited HA CLI is opt-in: type `ha`

## Intentionally not changed

- `hassio_cli` container artwork (plugin-cli, pulled at runtime)
- `ha-cli@.service` still owns the VGA console (appliance behavior)
- RAUC A/B, Supervisor, OS Agent, `HAOS_ID`
- Home Assistant onboarding on :8123
