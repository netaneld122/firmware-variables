from firmware_variables import *


def doit():
    with privileges():
        print(get_boot_order())


if __name__ == "__main__":
    doit()
