# M2 grol-hostd

Implementation language: **Go**. Not CPython.

Why: HAOS already builds Go for OS Agent. The appliance rootfs should not gain a CPython runtime just to serve five read-only status methods.

Package: `buildroot-external/package/grol-hostd`
Source: `grol/services/grol-hostd`
Enable with `BR2_PACKAGE_GROL_HOSTD=y` next to `BR2_PACKAGE_OS_AGENT` on the boards we care about (OVA first).

Protocol: `grol/specs/HOST_API_V0.md`

Flip the defconfig bit when the next OVA after M1-B2 is accepted. Do not block splash validation on hostd landing in that same image.
