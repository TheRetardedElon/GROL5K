# Substrate vs runtime stack

There is no KDE. There is no graphical desktop in the base image.
GRUB splash / `grol >` is **appliance substrate branding**, not the
GROL5000 product experience.

## What this repo builds today

```text
UEFI / GRUB
    → Linux / systemd / Buildroot / EROFS
    → Docker + RAUC + NetworkManager + OS Agent
    → Supervisor container
         → pulls ghcr.io/home-assistant/qemux86-64-homeassistant
         → Core serves :8123
         → upstream frontend ("Create user" / "Preparing Home Assistant")
```

`grol5k` is the bottom box. Hostname `grol5000` and later `grol >` live
here. The page at `grol5000.local` is still upstream Core + frontend
because Supervisor still downloads those images.

Home Assistant Core is not a second kernel. It is a userspace container.
From the product side it is still the other half of the system.

## What GROL5000 has to own

```text
GROL OS                 this repo
GROL Supervisor         descendant of home-assistant/supervisor
GROL Core               descendant of home-assistant/core
GROL Frontend           descendant of home-assistant/frontend
GROL CLI                descendant of plugin-cli
grol-bot / gateway / buildd / broker
```

Supervisor must eventually pull:

```text
ghcr.io/<grol-org>/grol-core:<version>
```

not only:

```text
ghcr.io/home-assistant/qemux86-64-homeassistant:<version>
```

That is M5+ (ADR-0005). Until those images exist, :8123 will keep saying
Home Assistant no matter how pretty GRUB is.

## What M1-B2 is

Console/boot less embarrassing on the substrate. Validation after the
next OVA:

- GRUB visible ~3s, titles say GROL5000
- less `[ OK ]` spam
- tty1 is `grol >`
- `ha` still opens inherited CLI
- `grol5000.local:8123` still works (still upstream Core)
