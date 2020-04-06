from ctypes import WINFUNCTYPE, windll, create_string_buffer, pointer, WinError, get_last_error
from ctypes.wintypes import LPCSTR, LPVOID, DWORD, PDWORD


def generate_stdcall_binding(lib, name, return_type, params):
    prototype = WINFUNCTYPE(return_type, *(e[0] for e in params))
    paramflags = tuple((1, e[1]) for e in params)
    return prototype((name, lib), paramflags)


def get_firmware_environment_variable_ex_a(*args, **kwargs):
    func = generate_stdcall_binding(
        lib=windll.kernel32,
        name="GetFirmwareEnvironmentVariableExA",
        return_type=DWORD,
        params=(
            (LPCSTR, "name"),
            (LPCSTR, "guid"),
            (LPVOID, "buffer"),
            (DWORD, "size"),
            (PDWORD, "attributes")
        ))
    return func(*args, **kwargs)


GLOBAL_NAMESPACE = "{8BE4DF61-93CA-11d2-AA0D-00E098032B8C}"

ERROR_BUFFER_TOO_SMALL = 122


def get(name, namespace=GLOBAL_NAMESPACE):
    allocation = 16

    while True:

        attributes = DWORD(0)
        buffer = create_string_buffer(allocation)
        stored_bytes = get_firmware_environment_variable_ex_a(
            name.encode(),
            namespace.encode(),
            pointer(buffer),
            len(buffer),
            pointer(attributes))

        if stored_bytes != 0:
            return buffer.raw[:stored_bytes]
        elif stored_bytes == 0 and get_last_error() != ERROR_BUFFER_TOO_SMALL:
            raise WinError()
        else:
            allocation *= 2
