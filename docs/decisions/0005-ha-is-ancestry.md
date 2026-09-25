# ADR-0005: Home Assistant is ancestry, not the product ceiling

- Status: Accepted
- Date: 2026-09-25

## Context

Early GROL5K docs and reviews said things like "do not fork Core" and
"Home Assistant is the wiring." Those sentences were meant as *M0/M1
sequencing*: prove the inherited image boots before we take on four more
upstream trees.

They were read, including by Grok, as an end-state: GROL sits on top of
Home Assistant forever and Core stays sacred.

That is not the product.

GROL5000 is Home Assistant *turned into* GROL5000. Grok Bot and Grok
Build are native system capabilities, not an add-on chatbot talking to
an unmodified HA.

## Decision

Home Assistant OS, Supervisor, Core, frontend, and plugin-cli are the
**starting codebase**. They are not the final product boundary.

Eventual tree:

```text
GROL5000
├── GROL OS            (this repo; fork of home-assistant/operating-system)
├── GROL Supervisor    (fork/evolution of home-assistant/supervisor)
├── GROL Core          (fork/evolution of home-assistant/core)
├── GROL Frontend      (fork/evolution of home-assistant/frontend)
├── GROL CLI           (rework of plugin-cli)
├── Grok Bot           (native persistent agent)
├── Grok AI Gateway
├── Grok Build Runtime (native grol-buildd; not an unsandboxed root shell)
├── GROL Capability Broker
└── HA integration ecosystem kept as compatibility ancestry
```

First-class concepts that belong *inside* GROL Core over time, not only
as external tools:

- `grol.agent`
- `grol.intent`
- `grol.capability`
- `grol.grant`
- `grol.proposal`
- `grol.action`
- `grol.build_job`
- `grol.voice_session`
- `grol.audit_event`

Upstream Home Assistant continues to be merged so the device/integration
ecosystem is not thrown away. Divergence is documented. Sacredness is
not a policy.

## What this does not change

- Grok / Grok Bot are still userspace (ADR-0003). Not the kernel.
- Model output is still not PID 1, not root, not the Docker socket.
- Grok Build still lands through `grol-buildd` + broker, not `shell.exec`.
- M1 still does not fork Core just to change a landing-page string.
- M2 still stands up GROL host services in *this* repo first.

Sequencing is not permission architecture. Owning Core is the plan.
Doing it before the OS identity and host sockets exist is still the
wrong week.

## Consequences

- Roadmap M5+ explicitly includes Core / Supervisor / frontend repos.
- Docs that said "never patch Core" are wrong and are updated.
- Maintenance of multiple HA-descended forks is accepted project cost.
- Compatibility with HA integrations remains a feature, not a veto.
