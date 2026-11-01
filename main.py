import customtkinter as ctk
import random
from decimal import Decimal, InvalidOperation, DivisionByZero
from PIL import Image
from pathlib import Path
from calculator import (
    calculate_numbers,
    format_number,
    convert_temperature as convert_value,
)
from personality import (
    hostility_level,
    random_comment,
    should_confirm,
    should_delay,
    processing_message,
    should_become_gentleman,
)


ctk.set_appearance_mode("light")
ctk.set_widget_scaling(1.0)
ctk.set_window_scaling(1.0)

COLORS = {
    "background": "#F8F5F0",
    "numbers": "#DCEAF3",
    "operators": "#E5DDF2",
    "accent": "#EBCBD1",
    "text": "#34343A",
    "muted": "#777780",
    "white": "#FFFFFF",
}


class ProbablyFour(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Probably 4")
        self.geometry("400x700")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["background"])

        self.current_input = "0"
        self.first_number = None
        self.operator = None
        self.start_new_input = False
        self.mode = "Calculator"
        self.temperature_unit = None
        self.calculation_count = 0
        self.processing = False
        self.gentleman_mode = False

        self.create_interface()
        self.bind("<KeyPress>", self.on_key_press)

    def create_interface(self):
        # Title
        # Header
        header = ctk.CTkFrame(
            self,
            fg_color="transparent",
            width=340,
            height=100,
        )
        header.pack(pady=(20, 5))
        header.pack_propagate(False)

        # Left side: title and subtitle
        header_text = ctk.CTkFrame(
            header,
            fg_color="transparent",
        )
        header_text.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(
            header_text,
            text="Probably 4",
            font=("Arial", 28, "bold"),
            text_color=COLORS["text"],
            anchor="w",
        ).pack(anchor="w", pady=(12, 5))

        ctk.CTkLabel(
            header_text,
            text="Correct answers.\nQuestionable manners.",
            font=("Arial", 16, "bold"),
            text_color=COLORS["muted"],
            justify="left",
            anchor="w",
        ).pack(anchor="w")

        # Right side: logo
        logo_path = Path(__file__).resolve().parent / "assets" / "logo.png"

        self.logo_image = ctk.CTkImage(
            light_image=Image.open(logo_path),
            dark_image=Image.open(logo_path),
            size=(65, 83),
        )

        self.logo_label = ctk.CTkLabel(
            header,
            image=self.logo_image,
            text="",
        )

        self.logo_label.pack(
            side="right",
            padx=(10, 0),
        )

        self.mode_switch = ctk.CTkSegmentedButton(
            self,
            values=["Calculator", "Converter"],
            width=280,
            height=42,
            font=("Arial", 17, "bold"),
            corner_radius=12,
            command=self.change_mode,
            selected_color=COLORS["operators"],
            selected_hover_color="#C9C4D5",
            unselected_color=COLORS["numbers"],
            unselected_hover_color="#C9C4D5",
            text_color=COLORS["text"],
        )
        self.mode_switch.pack(pady=(15, 0))
        self.mode_switch.set("Calculator")

        # Display
        self.display = ctk.CTkEntry(
            self,
            width=320,
            height=65,
            corner_radius=15,
            font=("Arial", 32),
            justify="right",
            fg_color=COLORS["white"],
            text_color=COLORS["text"],
            border_width=0,
        )
        self.display.pack(pady=(25, 10))
        self.display.insert(0, "0")
        self.display.configure(state="readonly")

        # Personality text
        self.comment_font = ctk.CTkFont(
            family="Arial",
            size=18,
            weight="bold",
        )

        self.comment = ctk.CTkLabel(
            self,
            text="At your service. Regrettably.",
            font=self.comment_font,
            text_color=COLORS["muted"],
            wraplength=340,
            justify="center",
        )
        self.comment.pack(pady=(0, 15))

        self.progress = ctk.CTkProgressBar(
            self,
            width=220,
            height=5,
            mode="indeterminate",
            progress_color=COLORS["accent"],
            fg_color=COLORS["operators"],
        )

        self.converter_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        ctk.CTkLabel(
            self.converter_frame,
            text="Choose your input unit",
            font=("Arial", 16),
            text_color=COLORS["text"],
        ).pack(pady=(10, 8))

        self.temperature_choice = ctk.CTkSegmentedButton(
            self.converter_frame,
            values=["Celsius", "Fahrenheit"],
            command=self.select_temperature,
            selected_color=COLORS["accent"],
            selected_hover_color="#D9B8C0",
            unselected_color=COLORS["numbers"],
            unselected_hover_color="#C9C4D5",
            text_color=COLORS["text"],
        )
        self.temperature_choice.pack(pady=(0, 20))

        self.converter_input = ctk.CTkEntry(
            self.converter_frame,
            width=300,
            height=55,
            corner_radius=12,
            font=("Arial", 26),
            justify="right",
            placeholder_text="Enter a temperature",
            fg_color=COLORS["white"],
            text_color=COLORS["text"],
            border_width=0,
        )
        self.converter_input.pack(pady=(0, 12))
        self.converter_input.bind(
            "<Return>",
            lambda event: self.process_calculation(),
        )

        self.conversion_direction = ctk.CTkLabel(
            self.converter_frame,
            text="Select a unit to begin",
            font=("Arial", 15),
            text_color=COLORS["muted"],
        )
        self.conversion_direction.pack(pady=(0, 12))

        self.converter_result = ctk.CTkLabel(
            self.converter_frame,
            text="—",
            width=300,
            height=65,
            corner_radius=12,
            fg_color=COLORS["white"],
            font=("Arial", 28, "bold"),
            text_color=COLORS["text"],
        )
        self.converter_result.pack(pady=(0, 20))

        ctk.CTkButton(
            self.converter_frame,
            text="CONVERT",
            width=300,
            height=50,
            corner_radius=12,
            font=("Arial", 17, "bold"),
            fg_color=COLORS["accent"],
            hover_color="#D9B8C0",
            text_color=COLORS["text"],
            command=self.process_calculation,
        ).pack()

        # Button grid
        self.button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        self.button_frame.pack()

        button_frame = self.button_frame


        buttons = [
            ["7", "8", "9", "÷"],
            ["4", "5", "6", "×"],
            ["1", "2", "3", "−"],
            ["C", "0", ".", "+"],
            ["", "", "=", ""],
        ]

        self.digit_buttons = []

        for row_index, row in enumerate(buttons):
            for col_index, value in enumerate(row):
                if not value:
                    continue
                if value == "=":
                    color = COLORS["accent"]
                elif value in ["+", "−", "×", "÷"]:
                    color = COLORS["operators"]
                else:
                    color = COLORS["numbers"]

                button = ctk.CTkButton(
                    button_frame,
                    text=value,
                    width=70,
                    height=55,
                    corner_radius=12,
                    font=("Arial", 24),
                    fg_color=color,
                    hover_color="#C9C4D5",
                    text_color=COLORS["text"],
                    command=lambda v=value: self.handle_button(v),
                )

                if value.isdigit():
                    self.digit_buttons.append(button)

                if value == "=":
                    button.grid(
                        row=row_index,
                        column=1,
                        columnspan=2,
                        padx=5,
                        pady=5,
                        sticky="ew",
                    )
                else:
                    button.grid(
                        row=row_index,
                        column=col_index,
                        padx=5,
                        pady=5,
                    )

    def update_display(self):
        self.display.configure(state="normal")
        self.display.delete(0, "end")
        self.display.insert(0, self.current_input)
        self.display.configure(state="readonly")

    def handle_button(self, value):
        if self.processing:
            return

        if value == "C":
            self.clear()

        elif value in ["+", "−", "×", "÷"]:
            self.set_operator(value)

        elif value == "=":
            if self.first_number is not None and self.operator is not None:
                self.process_calculation()
            return

        else:
            self.enter_digit(value)

            if value.isdigit() and not self.gentleman_mode:
                self.shuffle_digits()

        self.update_display()

    def enter_digit(self, digit):
        if self.current_input == "Error":
            self.clear()

        if self.start_new_input:
            self.current_input = "0"
            self.start_new_input = False

        if digit == ".":
            if "." not in self.current_input:
                self.current_input += "."
        elif self.current_input == "0":
            self.current_input = digit
        else:
            self.current_input += digit

    def set_operator(self, operator):
        if self.current_input == "Error":
            return

        if self.first_number is not None and not self.start_new_input:
            self.calculate()
            if self.current_input == "Error":
                return

        self.first_number = Decimal(self.current_input)
        self.operator = operator
        self.start_new_input = True

    def calculate(self):
        if self.first_number is None or self.operator is None:
            return

        try:
            second_number = Decimal(self.current_input)

            result = calculate_numbers(
                self.first_number,
                self.operator,
                second_number,
            )

            self.current_input = format_number(result)

        except (InvalidOperation, ZeroDivisionError, ValueError):
            self.current_input = "Error"
            self.comment.configure(
                text="Even I have my limits."
            )

        self.first_number = None
        self.operator = None
        self.start_new_input = True

    def change_mode(self, mode):
        self.mode = mode

        if mode == "Converter":
            self.display.pack_forget()
            self.button_frame.pack_forget()

            self.converter_frame.pack(pady=(5, 10))

            self.temperature_unit = None
            self.temperature_choice.set("")
            self.converter_input.delete(0, "end")
            self.converter_result.configure(text="—")
            self.conversion_direction.configure(
                text="Select a unit to begin"
            )

            self.comment.configure(
                text=(
                    "Very well. You appear capable enough."
                    if self.gentleman_mode
                    else "A matter of considerable importance."
                )
            )

        else:
            self.converter_frame.pack_forget()

            self.display.pack(
                before=self.comment,
                pady=(25, 10),
            )
            self.button_frame.pack()

            self.clear()
            self.comment.configure(
                text="Back to elementary mathematics, I see."
            )


    def select_temperature(self, selected):
        if self.gentleman_mode:
            # For once, the user's preference is respected.
            self.temperature_unit = selected

            self.comment.configure(
                text="Very well. Your preference shall be respected."
            )

        elif selected == "Celsius":
            self.temperature_unit = "Fahrenheit"
            self.temperature_choice.set("Fahrenheit")

            self.comment.configure(
                text="Celsius? How provincial."
            )

        else:
            self.temperature_unit = "Celsius"
            self.temperature_choice.set("Celsius")

            self.comment.configure(
                text="Fahrenheit? An eccentric preference."
            )

        if self.temperature_unit == "Celsius":
            direction = "Celsius → Fahrenheit"
        else:
            direction = "Fahrenheit → Celsius"

        self.conversion_direction.configure(text=direction)
        self.converter_result.configure(text="—")


    def convert_temperature(self):
        if self.temperature_unit is None:
            self.comment.configure(
                text="One must first select a unit."
            )
            return False

        try:
            value = Decimal(self.converter_input.get().strip())

            result, unit = convert_value(
                value,
                self.temperature_unit,
            )

            self.converter_result.configure(
                text=f"{result} {unit}"
            )

            return True

        except (InvalidOperation, ValueError, OverflowError):
            self.converter_result.configure(text="Error")
            self.comment.configure(
                text="Numbers, if you would be so kind."
            )
            return False


    def clear(self):
        self.current_input = "0"
        self.first_number = None
        self.operator = None
        self.start_new_input = False
        self.comment.configure(text="At your service. Regrettably.")

    def shuffle_digits(self):
        positions = [
            (int(button.grid_info()["row"]), int(button.grid_info()["column"]))
            for button in self.digit_buttons
        ]

        shuffled = positions.copy()

        while shuffled == positions:
            random.shuffle(shuffled)

        for button, (row, column) in zip(self.digit_buttons, shuffled):
            button.grid(row=row, column=column)

    def get_hostility_level(self):
        return hostility_level(self.calculation_count)


    def make_comment(self):
        self.comment.configure(
            text=random_comment(self.calculation_count)
        )

    def request_confirmation(self, on_confirm):
        if should_confirm(self.calculation_count):
            self.show_confirmation(on_confirm)
        else:
            on_confirm()

    def process_calculation(self):
        if self.processing:
            return

        if self.mode == "Converter":
            if self.temperature_unit is None:
                self.comment.configure(
                    text="One must first select a unit."
                )
                return

            try:
                value = Decimal(self.converter_input.get().strip())
                if not value.is_finite():
                    raise InvalidOperation
            except (InvalidOperation, ValueError):
                self.converter_result.configure(text="Error")
                self.comment.configure(
                    text="Numbers, if you would be so kind."
                )
                return

        self.processing = True

        if self.gentleman_mode:
            self.finish_calculation()
            return

        self.request_confirmation(self.continue_calculation)


    def continue_calculation(self):
        if should_delay(self.calculation_count):
            self.comment.configure(
                text=processing_message()
            )

            self.progress.pack(after=self.comment, pady=(0, 8))
            self.progress.start()

            self.mode_switch.configure(state="disabled")

            if self.mode == "Converter":
                self.converter_input.configure(state="disabled")
                self.temperature_choice.configure(state="disabled")

            delay = random.randint(1000, 2000)
            self.after(delay, self.finish_calculation)

        else:
            self.finish_calculation()

    def finish_calculation(self):
        try:
            if self.mode == "Converter":
                success = self.convert_temperature()
            else:
                self.calculate()
                success = self.current_input != "Error"

            if success:
                self.calculation_count += 1

                if self.gentleman_mode:
                    self.gentleman_mode = False

                    self.comment.configure(
                        text="Let us not make a habit of this."
                    )

                    if self.mode == "Converter":
                        self.temperature_unit = None
                        self.temperature_choice.set("")
                        self.conversion_direction.configure(
                            text="Select a unit to begin"
                        )

                else:
                    self.make_comment()
                    self.maybe_become_gentleman()

            self.update_display()

        finally:
            self.progress.stop()
            self.progress.pack_forget()
            self.processing = False
            self.mode_switch.configure(state="normal")
            self.converter_input.configure(state="normal")
            self.temperature_choice.configure(state="normal")


    def maybe_become_gentleman(self):
        if should_become_gentleman(self.calculation_count):
            self.gentleman_mode = True

            self.comment.configure(
                text="Very well. You appear capable enough."
            )

            if self.mode == "Converter":
                self.temperature_unit = None
                self.temperature_choice.set("")
                self.conversion_direction.configure(
                    text="Select a unit to begin"
                )

    def show_confirmation(self, on_confirm):
        self.mode_switch.configure(state="disabled")

        # Temporarily hide the active interface
        if self.mode == "Calculator":
            self.button_frame.pack_forget()
        else:
            self.converter_frame.pack_forget()

        panel = ctk.CTkFrame(
            self,
            width=330,
            height=200,
            corner_radius=16,
            fg_color=COLORS["white"],
            border_width=1,
            border_color=COLORS["operators"],
        )
        panel.pack(pady=(15, 10))
        panel.pack_propagate(False)

        ctk.CTkLabel(
            panel,
            text="Are you quite certain?",
            font=("Arial", 21, "bold"),
            text_color=COLORS["text"],
        ).pack(pady=(25, 8))

        ctk.CTkLabel(
            panel,
            text="One ought to think before calculating.",
            font=("Arial", 14),
            text_color=COLORS["muted"],
        ).pack(pady=(0, 25))

        def respond(accepted):
            panel.destroy()

            # Restore the normal interface
            if self.mode == "Calculator":
                self.button_frame.pack()
            else:
                self.converter_frame.pack(pady=(5, 10))

            self.mode_switch.configure(state="normal")

            if accepted:
                self.after_idle(on_confirm)
            else:
                self.processing = False
                self.comment.configure(
                    text="A rare moment of good judgement."
                )

        buttons = ctk.CTkFrame(
            panel,
            fg_color="transparent",
        )
        buttons.pack()

        ctk.CTkButton(
            buttons,
            text="Indeed",
            width=130,
            height=42,
            font=("Arial", 15, "bold"),
            fg_color=COLORS["numbers"],
            hover_color="#C9C4D5",
            text_color=COLORS["text"],
            command=lambda: respond(True),
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            buttons,
            text="I suppose not",
            width=130,
            height=42,
            font=("Arial", 15, "bold"),
            fg_color=COLORS["accent"],
            hover_color="#D9B8C0",
            text_color=COLORS["text"],
            command=lambda: respond(False),
        ).pack(side="left", padx=5)

    def on_key_press(self, event):
        if self.processing or self.mode != "Calculator":
            return

        key = event.keysym
        char = event.char

        if char and char in "0123456789":
            self.handle_button(char)

        elif key == "KP_Decimal" or char == ".":
            self.handle_button(".")

        elif key in ("Return", "KP_Enter") or char == "=":
            self.handle_button("=")

        elif key == "Escape":
            self.handle_button("C")

        elif key == "BackSpace":
            self.backspace()
            self.update_display()

        else:
            operators = {
                "+": "+",
                "-": "−",
                "*": "×",
                "/": "÷",
            }

            keypad_operators = {
                "KP_Add": "+",
                "KP_Subtract": "−",
                "KP_Multiply": "×",
                "KP_Divide": "÷",
            }

            operator = operators.get(char) or keypad_operators.get(key)

            if operator:
                self.handle_button(operator)

    def backspace(self):
        if self.current_input == "Error" or self.start_new_input:
            self.clear()
            return

        self.current_input = self.current_input[:-1] or "0"

        if self.current_input == "-":
            self.current_input = "0"

if __name__ == "__main__":
    app = ProbablyFour()
    app.mainloop()
