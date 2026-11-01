from decimal import Decimal

import pytest

from calculator import (
    calculate_numbers,
    convert_temperature,
    format_number,
)


@pytest.mark.parametrize(
    "first, operator, second, expected",
    [
        ("2", "+", "2", "4"),
        ("10", "−", "3", "7"),
        ("5", "×", "6", "30"),
        ("10", "÷", "4", "2.5"),
        ("0.1", "+", "0.2", "0.3"),
        ("5", "−", "8", "-3"),
    ],
)
def test_arithmetic(first, operator, second, expected):
    result = calculate_numbers(
        Decimal(first),
        operator,
        Decimal(second),
    )

    assert result == Decimal(expected)


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        calculate_numbers(
            Decimal(10),
            "÷",
            Decimal(0),
        )


def test_number_formatting():
    assert format_number(Decimal("4.000")) == "4"
    assert format_number(Decimal("2.500")) == "2.5"
    assert format_number(Decimal("0.000")) == "0"


def test_celsius_to_fahrenheit():
    result, unit = convert_temperature(
        Decimal(100),
        "Celsius",
    )

    assert result == Decimal("212.00")
    assert unit == "°F"


def test_fahrenheit_to_celsius():
    result, unit = convert_temperature(
        Decimal(32),
        "Fahrenheit",
    )

    assert result == Decimal("0.00")
    assert unit == "°C"
