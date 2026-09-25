# GROL5K Development Roadmap

Canonical product intent: `docs/architecture/GROK_BOT_PRODUCT_PLAN.md`  
Product ceiling: `docs/decisions/0005-ha-is-ancestry.md`

## M0 — Reproducible upstream baseline ✅

OVA builds, QEMU suite green, VirtualBox boot + `grol5000.local` onboarding proven.

## M1 — Identity

GROL hostname, splash, quieter console, `grol >` face. No Core fork *this milestone*.

## M2 — GROL system layer

`grol-hostd`, health, identity, provision. No model runtime.

## M3 — Thin Grok gateway

`grol-ai-gateway`, provisioned xAI creds, streaming, tool events, voice transport.

## M4 — Thin Grok Bot + native Build hook

`grol-bot`, Action Broker, entity grants, audit, push-to-talk.
`grol-buildd` exists at least as propose/diagnose. Apply is brokered.

## M5 — Own the HA-descended stack

Stand up GROL-owned repos (or official forks) of:

- Supervisor
- Core
- frontend
- plugin-cli

Introduce first-class Core objects: `grol.agent`, `grol.grant`,
`grol.action`, `grol.build_job`, `grol.audit_event`, …

Keep merging upstream HA so integrations are not abandoned.

## M6 — GROL5000 experience

GROL onboarding, dashboard, Bot surface, grants UI, CLI face, voice satellites.

## M7 — Retire inherited product identity

Landing page, Supervisor store chrome, and remaining "Home Assistant"
product strings become GROL while the integration ecosystem stays.

## M8 — GROL-owned distribution

CI, signed artifacts, channels, RAUC keys, SBOM.

## M9 — Hardware expansion

Pi 5 and other boards after x86 is stable.
