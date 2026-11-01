from decimal import Decimal, InvalidOperation


def calculate_numbers(
    first: Decimal,
    operator: str,
    second: Decimal,
) -> Decimal:
    if not first.is_finite() or not second.is_finite():
        raise InvalidOperation

    if operator == "+":
        result = first + second
    elif operator == "−":
        result = first - second
    elif operator == "×":
        result = first * second
    elif operator == "÷":
        if second == 0:
            raise ZeroDivisionError
        result = first / second
    else:
        raise ValueError(f"Unknown operator: {operator}")

    if not result.is_finite():
        raise InvalidOperation

    return result


def format_number(value: Decimal) -> str:
    text = format(value, "f")

    if "." in text:
        text = text.rstrip("0").rstrip(".")

    return text or "0"


def convert_temperature(
    value: Decimal,
    input_unit: str,
) -> tuple[Decimal, str]:
    if not value.is_finite():
        raise InvalidOperation

    if input_unit == "Celsius":
        result = value * Decimal("1.8") + 32
        output_unit = "°F"
    elif input_unit == "Fahrenheit":
        result = (value - 32) / Decimal("1.8")
        output_unit = "°C"
    else:
        raise ValueError(f"Unknown unit: {input_unit}")

    return result.quantize(Decimal("0.01")), output_unit
