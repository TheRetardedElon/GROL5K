# ADR-0001: Use HAOS as the GROL5K downstream base

- Status: Accepted
- Date: 2026-09-22

## Context

GROL5K needs an embedded operating-system foundation with strong hardware support, container orchestration, update/rollback capability, Home Assistant compatibility, and a mature device ecosystem.

Home Assistant OS already provides Buildroot, systemd, Docker, AppArmor, RAUC, GRUB/U-Boot support, OS Agent, Supervisor integration, and maintained hardware targets.

## Decision

GROL5K will begin as a downstream fork of `home-assistant/operating-system`.

The project will preserve upstream history and progressively layer GROL-owned identity, services, AI control plane, UI, policy, release tooling, and hardware definitions on top.

## Consequences

Positive:

- faster path to a bootable appliance OS
- retained Home Assistant ecosystem compatibility
- mature update and rollback foundation
- upstream kernel/driver/security work remains importable

Costs:

- upstream synchronization becomes an ongoing engineering responsibility
- GROL must carefully manage compatibility-sensitive divergence
- licensing and attribution obligations must remain visible
- some HAOS-specific internals may remain for a substantial period

## Follow-up

Deep renaming of internal HAOS identifiers is explicitly deferred until GROL-specific targets and services are stable.
