# GROL Services

| Service | Purpose | Earliest milestone |
|---|---|---|
| `grol-hostd` | Host API on `/run/grol/hostapi.sock` | M2 |
| `grol-healthd` | health aggregation | M2 |
| `grol-identity` | version/build/identity | M2 |
| `grol-provision` | first-run + credentials | M2 |
| `grol-ai-gateway` | provider/session | M3 |
| `grol-bot` | household operator | M4 |
| `grol-action-broker` | policy/execution | M4 |

`grol-hostd` is Go, packaged like OS Agent (`golang-package`, local tree).
No CPython on the appliance for this daemon.
