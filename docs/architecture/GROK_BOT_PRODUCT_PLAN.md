# Grok Bot product plan

**Status:** accepted planning doc (amended 2026-09-25, ADR-0005).  
**Does not authorize M3/M4 implementation this week.**

## Product sentence

GROL5000 is Home Assistant turned into a home operating system you talk
to. Grok Bot is the operator. Grok is the intelligence. Grok Build is a
native construction runtime behind a broker. Home Assistant is ancestry
and the integration ecosystem, not the ceiling.

## End-state (this is the product)

```text
                 YOU
                  |
                  v
              Grok Bot
                  |
        +---------+----------+
        v                    v
   Grok reasoning        Grok Build
        |                    |
        |              inspect / code /
        |              test / diagnose
        +---------+----------+
                  v
          GROL Capability Layer
                  |
      +-----------+------------+
      v           v            v
 GROL Core   GROL Supervisor   Host OS
      |           |            |
      +-----------+------------+
                  v
           Physical house
```

Grok Bot is woven through Core, frontend, CLI, voice, grants, and Build.
It is not a dashboard gadget talking to an unmodified Home Assistant.

We will own, over the life of the project:

- this OS repo
- Supervisor
- Core
- frontend
- CLI presentation
- Bot, gateway, broker, buildd

We merge upstream HA so their integrations keep landing. We do not treat
those repos as forbidden to change.

## Three different Grok things

Do not collapse these names.

| Name | What it is | Role on GROL5000 |
|---|---|---|
| **Grok** | xAI models (text, voice, coding) | Brain behind `grol-ai-gateway` |
| **Grok Bot** | Persistent household operator (`grol-bot`) | What the user talks to; eventually a Core-level agent |
| **Grok Build** | Native `grol-buildd` plus xAI coding models | How Bot constructs automations, integrations, dashboards, GROL itself |

Grok Build on a developer laptop working this git repo is separate from
appliance `grol-buildd`.

## Grok Build is native

Bot is supposed to be able to say:

- I need an automation for this
- I need a new integration
- I need to change this dashboard
- I need to diagnose this device
- I need to modify GROL configuration

and invoke Build.

Build may inspect configuration and schemas, draft automations and
integrations, generate dashboards, modify GROL-owned components, run
tests, stage patches, request privileged apply, and roll back a failed
change.

Build may **not** be: cloud model → unrestricted root shell.

Apply still goes through the capability broker. That is an executor
boundary, not a claim that Build is optional or off-box.

Normative isolation: `grol/specs/GROK_BUILD_V0.md`, ADR-0004, ADR-0005.

## Voice ladder

Spoken "yes" is not confirmation in the first voice slice.

| Step | User experience | When |
|---|---|---|
| Push-to-talk | Bot + Grok Voice, tools through broker | M3 path + M4 broker |
| Satellite / phone mic | Same session | M6 UX |
| Wake word "Hey Grok" | After false-accept is measured | after M6 |

## Sequencing (order of work, not a ban list)

1. M1-B2 polish on the OS we already booted.
2. M2 host layer in this repo (`grol-hostd` …).
3. Thin M3 gateway.
4. Thin M4 Bot + broker + first granted lights/switches.
5. **M5 begin GROL Core / Supervisor / frontend repos** and first-class
   `grol.*` domain objects. This is planned ownership, not a maybe.
6. M6 GROL-owned UX / onboarding / CLI face.
7. M7 retire remaining HA product identity while keeping integrations.
8. M8 GROL-owned distribution.

M1 does not fork Core to change "Preparing Home Assistant." M5 does fork
Core because GROL5000 is the product.

## Non-goals for the next engineering month

- unsandboxed `grok` CLI on the live appliance rootfs
- provider-hosted tools on the household session
- spoken "yes" as confirmation
- pretending Core is off-limits forever
