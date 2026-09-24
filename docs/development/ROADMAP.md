# GROL5K Development Roadmap

Canonical product intent for Bot / Build / voice:
`docs/architecture/GROK_BOT_PRODUCT_PLAN.md`

## M0 — Reproducible upstream baseline ✅ COMPLETE

M0 evidence: `docs/build-records/M0-2026-09-23-ova.md`

## M1 — Identity

Planned changes:

- GROL hostname/default identity
- console banner
- `os-release` / release metadata
- GROL artifact naming where safe
- GRUB/boot branding
- splash artwork
- GROL version metadata

Tranches:

- **M1-A** — hostname, issue, MOTD, visible OS name, OVA product metadata
- **M1-B1** — graphical GRUB / splash (`Grol5k.png`) without breaking QEMU suite
- **M1-B2** — polish splash scale, GRUB text overlay, reduce pre-login boot noise

No deep Supervisor, OS Agent, partition, or RAUC renaming yet.

M1 is not complete until a human has visually inspected the OVA boot sequence and the QEMU suite still passes.

## M2 — GROL system layer

Introduce:

- `grol-hostd` (Host API on `/run/grol/hostapi.sock`)
- `grol-healthd`
- `grol-identity`
- `grol-provision` (including xAI key slot and empty AI entity-grant file)

No model runtime in M2.

## M3 — Thin Grok gateway

Introduce:

- `grol-ai-gateway`
- xAI credential provisioning (not baked into the image)
- streaming text
- tool-call event normalization
- realtime/voice transport ownership (gateway terminates provider WS)
- provider abstraction
- offline/degraded banner

Hosted tools (`web_search`, MCP, collections, Grok Build CLI) stay **off**.

## M4 — Thin Grok Bot

Introduce:

- `grol-bot` as the only user-facing agent
- Action Broker
- entity-level HA policy (`light` / `switch` grants only)
- confirmation UI (spoken "yes" is not confirmation)
- audit trail
- push-to-talk voice on the same broker path

Optional later in M4, not the first slice:

- `grol.build.propose` drafts only (ADR-0004)

## M5 — GROL5000 experience

Introduce:

- branded first boot
- GROL setup and entity-grant UX
- primary dashboard
- Grok Bot surface
- voice satellite / phone-as-mic
- system/update/recovery UI

Wake word "Hey Grok" is after M5, not part of first voice.

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
