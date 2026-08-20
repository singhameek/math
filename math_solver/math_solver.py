import math

import numpy as np
import reflex as rx
import sympy as sp


MODES = [
    "Single Equation",
    "Simultaneous",
    "Trig",
    "Quadratics",
    "Calculus",
    "Stats",
    "Unit Conversion",
]

LENGTH_UNITS = {
    "Meters": 1.0,
    "Kilometers": 1000.0,
    "Centimeters": 0.01,
    "Millimeters": 0.001,
    "Miles": 1609.34,
    "Yards": 0.9144,
    "Feet": 0.3048,
    "Inches": 0.0254,
}

WEIGHT_UNITS = {
    "Kilograms": 1000.0,
    "Grams": 1.0,
    "Metric Ton": 1_000_000.0,
    "Dram": 1.772,
    "Ounce": 28.35,
    "Pound": 453.59,
    "Stone": 6350.29,
    "Troy Ounce": 31.10,
    "Tola": 11.66,
}

TEMP_UNITS = ["Celsius", "Fahrenheit", "Kelvin"]

# Values are megabytes per unit.
DATA_UNITS = {
    "Bit": 0.000000125,
    "Nibble": 0.0000005,
    "Byte": 0.000001,
    "Kilobyte": 0.001,
    "Megabyte": 1.0,
    "Gigabyte": 1000.0,
    "Terabyte": 1_000_000.0,
    "Petabyte": 1_000_000_000.0,
    "Exabyte": 1_000_000_000_000.0,
    "Zettabyte": 1_000_000_000_000_000.0,
    "Yottabyte": 1_000_000_000_000_000_000.0,
}


