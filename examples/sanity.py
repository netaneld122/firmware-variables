from firmware_variables import *


def doit():
    with privileges():
        order = get_boot_order()
        for entry_id in order:
            raw = get_boot_entry(entry_id)
            load_option = LoadOption.from_bytes(raw)

            print("{:04X} {}".format(entry_id, load_option))

            assert load_option.to_bytes() == raw


if __name__ == "__main__":
    doit()
