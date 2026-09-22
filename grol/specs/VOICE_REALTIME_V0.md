# GROL Voice / Realtime Session v0

Status: design draft.

## Purpose

Define the lifecycle between microphone/UI input, Grok realtime capabilities, Bot state, and brokered actions.

Voice is a transport and interaction mode. It does not receive extra authorization privileges.

## Session lifecycle

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

## Barge-in

When the user starts speaking while the Bot is speaking:

1. stop/attenuate TTS immediately
2. cancel or truncate the current provider output if supported
3. preserve tool transactions already committed to the broker
4. do not cancel an executing privileged action merely because speech output was interrupted
5. start a new turn with clear correlation IDs

## Tool calls during realtime sessions

Tool calls follow the exact same Action Broker path as text sessions.

Realtime provider events are normalized into the provider adapter event stream.

The voice transport must never:

- bypass confirmation
- execute a tool locally
- infer confirmation from background speech
- send provider credentials to the UI

## Confirmation

For consequential actions, confirmation should be explicit and scoped.

Voice confirmation may be supported later, but the broker must receive a distinct authenticated confirmation event tied to:

- request ID
- exact tool
- exact normalized arguments
- expiration time

A generic "yes" outside the pending confirmation state must not authorize a tool.

## Cancellation

Cancellation semantics need three independent concepts:

- cancel model generation
- cancel speech playback
- cancel pending broker request

These are not interchangeable.

Once an executor has begun an operation that cannot safely be interrupted, UI cancellation should report that the action is already in progress rather than pretending it was stopped.

## Offline behavior

If realtime/xAI is unavailable:

- text/local UI remains available where possible
- HA automation remains available
- UI shows degraded AI state
- no pending privileged request is replayed automatically when connectivity returns
