from .variables import get_variable, set_variable, delete_variable, Attributes
from .variables import GLOBAL_NAMESPACE, DEFAULT_ATTRIBUTES

from .privileges import adjust_privileges, patch_current_process_privileges

from .boot import get_boot_order, get_boot_entry, set_boot_entry, set_boot_order
from .boot import get_parsed_boot_entry, set_parsed_boot_entry

from .load_option import LoadOption