class State(rx.State):
    mode: str = "Single Equation"

    # Single equation: ax + b = c
    a1: str = "0"
    b1: str = "0"
    c1: str = "0"
    single_result: str = ""
    single_error: str = ""

    # Simultaneous equations:
    # ax + by = c
    # dx + ey = f
    a2: str = "0"
    b2: str = "0"
    c2: str = "0"
    d2: str = "0"
    e2: str = "0"
    f2: str = "0"
    sim_result: str = ""
    sim_error: str = ""
    line1_points: list[dict[str, float]] = []
    line2_points: list[dict[str, float]] = []
    intersection_points: list[dict[str, float]] = []

    # Trigonometry
    trig_func: str = "sine"
    trig_value: str = "0"
    trig_result: str = ""
    trig_error: str = ""

    # Quadratics
    quad_a: str = "1"
    quad_b: str = "0"
    quad_c: str = "0"
    quad_result: str = ""
    quad_info: str = ""
    quad_error: str = ""

    # Calculus
    calc_input: str = "x**2 + x*5"
    calc_deriv: str = ""
    calc_integ: str = ""
    calc_error: str = ""

    # Statistics
    stats_raw: str = "0, 0"
    stats_mean: str = ""
    stats_median: str = ""
    stats_std: str = ""
    stats_min: str = ""
    stats_max: str = ""
    stats_len: str = ""
    stats_error: str = ""

    # Unit conversion
    unit_category: str = "Length"

    len_from: str = "Meters"
    len_to: str = "Kilometers"
    len_value: str = "1"

    wt_from: str = "Kilograms"
    wt_to: str = "Grams"
    wt_value: str = "1"

    temp_from: str = "Celsius"
    temp_to: str = "Fahrenheit"
    temp_value: str = "0"

    data_from: str = "Megabyte"
    data_to: str = "Kilobyte"
    data_value: str = "1"

    unit_result: str = ""
    unit_error: str = ""

    # Explicit setters are required because automatic setters are disabled.
    @rx.event
    def set_mode(self, value: str):
        self.mode = value

    @rx.event
    def set_a1(self, value: str):
        self.a1 = value

    @rx.event
    def set_b1(self, value: str):
        self.b1 = value

    @rx.event
    def set_c1(self, value: str):
        self.c1 = value

    @rx.event
    def set_a2(self, value: str):
        self.a2 = value

    @rx.event
    def set_b2(self, value: str):
        self.b2 = value

    @rx.event
    def set_c2(self, value: str):
        self.c2 = value

    @rx.event
    def set_d2(self, value: str):
        self.d2 = value

    @rx.event
    def set_e2(self, value: str):
        self.e2 = value

    @rx.event
    def set_f2(self, value: str):
        self.f2 = value

    @rx.event
    def set_trig_func(self, value: str):
        self.trig_func = value

    @rx.event
    def set_trig_value(self, value: str):
        self.trig_value = value

    @rx.event
    def set_quad_a(self, value: str):
        self.quad_a = value

    @rx.event
    def set_quad_b(self, value: str):
        self.quad_b = value

    @rx.event
    def set_quad_c(self, value: str):
        self.quad_c = value

    @rx.event
    def set_calc_input(self, value: str):
        self.calc_input = value

    @rx.event
    def set_stats_raw(self, value: str):
        self.stats_raw = value

    @rx.event
    def set_unit_category(self, value: str):
        self.unit_category = value
        self.unit_result = ""
        self.unit_error = ""

    @rx.event
    def set_len_from(self, value: str):
        self.len_from = value

    @rx.event
    def set_len_to(self, value: str):
        self.len_to = value

    @rx.event
    def set_len_value(self, value: str):
        self.len_value = value

    @rx.event
    def set_wt_from(self, value: str):
        self.wt_from = value

    @rx.event
    def set_wt_to(self, value: str):
        self.wt_to = value

    @rx.event
    def set_wt_value(self, value: str):
        self.wt_value = value

    @rx.event
    def set_temp_from(self, value: str):
        self.temp_from = value

    @rx.event
    def set_temp_to(self, value: str):
        self.temp_to = value

    @rx.event
    def set_temp_value(self, value: str):
        self.temp_value = value

    @rx.event
    def set_data_from(self, value: str):
        self.data_from = value

    @rx.event
    def set_data_to(self, value: str):
        self.data_to = value

    @rx.event
    def set_data_value(self, value: str):
        self.data_value = value

    @rx.event
    def solve_single(self):
        self.single_result = ""
        self.single_error = ""

        try:
            a = float(self.a1)
            b = float(self.b1)
            c = float(self.c1)
        except ValueError:
            self.single_error = "Please enter valid numbers."
            return

        if a == 0:
            self.single_error = "a cannot be 0."
            return

        self.single_result = f"x = {round((c - b) / a, 4)}"

    @rx.event
    def solve_simultaneous(self):
        self.sim_result = ""
        self.sim_error = ""
        self.line1_points = []
        self.line2_points = []
        self.intersection_points = []

        try:
            a = float(self.a2)
            b = float(self.b2)
            c = float(self.c2)
            d = float(self.d2)
            e = float(self.e2)
            f = float(self.f2)
        except ValueError:
            self.sim_error = "Please enter valid numbers."
            return

        determinant = a * e - b * d

        if determinant == 0:
            self.sim_error = "No unique solution (lines are parallel or identical)."
            return

        x_res = (c * e - b * f) / determinant
        y_res = (a * f - c * d) / determinant

        self.sim_result = f"x = {round(x_res, 4)}, y = {round(y_res, 4)}"

        limit = max(abs(x_res), abs(y_res), 10) + 2
        x_values = np.linspace(-limit, limit, 60)

        if b == 0:
            x_value = round(c / a, 4)
            self.line1_points = [
                {"x": x_value, "y": -limit},
                {"x": x_value, "y": limit},
            ]
        else:
            self.line1_points = [
                {
                    "x": round(float(xv), 4),
                    "y": round((c - a * float(xv)) / b, 4),
                }
                for xv in x_values
            ]

        if e == 0:
            x_value = round(f / d, 4)
            self.line2_points = [
                {"x": x_value, "y": -limit},
                {"x": x_value, "y": limit},
            ]
        else:
            self.line2_points = [
                {
                    "x": round(float(xv), 4),
                    "y": round((f - d * float(xv)) / e, 4),
                }
                for xv in x_values
            ]

        self.intersection_points = [
            {"x": round(x_res, 4), "y": round(y_res, 4)}
        ]

    @rx.event
    def solve_trig(self):
        self.trig_error = ""
        self.trig_result = ""

        try:
            value = float(self.trig_value)
        except ValueError:
            self.trig_error = "Please enter a valid number."
            return

        if self.trig_func == "sine":
            self.trig_result = str(round(math.sin(math.radians(value)), 4))
        elif self.trig_func == "cosine":
            self.trig_result = str(round(math.cos(math.radians(value)), 4))
        elif self.trig_func == "tangent":
            self.trig_result = str(round(math.tan(math.radians(value)), 4))
        elif self.trig_func == "inverse sine":
            if -1 <= value <= 1:
                self.trig_result = str(round(math.degrees(math.asin(value)), 4))
            else:
                self.trig_error = "Value must be between -1 and 1."
        elif self.trig_func == "inverse cosine":
            if -1 <= value <= 1:
                self.trig_result = str(round(math.degrees(math.acos(value)), 4))
            else:
                self.trig_error = "Value must be between -1 and 1."
        elif self.trig_func == "inverse tangent":
            self.trig_result = str(round(math.degrees(math.atan(value)), 4))

    @rx.event
    def solve_quadratic(self):
        self.quad_error = ""
        self.quad_result = ""
        self.quad_info = ""

        try:
            a = float(self.quad_a)
            b = float(self.quad_b)
            c = float(self.quad_c)
        except ValueError:
            self.quad_error = "Please enter valid numbers."
            return

        if a == 0:
            if b == 0:
                self.quad_error = "a and b cannot both be 0."
            else:
                self.quad_result = f"Linear equation: x = {round(-c / b, 4)}"
                self.quad_info = "a = 0, so this is actually linear."
            return

        discriminant = b**2 - 4 * a * c

        if discriminant < 0:
            real_part = round(-b / (2 * a), 4)
            imag_part = round((abs(discriminant) ** 0.5) / (2 * a), 4)
            self.quad_info = "The roots are complex."
            self.quad_result = (
                f"x1 = {real_part} + {imag_part}i, "
                f"x2 = {real_part} - {imag_part}i"
            )
        elif discriminant == 0:
            self.quad_result = f"One answer: x = {round(-b / (2 * a), 4)}"
        else:
            sqrt_discriminant = discriminant**0.5
            x1 = round((-b + sqrt_discriminant) / (2 * a), 4)
            x2 = round((-b - sqrt_discriminant) / (2 * a), 4)
            self.quad_result = f"x1 = {x1}, x2 = {x2}"

    @rx.event
    def solve_calculus(self):
        self.calc_error = ""
        self.calc_deriv = ""
        self.calc_integ = ""

        user_input = self.calc_input.strip()

        if not user_input:
            self.calc_error = "Please enter a function."
            return

        try:
            x = sp.symbols("x")
            expression = sp.sympify(user_input, locals={"x": x})

            self.calc_deriv = str(sp.diff(expression, x))
            self.calc_integ = f"{sp.integrate(expression, x)} + C"
        except Exception:
            self.calc_error = f"Could not parse '{user_input}'."

    @rx.event
    def solve_stats(self):
        self.stats_error = ""
        self.stats_mean = ""
        self.stats_median = ""
        self.stats_std = ""
        self.stats_min = ""
        self.stats_max = ""
        self.stats_len = ""

        try:
            data = [
                float(value.strip())
                for value in self.stats_raw.split(",")
                if value.strip()
            ]
        except ValueError:
            self.stats_error = "Please ensure you only use numbers and commas."
            return

        if not data:
            self.stats_error = "Please enter data."
            return

        self.stats_mean = f"{np.mean(data):.2f}"
        self.stats_median = f"{np.median(data):.2f}"
        self.stats_std = f"{np.std(data):.2f}"
        self.stats_min = str(np.min(data))
        self.stats_max = str(np.max(data))
        self.stats_len = str(len(data))

    @rx.event
    def convert_length(self):
        self.unit_result = ""
        self.unit_error = ""

        try:
            value = float(self.len_value)
            result = value * LENGTH_UNITS[self.len_from] / LENGTH_UNITS[self.len_to]
            self.unit_result = (
                f"{value} {self.len_from} = {result:.4f} {self.len_to}"
            )
        except (ValueError, KeyError):
            self.unit_error = "Please enter a valid number."

    @rx.event
    def convert_weight(self):
        self.unit_result = ""
        self.unit_error = ""

        try:
            value = float(self.wt_value)
            result = value * WEIGHT_UNITS[self.wt_from] / WEIGHT_UNITS[self.wt_to]
            self.unit_result = f"{value} {self.wt_from} = {result:.4f} {self.wt_to}"
        except (ValueError, KeyError):
            self.unit_error = "Please enter a valid number."

    @rx.event
    def convert_temp(self):
        self.unit_result = ""
        self.unit_error = ""

        try:
            value = float(self.temp_value)
        except ValueError:
            self.unit_error = "Please enter a valid number."
            return

        if self.temp_from == "Celsius":
            celsius = value
        elif self.temp_from == "Fahrenheit":
            celsius = (value - 32) * 5 / 9
        else:
            celsius = value - 273.15

        if self.temp_to == "Celsius":
            result = celsius
        elif self.temp_to == "Fahrenheit":
            result = celsius * 9 / 5 + 32
        else:
            result = celsius + 273.15

        self.unit_result = f"{value} {self.temp_from} = {result:.2f} {self.temp_to}"

    @rx.event
    def convert_data(self):
        self.unit_result = ""
        self.unit_error = ""

        try:
            value = float(self.data_value)
            result = value * DATA_UNITS[self.data_from] / DATA_UNITS[self.data_to]
            self.unit_result = f"{value} {self.data_from} = {result:.2f} {self.data_to}"
        except (ValueError, KeyError):
            self.unit_error = "Please enter a valid number."


