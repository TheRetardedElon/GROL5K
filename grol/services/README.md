# GROL Services

This directory will contain GROL-owned services introduced after M0.

Planned services:

| Service | Purpose | Earliest milestone |
|---|---|---|
| `grol-healthd` | aggregate GROL service/platform health | M2 |
| `grol-identity` | expose GROL version, build, target and identity | M2 |
| `grol-provision` | first-run and credential provisioning | M2 |
| `grol-ai-gateway` | AI provider abstraction and streaming sessions | M3 |
| `grol-bot` | persistent conversational agent runtime | M4 |
| `grol-action-broker` | policy, confirmation and capability execution | M4 |

## Packaging direction

The services should eventually be represented as explicit Buildroot packages and systemd units, rather than opaque scripts copied into the image.

Before implementation, each service needs:

- a narrow responsibility
- a documented IPC/API surface
- health semantics
- restart behavior
- logging policy
- secret-handling rules
- privilege requirements
- tests

No GROL AI service should require direct Docker socket access.
