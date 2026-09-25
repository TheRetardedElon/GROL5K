# GROL5K Component Boundaries

## GROL UI / Frontend

Target: GROL-owned frontend (HA frontend fork). May display house state,
Bot, confirmations, grants, Build proposals, system health.

Must not hold root credentials or bypass the Action Broker.

## grol-ai-gateway

Provider adapter and session transport. No host shell, no Docker, no
unbrokered Core mutation.

## grol-bot

Persistent operator. Interprets intent, plans, requests tools, explains.
Not an authorization source. Eventually a first-class Core agent
(`grol.agent`), not only an external process.

## grol-buildd

Native construction runtime. Inspects, drafts, tests, stages. Does not
apply live privileged changes itself.

## grol-action-broker

Policy and capability execution. The only AI-adjacent holder of HA
mutation credentials and the Host API socket.

## GROL Core

Fork/evolution of Home Assistant Core. Device/entity/automation engine
plus GROL domain objects (`grol.grant`, `grol.action`, `grol.build_job`,
…). Started as a separate repo at M5. Not forbidden before then because
it is sacred — delayed because M1/M2 live in the OS repo.

## GROL Supervisor

Fork/evolution of Home Assistant Supervisor. Manages Core, apps, OS
updates. GROL-owned when we need Supervisor-level identity, app policy,
or Bot lifecycle that upstream will not take.

## GROL host services

OS-level information and later controlled host operations. Narrow APIs
to the broker. Not a second unpublished D-Bus stack.

## Secrets

Provider keys and signing material are never model context by default.
