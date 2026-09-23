# GROL5K Development Roadmap

## M0 — Reproducible upstream baseline ✅ COMPLETE

M0 evidence: `docs/build-records/M0-2026-09-23-ova.md`

Exit criteria:

- clone with submodules
- build supported development target without GROL modifications
- boot successfully in QEMU/OVA
- capture build provenance
- document host requirements and commands

## M1 — Identity

Planned changes:

- GROL hostname/default identity
- console banner
- `os-release` / release metadata
- GROL artifact naming where safe
- GRUB/boot branding
- splash artwork
- GROL version metadata

No deep Supervisor, OS Agent, partition, or RAUC renaming yet.

## M2 — GROL system layer

Introduce:

- `grol-healthd`
- `grol-identity`
- `grol-provision`
- service health API
- GROL system information endpoint

## M3 — Grok

Introduce:

- `grol-ai-gateway`
- xAI configuration/provisioning
- streaming text
- realtime/voice path
- provider abstraction
- offline/error behavior

## M4 — Grok Bot

Introduce:

- persistent agent runtime
- structured tool contracts
- Action Broker
- policy engine
- audit trail
- confirmation flows

## M5 — GROL5000 experience

Introduce:

- branded first boot
- GROL setup
- primary dashboard
- Grok Bot surface
- system/update/recovery UI
- boot and error-state visuals

## M6 — Release system

Introduce:

- GROL-owned CI
- signed release artifacts
- dev/beta/stable channels
- RAUC signing ownership
- rollback qualification
- SBOM/provenance publication

## M7 — Hardware expansion

After x86/OVA stability:

- Raspberry Pi 5
- additional validated targets
- hardware-specific boot/driver qualification
