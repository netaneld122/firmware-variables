import struct

EFI_DEVICE_PATH = struct.Struct("<BBH")


class DevicePath:
    """
    This class represents an EFI_DEVICE_PATH
    """

    def __init__(self, path_type, subtype, data=b''):
        self.path_type = path_type
        self.subtype = subtype
        self.data = data


class DevicePathList:
    """
    This class represents a list of EFI_DEVICE_PATH structures
    """

    def __init__(self):
        self.paths = []

    @staticmethod
    def from_bytes(raw):

        device_path_list = DevicePathList()

        offset = 0
        while offset < len(raw):
            header = EFI_DEVICE_PATH.unpack_from(raw, offset)
            path_type, subtype, length = header

            # Append the device path node
            data = raw[offset + EFI_DEVICE_PATH.size:offset + length]
            device_path_list.paths.append(DevicePath(path_type, subtype, data))

            offset += length

        return device_path_list

    def to_bytes(self):
        raw = b''
        for path in self.paths:
            raw += EFI_DEVICE_PATH.pack(path.path_type, path.subtype, EFI_DEVICE_PATH.size + len(path.data))
            raw += path.data

        return raw
