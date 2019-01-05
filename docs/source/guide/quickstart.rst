.. _quickstart:

Quickstart
==========

.. module:: colorguard

Color Guard only has three classes, so we can import those directly.

.. code-block:: pycon

    >>> from colorguard import Bits, PaddedBits, BitFlag

Bits
----

Making Bits objects
~~~~~~~~~~~~~~~~~~~

There are several ways to make :class:`Bits` objects. The simplest is pass an integer to the :class:`Bits` class.

.. code-block:: pycon

    >>> b = Bits(44)

You can also create a :class:`Bits` object from a binary or hexadecimal string:

.. code-block:: pycon

    >>> b = Bits.from_binary("0b101100")
    >>> b = Bits.from_binary("101100")

    >>> b = Bits.from_hex("0x2C")
    >>> b = Bits.from_hex("2C")

Lastly, a :class:`Bits` object can be created from a byte string:

.. code-block:: pycon

    >>> b = Bits.from_bytes(b',')

You can also specify the byte order if necessary:

.. code-block:: pycon

    >>> b = Bits.from_bytes(b'abc123', byteorder="little")

Math with Bits
~~~~~~~~~~~~~~

All math operations and comparisons and Python can be used on :class:`Bits` objects, even with other data types.
For example:

.. code-block:: pycon

    >>> Bits(5) + Bits(3)
    Bits(0b1000)
    >>> Bits(5) + 3
    Bits(0b1000)
    >>> 3 + Bits(5)
    Bits(0b1000)

    >>> Bits(5) < Bits(8)
    True
    >>> Bits(8) == 8
    True


Two :class:`Bits` objects can also be concatenated with :meth:`Bits.join`.

.. code-block:: pycon

    >>> Bits(5).join(Bits(3))
    Bits(0b10111)

Bitwise operations also work with :class:`Bits` objects.

.. code-block:: pycon

    >>> Bits(5) << 2
    Bits(0b10100)
    >>> Bits(15) >> 3
    Bits(0b1)

    >>> Bits(5) & Bits(3)
    Bits(0b1)
    >>> Bits(5) | Bits(3)
    Bits(0b111)
    >>> Bits(5) ^ Bits(3)
    Bits(0b110)

Bit Indexing
~~~~~~~~~~~~

:class:`Bits` objects can also be indexed like strings or lists.

.. code-block:: pycon

    >>> b = Bits(0b11110011)
    >>> b[1]
    Bits(0b1)
    >>> b[1] = 0
    >>> b
    Bits(0b10110011)

You can also slice :class:`Bits` just how you would a string.

.. code-block:: pycon

    >>> b[2:6]
    Bits(0b1100)
    >>> b[-5:]
    Bits(0b10011)
    >>> b[:4] = 0b1010
    >>> b
    Bits(0b10100011)

When setting a slice of bits, the length doesn't have to match.

.. code-block:: pycon

    >>> b[:4] = 0b10
    >>> b
    Bits(0b100011)

Type Conversion
~~~~~~~~~~~~~~~

:class:`Bits` objects can be converted to masny other data types.

.. code-block:: pycon

    >>> int(Bits(0b111))
    7
    >>> str(Bits(7))
    '0b111'
    >>> list(Bits(7))
    [1, 1, 1]
    >>> bytes(Bits(7))
    b'\x07'

If you want to specify the byte order, use :meth:`Bits.to_bytes` instead of the ``bytes`` function.

.. code-block:: pycon

    >>> Bits(123456).to_bytes(byteorder="little")
    b'@\xe2\x01'

PaddedBits
----------

Sometimes, it's useful to limit the number of bits in a number. The :class:`PaddedBits` class has
the same functionality as the :class:`Bits` class, but if any operations result in a number greater
than the set bit length, an error is raised.

The string and list representation of the number is also padded to match the set bit length.

Creating a :class:`PaddedBits` object is the same as for Bits, except that you can set a bit length.
If you don't specify one, it will be chosen automatically.

.. code-block:: pycon

    >>> b = PaddedBits(5, bit_length=8)
    >>> b
    PaddedBits(0b00000101, bit_length=8)

The bit length can be changed via :attr:`PaddedBits.bits`. If the value doesn't fit in the new
bit length, an error will be raised.

    >>> b.bits = 4
    >>> b
    PaddedBits(0b0101, bit_length=4)
    >>> b.bits = 2
    Traceback (most recent call last):
      File "<input>", line 1, in <module>
      File "~/PycharmProjects/colorguard/colorguard/bits.py", line 291, in bits
        raise ValueError("current value {} doesn't fit in {} bits".format(self.value, value))
    ValueError: current value 5 doesn't fit in 2 bits

BitFlags
--------

Bit flags allow you to squeeze multiple fields into one, longer number. The fields don't even
have to be numbers, they also represent booleans or enums.

Bit flags are created in colorguard by inheriting from the :class:`BitFlag` class.

.. code-block:: python

    class Pizza(BitFlag):
        size = 3  # "size" is a 3 bit field

        pepperoni = 1  # 1 bit boolean
        meat = 1  # 1 bit boolean
        mushrooms = 1  # 1 bit boolean

        crust = 2  # 2 bit field

This bit flag could be used to describe a pizza. When using the bit flag directly, you just
pass some values.

.. code-block:: pycon

    >>> pizza = Pizza(size=4, pepperoni=1, meat=1, mushrooms=0, crust=0)

Accessing and changing fields is simple. Just index the bit flag like a dictionary:

.. code-block:: pycon

    >>> pizza["size"] = 3
    >>> pizza["crust"] = 1
    >>> pizza
    Pizza(size=3, pepperoni=1, meat=1, mushrooms=0, crust=1)

From there, we can convert our pizza to a single 8-bit value. :attr:`BitFlag.bits` will return
a :class:`PaddedBits` object with our fields packed in.

.. code-block:: pycon

    >>> pizza.bits
    PaddedBits(0b01111001, bit_length=8)

You can also populate a bit flag with a bits object like this one. In fact, we should see the same
fields if we use this value.

.. code-block:: pycon

    >>> pizza = Pizza.from_bits(0b01111001)
    >>> pizza
    Pizza(size=3, pepperoni=1, meat=1, mushrooms=0, crust=1)

If we want to make further use of bit flags, we can add custom ``@property`` functions to describe
properties.

.. code-block:: python

    class Pizza(BitFlag):
        _size = 3  # "size" is a 3 bit field

        pepperoni = 1  # 1 bit boolean
        meat = 1  # 1 bit boolean
        mushrooms = 1  # 1 bit boolean

        _crust = 2  # 2 bit field

        @property
        def size():
            return (
                "Small",
                "Medium",
                "Large",
                "X-Large",
                "Jumbo",
                "Colossal"
            )[self["_size"]]

        @property
        def crust():
            return (
                "Thin",
                "Stuffed",
                "Cheesy"
            )[self["_crust"]]

Now, the size and crust are treated like Enum values.

.. code-block:: pycon

    >>> pizza = Pizza(size=4, pepperoni=1, meat=1, mushrooms=0, crust=0)
    >>> pizza.size
    Jumbo
    >>> pizza.crust
    Thin

