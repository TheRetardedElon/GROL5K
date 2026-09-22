# GROL Action Broker v0 Contract

Status: design draft.

The Action Broker is the only approved path from AI intent to privileged execution.

## Request envelope

```json
{
  "version": "grol.action.v0",
  "request_id": "uuid",
  "session_id": "opaque-session-id",
  "actor": {
    "type": "grok-bot",
    "instance": "primary"
  },
  "tool": "homeassistant.service.call",
  "risk": "tier1",
  "arguments": {},
  "reason": "User requested the kitchen lights be turned off."
}
```

## Broker result

```json
{
  "version": "grol.action-result.v0",
  "request_id": "uuid",
  "decision": "executed",
  "confirmation_required": false,
  "result": {},
  "audit_id": "uuid"
}
```

Allowed decisions: `denied`, `confirmation_required`, `executed`, `failed`.

## Core rules

1. Unknown tools are denied.
2. Tool risk tier is defined by broker policy, not by the model.
3. Model-provided `risk` and `reason` are advisory inputs only.
4. Arguments are validated against a per-tool schema.
5. Security-sensitive tools require explicit authorization policy.
6. No generic `shell.exec` tool exists in the normal agent catalog.
7. Credentials are resolved by the executor, not supplied by the model.
8. Every accepted request receives an audit record.
9. Tool responses are bounded and redacted before returning to the model.

## Initial tool namespaces

```text
homeassistant.state.read
homeassistant.service.call
grol.system.status
grol.update.status
grol.network.status
grol.hardware.status
```

Host-mutating tools are deferred until the policy engine and confirmation UX exist.

## Risk tiers

- Tier 0: read-only
- Tier 1: reversible low-risk automation
- Tier 2: consequential environmental action
- Tier 3: security-sensitive action
- Tier 4: host administration

Tier 4 should be disabled by default.
