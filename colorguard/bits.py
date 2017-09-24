class Bits(object):
    def __init__(self, value=0):
        self.value = int(value)

    @classmethod
    def from_binary(cls, binary):
        if isinstance(binary, int):
            return Bits(binary)

        if not binary.startswith("0b"):
            binary = "0b" + binary

        return Bits(int(binary, 2))

    @classmethod
    def from_hex(cls, hex_):
        if isinstance(hex_, int):
            return Bits(hex_)

        if not hex_.startswith("0x"):
            hex_ = "0x" + hex_

        return Bits(int(hex_, 16))

    @classmethod
    def from_bytes(cls, b, byteorder="big"):
        value = int.from_bytes(b, byteorder=byteorder)

        return Bits(value)

    def to_bytes(self, byteorder="big"):
        bl = (self.value.bit_length() + 7) // 8

        return self.value.to_bytes(bl, byteorder)

    def __bytes__(self):
        return self.to_bytes()

    def __hash__(self):
        return self.value

    def __repr__(self):
        return "Bits({})".format(bin(self.value)[2:])

    def __str__(self):
        return bin(self.value)

    def __int__(self):
        return self.value

    def __float__(self):
        return float(self.value)

    def __index__(self):
        return self.value

    def __bool__(self):
        return True if self.value else False

    def __len__(self):
        return self.value.bit_length()

    def __getitem__(self, item):
        if isinstance(item, slice):
            start = item.start or 0
            stop = item.stop or self.value.bit_length()

            if stop < 0:
                stop = self.value.bit_length() + stop

            span = stop - start
            mask = 2 ** span - 1

            offset = self.value.bit_length() - stop

            if offset < 0:
                raise ValueError("Bit range {}:{} to large for {!r}".format(start, stop, self))

            return Bits((self.value & (mask << offset)) >> offset)

        elif isinstance(item, int):
            shift = (self.value.bit_length() - item - 1)

            if shift < 0:
                raise IndexError("{!r} is out of bit range for {}".format(item, bin(self.value)))
            pos = 1 << shift

            return Bits(1 if (self.value & pos) else 0)

    def __eq__(self, other):
        return self.value == float(other)

    def __gt__(self, other):
        return float(other) < self.value

    def __ge__(self, other):
        return float(other) <= self.value

    def __lt__(self, other):
        return float(other) > self.value

    def __le__(self, other):
        return float(other) >= self.value

    def __ne__(self, other):
        return float(other) == self.value

    def __add__(self, other):
        return Bits(self.value + other)

    def __sub__(self, other):
        return Bits(self.value - other)

    def __mul__(self, other):
        return Bits(self.value * other)

    def __truediv__(self, other):
        return Bits(self.value // other)

    def __floordiv__(self, other):
        return Bits(self.value // other)

    def __mod__(self, other):
        return Bits(self.value % other)

    def __pow__(self, power, modulo=None):
        return Bits(pow(self.value, power, modulo))

    def __lshift__(self, other):
        return Bits(self.value << other)

    def __rshift__(self, other):
        return Bits(self.value >> other)

    def __and__(self, other):
        return Bits(self.value & other)

    def __xor__(self, other):
        return Bits(self.value ^ other)

    def __or__(self, other):
        return Bits(self.value | other)

