# GROL Grok Build v0

**Status:** design draft. Not scheduled for implementation before thin M4 exists.

## Purpose

Define how GROL5000 may use xAI Grok Build (the coding-agent CLI/harness) without giving it host privilege.

Grok Build is optional. The household agent is `grol-bot`. Home control does not depend on Build.

## Allowed use

The only v0-shaped tool is:

```text
grol.build.propose
```

It may:

- send a bounded coding/planning prompt through `grol-ai-gateway`
- or, after a later ADR, start a disposable sandbox harness

It may return:

- a natural-language summary
- a proposed file or HA automation draft
- a structured "not applied" artifact list

It may not:

- execute host commands
- write the data partition
- call Home Assistant
- open `/run/grol/hostapi.sock`
- receive the Docker socket
- enable MCP servers that reach the LAN
- apply its own output

Applying a proposal is a **different** brokered tool, denied until an automation-create ADR exists.

## Isolation (sandbox profile, when introduced)

- dedicated container or VM
- scratch workspace only
- no bind-mount of `/`, `/mnt/data`, `/run/grol`, Docker socket
- no HA token in the environment
- egress allowlist: xAI API only
- hard wall-clock and token budget
- stdout/stderr size-capped before it re-enters Bot context (tool-result injection)

## Relationship to other specs

- Bot requests the tool: `GROK_BOT_RUNTIME_V0.md`
- Gateway does not execute it: `AI_PROVIDER_V0.md`
- Broker authorizes it: `ACTION_BROKER_V0.md`
- Provider-hosted MCP stays off: `THREAT_MODEL_TOOL_INJECTION_V0.md`
- Product intent: `docs/architecture/GROK_BOT_PRODUCT_PLAN.md`
- Decision: `docs/decisions/0004-grok-build-isolation.md`
