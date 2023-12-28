import hid
import argparse

from dataclasses import dataclass
from typing import Tuple


@dataclass
class MonitorProperty:
    """
    A configurable monitor property
    """
    name: str
    value: int
    range: Tuple[int, int]
    description: str = ''


class Monitor:
    """
    This class sets configurable monitor properties
    """
    VID = 0x0bda
    PID = 0x1100

    @property
    def configurable_properties(self):
        return {
            "brightness": MonitorProperty(name="brightness", range=tuple((0, 100)), value=0x10, ),

            "contrast": MonitorProperty(name="contrast", range=tuple((0, 100)), value=0x12, ),
            "sharpness": MonitorProperty(name="sharpness", range=tuple((0, 10)), value=0x87, ),
            "low-blue-light": MonitorProperty(name="low-blue-light", range=tuple((0, 10)), value=0xe00b,
                                              description="Blue light reduction. 0 means no reduction.", ),
            "kvm-switch": MonitorProperty(name="kvm-switch", range=tuple((0, 1)), value=0xe069,
                                          description="Switch KVM to device 0 or 1", ),
            "colour-mode": MonitorProperty(name="colour-mode", range=tuple((0, 3)), value=0xe003,
                                           description="0 is cool, 1 is normal, 2 is warm, 3 is user-defined.", ),
            "rgb-red": MonitorProperty(name="rgb-red", range=tuple((0, 100)),
                                       value=0xe004, description="Red value -- only works if colour-mode is set to 3", ),
            "rgb-green": MonitorProperty(name="rgb-green", range=tuple((0, 100)), value=0xe005,
                                         description="Green value -- only works if colour-mode is set to 3", ),
            "rgb-blue": MonitorProperty(name="rgb-blue", range=tuple((0, 100)), value=0xe006,
                                        description="Blue value -- only works if colour-mode is set to 3", ),
        }

    @staticmethod
    def _build_request(monitor_property: MonitorProperty, property_value: int) -> bytes:
        """
        Builds a HID reqeust for setting the property whose name is prop_name to property_value
        :param monitor_property: The property to set
        :param property_value: The value to set the property to
        :return: A byte string representation of the request
        """
        # +1 for Null byte in the header
        request_size = 192 + 1
        header_size = 0x40 + 1
        assert property_value in monitor_property.range, \
            f'Illegal value {property_value}, legal values: {monitor_property.range}'
        # Buffer needs to start with a null byte
        buffer = [0x00]
        # Request header
        buffer += [0x40, 0xc6]
        buffer += [0x00] * 4
        buffer += [0x20, 0x00, 0x6e, 0x00, 0x80]

        # preamble needs this to be set up
        msg = [monitor_property.value >> 8, monitor_property.value & 0xff, 0x00, property_value]

        preamble = [0x51, 0x81 + len(msg), 0x03]

        # Header padding
        buffer = buffer + [0x00] * (header_size - len(buffer))

        buffer += preamble
        buffer += msg
        buffer += ([0x00] * (request_size - len(buffer)))
        return bytes(buffer)

    def set_property(self, property_name: str, property_value: int):
        """
        Sets property_name to property_value
        :param property_name: The name of the property to set
        :param property_value: The value to set the property to
        :return: Number of bytes written to the hid device
        """
        assert property_name in self.configurable_properties, \
            f"Invalid property {property_name}, " \
            f"valid options: {list(self.configurable_properties.keys())}"

        prop = self.configurable_properties[property_name]
        assert property_value in prop.range, f'{property_value} not in {prop.name}\'s legal value range.\n' \
                                             f'The legal value range is: {prop.range}'
        with hid.Device(self.VID, self.PID) as device:
            return device.write(Monitor._build_request(prop, property_value))


def main():
    monitor = Monitor()
    parser = argparse.ArgumentParser(description='Set monitor property.')
    parser.add_argument('-p', '--property',
                        required=True, help='Property to set', choices=monitor.configurable_properties.keys())
    parser.add_argument('-v', '--value',
                        required=True, help='Monitor property value', metavar="[0-255]",
                        type=int)
    args = parser.parse_args()
    monitor.set_property(args.property, args.value)


if __name__ == "__main__":
    main()
