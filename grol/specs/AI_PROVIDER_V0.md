# GROL AI Provider Adapter v0

**Status:** design draft for GPT + Grok review.  
**Revised:** 2026-09-22 (v0.3 adversarial review)

The purpose of this contract is to keep the GROL AI control plane provider-aware but not provider-coupled.

The initial provider is expected to be Grok/xAI, but GROL services should depend on this adapter contract rather than scattering provider-specific request shapes throughout the OS.

Provider-specific mapping lives in Annex A. The core event and capability names stay generic.

## Responsibilities

A provider adapter may:

- report provider/model capabilities
- establish authenticated sessions
- stream text/model events
- support structured tool-call events
- support realtime audio where available
- cancel an active generation/session
- report provider health and rate/error state

A provider adapter must not:

- directly execute GROL tools
- directly access Home Assistant privileged APIs
- receive host root credentials
- decide whether a requested action is authorized
- enable provider-hosted tools unless an ADR allows a specific read-only tool

Tool execution remains the responsibility of the GROL Action Broker.

## Capability model

Suggested capability names:

```text
text
text_stream
tool_calls
vision
audio_input
audio_output
realtime
structured_output
server_vad
ephemeral_tokens
provider_hosted_tools
```

The gateway should negotiate behavior from declared capabilities rather than assuming every model supports every mode.

`ephemeral_tokens` may be reported if the provider supports them. GROL UI must not use them in v0.

`provider_hosted_tools` MUST be reported when present and MUST default off.

## Normalized event stream

Provider-specific responses should be translated into a small GROL event set:

```text
session.started
session.updated
response.started
text.delta
text.completed
tool.arguments.delta
tool.requested
audio.delta
audio.input_speech_started
audio.input_speech_stopped
response.completed
response.cancelled
response.failed
error.rate_limited
error.auth_failed
session.closed
```

## Tool request normalization

Provider tool/function calls are normalized into the Action Broker envelope defined by:

- `grol/specs/ACTION_BROKER_V0.md`
- `grol/specs/action-request.schema.json`

Provider-supplied risk labels never override broker policy.

IDs that MUST be preserved end-to-end:

- provider session id
- provider response id
- provider function call id
- GROL request_id / session_id / turn_id

## Secret handling

- provider credentials are provisioned at runtime
- secrets are not baked into OS images
- secrets are not written to model-visible logs
- model context never receives the raw API credential
- adapters should support credential rotation without rebuilding the OS

## Failure behavior

If the provider is unavailable:

1. local Home Assistant automations continue
2. GROL UI reports AI degraded/offline state
3. queued privileged actions are not silently replayed without policy review
4. the Action Broker remains available for non-AI callers if designed to support them
5. recovery should not require a provider connection

## Cancellation and retry

- adapter `cancel()` cancels generation/session transport only
- it never implies broker abort of an executing capability
- transport retries are allowed with backoff
- tool execution is never retried as a side effect of reconnect
- on reconnect, in-flight `tool.requested` MUST be reconciled from broker audit, not replayed from model memory

## Annex A — xAI/Grok mapping

Informative to the core contract. Normative for the first adapter.

### Endpoints (current public xAI surface)

- Text/tooling: existing xAI Responses / chat APIs used by the gateway
- Realtime voice: `wss://api.x.ai/v1/realtime` with a pinned model id
- Aliases such as `grok-voice-latest` are dev-only. Production config pins a versioned model.

### Realtime session ownership

The gateway terminates the provider WebSocket.

The UI never holds `XAI_API_KEY` and does not use ephemeral tokens in v0.

### Hosted tools

xAI realtime can attach `web_search`, `x_search`, `file_search` / collections, and remote MCP.

The first adapter MUST leave those off. Only GROL `function` tools that map 1:1 to the Action Broker catalog may be advertised to the model.

Enabling any non-function provider tool requires an ADR.

### Example event map

| xAI realtime event | GROL event |
|---|---|
| `session.created` / `session.updated` | `session.started` / `session.updated` |
| `input_speech_started` | `audio.input_speech_started` |
| `input_speech_stopped` | `audio.input_speech_stopped` |
| `response.output_text.delta` / `response.text.delta` | `text.delta` |
| `response.output_audio.delta` | `audio.delta` |
| `response.function_call_arguments.delta` | `tool.arguments.delta` |
| `response.function_call_arguments.done` | `tool.requested` |
| provider cancel/complete/error events | `response.cancelled` / `response.completed` / `response.failed` |

Exact provider event names should be re-checked against live xAI docs at M3 implementation time. The rest of the OS depends only on the GROL names.

### Open items for M3

- pin production text and voice model IDs
- confirm the live cancel-event name
- confirm current session max duration and concurrent-session caps
- decide whether text and voice share one gateway process or two adapters behind the same contract
