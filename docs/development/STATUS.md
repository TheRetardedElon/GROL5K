# GROL5K Development Status

This file is the canonical short-form project handoff for humans and AI collaborators.

## Current state

- Project: **GROL5K / GROL5000**
- Base: Home Assistant Operating System
- Default branch: `dev`
- GROL version: `0.1.0-dev`
- Initial upstream baseline: `home-assistant/operating-system@3019c7fe8745900a3e9dcb3879d96bacf7958543`
- Current phase: **Foundation / M0 preparation**
- Primary validation target: **OVA / QEMU**
- First physical target: **generic x86-64 UEFI**
- Later target: **Raspberry Pi 5**

## What has been established

- GROL repository and upstream lineage
- GROL project README and branding
- architecture overview
- AI control-plane concept
- security model
- upstream sync policy
- development roadmap
- initial build documentation
- first architecture decision record
- GROL foundation guardrails and CI workflow
- build-record evidence generator
- initial AI provider adapter contract

## Immediate priorities

1. Reproduce the unmodified upstream OVA build.
2. Boot and validate the image in QEMU.
3. Record hashes, host details, logs, and test results.
4. Only after M0 passes, begin M1 visible identity changes.
5. Keep Supervisor, OS Agent, RAUC compatibility, partition labels, and `haos-*` internal service names intact during early M1.

## Current M1 identity candidates

Low-risk visible surfaces already located:

- `buildroot-external/configs/ova_defconfig`
  - `BR2_TARGET_GENERIC_HOSTNAME`
  - `BR2_TARGET_GENERIC_ISSUE`
- `buildroot-external/configs/generic_x86_64_defconfig`
  - same two fields
- `buildroot-external/rootfs-overlay/etc/motd`
- `buildroot-external/scripts/post-build.sh` generated `os-release`
- `buildroot-external/meta` `HAOS_NAME` (candidate; compatibility review required)
- `buildroot-external/board/pc/ova/home-assistant.ovf` visible VM/product naming
- GRUB presentation in `buildroot-external/board/pc/grub.cfg`

## Important compatibility warning

`HAOS_ID` is not just branding. It participates in image naming and RAUC compatibility through `scripts/name.sh`. Do **not** rename it casually.

The same rule applies to:

- `BR2_EXTERNAL_HAOS_PATH`
- `BR2_PACKAGE_HASSIO_*`
- Supervisor machine IDs
- OS Agent board IDs
- `haos-*` systemd unit names
- partition identities
- RAUC compatible strings

## Collaboration rule

Update this file whenever a milestone changes state, an architectural decision is accepted, or a handoff to another developer/model occurs.
