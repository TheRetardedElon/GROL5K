# GROL5K Upstream Baseline

GROL5K is a downstream operating-system project derived from Home Assistant Operating System.

## Current baseline

- Upstream repository: `home-assistant/operating-system`
- Upstream branch: `dev`
- Pinned baseline commit: `3019c7fe8745900a3e9dcb3879d96bacf7958543`
- Baseline commit subject: `Linux: Update kernel to 6.18.52 (#5012)`
- GROL bootstrap branch: `grol/bootstrap-v0.1`

## Upstream policy

GROL5K should preserve a clean relationship with HAOS so that kernel, Buildroot, driver, security, bootloader, RAUC, container-runtime, and hardware-support changes can be reviewed and imported deliberately.

Rules:

1. Never erase upstream history.
2. Keep GROL-specific changes isolated and documented.
3. Prefer additive GROL packages, overlays, services, and target definitions over invasive edits.
4. Record any compatibility-sensitive divergence in an ADR.
5. Before rebasing or merging upstream, build and test the current GROL baseline.
6. After importing upstream changes, rerun boot, update, rollback, container, network, storage, and AI-control-plane tests.

## Compatibility boundary

The first milestones intentionally leave HAOS plumbing such as `BR2_EXTERNAL_HAOS_PATH`, Supervisor compatibility, OS Agent identifiers, partition labels, and update internals intact unless there is a concrete reason to change them.

Visible identity and GROL-owned services come first. Deep internal renaming comes later, after the system can build and boot reproducibly.
