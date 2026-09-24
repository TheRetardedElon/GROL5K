# Grok Bot product plan

**Status:** accepted planning doc (2026-09-24).  
**Does not authorize M3/M4 implementation yet.**

## Product sentence

GROL5000 is a home OS you talk to. Grok Bot is the only mouth. Grok is the brain. Grok Build is a contractor in a locked room. Home Assistant is the wiring. The Action Broker is the fuse box.

## Three different Grok things

Do not collapse these names.

| Name | What it is | Role on GROL5000 |
|---|---|---|
| **Grok** | xAI models (text, voice, coding) | Brain behind `grol-ai-gateway` |
| **Grok Bot** | Persistent household agent (`grol-bot`) | Only thing the user talks to |
| **Grok Build** | xAI coding agent CLI / harness (`grok`, ACP, skills, MCP) | A tool the Bot may *request*, never a second OS owner |

Grok Build on a developer workstation (building this repo) is unrelated to Grok Build on the appliance. Laptop use stays on the laptop.

## User-visible flow

```text
"Hey Grok, turn on the kitchen lights"
"Hey Grok, draft an automation that dims the hall at sunset"
                |
                v
         GROL UI / voice satellite
                |
                v
            grol-bot
                |
                v
         grol-ai-gateway   <-- Grok text / Grok Voice / later Build harness
                |
                v
         grol-action-broker
           |-- Home Assistant (granted lights/switches only in v0)
           |-- GROL Host API (status only in v0)
           +-- grol-build sandbox (not in v0)
```

If xAI is unreachable: local Home Assistant automations continue. Bot reports degraded. Nothing privileged is replayed when connectivity returns.

## Grok Build rules

Grok Build is a coding agent that can run shell, edit files, speak MCP, and loop until a task finishes. On a workstation that is the point. On an appliance that is a rootkit installer unless isolated.

**Grok Build never gets** the Docker socket, the Host API socket, an HA admin token, or the data partition as a writable workspace.

Rollout:

1. **Advice only (first M4).** Bot asks a coding model for an HA automation *draft*. Result is a proposal. User sees it in UI. Broker still does not create automations/scripts/scenes in v0.
2. **Sandboxed Build (after M4, needs ADR).** Headless `grok -p …` in a disposable container: scratch dir only, no host mounts of `/`, no HA, no Host API, network allowlist to xAI only. Bot receives a summary + files. Applying them is a separate brokered action.
3. **Developer workstation.** Humans/GPT/Grok use Grok Build to work on `GROL5K`. That is not an OS feature.

The future tool name is `grol.build.propose`. There is no `shell.exec`.

Normative isolation notes: `grol/specs/GROK_BUILD_V0.md` and ADR-0004.

## Voice ladder

Spoken "yes" is not confirmation in v0. Ambient audio is a threat source.

| Step | User experience | When |
|---|---|---|
| Push-to-talk in GROL UI / companion | Same Bot, Grok Voice realtime, tools through broker | M3 voice path + M4 broker |
| HA voice satellite / phone as mic | Same session, local transport → gateway | M5 |
| Wake word "Hey Grok" | After false-accept rate is measured | after M5 |

First house command that should work:

```text
User: turn on the kitchen lights
Bot:  kitchen lights aren't approved for AI control yet.
      [Approve light.kitchen_main]  [Not now]
```

Empty entity grant list at ship. Conversation text cannot create grants. See `HOME_ASSISTANT_TOOL_POLICY_V0.md`.

## Sequencing (do not skip)

1. Finish **M1-B1 visual inspect** of the current OVA (GRUB/`Grol5k.png`, boot text, `grol5000 login:`).
2. **M1-B2** polished startup. Rebuild OVA. Same QEMU suite plus identity tests.
3. **M2** host layer: `grol-hostd`, identity, health, provision (xAI key slot + empty grant file). No model code.
4. **Thin M3**: `grol-ai-gateway` only. Provisioned key. Text stream + tool-call events. Hosted tools off. Degraded banner.
5. **Thin M4**: `grol-bot` + Action Broker. `homeassistant.state.read` + granted `light.*` / `switch.*`. Confirmation UI. Audit. Push-to-talk voice on the same broker path.
6. **Later**: `grol.build.propose`, automation-create ADR, wake word.

## Non-goals for the next engineering month

- install the `grok` CLI on the GROL image with host filesystem access
- enable xAI MCP / web_search / provider-hosted tools on the household session
- let Bot create HA scripts or scenes
- ship a wake word before push-to-talk works
- start M3 runtime before M1-B2 is visually accepted and M2 sockets exist
