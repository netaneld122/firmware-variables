from ctypes.wintypes import DWORD
from ctypes import windll, create_string_buffer, pointer

from .bindings import get_firmware_environment_variable_ex_w


class UnsupportedFirmware(RuntimeError):
    pass


ERROR_INVALID_FUNCTION = 1


def verify_uefi_firmware():
    attributes = DWORD(0)
    buffer = create_string_buffer(0)
    stored_bytes = get_firmware_environment_variable_ex_w(
        "",
        "{00000000-0000-0000-0000-000000000000}",
        pointer(buffer),
        len(buffer),
        pointer(attributes))
    if stored_bytes == 0 and gle() == ERROR_INVALID_FUNCTION:
        raise UnsupportedFirmware()


def gle():
    return windll.kernel32.GetLastError()
