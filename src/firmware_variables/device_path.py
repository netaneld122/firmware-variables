import struct

from enum import Enum

from .utils import utf16_string_from_bytes, string_to_utf16_bytes

EFI_DEVICE_PATH = struct.Struct("<BBH")


class DevicePathType(Enum):
    HARDWARE_DEVICE_PATH = 0x01
    ACPI_DEVICE_PATH = 0x02
    MESSAGING_DEVICE_PATH = 0x03
    MEDIA_DEVICE_PATH = 0x04
    BIOS_BOOT_SPECIFICATION_DEVICE_PATH = 0x05
    END_OF_HARDWARE_DEVICE_PATH = 0x7F


class HardwareDevicePathSubtype(Enum):
    PCI = 0x01
    PCCARD = 0x02
    MEMORY_MAPPED = 0x03
    VENDOR = 0x04
    CONTROLLER = 0x05
    BMC = 0x06


class AcpiDevicePathSubtype(Enum):
    ACPI_DEVICE_PATH = 0x01
    EXPANDED_ACPI_DEVICE_PATH = 0x02
    ADR_DEVICE_PATH = 0x03
    NVDIMM_DEVICE = 0x04


class MessagingDevicePathSubtype(Enum):
    ATAPI = 0x01
    SCSI = 0x02
    FIBRE_CHANNEL = 0x03
    _1394 = 0x04
    USB = 0x05
    I20_RANDOM_BLOCK_STORAGE_CLASS = 0x06
    INFIBAND = 0x09
    VENDOR = 0x0A
    MAC_ADDRESS_FOR_NETWORK_INTERFACE = 0x0B
    IPV4 = 0x0C
    IPV6 = 0x0D
    UART = 0x0E
    USB_CLASS = 0x0F
    USB_WWID = 0x10
    DEVICE_LOGICAL_UNIT = 0x11
    SATA = 0x12
    ISCSI = 0x13
    VLAN = 0x14
    FIBRE_CHNNEL_EX = 0x15
    SAS_EX = 0x16
    NVM_EXPRESS_NAMESPACE = 0x17
    UNIVERSAL_RESOURCE_IDENTIFIER = 0x18
    UFS = 0x19
    SD = 0x1A
    BLUETOOTH = 0x1B
    WIFI = 0x1C
    EMMC = 0x1D
    BLUETOOTH_LE = 0x1E
    DNS = 0x1F
    NVDIMM_OR_REST_SERVICE = 0x20


class MediaDevicePathSubtype(Enum):
    HARD_DRIVE = 0x01
    CD_ROM = 0x02
    VENDOR = 0x03
    FILE_PATH = 0x04
    MEDIA_PROTOCOL = 0x05
    PIWG_FIRMWARE_FILE = 0x06
    PIWG_FIRMWARE_VOLUME = 0x07
    RELATIVE_OFFSET_RANGE = 0x08
    RAM_DISK_DEVICE_PATH = 0x09


class BiosBootSpecificationDevicePathSubtype(Enum):
    VERSION_1_01 = 0x01


class EndOfHardwareDevicePathSubtype(Enum):
    END_THIS_INSTANCE_OF_DEVICE_PATH = 0x01
    END_ENTIRE_DEVICE_PATH = 0xFF


SUBTYPES_MAPPING = {
    DevicePathType.HARDWARE_DEVICE_PATH: HardwareDevicePathSubtype,
    DevicePathType.ACPI_DEVICE_PATH: AcpiDevicePathSubtype,
    DevicePathType.MESSAGING_DEVICE_PATH: MessagingDevicePathSubtype,
    DevicePathType.MEDIA_DEVICE_PATH: MediaDevicePathSubtype,
    DevicePathType.BIOS_BOOT_SPECIFICATION_DEVICE_PATH: BiosBootSpecificationDevicePathSubtype,
    DevicePathType.END_OF_HARDWARE_DEVICE_PATH: EndOfHardwareDevicePathSubtype,
}


class DevicePath:
    """
    This class represents an EFI_DEVICE_PATH
    """

    def __init__(self, path_type, subtype, data=b''):
        self.path_type = DevicePathType(path_type)
        self.subtype = SUBTYPES_MAPPING[self.path_type](subtype)
        self.data = data

    def __repr__(self):
        return "<{}, {}>".format(self.path_type, self.subtype)


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
            raw += EFI_DEVICE_PATH.pack(
                path.path_type.value,
                path.subtype.value,
                EFI_DEVICE_PATH.size + len(path.data))
            raw += path.data

        return raw

    # Convenience methods for controlling file paths (if possible)

    def get_file_path(self):
        r"""
        Get the file path that this device path list points to.
        This will only work if there's a file device path node
        with the type=MEDIA_DEVICE_PATH and subtype=FILE_PATH.
        :return: Path of the form \EFI\... if the node exists, None otherwise
        """
        for path in self.paths:
            if path.path_type == DevicePathType.MEDIA_DEVICE_PATH and \
                    path.subtype == MediaDevicePathSubtype.FILE_PATH:
                return utf16_string_from_bytes(path.data)
        return None

    def set_file_path(self, file_path):
        r"""
        Set the file path that this device path list points to.
        This will only work if there's a file device path node
        with the type=MEDIA_DEVICE_PATH and subtype=FILE_PATH.
        :param file_path: Path of the form \EFI\...
        :return: True if the operation succeeded, False otherwise
        """
        for path in self.paths:
            if path.path_type == DevicePathType.MEDIA_DEVICE_PATH and \
                    path.subtype == MediaDevicePathSubtype.FILE_PATH:
                path.data = string_to_utf16_bytes(file_path)
                return True
        return False

    def __repr__(self):
        return self.get_file_path() or "<Custom Location>"
