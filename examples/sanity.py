from firmware_variables import get, privileges


def doit():
    with privileges():
        print(get("BootOrder"))


if __name__ == "__main__":
    doit()
