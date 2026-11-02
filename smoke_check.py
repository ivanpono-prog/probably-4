"""Small GUI integration check shared by source and frozen Windows builds."""

from decimal import Decimal


def check_app(app):
    app.withdraw()
    app.update()
    app.first_number = Decimal(2)
    app.operator = "+"
    app.current_input = "2"
    app.calculate()
    assert app.current_input == "4", "Arithmetic failed"
    app.first_number = Decimal(1)
    app.operator = "÷"
    app.current_input = "0"
    app.calculate()
    assert app.current_input == "Error", "Division by zero was not handled"
    app.clear()
    app.handle_button("7")
    assert app.current_input == "7", "Digit input failed"
    app.backspace()
    assert app.current_input == "0", "Backspace failed"
    app.change_mode("Converter")
    app.gentleman_mode = True
    app.select_temperature("Celsius")
    app.converter_input.delete(0, "end")
    app.converter_input.insert(0, "100")
    app.convert_temperature()
    assert "212" in app.converter_result.cget("text"), "Temperature conversion failed"
    assert app.logo_image is not None, "Logo was not loaded"
    app.update()
    return {
        "ok": True,
        "checks": [
            "startup",
            "logo",
            "arithmetic",
            "zero_division",
            "digit_input",
            "backspace",
            "converter",
        ],
    }
