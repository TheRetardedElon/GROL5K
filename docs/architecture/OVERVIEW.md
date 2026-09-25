# GROL5K Architecture Overview

## Purpose

GROL5K starts as a Home Assistant OS fork and becomes GROL5000: a home
operating system whose operator is Grok Bot and whose construction
runtime is Grok Build.

Home Assistant is ancestry. The integration ecosystem is kept. The
product ceiling is GROL. See ADR-0005.

## Layer model (target)

```text
+----------------------------------------------------------+
|                 GROL5000 Experience                      |
| UI · Voice · Onboarding · Grants · Recovery · Console    |
+----------------------------------------------------------+
|                 GROL AI + Build plane                    |
| Gateway · Grok Bot · grol-buildd · Action Broker         |
+----------------------------------------------------------+
|                 GROL-owned HA descendants                |
| GROL Core · GROL Supervisor · Apps · Integrations        |
+----------------------------------------------------------+
|                 GROL system services                     |
| hostd · health · identity · provision · updates          |
+----------------------------------------------------------+
|                 GROL OS / HAOS platform                  |
| Buildroot · systemd · Docker · AppArmor · RAUC · EROFS   |
+----------------------------------------------------------+
|                 Hardware                                 |
+----------------------------------------------------------+
```

AI components stay userspace (ADR-0003). They do not live in the kernel.
They *do* become first-class across Core and Supervisor, not a sidecar
chatbot.

## Principles

- Reproducibility first (M0 is done).
- Additive before invasive *in the current milestone*, not forever.
- AI is not root. Bot is the operator. Build is native and brokered.
- Local automations survive xAI loss.
- Signed updates stay mandatory.
- Upstream HA is merged and tracked. It is not a veto.
