# get it?
#
# colorguard?
#
# flags?
#
# haha. i'm so funny.

from colorguard import PaddedBits


# noinspection PyInitNewSignature
class BitFlagMeta(type):
    __fields__ = {}
    __bit_length__ = 0

    def __init__(cls, name, bases, atts):
        super(BitFlagMeta, cls).__init__(name, bases, atts)

        bit_pos = 0

        IGNORED = ["from_bits", "from_bytes"]

        for flag, bit_length in list(cls.__dict__.items()):

            # ignore builtin attributes
            if flag.startswith("__") or flag in IGNORED:
                continue

            cls.__fields__[flag] = (bit_pos, bit_length)
            cls.__bit_length__ += bit_length
            bit_pos += bit_length


class _LoadedBitFlag(object):
    def __init__(self, name, fields, bit_length, attrs_given=None):
        self._bits = PaddedBits(0, bit_length)
        self._name = name
        self._fields = fields
        self._bit_length = bit_length

        self._attrs = {}
        for field in self._fields:
            self._attrs[field] = attrs_given.get(field, 0)

        self._remake_bits()

    def __getitem__(self, item):
        if item not in self._fields:
            raise KeyError("{!r} isn't a field for {!r}".format(item, self._name))

        return self._attrs[item]

    def __setitem__(self, item, value):
        if item not in self._fields:
            raise KeyError("{!r} isn't a field for {!r}".format(item, self._name))

        field_bit_length = self._fields[item][1]
        if value.bit_length() > field_bit_length:
            raise ValueError("{!r} doesn't fit in {} bits".format(value, field_bit_length))

        self._attrs[item] = value

        self._remake_bits()

    def _remake_bits(self):
        for field, properties in self._fields.items():
            self._bits[properties[0]: properties[0] + properties[1]] = self._attrs[field]

    @property
    def bits(self):
        return self._bits
