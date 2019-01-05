.. Color Guard documentation master file, created by
   sphinx-quickstart on Sat Jan  5 02:14:49 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Color Guard
===========

.. toctree::
   :maxdepth: 2
   :caption: Contents:

**Color Guard** provides easy bit manipulation and an bit flag reading/writing in Python. Everything is built off of
the builtin ``int`` type so no math functionality is lost, while making it possible to index and slice binary numbers
like strings.

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
   >>> int(Bits(1011010))
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

Guide
-----

Example usages of Color Guard with explanations.

.. toctree::
   :maxdepth: 2

   user/install



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
