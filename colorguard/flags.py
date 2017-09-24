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

    def __init__(cls, name, bases, atts):
        super(BitFlagMeta, cls).__init__(name, bases, atts)

        bit_pos = 0
        for flag, bit_length in cls.__dict__.items():
            # ignore builtin attributes
            if flag.startswith("__"):
                continue

            cls.__flags__[flag] = (bit_pos, bit_length)


class BitFlag(object, metaclsas=BitFlagMeta):
    __flags__ = {}

    def __new__(cls, **kwargs):
        use_flags = cls.__flags__

        bits = Bits()

        for ident, value in kwargs.items():
            if ident not in cls.__flags__:
                raise KeyError("Invalid flag {!r} given".format(ident))

