Color Guard
===========

.. image:: https://img.shields.io/pypi/v/colorguard.svg
    :target: https://pypi.org/project/colorguard/

**Color Guard** provides simple bit manipulation and bit flags in Python. Everything is built on
the ``int`` type so no number functionality is lost, while making it possible to index and slice binary numbers
like strings.

.. image:: https://i.imgur.com/nety2Ty.jpg
   :width: 100%

---------------------

Basic usage:

.. code-block:: pycon

   >>> num = Bits(20)
   >>> num
   Bits(0b10100)
   >>> num * 3
   Bits(0b111100)
   >>> num[:4]
   Bits(0b1010)
   >>> num.bit_length()
   5
   >>> num.join(0b101)
   Bits(0b10100101)

Color Guard also supports conversion to and from other Python data types.

.. code-block:: pycon

   >>> Bits.from_binary("111101001101")
   Bits(0b111101001101)
   >>> Bits.from_hex("abc123")
   Bits(0b101010111100000100100011)
   >>> Bits.from_bytes(b"abc")
   Bits(0b11000010110001001100011)

   >>> bytes(Bits(367))
   b'\x01o'
   >>> int(Bits(0b1011010))
   90
   >>> list(Bits(367))
   [1, 0, 1, 1, 0, 1, 1, 1, 1]

Features
--------

- Indexing and slicing of binary numbers like strings
- Conversion between several Python data types
- All builtin math operations including bit manipulation and comparison
- Padded binary numbers that maintain bit length
- Custom, easy-to-use bit flags
   - Bit field loading from bytes or stream
   - Custom data descriptors for fields
   - Field editing & conversion to bytes

For further documentation, visit http://paric.xyz/python/