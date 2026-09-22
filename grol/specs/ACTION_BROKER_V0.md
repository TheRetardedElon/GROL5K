# GROL Action Broker v0 Contract

**Status:** design draft.  
**Revised:** 2026-09-22 (v0.3 adversarial review)

The Action Broker is the only approved path from AI intent to privileged execution.

It is the only AI-adjacent component allowed to hold a Home Assistant mutation token or the Host API socket.

## Request envelope

```json
{
  "version": "grol.action.v0",
  "request_id": "uuid",
  "session_id": "opaque-session-id",
  "turn_id": "opaque-turn-id",
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
4. Arguments are validated against a per-tool schema with `additionalProperties: false`.
5. Security-sensitive tools require explicit authorization policy.
6. No generic `shell.exec` tool exists in the normal agent catalog.
7. Credentials are resolved by the executor, not supplied by the model.
8. Every accepted request receives an audit record.
9. Tool responses are bounded, labeled untrusted, and redacted before returning to the model.
10. Confirmation is a broker event. Model prose and spoken "yes" cannot satisfy it.
11. A confirmation token binds `sha256(tool + canonical_json(normalized_args))`. Digest drift is deny.
12. Entity IDs for mutating HA calls are re-resolved against the live registry at execute time.

## Initial tool namespaces

```text
homeassistant.state.read
homeassistant.service.call
grol.system.status
grol.update.status
grol.network.status
grol.hardware.status
```

`grol.*.status` tools return the **model-facing projection** defined in `HOST_API_V0.md`, not raw Host API payloads.

Host-mutating tools are deferred until the policy engine and confirmation UX exist.

## Home Assistant service-call allowlist (v0)

`homeassistant.service.call` is not "any HA service."

v0 allowlist is domain + service. Starting set:

- `light.turn_on` / `light.turn_off` / `light.toggle`
- `switch.turn_on` / `switch.turn_off` / `switch.toggle`
- `script.turn_on` (existing scripts only; no script create/update)
- `scene.turn_on` (existing scenes only)

v0 deny on the AI path includes at least:

- `shell_command.*`
- `command_line.*`
- `rest_command.*`
- `python_script.*`
- `system_log.*`
- automation / script / helper **create or update**
- lock / alarm / cover / security domains until an explicit later policy says otherwise

Unknown domain+service pairs are denied.

## Risk tiers

- Tier 0: read-only
- Tier 1: reversible low-risk automation
- Tier 2: consequential environmental action
- Tier 3: security-sensitive action
- Tier 4: host administration

Tier 4 should be disabled by default.

## Limits

- per-session tool budget
- per-tool rate limit
- max argument document size bounded by the request schema
