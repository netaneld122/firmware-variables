from ctypes import create_string_buffer, pointer, WinError
from ctypes.wintypes import DWORD
from enum import IntFlag

from .utils import gle, verify_uefi_firmware
from .bindings import get_firmware_environment_variable_ex_w, set_firmware_environment_variable_ex_w

GLOBAL_NAMESPACE = "{8BE4DF61-93CA-11d2-AA0D-00E098032B8C}"

ERROR_BUFFER_TOO_SMALL = 122


class Attributes(IntFlag):
    NON_VOLATILE = 0x00000001
    BOOT_SERVICE_ACCESS = 0x00000002
    RUNTIME_ACCESS = 0x00000004
    HARDWARE_ERROR_RECORD = 0x00000008
    AUTHENTICATED_WRITE_ACCESS = 0x00000010
    TIME_BASED_AUTHENTICATED_WRITE_ACCESS = 0x00000020
    APPEND_WRITE = 0x00000040


DEFAULT_ATTRIBUTES = Attributes.NON_VOLATILE | \
                     Attributes.BOOT_SERVICE_ACCESS | \
                     Attributes.RUNTIME_ACCESS


def get_variable(name, namespace=GLOBAL_NAMESPACE):
    """
    Get the UEFI variable
    :param name: Variable name
    :param namespace: Guid of the form {XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}
    :param attributes: @see Attributes
    :return: tuple of bytes and attributes
    """

    verify_uefi_firmware()

    allocation = 16

    while True:
        attributes = DWORD(0)
        buffer = create_string_buffer(allocation)
        stored_bytes = get_firmware_environment_variable_ex_w(
            name,
            namespace,
            pointer(buffer),
            len(buffer),
            pointer(attributes))

        if stored_bytes != 0:
            return buffer.raw[:stored_bytes], Attributes(attributes.value)
        elif stored_bytes == 0 and gle() == ERROR_BUFFER_TOO_SMALL:
            allocation *= 2
        else:
            raise WinError()


def set_variable(name, value, namespace=GLOBAL_NAMESPACE, attributes=DEFAULT_ATTRIBUTES):
    """
    Set the UEFI variable
    :param name: Variable name
    :param value: Data to put in the variable
    :param namespace: Guid of the form {XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}
    :param attributes: @see Attributes
    """

    verify_uefi_firmware()

    attributes = DWORD(attributes)
    res = set_firmware_environment_variable_ex_w(
        name,
        namespace,
        value,
        len(value),
        attributes)
    if res == 0:
        raise WinError()


def delete_variable(name, *args):
    """
    Delete the UEFI variable
    :param name: Variable name
    :param namespace: Guid of the form {XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}
    :param attributes: @see Attributes
    """
    set_variable(name, value=b"", *args)
