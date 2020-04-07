import struct

from enum import IntFlag

from .device_path import DevicePathList
from .utils import utf16_string_from_bytes, string_to_utf16_bytes

EFI_LOAD_OPTION = struct.Struct("<IH")


class LoadOptionAttributes(IntFlag):
    LOAD_OPTION_ACTIVE = 0x00000001
    LOAD_OPTION_FORCE_RECONNECT = 0x00000002
    LOAD_OPTION_HIDDEN = 0x00000008
    LOAD_OPTION_CATEGORY_APP = 0x00000100


class LoadOption:
    """
    This class represents the EFI_LOAD_OPTION in the UEFI spec
    """

    def __init__(self):
        self.attributes = 0
        self.description = ""
        self.file_path_list = DevicePathList()
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
        load_option.description = utf16_string_from_bytes(raw[EFI_LOAD_OPTION.size:])

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
        raw += string_to_utf16_bytes(self.description)
        raw += raw_file_path_list
        raw += self.optional_data

        return raw

    def __repr__(self):
        return f"<{self.description} {self.file_path_list} [{str(self.attributes)}]>"
