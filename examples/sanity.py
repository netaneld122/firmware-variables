from firmware_variables import get_variable, set_variable, privileges


def doit():
    with privileges():
        set_variable("test", b"test")
        print(get_variable("test"))
        print(get_variable("BootOrder"))


if __name__ == "__main__":
    doit()
