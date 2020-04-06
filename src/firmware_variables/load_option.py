import struct

from enum import IntFlag


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
        load_option.description = raw[EFI_LOAD_OPTION.size:].split(b'\x00\x00')[0].decode()

        # Decode file path list
        # @TODO: Parse it too
        file_path_list_offset = EFI_LOAD_OPTION.size + len(load_option.description) + 2
        load_option.file_path_list = raw[file_path_list_offset:file_path_list_offset + file_path_list_length]

        # Decode optional data
        load_option.optional_data = raw[file_path_list_offset + file_path_list_length:]

        return load_option

    def to_bytes(self):
        """
        Encode this load option as a boot entry blob
        :return: bytes
        """
        header = EFI_LOAD_OPTION.pack(self.attributes, len(self.file_path_list))
        return header + self.description.encode() + b'\x00\x00' + self.file_path_list + self.optional_data

    def __repr__(self):
        return f"<{self.description} ({str(self.attributes)})>"
