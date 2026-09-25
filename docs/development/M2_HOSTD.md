# M2 — grol-hostd

M0 booted. M1 identity is visible enough to keep going. M2 is the first GROL-owned control-plane service.

## In this tranche

- `grol-hostd` Unix socket at `/run/grol/hostapi.sock`
- read-only probes from HOST_API_V0
- `SO_PEERCRED` + UID allowlist
- systemd unit, sysusers, tmpfiles
- unittest that does not need an OVA rebuild

## Out of this tranche

- Action Broker
- Grok Bot / gateway
- host mutations
- replacing OS Agent
- forking Home Assistant Core

## How to try it after the next image

```text
grol-hostctl grol.system.status
```

Until then, run the unit tests on any Linux box with Python 3.
