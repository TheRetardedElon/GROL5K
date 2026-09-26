################################################################################
#
# grol-hostd
#
################################################################################

GROL_HOSTD_VERSION = 0.2.0
GROL_HOSTD_SITE = $(BR2_EXTERNAL_HAOS_PATH)/../grol/services/grol-hostd
GROL_HOSTD_SITE_METHOD = local
GROL_HOSTD_LICENSE = Apache-2.0
GROL_HOSTD_GOMOD = github.com/grol5000/grol-hostd

# Create the service identity in the target rootfs at build time. systemd must
# be able to resolve User=/Group= before it can execute grol-hostd; sysusers.d
# alone is too late/unreliable for this immutable HAOS-derived image path.
define GROL_HOSTD_USERS
	grol-hostd -1 grol-hostapi -1 * - /bin/false - GROL Host API
endef

define GROL_HOSTD_INSTALL_INIT_SYSTEMD
	$(INSTALL) -D -m 0644 $(@D)/systemd/grol-hostd.service \
		$(TARGET_DIR)/usr/lib/systemd/system/grol-hostd.service
	$(INSTALL) -D -m 0644 $(@D)/systemd/grol.conf \
		$(TARGET_DIR)/usr/lib/tmpfiles.d/grol-hostd.conf
	$(INSTALL) -D -m 0644 $(@D)/hostapi-allowlist \
		$(TARGET_DIR)/etc/grol/hostapi-allowlist
endef

$(eval $(golang-package))
