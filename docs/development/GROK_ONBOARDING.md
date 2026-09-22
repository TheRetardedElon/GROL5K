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

## Current phase

Foundation / M0 preparation.

The project must first reproduce and boot the inherited OVA target before deep customization.

## First Grok review requests

1. Review the AI control-plane boundary.
2. Review `grol/specs/ACTION_BROKER_V0.md`.
3. Propose the xAI provider adapter contract without coupling the whole OS to one API shape.
4. Identify realtime/voice session requirements.
5. Identify what Grok Bot should remember locally versus what belongs in Home Assistant state.
6. Threat-model prompt/tool injection paths.
7. Review failure behavior when xAI is unreachable.

## Do not do yet

- do not replace Supervisor
- do not rename RAUC compatibility
- do not give Grok Bot Docker socket access
- do not put xAI credentials into the image
- do not rewrite HAOS internals for aesthetics
- do not claim M0 passed without a real build and boot