def labeled_input(label: str, value, on_change) -> rx.Component:
    return rx.vstack(
        rx.text(label, size="2", color="gray"),
        rx.input(
            value=value,
            on_change=on_change,
            type="text",
            width="100%",
        ),
        spacing="1",
        width="100%",
    )


def statistic_card(label: str, value) -> rx.Component:
    return rx.box(
        rx.text(label, size="2", color="gray"),
        rx.heading(value, size="5"),
        padding="1em",
        border="1px solid #eaeaea",
        border_radius="8px",
        min_width="150px",
    )


def single_equation() -> rx.Component:
    return rx.vstack(
        rx.heading("Solve ax + b = c", size="5"),
        rx.hstack(
            labeled_input("a", State.a1, State.set_a1),
            labeled_input("b", State.b1, State.set_b1),
            labeled_input("c", State.c1, State.set_c1),
            spacing="3",
            width="100%",
        ),
        rx.button("Solve", on_click=State.solve_single, color_scheme="blue"),
        rx.cond(
            State.single_error != "",
            rx.callout(State.single_error, color_scheme="red"),
        ),
        rx.cond(
            State.single_result != "",
            rx.callout(State.single_result, color_scheme="green"),
        ),
        spacing="4",
        width="100%",
    )


def simultaneous() -> rx.Component:
    return rx.vstack(
        rx.heading("Solve ax + by = c and dx + ey = f", size="5"),
        rx.hstack(
            rx.vstack(
                labeled_input("a", State.a2, State.set_a2),
                labeled_input("b", State.b2, State.set_b2),
                labeled_input("c", State.c2, State.set_c2),
                spacing="2",
                width="100%",
            ),
            rx.vstack(
                labeled_input("d", State.d2, State.set_d2),
                labeled_input("e", State.e2, State.set_e2),
                labeled_input("f", State.f2, State.set_f2),
                spacing="2",
                width="100%",
            ),
            spacing="4",
            width="100%",
        ),
        rx.button("Solve", on_click=State.solve_simultaneous, color_scheme="blue"),
        rx.cond(
            State.sim_error != "",
            rx.callout(State.sim_error, color_scheme="red"),
        ),
        rx.cond(
            State.sim_result != "",
            rx.vstack(
                rx.callout(State.sim_result, color_scheme="green"),
                rx.recharts.scatter_chart(
                    rx.recharts.scatter(
                        data=State.line1_points,
                        name="Line 1",
                        line=True,
                        fill="#2563eb",
                    ),
                    rx.recharts.scatter(
                        data=State.line2_points,
                        name="Line 2",
                        line=True,
                        fill="#16a34a",
                    ),
                    rx.recharts.scatter(
                        data=State.intersection_points,
                        name="Intersection",
                        fill="#dc2626",
                    ),
                    rx.recharts.x_axis(data_key="x", type_="number"),
                    rx.recharts.y_axis(type_="number"),
                    rx.recharts.legend(),
                    width=600,
                    height=400,
                ),
                width="100%",
            ),
        ),
        spacing="4",
        width="100%",
    )


