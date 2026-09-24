# GROL5K Development Status

This file is the canonical short-form project handoff for humans and AI collaborators.

## Current state

- Project: **GROL5K / GROL5000**
- Base: Home Assistant Operating System
- Default branch: `dev`
- GROL version: `0.1.0-dev`
- Initial upstream baseline: `home-assistant/operating-system@3019c7fe8745900a3e9dcb3879d96bacf7958543`
- Current phase: **M1 identity — B1 built, visual inspect then M1-B2 polish**
- Primary validation target: **OVA / QEMU**
- First physical target: **generic x86-64 UEFI**
- Later target: **Raspberry Pi 5**

Product sentence: GROL5000 is a home OS you talk to. Grok Bot is the only mouth. Grok is the brain. Grok Build is a contractor in a locked room. Home Assistant is the wiring. The Action Broker is the fuse box.

Plan: `docs/architecture/GROK_BOT_PRODUCT_PLAN.md`

## What has been established

- GROL repository and upstream lineage
- GROL project README and branding
- architecture overview
- AI control-plane concept
- security model
- upstream sync policy
- development roadmap
- initial build documentation
- architecture decision records 0001–0004
- GROL foundation guardrails and CI workflow
- build-record evidence generator
- AI provider adapter contract, including xAI annex
- Grok Bot runtime, Host API, tool-injection threat model, and voice/realtime specs
- v0.3/v0.4 HA entity-level mutation policy and `grol-hostd`
- Bot/Build/voice product plan and Grok Build isolation ADR

## M0 result

**PASS** — OS build #3 from `dev@b2575b25`. Evidence: `docs/build-records/M0-2026-09-23-ova.md`.

## Immediate priorities

1. Human-boot the current M1-B1 OVA. Capture power-on, GRUB/splash, kernel text, `grol5000 login:`.
2. M1-B2 splash/GRUB/login polish only.
3. Rebuild OVA and rerun the QEMU suite plus GROL identity tests.
4. Do not start M3/M4 runtime until M1-B2 is accepted and M2 host sockets exist.
5. Keep Supervisor, OS Agent, RAUC compatibility, partition labels, `HAOS_ID`, and `haos-*` names intact.

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
