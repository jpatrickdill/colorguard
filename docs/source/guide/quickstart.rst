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