def trig() -> rx.Component:
    return rx.vstack(
        rx.heading("Solve Trig Functions", size="5"),
        rx.vstack(
            rx.text("Choose function", size="2", color="gray"),
            rx.select(
                [
                    "sine",
                    "cosine",
                    "tangent",
                    "inverse sine",
                    "inverse cosine",
                    "inverse tangent",
                ],
                value=State.trig_func,
                on_change=State.set_trig_func,
            ),
            spacing="1",
            width="100%",
        ),
        labeled_input(
            "Value (degrees for sin/cos/tan, ratio for inverse)",
            State.trig_value,
            State.set_trig_value,
        ),
        rx.button("Solve", on_click=State.solve_trig, color_scheme="blue"),
        rx.cond(
            State.trig_error != "",
            rx.callout(State.trig_error, color_scheme="red"),
        ),
        rx.cond(
            State.trig_result != "",
            rx.callout(f"Result: {State.trig_result}", color_scheme="green"),
        ),
        spacing="4",
        width="100%",
    )


def quadratics() -> rx.Component:
    return rx.vstack(
        rx.heading("Solve ax² + bx + c = 0", size="5"),
        rx.hstack(
            labeled_input("a", State.quad_a, State.set_quad_a),
            labeled_input("b", State.quad_b, State.set_quad_b),
            labeled_input("c", State.quad_c, State.set_quad_c),
            spacing="3",
            width="100%",
        ),
        rx.button("Solve", on_click=State.solve_quadratic, color_scheme="blue"),
        rx.cond(
            State.quad_error != "",
            rx.callout(State.quad_error, color_scheme="red"),
        ),
        rx.cond(
            State.quad_info != "",
            rx.callout(State.quad_info, color_scheme="blue"),
        ),
        rx.cond(
            State.quad_result != "",
            rx.callout(State.quad_result, color_scheme="green"),
        ),
        spacing="4",
        width="100%",
    )


