# Grok Onboarding Packet

Welcome to GROL5K.

## Project goal

Build GROL5000 into a real smart-environment operating system descended from HAOS, with first-class Grok and Grok Bot capabilities while preserving robust local automation, security boundaries, signed updates, and recoverability.

## Read in this order

1. `README.md`
2. `docs/development/STATUS.md`
3. `GROL_UPSTREAM.md`
4. `docs/architecture/OVERVIEW.md`
5. `docs/architecture/COMPONENT_BOUNDARIES.md`
6. `docs/architecture/AI_CONTROL_PLANE.md`
7. `docs/architecture/SECURITY_MODEL.md`
8. `docs/development/CODEBASE_MAP.md`
9. `docs/development/ROADMAP.md`
10. `docs/development/AI_COLLABORATION.md`
11. `docs/decisions/0003-ai-userspace-boundary.md`
12. `grol/specs/AI_PROVIDER_V0.md`
13. `grol/specs/GROK_BOT_RUNTIME_V0.md`
14. `grol/specs/HOST_API_V0.md`
15. `grol/specs/THREAT_MODEL_TOOL_INJECTION_V0.md`
16. `grol/specs/VOICE_REALTIME_V0.md`

## Current phase

Foundation / M0 preparation.

The project must first reproduce and boot the inherited OVA target before deep customization.

## Grok review status

The initial repository/architecture review has been incorporated. The project now locks Grok and Grok Bot to first-class userspace services rather than kernel components.

Current review targets:

1. Review the normalized provider capability/event contract in `grol/specs/AI_PROVIDER_V0.md` against current xAI/Grok APIs.
2. Review `grol/specs/GROK_BOT_RUNTIME_V0.md`, especially memory/state ownership.
3. Review `grol/specs/HOST_API_V0.md` and keep the host surface intentionally tiny.
4. Adversarially review `grol/specs/THREAT_MODEL_TOOL_INJECTION_V0.md`.
5. Review `grol/specs/VOICE_REALTIME_V0.md` for xAI realtime session/cancellation semantics.
6. Do not implement M3/M4 runtime code until M0 has real build/boot evidence.

## Do not do yet

- do not replace Supervisor
- do not rename RAUC compatibility
- do not give Grok Bot Docker socket access
- do not put xAI credentials into the image
- do not rewrite HAOS internals for aesthetics
- do not claim M0 passed without a real build and boot
