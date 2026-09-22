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
17. `grol/specs/HOME_ASSISTANT_TOOL_POLICY_V0.md`
17. `grol/specs/ACTION_BROKER_V0.md`

## Current phase

Foundation / M0 preparation.

The project must first reproduce and boot the inherited OVA target before deep customization.

The inherited HAOS root filesystem is **EROFS**, not squashfs.

## Grok review status

v0.2 specs landed in PR #4. v0.3 adversarial review tightened:

- state ownership (preferences vs durable memory vs HA/system/secrets)
- Host API caller isolation and model-facing redaction
- provider-hosted tool ban (web_search / MCP / collections)
- confirmation token + argument digest
- voice transport ownership and cancellation triad
- xAI annex on `AI_PROVIDER_V0.md` without coupling the OS to one wire format

Do not implement M3/M4 runtime code until M0 has real build/boot evidence.

## Do not do yet

- do not replace Supervisor
- do not rename RAUC compatibility
- do not give Grok Bot Docker socket or Host API socket access
- do not put xAI credentials into the image
- do not enable provider-hosted tools
- do not rewrite HAOS internals for aesthetics
- do not claim M0 passed without a real build and boot
