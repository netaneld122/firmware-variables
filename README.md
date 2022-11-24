# firmware_variables
![](https://github.com/netaneld122/firmware-variables/workflows/Build/badge.svg)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/netaneld122/firmware-variables.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/netaneld122/firmware-variables/context:python)

Python library for controlling UEFI variables in Windows.

## Requirements
* Windows ≥ 8
* Python ≥ 3.7 (might work on Python >= 2.7 but not formally supported)
* UEFI Firmware (required for most APIs)
* Administrative privileges (required for most APIs)

## Installation

```python
pip install firmware_variables
```

## Usage

Run as Administrator

#### Read variables

```python
from firmware_variables import *

# Acquire privileges to read the firmware state in your process
with privileges():
    # Read the current boot id 
    data, attr = get_variable("BootCurrent")
    print(data)
    print(attr)
```
Output:
```
b'\x00\x00'
Attributes.RUNTIME_ACCESS|BOOT_SERVICE_ACCESS
```

#### Display the boot order
```python
from firmware_variables import *

with privileges():
    for entry_id in get_boot_order():
        load_option = get_parsed_boot_entry(entry_id)
        print(f"{entry_id} {load_option}")
```

Output:

```
0 <Windows Boot Manager \EFI\MICROSOFT\BOOT\BOOTMGFW.EFI [LoadOptionAttributes.LOAD_OPTION_ACTIVE]>
2 <Hard Drive <Custom Location> [LoadOptionAttributes.LOAD_OPTION_ACTIVE]>
```

#### Manipulate system state
**Caution:** The following commands will modify your system state.  
**Do not run it on your host machine unless you know what you're doing**.

```python
from firmware_variables import *

with privileges():

    # Create a new variable
    set_variable("Test", b"\x00",
    namespace="{f29e2c32-8cca-44ff-93d7-87195ace38b9}", 
    attributes= Attributes.NON_VOLATILE | 
                Attributes.BOOT_SERVICE_ACCESS |
                Attributes.RUNTIME_ACCESS)
    
    # Delete it
    delete_variable("Test", namespace="{f29e2c32-8cca-44ff-93d7-87195ace38b9}")
    
    # Add a new entry id to your boot order
    order = get_boot_order()
    new_id = max(order) + 1
    set_boot_order(order + [new_id])
    
    # Read the first boot entry
    load_option = get_parsed_boot_entry(order[0])
    load_option.description = "My Boot Entry"
    load_option.file_path_list.set_file_path(r"\EFI\Boot\myfile.efi")
    
    # Create our new boot entry based on the first entry
    set_parsed_boot_entry(new_id, load_option)
```
