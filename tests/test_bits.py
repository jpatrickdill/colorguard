from colorguard import Bits
import pytest


def test_value_setting():
    bits = Bits.from_binary("101")
    assert bits == 5

    bits = Bits.from_hex("ff")
    assert bits == 255


def test_index():
    bits = Bits(0b101)

    assert bits[0] == 1 and bits[1] == 0

    bits[1] = 1
    assert bits == 0b111


def test_slice():
    bits = Bits(0b1010)

    assert bits[:3] == 0b101
    assert bits[1:] == 0b10
    assert bits[1:0] == 0

    bits[1:3] = 0b10
    assert bits == 0b1100

    with pytest.raises(ValueError):
        bits[1:3] = 0b100


def test_bytes():
    assert Bits.from_bytes(b"h") == 104

    assert Bits(104).to_bytes() == b"h"
