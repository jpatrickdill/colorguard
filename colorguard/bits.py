class Bits(object):
    def __init__(self, value=0):
        self._value = int(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value < 0:
            raise ValueError("value must be >= 0")

        if not isinstance(value, int):
            raise TypeError("value must be int")

        self._value = value

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
        return "Bits({})".format(bin(self.value))

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

    def bit_length(self):
        return self.value.bit_length()

    def __getitem__(self, item):
        if isinstance(item, slice):
            start = 0 if item.start is None else item.start
            stop = self.value.bit_length() if item.stop is None else item.stop

            if stop < 0:
                stop = self.value.bit_length() + stop
            if start < 0:
                start = self.value.bit_length() + start

            span = stop - start
            if span <= 0:
                return Bits(0)

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

    def __setitem__(self, item, value):
        if type(value) in (list, tuple):  # list of bits given
            value_bits = "".join(map(str, value))
            value = int(value_bits, 2)

        value = int(value)

        if isinstance(item, slice):
            start = 0 if item.start is None else item.start
            stop = self.value.bit_length() if item.stop is None else item.stop

            if stop < 0:
                stop = self.value.bit_length() + stop
            if start < 0:
                start = self.value.bit_length() + start

            span = stop - start
            if value.bit_length() > span:
                raise ValueError("{!r} doesn't fit in {} bit(s)".format(value, span))

            nv = self[:start] << span
            nv |= value

            nv <<= self.bit_length() - stop
            nv |= (self[stop + 1:]).value

            self.value = nv.value

        elif isinstance(item, int):
            if item >= self.bit_length():
                raise KeyError("{!r} not in bit range for {}".format(item, self.value))

            if value not in (0, 1):
                raise ValueError("Single bit must be either 0 or 1")

            nv = self[:item] << 1
            nv |= value

            nv <<= self.bit_length() - item - 1
            nv |= (self[item + 1:]).value

            self.value = nv.value

    def __iter__(self):
        return iter(map(int, bin(self.value)[2:]))

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

    def join(self, other):
        other = int(other)

        shifted = self.value << other.bit_length()

        return Bits(shifted + other)


class PaddedBits(Bits):
    def __init__(self, value, bit_length):
        super().__init__(value=value)

        self._value = value
        self._bits = bit_length

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not isinstance(value, int):
            raise TypeError("value must be int")

        if value.bit_length() > self.bits:
            raise ValueError("{!r} doesn't fit in {} bits".format(value, self.bits))

        if value < 0:
            raise ValueError("value must be >= 0")

        self._value = value

    @property
    def bits(self):
        return self._bits

    @bits.setter
    def bits(self, value):
        if self.value.bit_length() > value:
            raise ValueError("current value {} doesn't fit in {} bits".format(self.value, value))

        self._bits = value

    @classmethod
    def from_bytes(cls, b, byteorder="big", bit_length=None):
        value = int.from_bytes(b, byteorder=byteorder)

        bit_length = bit_length or ((value.bit_length() + 7) // 8) * 8

        return PaddedBits(value, bit_length)

    def to_bytes(self, byteorder="big"):
        bl = (self.bits + 7) // 8

        return self.value.to_bytes(bl, byteorder)

    def bit_length(self):
        return self.bits

    def __repr__(self):
        return "PaddedBits({}, bit_length={})".format(str(self), self.bits)

    def __str__(self):
        return "0b"+"".join(map(str, iter(self)))

    def __iter__(self):
        bit_length = self.value.bit_length() if self.value > 0 else 1

        return iter([0] * (self.bits - bit_length) + list(map(int, list(bin(self.value)[2:]))))  # oof

    def __add__(self, other):
        nv = self.value + int(other)
        if nv.bit_length() > self.bits:
            raise ValueError("{} is more than {} bits".format(nv, self.bits))

        return PaddedBits(nv, self.bits)

    def __sub__(self, other):
        nv = self.value - int(other)
        if nv.bit_length() > self.bits:
            raise ValueError("{} is more than {} bits".format(nv, self.bits))

        return PaddedBits(nv, self.bits)

    def __mul__(self, other):
        nv = self.value * int(other)
        if nv.bit_length() > self.bits:
            raise ValueError("{} is more than {} bits".format(nv, self.bits))

        return PaddedBits(nv, self.bits)

    def __truediv__(self, other):
        nv = self.value // int(other)
        if nv.bit_length() > self.bits:
            raise ValueError("{} is more than {} bits".format(nv, self.bits))

        return PaddedBits(nv, self.bits)

    def __floordiv__(self, other):
        nv = self.value // int(other)
        if nv.bit_length() > self.bits:
            raise ValueError("{} is more than {} bits".format(nv, self.bits))

        return PaddedBits(nv, self.bits)

    def __mod__(self, other):
        nv = self.value % int(other)
        if nv.bit_length() > self.bits:
            raise ValueError("{} is more than {} bits".format(nv, self.bits))

        return PaddedBits(nv, self.bits)

    def __pow__(self, power, modulo=None):
        nv = pow(self.value, int(power), int(modulo))
        if nv.bit_length() > self.bits:
            raise ValueError("{} is more than {} bits".format(nv, self.bits))

        return PaddedBits(nv, self.bits)

    def __lshift__(self, other):
        nv = self.value << int(other)

        return PaddedBits(nv, self.bits + int(other))

    def __rshift__(self, other):
        if int(other) > self.bits:
            raise ValueError("Can't RShift {} bits".format(int(other)))

        nv = self.value >> int(other)

        return PaddedBits(nv, self.bits - int(other))

    def __and__(self, other):
        nv = self.value & int(other)
        if nv.bit_length() > self.bits:
            raise ValueError("{} is more than {} bits".format(nv, self.bits))

        return PaddedBits(nv, self.bits)

    def __xor__(self, other):
        nv = self.value ^ int(other)
        if nv.bit_length() > self.bits:
            raise ValueError("{} is more than {} bits".format(nv, self.bits))

        return PaddedBits(nv, self.bits)

    def __or__(self, other):
        nv = self.value | int(other)
        if nv.bit_length() > self.bits:
            raise ValueError("{} is more than {} bits".format(nv, self.bits))

        return PaddedBits(nv, self.bits)

    def join(self, other):
        other = int(other)

        shifted = self.value << other.bit_length()

        return PaddedBits(shifted | other, self.bits + other.bit_length())

    def __getitem__(self, item):
        if isinstance(item, list):  # list of bits given
            value_bits = "".join(map(str, item))
            item = int(value_bits, 2)

        if isinstance(item, slice):
            start = 0 if item.start is None else item.start
            stop = self.bits if item.stop is None else item.stop

            if start < 0:
                start += self.bits
            if stop < 0:
                stop += self.bits

            span = stop - start

            mask = 2 ** span - 1

            mask_shift = self.bits - stop
            mask <<= mask_shift

            return PaddedBits((self.value & mask) >> mask_shift, span)

        elif not isinstance(item, float):
            item = int(item)

            if item < 0:
                item += self.bits

            if item >= self.bits:
                raise KeyError("bit {} not in range for {!r}".format(item, self))

            return PaddedBits(list(self)[item], 1)

    def __setitem__(self, item, value):
        if type(value) in (list, tuple):  # list of bits given
            value_bits = "".join(map(str, value))
            value = int(value_bits, 2)

        value = int(value)

        if isinstance(item, slice):
            start = 0 if item.start is None else item.start
            stop = self.bits if item.stop is None else item.stop

            if start < 0:
                start += self.bits
            if stop < 0:
                stop += self.bits

            span = stop - start

            if value.bit_length() > span:
                raise ValueError("{!r} doesn't fit in {} bits".format(value, span))

            nv = self[:start]
            nv <<= span
            nv |= value
            nv <<= self.bits - stop
            nv |= self[stop:]

            self.value = nv.value

        elif isinstance(item, int):
            if item < 0:
                item += self.bits

            if item >= self.bits:
                raise KeyError("bit {} not in range for {!r}".format(item, self))

            nv = self[:item] << 1
            nv |= value
            nv <<= self.bits - item - 1
            nv |= self[item + 1:]

            self.value = nv.value
