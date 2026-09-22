# Home Assistant Tool Policy v0

**Status:** design draft.  
**Revised:** 2026-09-22 (v0.4.1 Grok follow-up)

## Purpose

This policy defines what `grol-action-broker` may expose through the AI-facing Home Assistant tool path.

A domain + service allowlist is necessary but not sufficient. Home Assistant can route apparently simple services through scripts, scenes, template entities, helpers, automations, webhooks, and integrations whose effects are much broader than the service name suggests.

The v0 rule is therefore:

> **A mutating HA call is allowed only when both the service and every resolved target are explicitly eligible under broker policy.**

## v0 mutating services

Eligible service names:

- `light.turn_on`
- `light.turn_off`
- `light.toggle`
- `switch.turn_on`
- `switch.turn_off`
- `switch.toggle`

Eligibility does **not** mean blanket authorization.

Every resolved target must pass the entity policy below.

Prefer `turn_on` / `turn_off` over `toggle` when the user intent is directional. `toggle` is allowed but is race-prone against live state and should default to `confirmation_required` unless the entity is classified `low_risk_mutation`.

## Explicitly disabled in v0

These are not AI-callable in v0, even when they already exist:

- `script.turn_on`
- `scene.turn_on`
- `homeassistant.turn_on` / `homeassistant.turn_off` / `homeassistant.turn_toggle`
- automation trigger/create/update
- helper create/update
- `shell_command.*`
- `command_line.*`
- `rest_command.*`
- `python_script.*`
- lock, alarm, cover, security-system domains
- fan, climate, media_player, vacuum, water_heater, siren
- any generic service-call escape hatch

Reason: scripts and scenes can contain transitive effects that bypass the visible domain/service allowlist. The generic `homeassistant.turn_*` services can address mixed domains in one call. They may return in a later policy only after the broker has a reviewed way to prove or constrain their effect graph.

## Target policy

For Tier >= 1 calls, the broker resolves requested targets against the **live Home Assistant registry at execution time**.

A target is executable only if:

1. it resolves to a current entity registry entry,
2. the entity's current domain matches the requested service domain,
3. the entity is allowed by GROL policy for AI mutation,
4. the entity is not marked restricted/denied,
5. the entity's current integration/platform matches the platform recorded in the policy grant,
6. any area/device/label/floor/group expansion resolves entirely to individually allowed entities,
7. the normalized target set matches the confirmed target set when confirmation is required.

Group, template, `command_line`, `rest`, and MQTT command entities are **denied for mutation in v0** unless a later policy explicitly classifies that exact registry identity and platform. A `switch` is not trusted merely because its domain is `switch`.

### Default posture

v0 is **explicit allow**, not "all lights and switches are safe."

New entities discovered after provisioning are read-only until policy classifies them.

Suggested broker-side policy classes:

- `read_only`
- `low_risk_mutation`
- `confirmation_required`
- `denied`

The effective risk is the maximum of:

- tool/service baseline risk,
- entity policy risk,
- contextual policy escalation.

The model cannot lower any of these values.

### Who writes policy

Entity grants are user-owned configuration, not model memory.

`grol-provision` / GROL UI may create or change grants. `grol-bot` may request a grant change only as a non-executing suggestion. The Action Broker never infers a new mutation grant from conversation text.

v0 can ship with an empty grant list. That means the AI path can read (redacted) and cannot mutate until the household approves specific lights/switches.

## Entity identity

Human-facing `entity_id` values may be renamed. Integrations can also be swapped under the same `entity_id`.

GROL mutation grants bind to **all** of:

- Home Assistant entity-registry id (stable id),
- current domain,
- current integration / platform.

The current `entity_id` is resolved at execution time and is not the grant key.

If any bound field cannot be proven, or if platform/integration drifted since the grant, deny mutation and require policy reprovisioning.

## Multi-target calls

If a request targets multiple entities, an area, a device, a label, a floor, or an expanded group:

- resolve the complete concrete entity set before policy evaluation,
- apply policy to every member,
- deny the entire call if any target is denied or unresolved,
- do not silently drop disallowed members and execute the rest.

This avoids turning an apparently safe area/group request into an unintended mixed-risk action.

## Service data

Each allowed service has a dedicated JSON schema.

Examples:

### `light.turn_on`

May eventually allow bounded fields such as:

- brightness
- brightness_pct
- color_temp_kelvin
- rgb_color

Unknown fields are rejected. `flash`, `effect`, and profile names are denied in v0 until separately reviewed.

### `switch.turn_on/off/toggle`

No arbitrary service data beyond the validated target selector in v0.

## Read path

`homeassistant.state.read` can cover more domains than the mutation path, but model-facing output is still minimized.

Default redaction should exclude or summarize sensitive attributes such as:

- access codes
- tokens
- raw location coordinates
- alarm/security secrets
- camera credentials/URLs
- personally identifying device metadata not required by the request

Read access does not imply mutation eligibility.

## Confirmation binding

When a call requires confirmation, the broker freezes:

- tool name,
- normalized service data,
- stable resolved target identities,
- integration/platform for each target,
- effective policy/risk class.

The confirmation digest uses a versioned, domain-separated preimage. Resolved targets are first-class fields, not an accident of `arguments`:

```text
sha256(
  "grol-confirm-v0\0" +
  tool + "\0" +
  canonical_json(normalized_args) + "\0" +
  canonical_json(resolved_targets) + "\0" +
  effective_risk_class
)
```

`resolved_targets` is a sorted list of `{registry_id, domain, platform, entity_id}`.

Any change to the confirmed arguments or resolved target set invalidates confirmation.

## Future scripts/scenes

A future policy MAY allow selected existing scripts or scenes only if one of these approaches is accepted by ADR:

1. static/transitive effect analysis proves the called graph stays inside approved capabilities, or
2. the user explicitly approves a specific immutable version/hash and the broker can detect graph changes.

Until then, scripts/scenes stay outside the AI mutation path.

## Acceptance tests

- newly discovered switch is not mutable by default
- area expansion containing one denied entity denies the whole request
- renamed entity resolves through stable registry identity
- unresolved registry identity denies mutation
- platform/integration drift since the grant denies mutation
- template / command_line / rest / MQTT-command switch denied in v0 unless explicitly granted
- existing script that calls `shell_command` cannot be invoked by AI
- scene that includes a restricted entity cannot be invoked by AI
- `homeassistant.turn_off` denied even when every member would have been an allowed light
- extra `light.turn_on` service data is rejected
- model-supplied lower risk value does not affect broker policy
- conversation text cannot create a mutation grant
