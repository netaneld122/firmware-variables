# firmware_variables

Python library for controlling UEFI variables on Windows.

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

    # Manipulate boot order
    order = get_boot_order()
    print(get_boot_entry(order[0]))
    set_boot_order(order[1:])
```