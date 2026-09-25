# GROL Services

Planned services:

| Service | Purpose | Earliest milestone |
|---|---|---|
| `grol-hostd` | serve the narrow local Host API over `/run/grol/hostapi.sock` | M2 (v0 code in this tree) |
| `grol-healthd` | aggregate GROL service/platform health | M2 |
| `grol-identity` | expose GROL version, build, target and identity | M2 |
| `grol-provision` | first-run and credential provisioning | M2 |
| `grol-ai-gateway` | AI provider abstraction and streaming sessions | M3 |
| `grol-bot` | persistent conversational agent runtime | M4 |
| `grol-action-broker` | policy, confirmation and capability execution | M4 |

`grol-hostd` is an information plane. It wraps documented OS Agent / systemd / RAUC probes. It is not a shell, not a policy engine, and not model code.

Implementation: [`grol/services/grol-hostd/`](grol-hostd/).
