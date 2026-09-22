# GROL5K Codebase Map

This map classifies the inherited HAOS tree by how GROL5K should treat it during early development.

## 1. Build orchestration

### Root `Makefile`

Discovers targets from `buildroot-external/configs/*_defconfig`.

**Policy:** KEEP initially. Future GROL targets can be added without rewriting the root build entry point.

### `Dockerfile`

Build environment for HAOS development.

**Policy:** KEEP during M0; review only when GROL needs its own pinned builder image.

### `.gitmodules`

Tracks the HAOS Buildroot fork.

**Policy:** KEEP. Forking Buildroot is a later decision, not an M1 requirement.

## 2. Buildroot external tree

### `buildroot-external/configs/`

Board/target defconfigs. OVA and generic x86-64 currently set hostname, issue/banner, Supervisor machine/arch identifiers, OS Agent board identifiers, kernel and firmware configuration.

**Policy:** REBRAND only visible identity fields in M1. Preserve compatibility identifiers.

### `buildroot-external/meta`

Owns OS version, `HAOS_NAME`, `HAOS_ID`, and deployment channel.

**Policy:** SPLIT CONCEPTUALLY.

`HAOS_NAME` is a candidate for visible GROL identity after M0.  
`HAOS_ID` is compatibility-sensitive and must remain `haos` initially.

### `buildroot-external/scripts/post-build.sh`

Generates `/usr/lib/os-release` from metadata and board data, then configures RAUC.

**Policy:** EXTEND CAREFULLY.

### `buildroot-external/scripts/name.sh`

Controls artifact names, version formatting, and RAUC compatibility. It derives image names from HAOS_ID + board ID and derives RAUC compatibility from the same identifier.

**Policy:** DEFER renaming. This is release/update plumbing.

### `buildroot-external/scripts/post-image.sh`

Creates disk/OTA artifacts after board hooks.

**Policy:** KEEP for M0/M1.

## 3. PC / virtual targets

### `buildroot-external/board/pc/grub.cfg`

Implements A/B slot selection, retry counters, rescue entries, kernel arguments, and RAUC slot selection.

**Policy:** KEEP boot logic. M1 may alter presentation only after confirming GRUB graphics/module requirements.

### `buildroot-external/board/pc/ova/home-assistant.ovf`

Contains visible VM identity including Home Assistant names and VirtualBox VM metadata. It also references `home-assistant.vmdk`.

**Policy:** REBRAND visible metadata only after verifying generated VMDK/OVA filename coupling.

### Board `meta` files

Contain board IDs, names, bootloader, Supervisor machine, and architecture.

**Policy:** KEEP internal board IDs through early milestones.

## 4. Root filesystem overlay

### `buildroot-external/rootfs-overlay/etc/motd`

Currently greets users with Home Assistant OS branding.

**Policy:** SAFE M1 REBRAND.

### `buildroot-external/rootfs-overlay/usr/lib/systemd/system/haos-*`

HAOS system services for data, overlay, Supervisor, AppArmor, swap, expansion, wipe, and more.

**Policy:** KEEP names and behavior initially.

### `buildroot-external/rootfs-overlay/usr/libexec/haos-*`

Implementation scripts backing HAOS units.

**Policy:** KEEP initially.

## 5. Home Assistant compatibility packages

### `buildroot-external/package/hassio/`

Supervisor/bootstrap integration.

**Policy:** KEEP.

### `buildroot-external/package/os-agent/`

OS Agent package and board integration.

**Policy:** KEEP.

GROL-owned services should sit beside these before attempting to replace them.

## 6. Update system

Relevant areas include `buildroot-external/ota/`, `buildroot-external/scripts/rauc.sh`, generated RAUC config, and A/B GRUB slot logic.

**Policy:** PRESERVE during M0-M5 unless a change is explicitly required and rollback-tested.

GROL-owned signing/release infrastructure belongs in M6.

## 7. CI / GitHub Actions

Inherited workflows still assume HAOS infrastructure and names, including `haos_*` artifacts, HAOS R2 storage, Home Assistant release helpers, upstream reusable workflows, and Home Assistant version channels.

**Policy:** DO NOT treat inherited release CI as GROL production CI.

For now:
- reuse local/build logic where practical
- avoid publishing to upstream infrastructure
- create GROL-specific CI/release workflows separately
- keep upstream workflows available as reference until replacement is proven

## 8. GROL-owned tree

`grol/` is where new GROL-specific work should live when it does not need to patch inherited platform code.

Planned ownership:

```text
grol/
├── branding/
├── policies/
├── release/
├── services/
└── specs/
```

This separation makes upstream syncs and code review easier.
