# firmware_variables
![](https://github.com/netaneld122/firmware-variables/workflows/build/badge.svg)

Python library for controlling UEFI variables in Windows.

## Installation

```python
pip install firmware_variables
```

## Library Usage Example
```python
from firmware_variables import *

with privileges():

    # Manipulate variables
    get_variable("BootCurrent")
    set_variable("Test", b"\x0000")
    
    # Be explicit
    set_variable("Test", b"\x0000",
        namespace="{f29e2c32-8cca-44ff-93d7-87195ace38b9}", 
        attributes= Attributes.NON_VOLATILE | 
                    Attributes.BOOT_SERVICE_ACCESS |
                    Attributes.RUNTIME_ACCESS)

    # Manipulate the boot order
    order = get_boot_order()
    set_boot_order(order[1:])

    # Modify boot entries
    load_option = get_parsed_boot_entry(order[0])
    load_option.description = "Windows Groot Entry"
    load_option.file_path_list.set_file_path(r"\EFI\Boot\myfile.efi")
    set_parsed_boot_entry(order[0], load_option)
```