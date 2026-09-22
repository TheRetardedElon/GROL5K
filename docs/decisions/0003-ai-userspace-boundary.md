# ADR-0003: Grok and Grok Bot are first-class userspace services, not kernel components

- Status: Accepted
- Date: 2026-09-22

## Context

GROL5000 is intended to make Grok and Grok Bot feel like native parts of the operating system.

That does not require the model runtime to live in the Linux kernel.

HAOS is structured as a small appliance OS with a Linux kernel, systemd/NetworkManager/Docker/AppArmor/RAUC userspace, OS Agent, Supervisor, Home Assistant Core, and add-ons/apps.

Placing model logic in the kernel would couple model/API churn to kernel updates, weaken isolation, make failure recovery more dangerous, and violate the project's existing rule that the model is not an authorization authority or root user.

## Decision

Grok and Grok Bot will be **first-class GROL5000 userspace components**.

The Linux kernel remains responsible for normal kernel concerns:

- hardware
- drivers
- networking
- filesystems
- security mechanisms
- resource control

The AI control plane will live above the kernel:

- `grol-ai-gateway` — provider/session adapter
- `grol-bot` — persistent agent runtime
- `grol-action-broker` — privileged policy/execution boundary

Only the Action Broker may cross into privileged Home Assistant or narrow GROL host capabilities.

## Required properties

1. AI services may fail without preventing normal boot.
2. Home Assistant local automations continue when xAI is unreachable.
3. Recovery mode does not depend on AI availability.
4. No AI component receives the Docker socket.
5. No generic shell tool is exposed to the normal agent catalog.
6. Model-supplied risk classifications never override broker policy.
7. Provider credentials are provisioned at runtime and are not embedded in OS images.
8. Host administration remains disabled by default for the AI path.

## Consequences

- GROL can ship Grok as a native, always-present system capability without modifying Linux semantics.
- AI services can be restarted, updated, sandboxed, or disabled independently.
- Kernel/Buildroot/HAOS upstream sync remains tractable.
- Security policy is concentrated in one reviewable broker.
- A safe-mode boot path can explicitly disable the AI control plane.
