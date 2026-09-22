# GROL5K Architecture Overview

## Purpose

GROL5K is a purpose-built smart-environment operating system descended from Home Assistant OS and designed around the GROL5000 identity, Grok integration, and a persistent Grok Bot agent.

The goal is not merely to reskin HAOS. The goal is to preserve the strong embedded Linux, container, update, and hardware foundation while progressively replacing the user-facing identity, control plane, service layer, and operating experience with GROL-owned components.

## Layer model

```text
┌──────────────────────────────────────────────────────────┐
│                    GROL5000 Experience                   │
│ UI · Voice · Provisioning · Status · Recovery · Console │
├──────────────────────────────────────────────────────────┤
│                    GROL AI Control Plane                 │
│ Grok Gateway · Grok Bot · Action Broker · Policy Engine │
├──────────────────────────────────────────────────────────┤
│                Home Automation Compatibility             │
│ Home Assistant Core · Supervisor · Apps · Integrations  │
├──────────────────────────────────────────────────────────┤
│                    GROL System Services                  │
│ Health · Identity · Provisioning · Telemetry · Updates  │
├──────────────────────────────────────────────────────────┤
│                  GROL5K / HAOS Platform                 │
│ Buildroot · systemd · Docker · AppArmor · RAUC · GRUB   │
├──────────────────────────────────────────────────────────┤
│                         Hardware                         │
└──────────────────────────────────────────────────────────┘
```

## Initial design principles

- **Reproducibility first.** Before GROL changes, an untouched upstream image must build and boot.
- **Additive before invasive.** Introduce GROL packages and services before renaming deep HAOS internals.
- **AI is not root.** Grok and Grok Bot never receive unrestricted host or Docker access.
- **Explicit privilege boundary.** All privileged actions flow through the GROL Action Broker.
- **Local automation survives cloud loss.** Core home automation must remain operational if Grok/xAI is unavailable.
- **Signed updates and rollback remain mandatory.**
- **Observable failure modes.** Every GROL service must expose health and failure state.
- **Upstream remains trackable.** GROL divergence is documented rather than hidden.

## Initial targets

1. OVA/QEMU development image
2. Generic x86-64 UEFI
3. Raspberry Pi 5 after x86 baseline is stable

## Milestone sequence

- M0 — reproduce upstream HAOS build and boot
- M1 — GROL identity and boot experience
- M2 — GROL system services
- M3 — Grok gateway integration
- M4 — Grok Bot and privileged action broker
- M5 — GROL5000 UI and first-run experience
- M6 — GROL-owned update/release pipeline
- M7 — additional hardware targets
