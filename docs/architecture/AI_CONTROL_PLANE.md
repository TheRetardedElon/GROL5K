# GROL5K AI Control Plane

## Objective

GROL5K integrates Grok and Grok Bot as first-class operating-system capabilities without making the model itself a privileged system process.

Product plan: `docs/architecture/GROK_BOT_PRODUCT_PLAN.md`.

## Names

- **Grok** — xAI models behind `grol-ai-gateway`
- **Grok Bot** — `grol-bot`, the only user-facing agent
- **Grok Build** — optional coding harness, requested only as `grol.build.propose`, never an OS owner (ADR-0004)

## Components

### grol-ai-gateway

Provider-facing service responsible for:

- xAI authentication
- model selection
- streaming responses
- realtime/voice sessions
- tool schema publication
- request/response normalization
- rate and timeout handling
- provider abstraction for future model backends

The gateway does not execute privileged host actions.
The gateway does not enable provider-hosted tools in v0.
The gateway owns the provider WebSocket; the UI never holds `XAI_API_KEY`.

### grol-bot

Persistent GROL5000 agent runtime responsible for:

- conversational context
- intent interpretation
- multi-step planning
- environment summaries
- user-visible explanations
- tool selection
- asking the Action Broker to perform approved actions

Grok Bot is an agent, not a root shell.

### grol-action-broker

The sole privileged-action boundary.

Responsibilities:

- validate requested actions
- map requests to known capabilities
- enforce policy and user authorization
- issue short-lived capability grants
- audit actions
- reject unknown or unsafe operations
- mediate access to Home Assistant services and selected host APIs

Home Assistant mutation uses entity-level grants. Scripts, scenes, and generic `homeassistant.turn_*` are denied in v0.

## Example flow

```text
User
  ↓
GROL UI / Voice
  ↓
Grok Bot
  ↓
AI Gateway
  ↓
Tool request
  ↓
Action Broker
  ↓
Policy decision
  ├─ deny
  ├─ confirm with user
  └─ execute
        ↓
 Home Assistant / GROL service / (later) build proposal store
```

## Risk tiers

- Tier 0 — read-only status and information
- Tier 1 — reversible low-risk automation actions
- Tier 2 — consequential environment changes requiring stronger policy checks
- Tier 3 — security-sensitive actions requiring explicit confirmation
- Tier 4 — host/system administration, disabled by default and narrowly capability-scoped

## Non-goals

The AI layer must not receive:

- unrestricted Docker socket access
- unrestricted DBus access
- direct root shell access
- long-lived broad host credentials
- silent permission escalation
- unsandboxed Grok Build / `grok` CLI on the host
- provider-hosted MCP or web_search on the household session
