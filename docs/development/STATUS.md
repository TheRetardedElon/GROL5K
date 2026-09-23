# GROL5K Development Status

This file is the canonical short-form project handoff for humans and AI collaborators.

## Current state

- Project: **GROL5K / GROL5000**
- Base: Home Assistant Operating System
- Default branch: `dev`
- GROL version: `0.1.0-dev`
- Initial upstream baseline: `home-assistant/operating-system@3019c7fe8745900a3e9dcb3879d96bacf7958543`
- Current phase: **M1 identity — tranche A implementation**
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
- architecture decision records 0001–0003
- GROL foundation guardrails and CI workflow
- build-record evidence generator
- AI provider adapter contract, including xAI annex
- Grok Bot runtime, Host API, tool-injection threat model, and voice/realtime specs
- v0.3 adversarial review edits: state ownership, Host API isolation, provider-hosted tool ban, confirmation digests, EROFS correction
- v0.4 GPT follow-up: explicit HA entity-level mutation policy, scripts/scenes disabled in v0, dedicated `grol-hostd`, socket ownership clarified

## M0 attempt history

- OS build #1/#2 reached the inherited builder-image step and failed before any OS compilation.
- Root cause: GHCR/Docker repository names must be lowercase, while `github.repository_owner` resolves to `TheRetardedElon`.
- Repository rename to lowercase does not change the owner login value used by the workflow.
- Fix: normalize the GHCR owner to lowercase before constructing `ghcr.io/<owner>/haos-builder`.
- This is a build-workflow portability bug, not an OS/runtime failure and does not count as an M0 build attempt reaching Buildroot.

## M0 result

**PASS** — OS build #3 completed successfully from `dev@b2575b25cf6ae27387ffef2c82fe1d970205ab9d`.

- OVA Buildroot build: PASS
- Linux config validation: PASS
- OVA/QCOW2/RAUC/VDI/VMDK/VHDX artifacts: generated
- QEMU integration test job: PASS
- logs + JUnit reports: archived
- evidence: `docs/build-records/M0-2026-09-23-ova.md`

## M1 validation attempt history

- **OS build #4**: OVA build and Linux config validation passed; QEMU test harness failed before shell access.
- Root cause: inherited `tests/qemu-strategy.yaml` hard-coded `homeassistant login: `, while M1 correctly changed the hostname/login prompt to `grol5000 login: `.
- This was a test-harness compatibility failure, not evidence that the M1 image failed to build.
- Fix: accept both upstream and GROL login prompts in the QEMU strategy and add explicit GROL identity assertions.

## Immediate priorities

1. Begin M1 visible identity changes on a dedicated branch.
2. Change only safe presentation/identity surfaces first: hostname, issue/banner, MOTD, visible OS name, OVA product metadata, and boot presentation.
3. Preserve Supervisor, OS Agent, RAUC compatibility, partition labels, `HAOS_ID`, and `haos-*` internal service names during early M1.
4. Rebuild the OVA and rerun the same QEMU integration tests after each meaningful identity tranche.
5. M2 host services come before M3/M4 AI runtime code.

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