def calculus() -> rx.Component:
    return rx.vstack(
        rx.heading("Calculus Solver", size="5"),
        rx.callout(
            "Use * for multiplication and ** for powers.",
            color_scheme="blue",
        ),
        labeled_input("Enter function", State.calc_input, State.set_calc_input),
        rx.button("Solve", on_click=State.solve_calculus, color_scheme="blue"),
        rx.cond(
            State.calc_error != "",
            rx.callout(State.calc_error, color_scheme="red"),
        ),
        rx.cond(
            State.calc_deriv != "",
            rx.vstack(
                rx.heading("The Derivative", size="4"),
                rx.text(State.calc_deriv, size="4"),
                rx.heading("The Integral", size="4"),
                rx.text(State.calc_integ, size="4"),
                spacing="3",
                width="100%",
            ),
        ),
        spacing="4",
        width="100%",
    )


def stats() -> rx.Component:
    return rx.vstack(
        rx.heading("Statistics", size="5"),
        rx.text("Enter data separated by commas.", color="gray"),
        rx.text_area(
            value=State.stats_raw,
            on_change=State.set_stats_raw,
            width="100%",
        ),
        rx.button("Calculate", on_click=State.solve_stats, color_scheme="blue"),
        rx.cond(
            State.stats_error != "",
            rx.callout(State.stats_error, color_scheme="red"),
        ),
        rx.cond(
            State.stats_mean != "",
            rx.vstack(
                rx.hstack(
                    statistic_card("Mean (Average)", State.stats_mean),
                    statistic_card("Median", State.stats_median),
                    statistic_card("Std Deviation", State.stats_std),
                    spacing="6",
                ),
                rx.hstack(
                    statistic_card("Minimum", State.stats_min),
                    statistic_card("Maximum", State.stats_max),
                    statistic_card("Length", State.stats_len),
                    spacing="6",
                ),
                spacing="4",
                width="100%",
            ),
        ),
        spacing="4",
        width="100%",
    )


