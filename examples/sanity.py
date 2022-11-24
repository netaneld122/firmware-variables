from firmware_variables import adjust_privileges, get_boot_order, get_boot_entry, LoadOption


def doit():
    with adjust_privileges():
        order = get_boot_order()
        for entry_id in order:
            raw = get_boot_entry(entry_id)
            load_option = LoadOption.from_bytes(raw)

            print("0x{:04X} {}".format(entry_id, load_option))

            assert load_option.to_bytes() == raw


if __name__ == "__main__":
    doit()
