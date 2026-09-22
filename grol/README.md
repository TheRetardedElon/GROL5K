# GROL Platform Layer

This directory contains GROL5K-owned source, metadata, policies, service definitions, release tooling, specifications, and branding that should remain clearly separated from inherited HAOS code wherever practical.

Current structure:

```text
grol/
├── branding/       # OS/UI visual identity and boot assets
├── policies/       # authorization and security policy
├── release/        # GROL release metadata and tooling
├── services/       # GROL-owned host/user-space services
└── specs/          # cross-service contracts and schemas
```

## Rules

- Prefer new GROL components here instead of embedding unrelated logic into inherited HAOS files.
- Patch inherited HAOS code only when the integration point genuinely belongs there.
- Do not place secrets or signing keys in this tree.
- Cross-component interfaces should be documented under `grol/specs/`.
- Privileged AI actions must go through the Action Broker boundary.
- Keep compatibility-sensitive HAOS identifiers unchanged until an ADR and validation plan explicitly approve migration.

## Current specs

- [Action Broker v0](specs/ACTION_BROKER_V0.md)
- [Action request JSON schema](specs/action-request.schema.json)
- [AI Provider Adapter v0](specs/AI_PROVIDER_V0.md)
- [Grok Bot Runtime v0](specs/GROK_BOT_RUNTIME_V0.md)
- [GROL Host API v0](specs/HOST_API_V0.md)
- [Tool / Prompt Injection Threat Model v0](specs/THREAT_MODEL_TOOL_INJECTION_V0.md)
- [Voice / Realtime Session v0](specs/VOICE_REALTIME_V0.md)
- [Home Assistant Tool Policy v0](specs/HOME_ASSISTANT_TOOL_POLICY_V0.md)
- [GROL services map](services/README.md)

The exact Buildroot package layout for GROL services will be finalized after M0 reproduces and boots the inherited OVA baseline.
