# get it?
#
# colorguard?
#
# flags?
#
# haha. i'm so funny.

from colorguard import Bits


# noinspection PyInitNewSignature
class BitFlagMeta(type):
    __flags__ = {}
    __bit_length__ = 0

    def __init__(cls, name, bases, atts):
        super(BitFlagMeta, cls).__init__(name, bases, atts)

        bit_pos = 0

        IGNORED = ["from_bits", "from_bytes"]

        for flag, bit_length in list(cls.__dict__.items()):

            # ignore builtin attributes
            if flag.startswith("__") or flag in IGNORED:
                continue

            cls.__flags__[flag] = (bit_pos, bit_length)
            cls.__bit_length__ += bit_length
            bit_pos += bit_length


class Flags(object):
    def __init__(self, name, attrs):
        self._name = name
        self._attrs = attrs.keys()
        for name, value in attrs.items():
            setattr(self, name, value)

    def __repr__(self):
        ret = self._name + "("

        fields = []
        for attr in self._attrs:
            fields.append("{}={}".format(attr, getattr(self, attr)))

        return ret + ", ".join(fields) + ")"


class BitFlag(object, metaclass=BitFlagMeta):
    __flags__ = {}
    __bit_length__ = 0

    def __new__(cls, **kwargs):
        use_flags = {}

        bits = Bits(2 ** cls.__bit_length__ - 1)

        for ident, value in kwargs.items():
            if ident not in cls.__flags__:
                raise KeyError("Invalid flag {!r} given".format(ident))

            # make sure valye fits
            if value.bit_length() > cls.__flags__[ident][1]:
                raise ValueError("{!r} to big for {!r} field".format(value, ident))

            use_flags[ident] = value

        if len(use_flags) != len(cls.__flags__):
            raise KeyError("Missing fields in {}".format(cls.__name__))

        for flag, val in use_flags.items():
            start = cls.__flags__[flag][0]
            stop = cls.__flags__[flag][0] + cls.__flags__[flag][1]

            bits[start:stop] = val

        return bits

    @classmethod
    def from_bits(cls, bits):
        if not isinstance(bits, Bits):
            bits = Bits(bits)

        fields = {}
        for flag, span in cls.__flags__.items():
            start = cls.__flags__[flag][0]
            stop = cls.__flags__[flag][0] + cls.__flags__[flag][1]

            fields[flag] = int(bits[start:stop])

        return Flags(cls.__name__, fields)

    @classmethod
    def from_bytes(cls, b, byteorder="big"):
        bits = Bits.from_bytes(b, byteorder=byteorder)

        return cls.from_bits(bits)
