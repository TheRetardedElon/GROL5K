# M1 Identity Conversion Map

M1 makes a booted system visibly GROL5000 while preserving HAOS-compatible internals.

## Rule

**Change presentation first. Preserve plumbing.**

### Safe first wave

| Surface | File | Planned GROL identity | Risk |
|---|---|---|---|
| default hostname | `configs/ova_defconfig` | `grol5000` | Low |
| default hostname | `configs/generic_x86_64_defconfig` | `grol5000` | Low |
| console issue | same defconfigs | `Welcome to GROL5000` | Low |
| MOTD | `rootfs-overlay/etc/motd` | GROL5000 OS greeting | Low |
| project version marker | `GROL_VERSION` | retain GROL semver | Low |
| visible OS name | generated `os-release` | `GROL5000 OS` | Medium |
| OVA product strings | `board/pc/ova/home-assistant.ovf` | GROL5000 OS | Medium |

### Requires implementation review

#### `HAOS_NAME`

Defined in `buildroot-external/meta` and consumed by `post-build.sh` for `os-release`.

Likely M1 approach: show `GROL5000 OS` in visible name fields while retaining compatibility identifiers underneath.

#### `HOME_URL` and CPE name

`post-build.sh` currently writes Home Assistant URLs and a Home Assistant CPE namespace.

Do not invent final GROL values until project URLs and compatibility policy are decided.

#### OVA metadata

The OVF contains both visible names and the filename `home-assistant.vmdk`. Visible strings can be changed independently only after confirming the packaging hook's filename assumptions.

#### GRUB

Current PC GRUB config is primarily boot logic. A graphical splash/background may require additional GRUB modules/config changes.

Do not modify A/B selection, retry counters, PARTUUIDs, rescue logic, or RAUC slot arguments for branding.

## Explicitly deferred

Do **not** rename these in early M1:

- `HAOS_ID=haos`
- `BR2_EXTERNAL_HAOS_PATH`
- `BR2_PACKAGE_HASSIO_*`
- `SUPERVISOR_MACHINE`
- `SUPERVISOR_ARCH`
- OS Agent board IDs
- `haos-*.service`
- `haos-*` libexec tools
- RAUC compatible strings
- partition labels / UUID scheme
- inherited artifact prefix `haos_*` until GROL CI is ready

## M1 success condition

A user should see GROL5000 from boot/login/system information, while Home Assistant compatibility and A/B updates continue to work exactly as before.


## Tranche A implementation

Branch: `grol/m1-identity-core`

Changes in this tranche:

- OVA hostname: `homeassistant` → `grol5000`
- generic x86-64 hostname: `homeassistant` → `grol5000`
- console issue: `Welcome to GROL5000`
- MOTD: `GROL5000 OS`
- visible `os-release` name via `HAOS_NAME="GROL5000 OS"`
- visible `HOME_URL` points to the GROL5K repository
- OVA VM/product strings identify the appliance as GROL5000 OS

Intentionally unchanged:

- `HAOS_ID=haos`
- RAUC compatibility
- `haos_*` artifact prefix
- Supervisor machine/arch IDs
- OS Agent board IDs
- OVA internal file names `home-assistant.ovf` / `home-assistant.vmdk`
- GRUB A/B slot logic

### Validation gate

After merge, rerun the same OVA workflow used for M0 with tests enabled.

Tranche A is accepted only if:

1. OVA build passes,
2. QEMU integration suite passes,
3. visible identity checks confirm GROL5000,
4. compatibility-sensitive identifiers remain unchanged.
