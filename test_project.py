import pytest
from project import *
from mock_in_out import set_key_input
from datetime import date

def test_read_int():
    set_key_input(["1"])
    assert read_int("Input: ", 0, 2) == 1

def test_read_int_too_big():   
    with pytest.raises(ValueError):
        set_key_input(["3"])
        read_int("Input: ", 0, 2)

def test_read_string():
    set_key_input(["cat "])
    assert read_string("Favourite animal: ") == "cat"

def test_read_string_invalid():
    set_key_input([""])
    with pytest.raises(ValueError):
        read_string("Animal: ")

def test_convert_input_to_date_type():
    with pytest.raises(ValueError):
        convert_input_to_date_type("cat")
    assert isinstance(convert_input_to_date_type("01/02/2005"), date)
    with pytest.raises(ValueError):
        convert_input_to_date_type("2005/02/01")