import abc

# 110100101111111000101000
# VVVTTTAAAAABBBBBCCCCCZZZ
#
# V = version
# T = type
### if T = 4: literal value, else: operator
# A, B, C = numbers
### numbers = always 4 bits
# Z = right padding 0, to be ignored


PACKET_TYPES = {4: "LITERAL_VALUE"}

HEX_TO_BITS = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


class Packet(metaclass=abc.ABCMeta):
    def __init__(self, packet_version: int, packet_type: str) -> None:
        self.version: int = packet_version
        self.type: str = packet_type

    @abc.abstractmethod
    def sum_version(self):
        pass


class LiteralValuePacket(Packet):
    def __init__(self, packet_version: int, literal_value: int) -> None:
        super().__init__(packet_version, "LITERAL_VALUE")
        self.literal_value: int = literal_value

    def sum_version(self):
        return self.version


class OperatorPacket(Packet):
    def __init__(self, packet_version: int, operator_version: int) -> None:
        super().__init__(packet_version, "OPERATOR")
        self.operator_version: int = operator_version
        self.subpackets: list[Packet] = []

    def sum_version(self):
        version_sum = self.version
        for subpacket in self.subpackets:
            version_sum += subpacket.sum_version()
        return version_sum


test_input = "38006F45291200"
binary_str = "".join(map(lambda c: HEX_TO_BITS.get(c), test_input))


def parse_value(value_str):
    digits = []
    has_more_digit = True
    while has_more_digit:
        binary_digit = value_str[:5]
        if binary_digit[0] == "0":
            has_more_digit = False
        digits.append(binary_digit[1:])
        value_str = value_str[5:]
    return int("".join(digits), 2)


def parse_packet(packet_str):
    version = int(packet_str[:3], 2)
    packet_str = packet_str[3:]

    packet_type = PACKET_TYPES.get(int(packet_str[:3], 2), "OPERATOR")
    packet_str = packet_str[3:]

    if packet_type == "LITERAL_VALUE":
        value = parse_value(packet_str)
        return LiteralValuePacket(version, value)
    else:
        if packet_str[0] == "0":
            # total length
            length = int(packet_str[1:16], 2)
            print(f"L: {length}")
        else:
            # numnber of packet
            pass


parse_packet(binary_str)
