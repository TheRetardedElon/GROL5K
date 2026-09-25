# grol-hostd

M2 read-only Host API. Contract: `grol/specs/HOST_API_V0.md`.

```text
/run/grol/hostapi.sock
        ^
        |
 grol-action-broker   (later)
 grol-hostctl         (console test client)
```

Not a caller: grol-bot, grol-ai-gateway, Core, Supervisor, add-ons.

## Local test

```bash
python3 grol/services/grol-hostd/tests/test_hostd.py
```

## Methods

- `grol.system.status`
- `grol.update.status`
- `grol.network.status`
- `grol.hardware.status`
- `grol.service.status`

Mutations (`reboot`, Docker, updates) are rejected.
