# GROL Voice / Realtime Session v0

**Status:** design draft.  
**Revised:** 2026-09-22 (v0.3 adversarial review)

## Purpose

Define the lifecycle between microphone/UI input, Grok realtime capabilities, Bot state, and brokered actions.

Voice is a transport and interaction mode. It does not receive extra authorization privileges.

Voice session states are a **projection** of the Bot runtime FSM in `GROK_BOT_RUNTIME_V0.md`. They are not a second source of truth.

## Session lifecycle

Projected voice states:

```text
created
connecting
ready
listening
speech_detected
thinking
speaking
interrupted
closing
closed
failed
```

The UI must be able to distinguish:

- provider connecting
- microphone unavailable
- provider unavailable
- model thinking
- tool confirmation pending
- Bot speaking
- user interruption/barge-in

## Transport ownership

The provider WebSocket is owned by `grol-ai-gateway` only.

Path:

```text
mic/speaker ↔ local voice transport ↔ grol-bot / UI ↔ grol-ai-gateway ↔ provider
```

Forbidden in v0:

- UI holding `XAI_API_KEY`
- UI connecting to `wss://api.x.ai` with an ephemeral token
- Bot speaking the realtime protocol directly

## Provider tool policy

Realtime `session.tools` MAY contain only GROL function tools that already exist in the Action Broker catalog.

MUST NOT enable in v0:

- `web_search`
- `x_search`
- `file_search` / collections
- `mcp`
- any other provider-hosted execution surface

## Correlation map

Mandatory fields:

| GROL | Provider (xAI realtime example) |
|---|---|
| `grol.session_id` | local |
| `provider.session_id` | `session.id` |
| `grol.turn_id` | local |
| `provider.response_id` | `response.id` |
| `provider.call_id` | function `call_id` |
| `grol.request_id` | Action Broker `request_id` |

All GROL IDs plus `provider.call_id` MUST survive barge-in, cancellation, and tool execution.

## Event normalization

Map at least:

| Provider event (xAI example) | GROL event |
|---|---|
| `input_speech_started` | `audio.input_speech_started` |
| `input_speech_stopped` | `audio.input_speech_stopped` |
| `response.output_audio.delta` | `audio.delta` |
| `response.function_call_arguments.done` | `tool.requested` |
| `response.cancelled` | `response.cancelled` |
| `session.updated` | `session.updated` (gateway-internal) |

Do not normalize away `call_id`, `response.id`, or cancellation reason.

xAI event names may change. The adapter, not the rest of the OS, absorbs that.

## Barge-in

When the user starts speaking while the Bot is speaking:

1. stop/attenuate local TTS immediately
2. gateway cancels the *generation*, not the whole provider session
3. Bot enters `interrupted`
4. broker transactions already `executed` or `executing` continue
5. broker transactions still `confirmation_required` remain pending and are **not** auto-confirmed by the interrupting utterance
6. start a new turn with a new `grol.turn_id`

Server VAD does not authorize anything.

Preserve tool transactions already committed to the broker.

## Tool calls during realtime sessions

Tool calls follow the exact same Action Broker path as text sessions.

Realtime provider events are normalized into the provider adapter event stream.

The voice transport must never:

- bypass confirmation
- execute a tool locally
- infer confirmation from background speech
- send provider credentials to the UI

## Confirmation

The Action Broker owns the confirmation token and the argument digest.

For consequential actions, confirmation should be explicit and scoped.

v0 confirmation is a UI/broker event, not a spoken "yes".

The voice session may stay open. The pending tool is frozen until:

- broker receives `confirm(request_id, arg_digest)`, or
- the token expires, or
- the user cancels

Voice confirmation may be supported later via a dedicated ADR. A generic "yes" outside the pending confirmation state must not authorize a tool.

The broker must receive a distinct authenticated confirmation event tied to:

- request ID
- exact tool
- exact normalized arguments (`sha256(tool + canonical_json(args))`)
- expiration time

## Cancellation

Cancellation semantics need three independent concepts. They are not interchangeable.

| Intent | Affects | Does not affect |
|---|---|---|
| cancel generation | provider response + TTS | executing broker ops |
| cancel playback | local speaker only | provider or broker |
| cancel pending tool | broker request still not executing | already-started irreversible ops |

Once an executor has begun an operation that cannot safely be interrupted, UI cancellation should report that the action is already in progress rather than pretending it was stopped.

## Session limits

Gateway MUST rotate or close provider sessions before published provider max duration.

Resume is a new provider session plus an allowed local conversation projection.

No silent replay of tools on reconnect.

## Audio data

Raw audio is not Bot durable memory.

Do not write raw audio to the data partition by default.

Do not put transcripts of other household members into durable memory without an explicit later privacy ADR.

## Offline behavior

If realtime/xAI is unavailable:

- text/local UI remains available where possible
- HA automation remains available
- UI shows degraded AI state
- no pending privileged request is replayed automatically when connectivity returns
