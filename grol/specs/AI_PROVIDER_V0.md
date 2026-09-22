# GROL AI Provider Adapter v0

Status: design draft for GPT + Grok review.

The purpose of this contract is to keep the GROL AI control plane provider-aware but not provider-coupled.

The initial provider is expected to be Grok/xAI, but GROL services should depend on this adapter contract rather than scattering provider-specific request shapes throughout the OS.

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
```

The gateway should negotiate behavior from declared capabilities rather than assuming every model supports every mode.

## Normalized event stream

Provider-specific responses should be translated into a small GROL event set:

```text
session.started
response.started
text.delta
text.completed
tool.requested
audio.delta
response.completed
response.failed
session.closed
```

## Tool request normalization

Provider tool/function calls are normalized into the Action Broker envelope defined by:

- `grol/specs/ACTION_BROKER_V0.md`
- `grol/specs/action-request.schema.json`

Provider-supplied risk labels never override broker policy.

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

## Initial Grok review questions

- Which Grok API features map cleanly to the proposed capability model?
- What realtime session lifecycle should the gateway expose?
- Which provider events must be preserved rather than normalized away?
- What cancellation and retry semantics are required?
- What tool-call identifiers must survive end-to-end for tracing?
