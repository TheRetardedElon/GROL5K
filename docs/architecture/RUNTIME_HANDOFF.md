# Runtime handoff map

Repos now exist:

| GROL repo | Default branch | Upstream |
|---|---|---|
| `TheRetardedElon/grol5k` | `dev` | home-assistant/operating-system |
| `TheRetardedElon/grol-supervisor` | `main` | home-assistant/supervisor |
| `TheRetardedElon/grol-core` | `dev` | home-assistant/core |
| `TheRetardedElon/grol-frontend` | `dev` | home-assistant/frontend |
| `TheRetardedElon/grol-cli` | `master` | home-assistant/cli |

Do not start rewriting Core this week. First job is this map.

## What the live VM actually ran

```text
ghcr.io/home-assistant/qemux86-64-homeassistant:2026.10.0.dev202609250226
```

That string is not hardcoded in grol5k. It is assembled.

## Control points

### 1. Version index (what tag to pull)

`grol-supervisor/supervisor/updater.py` → `fetch_data()`

URL:

```text
https://version.home-assistant.io/{channel}.json
```

`grol5k` bakes the same URL in `buildroot-external/package/hassio/hassio.mk`
(`HASSIO_VERSION_URL`). OVA channel is `dev`.

From `dev.json`:

```text
homeassistant.qemux86-64 = 2026.10.0.dev202609250226
images.core              = ghcr.io/home-assistant/{machine}-homeassistant
images.supervisor        = ghcr.io/home-assistant/{arch}-hassio-supervisor
images.cli               = ghcr.io/home-assistant/{arch}-hassio-cli
```

`{machine}` comes from OS `SUPERVISOR_MACHINE` (`qemux86-64` on the OVA).
`{arch}` is `amd64` on that board.

### 2. Image template (which registry/name)

Same JSON `images.*` keys, applied in `updater.py`:

- Core: `.format(machine=sys_machine)`
- Supervisor/plugins: `.format(arch=sys_arch.supervisor)`

### 3. Install/start

`grol-supervisor/supervisor/homeassistant/core.py`

- first boot: `install_landingpage()` → tag `landingpage`
- then `install()` using `latest_version` from the updater
- `start()` runs that container; Core serves `:8123`

Frontend is **inside the Core image**, not a separate Supervisor pull.
`grol-frontend` matters when we build `grol-core` images.

### 4. What grol5k embeds at image-build time

`hassio.mk` downloads supervisor/dns/audio/cli/multicast/observer/core
via `fetch-container-image.sh`, but forces:

```text
.core = "landingpage"
```

so the OVA ships a landing-page Core and lets Supervisor replace it from
`version.home-assistant.io` after boot. That is exactly the progress bar
you watched.

## First GROL cut (later, not tonight)

To make Supervisor pull GROL Core we change **one index + one template**:

```text
version source  version.home-assistant.io/{channel}.json
             →  version.grol5000.dev/{channel}.json   (or equivalent)

images.core     ghcr.io/home-assistant/{machine}-homeassistant
             →  ghcr.io/<grol-org>/{machine}-grol-core
```

and point `HASSIO_VERSION_URL` in `hassio.mk` at that index.

Until that index exists and publishes real tags, keep pulling upstream.
Owning the git forks is not the same as flipping the live pull.

## Still do not fork

HA integrations, add-on stores, ESPHome, etc. Stay compatible.
