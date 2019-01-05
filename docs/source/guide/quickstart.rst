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

There are several ways to make ``Bits`` objects. The simplest is pass an integer to the ``Bits`` class.

.. code-block:: pycon

    >>> b = Bits(44)

You can also create a ``Bits`` object from a binary or hexadecimal string:

.. code-block:: pycon

    >>> b = Bits.from_binary("0b101100")
    >>> b = Bits.from_binary("101100")

    >>> b = Bits.from_hex("0x2C")
    >>> b = Bits.from_hex("2C")

Lastly, a ``Bits`` object can be created from a byte string:

.. code-block:: pycon

    >>> b = Bits.from_bytes(b',')

You can also specify the byte order if necessary:

.. code-block:: pycon

    >>> b = Bits.from_bytes(b'abc123', byteorder="little")

Math with Bits
~~~~~~~~~~~~~~

All math operations and comparisons and Python can be used on ``Bits`` objects, even with other data types.
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


Two ``Bits`` objects can also be concatenated with :meth:`Bits.join`.

.. code-block:: pycon

    >>> Bits(5).join(Bits(3))
    Bits(0b10111)

Bit Indexing
~~~~~~~~~~~~

``Bits`` objects can also be indexed like strings or lists.

.. code-block:: pycon

    >>> b = Bits(0b11110011)
    >>> b[1]
    Bits(0b1)
    >>> b[1] = 0
    >>> b
    Bits(0b10110011)

You can also slice ``Bits`` just how you would a string.

.. code-block:: pycon

    >>> b[2:6]
    Bits(0b1100)
    >>> b[-5:]
    Bits(0b10011)
    >>> b[:4] = 0b1010
    >>> b
    Bits(0b10100011)

When set a slice of bits, the length doesn't have to match.

.. code-block:: pycon

    >>> b[:4] = 0b10
    >>> b
    Bits(0b100011)
