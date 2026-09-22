# ADR-0002: Preserve HAOS compatibility identifiers during early GROL milestones

- Status: Accepted
- Date: 2026-09-22

## Context

Many HAOS-looking names are not cosmetic. `HAOS_ID`, Supervisor machine identifiers, OS Agent board IDs, RAUC compatibility strings, service names, partition identities, and artifact conventions participate in runtime/update behavior.

Renaming them all during initial branding would mix presentation work with platform migration and make failures difficult to isolate.

## Decision

M0-M1 will preserve compatibility-sensitive HAOS identifiers unless a specific identifier has been proven safe to change.

GROL5000 identity will first be introduced through visible names, banners, documentation, GROL-owned services, and later dedicated GROL targets.

## Consequences

- early GROL builds may contain internal `haos` names
- visible UX can still become GROL5000
- upstream sync remains easier
- failures are easier to attribute
- a later migration can rename internals deliberately with update/rollback tests

## Initial protected identifiers

- `HAOS_ID`
- `BR2_EXTERNAL_HAOS_PATH`
- Supervisor machine/architecture IDs
- OS Agent board IDs
- `haos-*` systemd units and helper programs
- RAUC compatible strings
- existing partition identity scheme
