# GROL5K Security Model

## Security posture

GROL5K treats AI reasoning, home automation, and host administration as separate trust domains.

## Core rules

1. Grok and Grok Bot are untrusted decision-support components from the host's point of view.
2. Privileged actions are capability-scoped and brokered.
3. Secrets are never embedded in images or committed to source control.
4. Cloud credentials are provisioned after installation and stored using the strongest practical local mechanism for the target.
5. AppArmor and existing HAOS isolation remain enabled while GROL policies are developed.
6. Update signing and rollback protection must not be weakened for branding convenience.
7. Home automation should degrade safely when external AI services are unavailable.
8. Security-sensitive commands require explicit user intent and should be auditable.

## Trust domains

```text
[External AI Provider]
        |
        v
[grol-ai-gateway] -- no host privilege
        |
        v
[grol-bot] ------- no host privilege
        |
        v
[grol-action-broker] -- constrained privilege
        |
   +----+----+
   |         |
   v         v
[HA APIs] [GROL host APIs]
```

## Audit expectations

The action broker should eventually record:

- timestamp
- requester/session
- proposed action
- policy decision
- confirmation state
- target
- execution result
- correlation/request ID

Sensitive values must be redacted.

## Safe mode

A future GROL safe mode should boot with:

- AI services disabled
- optional third-party apps disabled
- networking available where safe
- diagnostics available
- update rollback/recovery available
- Home Assistant recovery path preserved
