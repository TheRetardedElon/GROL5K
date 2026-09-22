# Building GROL5K

This document starts conservative: reproduce upstream first, then introduce GROL changes.

## Baseline

Pinned initial upstream commit:

```text
3019c7fe8745900a3e9dcb3879d96bacf7958543
```

## Clone

```bash
git clone --recurse-submodules https://github.com/TheRetardedElon/GROL5K.git
cd GROL5K
git checkout dev
git submodule update --init --recursive
```

## Build strategy

The upstream Makefile discovers targets from:

```text
buildroot-external/configs/*_defconfig
```

M0 must use an existing upstream target unchanged.

Long-term, GROL-owned targets should be introduced rather than pretending every image is still a stock HAOS target. Intended naming:

```text
grol5000_ova_defconfig
grol5000_x86_64_defconfig
grol5000_rpi5_defconfig
```

## Reproducibility record

Every significant build should record:

- GROL commit SHA
- upstream baseline SHA
- Buildroot submodule SHA
- target
- build host/environment
- build start/end
- artifact hashes
- boot-test result
- update/rollback-test result where applicable

## Rule

Do not begin deep platform changes until an unmodified baseline image has been successfully built and booted in the development environment.
