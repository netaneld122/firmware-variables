import contextlib
import win32security
import win32process
import win32con


@contextlib.contextmanager
def privileges():
    """
    Acquire SeSystemEnvironmentPrivilege in order to access UEFI variables.

    Usage example:
    ```
    with privileges():
        get_variable("SomeVar")
    ```
    """
    process = win32process.GetCurrentProcess()
    token = win32security.OpenProcessToken(
        process,
        win32security.TOKEN_ADJUST_PRIVILEGES | win32security.TOKEN_QUERY
    )
    luid = win32security.LookupPrivilegeValue(None, win32con.SE_SYSTEM_ENVIRONMENT_NAME)
    privilege_enable = [(luid, win32security.SE_PRIVILEGE_ENABLED)]
    privilege_disable = [(luid, win32security.SE_PRIVILEGE_REMOVED)]
    win32security.AdjustTokenPrivileges(token, False, privilege_enable)

    try:
        yield
    finally:
        win32security.AdjustTokenPrivileges(token, False, privilege_disable)
