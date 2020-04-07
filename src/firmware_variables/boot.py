import struct

from .variables import get_variable, set_variable
from .utils import verify_uefi_firmware


def get_boot_order():
    """
    Get the UEFI boot order
    :return: list of entry ids
    """
    verify_uefi_firmware()
    raw, _ = get_variable("BootOrder")
    return [e[0] for e in struct.iter_unpack("<h", raw)]


def set_boot_order(entry_ids):
    """
    Set the UEFI boot order
    :param entry_ids: list of entry ids
    """
    verify_uefi_firmware()
    raw = b''.join(struct.pack("<h", entry_id) for entry_id in entry_ids)
    set_variable("BootOrder", raw)


def get_boot_entry(entry_id):
    """
    Get the boot entry content
    :param entry_id
    :return: entry content bytes
    """
    verify_uefi_firmware()
    return get_variable("Boot{:04X}".format(entry_id))[0]


def set_boot_entry(entry_id, raw):
    """
    Set the boot entry content
    :param entry_id
    :param raw: bytes of boot entry content
    """
    verify_uefi_firmware()
    return set_variable("Boot{:04X}".format(entry_id), raw)[0]
