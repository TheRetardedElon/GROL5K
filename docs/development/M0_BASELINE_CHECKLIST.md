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


## GitHub Actions baseline path

The inherited `.github/workflows/build.yaml` is usable from this fork for M0.

For a focused first run in GitHub:

1. Open **Actions → OS build → Run workflow**.
2. Select branch `dev`.
3. Set **boards** to `ova`.
4. Set **publish** to `false`.
5. Set **run_tests** to `true`.
6. Set **hassio_channel** to `dev`.
7. Run the workflow.

Fork safety observed in the workflow:

- forks force `publish_build=false`, so the build does not publish to Home Assistant's artifact infrastructure
- if RAUC release secrets are absent, the workflow generates a temporary self-signed certificate for development
- the builder image is created under the fork owner's GHCR namespace
- OVA builds upload local GitHub Actions artifacts rather than upstream release assets

With tests enabled, the inherited test workflow downloads the generated OVA QCOW2 artifact, boots it under QEMU/KVM, runs the existing integration test suite, and archives logs/JUnit reports.

### Expected development artifacts for OVA

Depending on the inherited workflow path, the run may expose:

- `haos_ova-<version>.ova`
- `haos_ova-<version>.qcow2.xz`
- `haos_ova-<version>.raucb`
- `haos_ova-<version>.vmdk.zip`
- `haos_ova-<version>.vdi.zip`
- `haos_ova-<version>.vhdx.zip`

The `haos_` prefix is intentionally retained during M0 per ADR-0002.

A successful GitHub workflow is strong M0 evidence, but the final build record should still capture the run, artifact hashes, and test conclusions.
