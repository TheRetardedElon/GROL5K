# GROL Host API v0

Status: design draft.

## Purpose

The GROL Host API exposes a **small, explicit, local interface** for OS-level information and carefully selected operations that do not belong in Home Assistant.

The API is consumed by trusted GROL components such as `grol-action-broker`.

It is not a general-purpose host administration API.

## Transport

Preferred initial options:

1. Unix domain socket with filesystem permissions and peer credential checks.
2. Loopback HTTP only if Unix-socket integration materially complicates implementation.

Do not expose this API on LAN/WAN by default.

## Read-only v0 endpoints

### `grol.system.status`

Returns:

- GROL version
- build identifier
- board/target
- deployment channel
- uptime
- platform health summary

### `grol.update.status`

Returns:

- current OS version
- active slot
- update availability if known
- RAUC health/status summary
- rollback availability state

No installation operation in v0.

### `grol.network.status`

Returns bounded summaries:

- primary interface
- connectivity state
- IP family availability
- default route status
- DNS health summary

Do not return Wi-Fi passwords or raw secret material.

### `grol.hardware.status`

Returns bounded summaries:

- CPU architecture
- memory totals/pressure
- storage totals/pressure
- temperatures if available
- selected hardware health state

### `grol.service.status`

Returns health for GROL-owned services and selected platform dependencies.

## Mutating operations

Mutating host operations are **not part of the initial v0 tool catalog**.

Candidates for later versions may include:

- controlled reboot
- controlled shutdown
- update installation
- rollback

Each requires:

- separate ADR/security review
- explicit Action Broker policy
- confirmation UX
- audit logging
- failure/rollback semantics

## Authorization

The Host API does not trust model identity.

Authorization is based on the calling local process identity and/or capability presented by the Action Broker.

## Response rules

- structured JSON or equivalent typed schema
- bounded response sizes
- no raw journal dumps by default
- no secrets
- stable error codes
- monotonic request IDs for tracing where practical

## Failure model

If a subsystem is unavailable, return a partial/degraded response rather than fabricating state.

Example:

```json
{
  "status": "degraded",
  "components": {
    "rauc": "unavailable",
    "network": "ok"
  }
}
```
