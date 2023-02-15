from ctypes import WINFUNCTYPE, windll, POINTER
from ctypes.wintypes import LPCWSTR, LPVOID, DWORD

# Note: `PDWORD` is not defined in Python 2.7
PDWORD = POINTER(DWORD)


def generate_stdcall_binding(lib, name, return_type, params):
    prototype = WINFUNCTYPE(return_type, *(e[0] for e in params))
    paramflags = tuple((1, e[1]) for e in params)
    return prototype((name, lib), paramflags)


def get_firmware_environment_variable_ex_w(*args):
    func = generate_stdcall_binding(
        lib=windll.kernel32,
        name="GetFirmwareEnvironmentVariableExW",
        return_type=DWORD,
        params=(
            (LPCWSTR, "name"),
            (LPCWSTR, "guid"),
            (LPVOID, "buffer"),
            (DWORD, "size"),
            (PDWORD, "attributes")
        ))
    return func(*args)


def set_firmware_environment_variable_ex_w(*args):
    func = generate_stdcall_binding(
        lib=windll.kernel32,
        name="SetFirmwareEnvironmentVariableExW",
        return_type=DWORD,
        params=(
            (LPCWSTR, "name"),
            (LPCWSTR, "guid"),
            (LPVOID, "value"),
            (DWORD, "size"),
            (DWORD, "attributes")
        ))
    return func(*args)


def nt_enumerate_system_firmware_values_ex(*args):
    func = generate_stdcall_binding(
    lib=windll.ntdll,
    name="NtEnumerateSystemEnvironmentValuesEx",
    return_type=DWORD,
    params=(
        (DWORD, "info_class"),
        (LPVOID, "buffer"),
        (PDWORD, "buffer_length")
    ))
    return func(*args) & 0xFFFFFFFF
