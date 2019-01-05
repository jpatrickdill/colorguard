from colorguard import PaddedBits


# noinspection PyInitNewSignature
class BitFieldMeta(type):
    __fields__ = {}
    __bit_length__ = 0

    def __init__(cls, name, bases, atts):
        super(BitFieldMeta, cls).__init__(name, bases, atts)

        bit_pos = 0

        IGNORED = ("from_bits", "from_bytes")

        for flag, bit_length in list(cls.__dict__.items()):

            # ignore builtin attributes
            if flag.startswith("__") or flag in IGNORED:
                continue

            cls.__fields__[flag] = (bit_pos, bit_length)
            cls.__bit_length__ += bit_length
            bit_pos += bit_length


class BitField(object, metaclass=BitFieldMeta):
    __fields__ = {}
    __bit_length__ = 0

    def __new__(cls, **kwargs):
        for key in kwargs:
            if key not in cls.__fields__:
                raise KeyError("{!r} isn't a field for {!r}".format(key, cls.__name__))

        for key in cls.__fields__:
            if key not in kwargs:
                raise KeyError("Missing field {!r}".format(key))

        return _LoadedBitField(cls.__name__, cls.__fields__, cls.__bit_length__, attrs_given=kwargs)

    @classmethod
    def from_bits(cls, bits):
        if not isinstance(bits, PaddedBits):
            bits = PaddedBits(int(bits), cls.__bit_length__)

        fields_given = {}

        for field, props in cls.__fields__.items():
            fields_given[field] = int(bits[props[0]: props[0] + props[1]])

        return _LoadedBitField(cls.__name__, cls.__fields__, cls.__bit_length__, attrs_given=fields_given)

    @classmethod
    def from_bytes(cls, b, byteorder="big"):
        bits = PaddedBits.from_bytes(b, byteorder=byteorder)

        return cls.from_bits(bits)


class _LoadedBitField(object):
    def __init__(self, name, fields, bit_length, attrs_given=None):
        self._bits = PaddedBits(0, bit_length)
        self._name = name
        self._fields = fields
        self._bit_length = bit_length

        self._attrs = {}
        for field in self._fields:
            self._attrs[field] = attrs_given.get(field, 0)

        self._remake_bits()

    def __repr__(self):
        values = ["{}={}".format(key, self._attrs[key]) for key in self._fields]

        return self._name + "(" + ", ".join(values) + ")"

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
