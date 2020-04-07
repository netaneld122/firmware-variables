import contextlib
import win32security
import win32process
import win32con


class Patch:

    def __init__(self, token, privilege_disable):
        self.token = token
        self.privilege_disable = privilege_disable

    def revert(self):
        win32security.AdjustTokenPrivileges(self.token, False, self.privilege_disable)


def patch_current_process_privileges():
    """
    Patch the current process to acquire the SeSystemEnvironmentPrivilege privileges,
    it is discouraged to use it in production, this function exists only for use from ipython.
    Use the privileges() function instead when possible.
    :return: Patch object that can be reverted.
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

    return Patch(token, privilege_disable)


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
    patch = patch_current_process_privileges()
    try:
        yield
    finally:
        patch.revert()
