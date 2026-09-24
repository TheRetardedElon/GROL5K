#!/bin/bash
# shellcheck disable=SC2155

function haos_pre_image() {
    local BOOT_DATA="$(path_boot_dir)"
    local EFIPART_DATA="${BINARIES_DIR}/efi-part"

    mkdir -p "${BOOT_DATA}/EFI/BOOT"

    cp "${BOARD_DIR}/../grub.cfg" "${EFIPART_DATA}/EFI/BOOT/grub.cfg"
    cp "${BOARD_DIR}/cmdline.txt" "${EFIPART_DATA}/cmdline.txt"
    cp "${BR2_EXTERNAL_HAOS_PATH}/../GrolGFX/Grol5k.png" "${EFIPART_DATA}/EFI/BOOT/grol5k.png"
    if [ -f "${HOST_DIR}/share/grub/unicode.pf2" ]; then
        cp "${HOST_DIR}/share/grub/unicode.pf2" "${EFIPART_DATA}/EFI/BOOT/unicode.pf2"
    fi
    grub-editenv "${EFIPART_DATA}/EFI/BOOT/grubenv" create
    grub-editenv "${EFIPART_DATA}/EFI/BOOT/grubenv" set ORDER="A B"
    grub-editenv "${EFIPART_DATA}/EFI/BOOT/grubenv" set A_OK=1
    grub-editenv "${EFIPART_DATA}/EFI/BOOT/grubenv" set A_TRY=0

    cp -r "${EFIPART_DATA}/"* "${BOOT_DATA}/"
}


function haos_post_image() {
    convert_disk_image_xz
}

