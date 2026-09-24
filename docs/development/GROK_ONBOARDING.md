# Grok Onboarding Packet

Welcome to GROL5K.

## Project goal

Build GROL5000 into a real smart-environment operating system descended from HAOS, with first-class Grok and Grok Bot capabilities while preserving robust local automation, security boundaries, signed updates, and recoverability.

Product sentence: GROL5000 is a home OS you talk to. Grok Bot is the only mouth. Grok is the brain. Grok Build is a contractor in a locked room. Home Assistant is the wiring. The Action Broker is the fuse box.

## Read in this order

1. `README.md`
2. `docs/development/STATUS.md`
3. `GROL_UPSTREAM.md`
4. `docs/architecture/OVERVIEW.md`
5. `docs/architecture/GROK_BOT_PRODUCT_PLAN.md`
6. `docs/architecture/COMPONENT_BOUNDARIES.md`
7. `docs/architecture/AI_CONTROL_PLANE.md`
8. `docs/architecture/SECURITY_MODEL.md`
9. `docs/development/CODEBASE_MAP.md`
10. `docs/development/ROADMAP.md`
11. `docs/development/AI_COLLABORATION.md`
12. `docs/decisions/0003-ai-userspace-boundary.md`
13. `docs/decisions/0004-grok-build-isolation.md`
14. `grol/specs/AI_PROVIDER_V0.md`
15. `grol/specs/GROK_BOT_RUNTIME_V0.md`
16. `grol/specs/HOST_API_V0.md`
17. `grol/specs/THREAT_MODEL_TOOL_INJECTION_V0.md`
18. `grol/specs/VOICE_REALTIME_V0.md`
19. `grol/specs/HOME_ASSISTANT_TOOL_POLICY_V0.md`
20. `grol/specs/ACTION_BROKER_V0.md`
21. `grol/specs/GROK_BUILD_V0.md`

## Current phase

M0 has passed. M1 identity is in progress (A + B1). Next visible work is M1-B2 boot polish after a human inspects the current OVA splash/GRUB/login sequence.

Do not implement M3/M4 runtime until M1-B2 is accepted and M2 host sockets exist.

The inherited HAOS root filesystem is **EROFS**, not squashfs.

## Do not do yet

- do not replace Supervisor
- do not rename RAUC compatibility
- do not give Grok Bot Docker socket or Host API socket access
- do not put xAI credentials into the image
- do not enable provider-hosted tools
- do not install unsandboxed Grok Build / `grok` CLI on the appliance
- do not treat spoken "yes" as confirmation
- do not rewrite HAOS internals for aesthetics
