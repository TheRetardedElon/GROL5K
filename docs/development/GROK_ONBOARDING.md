# Grok Onboarding Packet

Welcome to GROL5K.

## Project goal

Turn Home Assistant into GROL5000. Grok Bot is the native operator.
Grok Build is a native construction runtime. Home Assistant is ancestry
and the integration ecosystem, not a sacred ceiling. ADR-0005.

## Read in this order

1. `README.md`
2. `docs/decisions/0005-ha-is-ancestry.md`
3. `docs/architecture/GROK_BOT_PRODUCT_PLAN.md`
4. `docs/development/ROADMAP.md`
5. `docs/architecture/OVERVIEW.md`
6. `docs/architecture/COMPONENT_BOUNDARIES.md`
7. `docs/decisions/0003-ai-userspace-boundary.md`
8. `docs/decisions/0004-grok-build-isolation.md`
9. `grol/specs/` (all v0 contracts)

## Current phase

M0 passed. VirtualBox + `grol5000.local` onboarding works. M1-B2 and M2
hostd are in flight in *this* repo.

M5 is when Core / Supervisor / frontend become GROL-owned repos. That is
planned work, not a rejection of the idea.

## Still true

- Bot/Build are userspace, not the kernel
- model output is not PID 1 / Docker socket / Host API socket
- do not bake xAI credentials into the image
- do not treat spoken yes as confirmation in v0 voice
