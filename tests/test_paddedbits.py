from colorguard import PaddedBits
import pytest


def test_value_setting():
    with pytest.raises(ValueError):
        bits = PaddedBits(100, 2)

    bits = PaddedBits(100, 8)

    with pytest.raises(ValueError):
        bits += 500
    with pytest.raises(ValueError):
        bits.value = 500


def test_padding():
    bits = PaddedBits(4, 8)

    assert str(bits) == "0b00000100"
