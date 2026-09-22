# GROL5K Component Boundaries

## GROL UI

May display Home Assistant state, converse with Grok Bot, show confirmations, and display system/update health.

Must not hold root credentials, talk directly to privileged host sockets, or bypass the Action Broker for sensitive actions.

## grol-ai-gateway

Purpose: provider adapter and session transport.

May authenticate to configured AI providers, stream responses, expose model capabilities, normalize tool calls, and manage realtime sessions.

Must not execute host commands, call Docker directly, or mutate Home Assistant without a brokered tool.

## grol-bot

Purpose: persistent conversational agent.

May interpret intent, plan, maintain allowed context, request tools, and explain outcomes.

Must not be trusted as an authorization source, possess unrestricted host privilege, or silently escalate an action's risk tier.

## grol-action-broker

Purpose: policy enforcement and capability execution.

May validate structured tool requests, check policy, request confirmation, invoke approved HA/GROL APIs, and write audit records.

Must not accept arbitrary shell text as a capability, accept unknown tools by default, or let model prose override policy.

## Home Assistant compatibility layer

Purpose: device, entity, automation, app, and integration ecosystem.

Early GROL5K policy: preserve compatibility and use documented/control-plane APIs rather than patching Core for every GROL feature.

## GROL host services

Purpose: OS-level functions that do not belong in Home Assistant.

Examples: system identity, update status, hardware health, provisioning, recovery, and GROL service health.

Expose narrow APIs to the Action Broker rather than broad root access.

## Secrets boundary

Provider keys, signing keys, and sensitive tokens are never model context by default.

AI services should receive only the minimum credential material required for their own outbound provider session.