def unit_conversion() -> rx.Component:
    return rx.vstack(
        rx.heading("Unit Conversion", size="5"),
        rx.vstack(
            rx.text("Select Category", size="2", color="gray"),
            rx.select(
                ["Length", "Weight", "Temperature", "Data"],
                value=State.unit_category,
                on_change=State.set_unit_category,
            ),
            spacing="1",
            width="100%",
        ),
        rx.cond(
            State.unit_category == "Length",
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.text("From:", size="2", color="gray"),
                        rx.select(
                            list(LENGTH_UNITS.keys()),
                            value=State.len_from,
                            on_change=State.set_len_from,
                        ),
                        labeled_input("Value", State.len_value, State.set_len_value),
                        spacing="2",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("To:", size="2", color="gray"),
                        rx.select(
                            list(LENGTH_UNITS.keys()),
                            value=State.len_to,
                            on_change=State.set_len_to,
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                ),
                rx.button("Convert", on_click=State.convert_length, color_scheme="blue"),
                spacing="3",
                width="100%",
            ),
        ),
        rx.cond(
            State.unit_category == "Weight",
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.text("From:", size="2", color="gray"),
                        rx.select(
                            list(WEIGHT_UNITS.keys()),
                            value=State.wt_from,
                            on_change=State.set_wt_from,
                        ),
                        labeled_input("Value", State.wt_value, State.set_wt_value),
                        spacing="2",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("To:", size="2", color="gray"),
                        rx.select(
                            list(WEIGHT_UNITS.keys()),
                            value=State.wt_to,
                            on_change=State.set_wt_to,
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                ),
                rx.button("Convert", on_click=State.convert_weight, color_scheme="blue"),
                spacing="3",
                width="100%",
            ),
        ),
        rx.cond(
            State.unit_category == "Temperature",
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.text("From:", size="2", color="gray"),
                        rx.select(
                            TEMP_UNITS,
                            value=State.temp_from,
                            on_change=State.set_temp_from,
                        ),
                        labeled_input("Value", State.temp_value, State.set_temp_value),
                        spacing="2",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("To:", size="2", color="gray"),
                        rx.select(
                            TEMP_UNITS,
                            value=State.temp_to,
                            on_change=State.set_temp_to,
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                ),
                rx.button("Convert", on_click=State.convert_temp, color_scheme="blue"),
                spacing="3",
                width="100%",
            ),
        ),
        rx.cond(
            State.unit_category == "Data",
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.text("From:", size="2", color="gray"),
                        rx.select(
                            list(DATA_UNITS.keys()),
                            value=State.data_from,
                            on_change=State.set_data_from,
                        ),
                        labeled_input("Value", State.data_value, State.set_data_value),
                        spacing="2",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("To:", size="2", color="gray"),
                        rx.select(
                            list(DATA_UNITS.keys()),
                            value=State.data_to,
                            on_change=State.set_data_to,
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                ),
                rx.button("Convert", on_click=State.convert_data, color_scheme="blue"),
                spacing="3",
                width="100%",
            ),
        ),
        rx.cond(
            State.unit_error != "",
            rx.callout(State.unit_error, color_scheme="red"),
        ),
        rx.cond(
            State.unit_result != "",
            rx.callout(State.unit_result, color_scheme="green"),
        ),
        spacing="4",
        width="100%",
    )


def mode_content() -> rx.Component:
    return rx.match(
        State.mode,
        ("Single Equation", single_equation()),
        ("Simultaneous", simultaneous()),
        ("Trig", trig()),
        ("Quadratics", quadratics()),
        ("Calculus", calculus()),
        ("Stats", stats()),
        ("Unit Conversion", unit_conversion()),
        single_equation(),
    )


def sidebar() -> rx.Component:
    return rx.vstack(
        rx.heading("Select Mode", size="4"),
        rx.select(
            MODES,
            value=State.mode,
            on_change=State.set_mode,
            width="100%",
        ),
        spacing="3",
        width="220px",
        padding="1em",
        border_right="1px solid #eaeaea",
        min_height="100vh",
        align_items="start",
    )


def index() -> rx.Component:
    return rx.hstack(
        sidebar(),
        rx.container(
            rx.vstack(
                rx.heading("Math Solver", size="8"),
                mode_content(),
                spacing="5",
                padding="2em",
                width="100%",
            ),
            max_width="900px",
        ),
        spacing="0",
        width="100%",
        align_items="start",
    )


app = rx.App()
app.add_page(index, title="Math Solver")