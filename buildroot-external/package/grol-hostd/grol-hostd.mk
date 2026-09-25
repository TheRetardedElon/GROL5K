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

define GROL_HOSTD_INSTALL_INIT_SYSTEMD
	$(INSTALL) -D -m 0644 $(@D)/systemd/grol-hostd.service \
		$(TARGET_DIR)/usr/lib/systemd/system/grol-hostd.service
	$(INSTALL) -D -m 0644 $(@D)/systemd/grol-sysusers.conf \
		$(TARGET_DIR)/usr/lib/sysusers.d/grol-hostd.conf
	$(INSTALL) -D -m 0644 $(@D)/systemd/grol.conf \
		$(TARGET_DIR)/usr/lib/tmpfiles.d/grol-hostd.conf
	$(INSTALL) -D -m 0644 $(@D)/hostapi-allowlist \
		$(TARGET_DIR)/etc/grol/hostapi-allowlist
endef

$(eval $(golang-package))
