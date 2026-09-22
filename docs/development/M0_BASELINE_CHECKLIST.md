# M0 Baseline Checklist

M0 proves that the fork can reproduce and boot its inherited operating system before GROL-specific runtime changes begin.

## Gate

**M0 passes only when an untouched HAOS-compatible target builds and boots from the GROL5K repository.**

## Recommended first target

`ova`

Why:
- isolated from physical hardware variables
- supported by the inherited build matrix
- produces QEMU/OVA-related artifacts
- ideal for repeatable boot testing

## Build record

For every baseline attempt, record:

- [ ] GROL5K commit SHA
- [ ] Buildroot submodule SHA
- [ ] host OS
- [ ] CPU architecture
- [ ] Docker version
- [ ] available RAM
- [ ] available disk
- [ ] target
- [ ] exact build command
- [ ] start/end timestamps
- [ ] result
- [ ] artifact filenames
- [ ] SHA-256 hashes
- [ ] build log location

## Boot validation

- [ ] firmware reaches GRUB
- [ ] valid slot selected
- [ ] kernel loads
- [ ] root filesystem mounts
- [ ] systemd reaches normal target
- [ ] NetworkManager starts
- [ ] Docker starts
- [ ] OS Agent starts
- [ ] Supervisor bootstrap starts
- [ ] no unexpected emergency shell
- [ ] no repeated boot loop
- [ ] journal captured
- [ ] clean shutdown/reboot works

## Compatibility validation

- [ ] `/usr/lib/os-release` matches expected upstream baseline
- [ ] board ID matches target
- [ ] Supervisor machine ID matches target
- [ ] RAUC status can be read
- [ ] active slot is identifiable
- [ ] data partition mounts
- [ ] overlay/persist mounts succeed

## Exit artifact

Create a record under `docs/build-records/M0-<date>-<target>.md`.

Do not begin compatibility-sensitive M1 changes until this checklist is complete.
