# GROL Host API v0

**Status:** design draft.  
**Revised:** 2026-09-22 (v0.4 policy hardening)

## Purpose

The GROL Host API exposes a **small, explicit, local interface** for OS-level information and carefully selected operations that do not belong in Home Assistant.

The API is consumed by trusted GROL components such as `grol-action-broker`.

It is not a general-purpose host administration API.

## Server ownership

A dedicated M2 host service, `grol-hostd`, owns the Host API.

This avoids making `grol-action-broker` the implementation of the host-information plane and keeps the broker focused on policy/execution.

## Transport

v0 uses a Unix domain stream socket with filesystem permissions **and** peer credential checks.

Do not expose this API on LAN/WAN.

Socket path: `/run/grol/hostapi.sock`  
Runtime tmpfs (`/run`), not the EROFS root filesystem.

Recommended systemd socket ownership:

- owner: `root`
- group: dedicated `grol-hostapi` group
- mode: `0660`

Only explicitly approved service UIDs belong to that group. Membership is necessary but not sufficient: `grol-hostd` also validates `SO_PEERCRED` against an exact UID/unit allowlist.

Bot and Gateway are not members of the group and the socket is not bind-mounted into their containers.

Loopback TCP/HTTP is deferred; adding a network socket requires a separate ADR.

## Callers (v0 allowlist)

MAY connect:

- `grol-action-broker`
- `grol-healthd`
- `grol-identity` (read-only subset)

MUST NOT connect:

- `grol-bot`
- `grol-ai-gateway`
- Home Assistant Core
- Supervisor
- any add-on/app
- any process running model code

Authorization uses `SO_PEERCRED` on the connected Unix socket.  
UID/unit allowlist is mandatory.  
A capability token is **not** a substitute for peer credentials.

If the implementation later changes transport semantics, credential passing must be re-reviewed rather than assuming `SCM_CREDENTIALS` and `SO_PEERCRED` are interchangeable.

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

MAY report only these names:

- `grol-hostd`
- `grol-healthd`
- `grol-identity`
- `grol-provision`
- `grol-ai-gateway`
- `grol-bot`
- `grol-action-broker`
- `docker`
- `networkmanager`
- `rauc`
- `supervisor`
- `os-agent`

Values: `running` | `degraded` | `stopped` | `unavailable`.

No process lists, no container inspect, no journal text.

## Model-facing projection

Host API responses are for GROL services.

Before any field is placed in model context, the Action Broker applies a redaction profile.

Allowed to the model in v0:

- GROL version, channel, health enum
- update available: yes/no
- connectivity: online/degraded/offline
- disk/memory pressure: ok/warn/critical

Never to the model in v0:

- raw IP addresses, SSIDs, BSSIDs, DNS servers
- slot identifiers beyond A/B
- serial numbers, MAC addresses
- full unit lists, journal text, RAUC cert material
- hardware identity strings that are not required for the user request

Bot reaches status information only as brokered, redacted `grol.*.status` tool results.

## Mutating operations

Mutating host operations are **not part of the initial v0 tool catalog**.

v0 MUST NOT expose: reboot, shutdown, update install, rollback, hostname change, network reconfiguration, disk wipe, SSH, or Docker control.

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

## Minimum service hardening

The eventual `grol-hostd.service` should start from a restrictive systemd/AppArmor posture and open only what its read-only probes require.

Design targets include:

- `NoNewPrivileges=yes`
- read-only system filesystem by default
- no shell execution API
- no Docker socket
- no model/provider network access
- AF_UNIX-only listener
- explicit filesystem/device exceptions rather than broad host access

Exact unit/AppArmor directives are implementation work for M2 and must be tested against the probes actually needed.

## Response rules

- structured JSON or equivalent typed schema
- bounded response sizes
- no raw journal dumps by default
- no secrets
- stable error codes
- monotonic request IDs for tracing where practical

## Limits

- max response size: 16 KiB
- max in-flight requests per caller: 2
- max requests per caller per second: 5

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
