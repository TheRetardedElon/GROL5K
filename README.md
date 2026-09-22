<p align="center">
  <img src="https://i.imgur.com/kBDHbaq.png" width="900" alt="GROL5000 — Global Robotic Overlord Logic">
</p>

<h1 align="center">GROL5K</h1>

<p align="center">
  <strong>Global Robotic Overlord Logic</strong><br>
  A purpose-built smart-environment operating system derived from Home Assistant OS, with a GROL-owned system layer, user experience, and AI control plane built around Grok and Grok Bot.
</p>

<p align="center">
  <img alt="Status" src="https://img.shields.io/badge/status-early%20development-b31b1b">
  <img alt="Version" src="https://img.shields.io/badge/version-0.1.0--dev-555">
  <img alt="Base" src="https://img.shields.io/badge/base-Home%20Assistant%20OS-18BCF2">
  <img alt="License" src="https://img.shields.io/badge/license-Apache--2.0-blue">
</p>

---

## What is GROL5K?

**GROL5K** is a downstream operating-system project based on
[Home Assistant Operating System](https://github.com/home-assistant/operating-system).

The project begins with HAOS's mature embedded-Linux foundation — Buildroot, systemd,
Docker, AppArmor, RAUC, GRUB/U-Boot, OS Agent, Supervisor compatibility, and broad
hardware support — then progressively adds a distinct GROL5000 platform on top.

The objective is **not** to make a themed copy of Home Assistant OS.

The objective is to build a real GROL5000 operating system with its own:

- boot and system identity
- first-run and provisioning experience
- system services and health layer
- user interface
- release and update pipeline
- Grok integration
- persistent Grok Bot agent
- permissions and action broker
- voice and conversational control
- security policies
- developer and hardware targets

Home Assistant remains an important compatibility and automation layer underneath while
GROL5K progressively takes ownership of the surrounding operating experience.

> **Current state:** GROL5K is in early development. The first milestone is reproducibly
> building and booting the upstream HAOS baseline before changing compatibility-sensitive
> internals.

---

## Architecture

```text
┌────────────────────────────────────────────────────────────┐
│                    GROL5000 Experience                     │
│   UI · Voice · Setup · Status · Recovery · System Console │
├────────────────────────────────────────────────────────────┤
│                    GROL AI Control Plane                   │
│ Grok Gateway · Grok Bot · Action Broker · Policy Engine   │
├────────────────────────────────────────────────────────────┤
│              Home Automation Compatibility Layer           │
│ Home Assistant Core · Supervisor · Apps · Integrations    │
├────────────────────────────────────────────────────────────┤
│                     GROL System Layer                      │
│ Identity · Health · Provisioning · Telemetry · Updates    │
├────────────────────────────────────────────────────────────┤
│                    GROL5K / HAOS Base                      │
│ Buildroot · systemd · Docker · AppArmor · RAUC · GRUB     │
├────────────────────────────────────────────────────────────┤
│                         Hardware                           │
└────────────────────────────────────────────────────────────┘
```

### AI privilege boundary

Grok and Grok Bot are designed as first-class system capabilities, but **the model is
not the operating system's root user**.

Privileged actions are intended to pass through a dedicated GROL Action Broker:

```text
User
  │
  ▼
GROL UI / Voice
  │
  ▼
Grok Bot
  │
  ▼
GROL AI Gateway
  │
  ▼
Tool request
  │
  ▼
GROL Action Broker
  ├── deny
  ├── request confirmation
  └── execute approved capability
          │
          ├── Home Assistant API
          └── constrained GROL host API
```

This keeps AI reasoning, automation control, and host administration in separate trust
domains.

---

## Development roadmap

| Milestone | Goal | Status |
|---|---|---|
| **M0** | Reproduce the upstream HAOS build and boot it unchanged | 🚧 In progress |
| **M1** | GROL5000 identity, hostname, boot visuals, release metadata | Planned |
| **M2** | GROL-owned system services and health layer | Planned |
| **M3** | Grok gateway, streaming, configuration, voice foundation | Planned |
| **M4** | Grok Bot, action broker, policy engine, audit trail | Planned |
| **M5** | Full GROL5000 UI, setup and primary operating experience | Planned |
| **M6** | GROL-owned signed release/update pipeline | Planned |
| **M7** | Additional validated hardware targets | Planned |

The initial development path is:

```text
OVA / QEMU
    ↓
Generic x86-64 UEFI
    ↓
Raspberry Pi 5
    ↓
Additional qualified hardware
```

---

## Repository strategy

GROL5K intentionally keeps a traceable relationship with upstream HAOS.

The initial upstream baseline is:

```text
Repository: home-assistant/operating-system
Branch:     dev
Commit:     3019c7fe8745900a3e9dcb3879d96bacf7958543
```

We avoid deep internal renaming during the first milestones. Compatibility-sensitive
items such as Supervisor plumbing, OS Agent identifiers, partition labels, RAUC slot
definitions, and internal HAOS paths remain intact until there is a tested reason to
change them.

GROL-specific functionality should be additive and isolated wherever practical.

---

## GROL-owned project structure

```text
GROL5K/
├── grol/
│   ├── branding/        # GROL visual/system identity
│   ├── policies/        # permission and security policy
│   ├── release/         # GROL release metadata/tooling
│   └── services/        # GROL-owned system services
│
├── docs/
│   ├── architecture/
│   ├── development/
│   └── decisions/
│
├── buildroot-external/  # HAOS platform definitions + future GROL targets
├── buildroot/           # upstream Buildroot submodule
├── scripts/
├── tests/
├── GROL_VERSION
└── GROL_UPSTREAM.md
```

Long-term target naming is expected to move toward dedicated GROL definitions such as:

```text
grol5000_ova_defconfig
grol5000_x86_64_defconfig
grol5000_rpi5_defconfig
```

---

## Documentation

Start here:

- [Current development status](docs/development/STATUS.md)
- [Architecture overview](docs/architecture/OVERVIEW.md)
- [Component boundaries](docs/architecture/COMPONENT_BOUNDARIES.md)
- [AI control plane](docs/architecture/AI_CONTROL_PLANE.md)
- [Security model](docs/architecture/SECURITY_MODEL.md)
- [Codebase map](docs/development/CODEBASE_MAP.md)
- [M0 baseline checklist](docs/development/M0_BASELINE_CHECKLIST.md)
- [M1 identity conversion map](docs/development/M1_IDENTITY_MAP.md)
- [Human + GPT + Grok collaboration protocol](docs/development/AI_COLLABORATION.md)
- [Grok onboarding packet](docs/development/GROK_ONBOARDING.md)
- [Development roadmap](docs/development/ROADMAP.md)
- [Building GROL5K](docs/development/BUILDING.md)
- [Upstream baseline and sync policy](GROL_UPSTREAM.md)
- [ADR-0001 — HAOS downstream strategy](docs/decisions/0001-haos-downstream.md)
- [ADR-0002 — compatibility boundary](docs/decisions/0002-compatibility-boundary.md)
- [ADR-0003 — AI stays in userspace](docs/decisions/0003-ai-userspace-boundary.md)
- [Action Broker v0 contract](grol/specs/ACTION_BROKER_V0.md)
- [AI provider adapter v0](grol/specs/AI_PROVIDER_V0.md)
- [Grok Bot runtime v0](grol/specs/GROK_BOT_RUNTIME_V0.md)
- [GROL Host API v0](grol/specs/HOST_API_V0.md)
- [Tool/prompt injection threat model v0](grol/specs/THREAT_MODEL_TOOL_INJECTION_V0.md)
- [Voice/realtime session v0](grol/specs/VOICE_REALTIME_V0.md)
- [Build-record evidence](docs/build-records/README.md)

---

## Building

Clone the repository with submodules:

```bash
git clone --recurse-submodules https://github.com/TheRetardedElon/GROL5K.git
cd GROL5K
git checkout dev
git submodule update --init --recursive
```

During **M0**, use an existing upstream HAOS target unchanged. The first task is to prove
that the exact baseline can be built and booted reproducibly before GROL-specific OS
changes are introduced.

See [docs/development/BUILDING.md](docs/development/BUILDING.md) for the evolving build
procedure.

---

## Design principles

1. **Reproducibility before customization.**
2. **Additive changes before invasive rewrites.**
3. **AI never receives unrestricted root or Docker access.**
4. **Local home automation must continue when cloud AI is unavailable.**
5. **Signed updates and rollback are mandatory platform features.**
6. **Failure states must be observable and recoverable.**
7. **Upstream HAOS changes remain reviewable and importable.**
8. **GROL5K becomes progressively more independent only when each layer is tested.**

---

## Upstream and attribution

GROL5K is derived from the open-source
[Home Assistant Operating System](https://github.com/home-assistant/operating-system)
project and retains its upstream history.

Home Assistant, Home Assistant OS, and related upstream components are projects of their
respective maintainers and organizations. GROL5K is a separate downstream project and
does not claim to be an official Home Assistant distribution.

Keeping attribution and upstream history intact is part of the project's engineering
policy, not an afterthought.

---

## License

The inherited operating-system source is distributed under the
[Apache License 2.0](LICENSE). Individual bundled or referenced components may have their
own licenses.

---

<p align="center">
  <strong>GROL5000</strong><br>
  <em>Global Robotic Overlord Logic</em>
</p>
