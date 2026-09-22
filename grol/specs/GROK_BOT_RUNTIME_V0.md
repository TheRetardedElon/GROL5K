# GROL Grok Bot Runtime v0

Status: design draft for implementation after M0/M1/M2.

## Purpose

`grol-bot` is the persistent conversational/agent runtime for GROL5000.

It is responsible for intent interpretation, conversational continuity, planning, and requesting structured tools.

It is **not** an authorization authority and does not directly control the host.

## Runtime placement

Recommended initial placement: containerized service managed by the GROL platform.

Required connections:

- `grol-ai-gateway`
- `grol-action-broker`
- read-only access to approved local context stores
- GROL UI / voice transport

Forbidden direct access:

- Docker socket
- raw D-Bus
- unrestricted filesystem
- host root shell
- RAUC
- long-lived Home Assistant admin credentials

## State model

Grok Bot needs multiple kinds of state. They must not be collapsed into one generic memory store.

### 1. Conversation state

Short-lived conversational context:

- active user request
- recent turns
- pending confirmation
- current tool transaction IDs

Retention: bounded and configurable.

### 2. Agent preferences

User-approved preferences that affect how GROL behaves.

Examples:

- preferred room aliases
- preferred response verbosity
- preferred confirmation behavior within policy limits

These belong in a GROL-owned local store, not in model-only memory.

### 3. Home state

Device/entity/automation state remains authoritative in Home Assistant.

Examples:

- light state
- thermostat state
- scene definitions
- automation definitions
- entity registry

Grok Bot may cache this briefly but must not become the source of truth.

### 4. System state

System/update/network/hardware state is authoritative in GROL host services.

Examples:

- current GROL version
- active RAUC slot
- update status
- network health
- service health

Again, Bot may consume but not own it.

### 5. Secrets

Secrets are never Bot memory.

Provider keys, HA tokens, signing keys, and host credentials are resolved by the relevant service and never exposed to model context.

## Session lifecycle

Suggested states:

```text
idle
listening
thinking
tool_pending
confirmation_pending
executing
responding
degraded
error
```

Transitions must be observable to the UI.

## Tool request behavior

The Bot may request only tools advertised by the Action Broker.

Unknown tools are treated as unavailable, not dynamically executed.

Each tool request must preserve:

- session ID
- response/turn ID
- provider tool-call ID when available
- GROL request ID
- user intent summary
- structured arguments

## Degraded mode

If Grok/xAI is unavailable:

- Bot reports AI unavailable/degraded
- existing Home Assistant automation continues
- pending privileged actions are not silently replayed later
- local UI remains functional
- recovery/update controls remain accessible without AI

## Restart behavior

After restart:

- unresolved confirmations expire
- incomplete privileged actions are reconciled from broker audit state
- conversational context may resume only from persisted, allowed state
- no tool execution resumes merely because a prior model turn requested it

## Initial acceptance tests

- model cannot directly invoke an unknown tool
- restarting Bot does not replay an action
- provider outage leaves HA automations operational
- Home Assistant remains authoritative for entity state
- secrets never appear in model-visible diagnostic output
