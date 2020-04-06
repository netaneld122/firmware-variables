import struct

from enum import IntFlag

from .device_path import DevicePathList

EFI_LOAD_OPTION = struct.Struct("<IH")


class LoadOptionAttributes(IntFlag):
    LOAD_OPTION_ACTIVE = 0x00000001
    LOAD_OPTION_FORCE_RECONNECT = 0x00000002
    LOAD_OPTION_HIDDEN = 0x00000008
    LOAD_OPTION_CATEGORY_APP = 0x00000100


# @TODO: Refactor this
def extract_utf16_string(raw):
    for i in range(0, len(raw), 2):
        if raw[i:i + 2] == b'\x00\x00':
            return raw[:i].decode('utf-16le')
    raise RuntimeError("Invalid input")


class LoadOption:
    """
    This class represents the EFI_LOAD_OPTION in the UEFI spec
    """

    def __init__(self):
        self.attributes = 0
        self.description = ""
        self.file_path_list = b''
        self.optional_data = b''

    @staticmethod
    def from_bytes(raw):
        """
        Decode a load option from a boot entry blob
        :param raw: boot entry data
        :return: LoadOption
        """
        # Decode load option header
        header = EFI_LOAD_OPTION.unpack(raw[:EFI_LOAD_OPTION.size])
        attributes, file_path_list_length = header

        load_option = LoadOption()

        # Decode attributes
        load_option.attributes = LoadOptionAttributes(attributes)

        # Decode description
        load_option.description = extract_utf16_string(raw[EFI_LOAD_OPTION.size:])

        # Decode file path list
        str_size = (len(load_option.description) + 1) * 2
        file_path_list_offset = EFI_LOAD_OPTION.size + str_size
        file_path_list = raw[file_path_list_offset:file_path_list_offset + file_path_list_length]
        load_option.file_path_list = DevicePathList.from_bytes(file_path_list)

        # Decode optional data
        load_option.optional_data = raw[file_path_list_offset + file_path_list_length:]

        return load_option

    def to_bytes(self):
        """
        Encode this load option as a boot entry blob
        :return: bytes
        """

        raw_file_path_list = self.file_path_list.to_bytes()
        header = EFI_LOAD_OPTION.pack(self.attributes, len(raw_file_path_list))

        # Concatenate all the parts
        raw = header
        raw += self.description.encode('utf-16le') + b'\x00\x00'
        raw += raw_file_path_list
        raw += self.optional_data

        return raw

    def __repr__(self):
        # @TODO: Refactor this
        p = ''
        for path in self.file_path_list.paths:
            if path.path_type == 4 and path.subtype == 4:
                p = extract_utf16_string(path.data)
        return f"<{self.description} {p} [{str(self.attributes)}]>"
