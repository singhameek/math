import math
import reflex as rx
import sympy as sp
import numpy as np

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
    "Meters": 1.0, "Kilometers": 1000.0, "Centimeters": 0.01, "Millimeters": 0.001,
    "Miles": 1609.34, "Yards": 0.9144, "Feet": 0.3048, "Inches": 0.0254,
}

WEIGHT_UNITS = {
    "Kilograms": 1000.0, "Grams": 1.0, "Metric Ton": 1000000.0,
    "Dram": 1.772, "Ounce": 28.35, "Pound": 453.59,
    "Stone": 6350.29, "Troy Ounce": 31.10, "Tola": 11.66,
}

TEMP_UNITS = ["Celsius", "Fahrenheit", "Kelvin"]

# Values are "megabytes per unit" (kept consistent so From/To conversion works)
DATA_UNITS = {
    "Bit": 0.000000125,
    "Nibble": 0.0000005,
    "Byte": 0.000001,
    "Kilobyte": 0.001,
    "Megabyte": 1.0,
    "Gigabyte": 1000.0,
    "Terabyte": 1000000.0,
    "Petabyte": 1000000000.0,
    "Exabyte": 1000000000000.0,
    "Zettabyte": 1000000000000000.0,
    "Yottabyte": 1000000000000000000.0,
}


class State(rx.State):
    mode: str = "Single Equation"

    # --- Single equation ---
    a1: str = "0"
    b1: str = "0"
    c1: str = "0"
    single_result: str = ""
    single_error: str = ""

    # --- Simultaneous ---
    a2: str = "0"
    b2: str = "0"
    c2: str = "0"
    d2: str = "0"
    e2: str = "0"
    f2: str = "0"
    sim_result: str = ""
    sim_error: str = ""
    plot_points: list[dict] = []
    intersection: dict = {}

    # --- Trig ---
    trig_func: str = "sine"
    trig_value: str = "0"
    trig_result: str = ""
    trig_error: str = ""

    # --- Quadratics ---
    quad_a: str = "1"
    quad_b: str = "0"
    quad_c: str = "0"
    quad_result: str = ""
    quad_info: str = ""
    quad_error: str = ""

    # --- Calculus ---
    calc_input: str = "x**2 + x*5"
    calc_deriv: str = ""
    calc_integ: str = ""
    calc_error: str = ""

    # --- Stats ---
    stats_raw: str = "0, 0"
    stats_mean: str = ""
    stats_median: str = ""
    stats_std: str = ""
    stats_min: str = ""
    stats_max: str = ""
    stats_len: str = ""
    stats_error: str = ""

    # --- Unit conversion ---
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

    def set_mode(self, mode: str):
        self.mode = mode

    # ---------- Single Equation ----------
    def solve_single(self):
        self.single_error = ""
        self.single_result = ""
        try:
            a = float(self.a1)
            b = float(self.b1)
            c = float(self.c1)
        except ValueError:
            self.single_error = "Please enter valid numbers."
            return
        if a == 0:
            self.single_error = "a cannot be 0"
            return
        x = (c - b) / a
        self.single_result = f"x = {round(x, 4)}"

    # ---------- Simultaneous ----------
    def solve_simultaneous(self):
        self.sim_error = ""
        self.sim_result = ""
        self.plot_points = []
        self.intersection = {}
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

        D = (a * e) - (b * d)
        if D == 0:
            self.sim_error = "No unique solution (lines are parallel or identical)."
            return

        x_res = ((c * e) - (b * f)) / D
        y_res = ((a * f) - (c * d)) / D
        self.sim_result = f"x = {round(x_res, 4)}, y = {round(y_res, 4)}"

        limit = max(abs(x_res), abs(y_res), 10) + 2
        x_vals = np.linspace(-limit, limit, 60)

        points = []
        if b != 0:
            for xv in x_vals:
                yv = (c - a * xv) / b
                points.append({"x": round(float(xv), 4), "line1": round(float(yv), 4)})
        else:
            # vertical line a*x = c -> x = c/a, skip plotting a curve
            points = [{"x": round(float(xv), 4), "line1": None} for xv in x_vals]

        self.plot_points = points
        self.intersection = {"x": round(x_res, 4), "y": round(y_res, 4)}

    # ---------- Trig ----------
    def solve_trig(self):
        self.trig_error = ""
        self.trig_result = ""
        try:
            value = float(self.trig_value)
        except ValueError:
            self.trig_error = "Please enter a valid number."
            return

        if self.trig_func == "sine":
            result = math.sin(math.radians(value))
            self.trig_result = str(round(result, 4))
        elif self.trig_func == "cosine":
            result = math.cos(math.radians(value))
            self.trig_result = str(round(result, 4))
        elif self.trig_func == "tangent":
            result = math.tan(math.radians(value))
            self.trig_result = str(round(result, 4))
        elif self.trig_func == "inverse sine":
            if -1 <= value <= 1:
                result_deg = math.degrees(math.asin(value))
                self.trig_result = str(round(result_deg, 4))
            else:
                self.trig_error = "Value must be between -1 and 1"
        elif self.trig_func == "inverse cosine":
            if -1 <= value <= 1:
                result_deg = math.degrees(math.acos(value))
                self.trig_result = str(round(result_deg, 4))
            else:
                self.trig_error = "Value must be between -1 and 1"
        elif self.trig_func == "inverse tangent":
            result_deg = math.degrees(math.atan(value))
            self.trig_result = str(round(result_deg, 4))

    # ---------- Quadratics ----------
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
            if b != 0:
                self.quad_result = f"Linear equation: x = {round(-c / b, 4)}"
                self.quad_info = "a = 0, so this is actually linear."
            else:
                self.quad_error = "a and b cannot both be 0."
            return

        discriminant = b ** 2 - 4 * a * c

        if discriminant < 0:
            real_part = round(-b / (2 * a), 4)
            imag_part = round((abs(discriminant) ** 0.5) / (2 * a), 4)
            self.quad_info = "The roots are complex."
            self.quad_result = f"x1 = {real_part} + {imag_part}i,  x2 = {real_part} - {imag_part}i"
        elif discriminant == 0:
            sol1 = round(-b / (2 * a), 4)
            self.quad_result = f"One answer: x = {sol1}"
        else:
            sqrt_disc = discriminant ** 0.5
            sol1 = round((-b + sqrt_disc) / (2 * a), 4)
            sol2 = round((-b - sqrt_disc) / (2 * a), 4)
            self.quad_result = f"x1 = {sol1}, x2 = {sol2}"

    # ---------- Calculus ----------
    def solve_calculus(self):
        self.calc_error = ""
        self.calc_deriv = ""
        self.calc_integ = ""
        user_input = self.calc_input.strip()
        if not user_input:
            return
        try:
            x = sp.symbols("x")
            expr = sp.sympify(user_input, locals={"x": x})
            deriv = sp.diff(expr, x)
            self.calc_deriv = sp.latex(deriv)
            integ = sp.integrate(expr, x)
            self.calc_integ = sp.latex(integ) + " + c"
        except Exception:
            self.calc_error = f"Could not parse '{user_input}'."

    # ---------- Stats ----------
    def solve_stats(self):
        self.stats_error = ""
        self.stats_mean = ""
        self.stats_median = ""
        self.stats_std = ""
        self.stats_min = ""
        self.stats_max = ""
        self.stats_len = ""
        try:
            data_list = [float(v.strip()) for v in self.stats_raw.split(",") if v.strip()]
        except ValueError:
            self.stats_error = "Please ensure you only use numbers and commas"
            return

        if len(data_list) == 0:
            self.stats_error = "Please enter data"
            return

        self.stats_mean = f"{np.mean(data_list):.2f}"
        self.stats_median = f"{np.median(data_list):.2f}"
        self.stats_std = f"{np.std(data_list):.2f}"
        self.stats_min = f"{np.min(data_list)}"
        self.stats_max = f"{np.max(data_list)}"
        self.stats_len = str(len(data_list))

    # ---------- Unit Conversion ----------
    def set_unit_category(self, category: str):
        self.unit_category = category
        self.unit_result = ""
        self.unit_error = ""

    def convert_length(self):
        self.unit_error = ""
        try:
            value = float(self.len_value)
            result = value * LENGTH_UNITS[self.len_from] / LENGTH_UNITS[self.len_to]
            self.unit_result = f"{value} {self.len_from} = {result:.4f} {self.len_to}"
        except ValueError:
            self.unit_error = "Please enter a valid number."

    def convert_weight(self):
        self.unit_error = ""
        try:
            value = float(self.wt_value)
            result = value * WEIGHT_UNITS[self.wt_from] / WEIGHT_UNITS[self.wt_to]
            self.unit_result = f"{value} {self.wt_from} = {result:.4f} {self.wt_to}"
        except ValueError:
            self.unit_error = "Please enter a valid number."

    def convert_temp(self):
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
            result = (celsius * 9 / 5) + 32
        else:
            result = celsius + 273.15

        self.unit_result = f"{value} {self.temp_from} = {result:.2f} {self.temp_to}"

    def convert_data(self):
        self.unit_error = ""
        try:
            value = float(self.data_value)
            result = value * DATA_UNITS[self.data_from] / DATA_UNITS[self.data_to]
            self.unit_result = f"{value} {self.data_from} = {result:.2f} {self.data_to}"
        except ValueError:
            self.unit_error = "Please enter a valid number."


def labeled_input(label: str, value, on_change) -> rx.Component:
    return rx.vstack(
        rx.text(label, size="2", color="gray"),
        rx.input(value=value, on_change=on_change, type="text"),
        spacing="1",
        width="100%",
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
        rx.heading("Solve ax+by=c and dx+ey=f", size="5"),
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
                rx.recharts.line_chart(
                    rx.recharts.line(data_key="line1", stroke="#2563eb", dot=False, name="Line 1"),
                    rx.recharts.x_axis(data_key="x", type_="number"),
                    rx.recharts.y_axis(type_="number"),
                    rx.recharts.reference_dot(
                        x=State.intersection["x"],
                        y=State.intersection["y"],
                        r=6,
                        fill="red",
                    ),
                    rx.recharts.legend(),
                    data=State.plot_points,
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
                ["sine", "cosine", "tangent", "inverse sine", "inverse cosine", "inverse tangent"],
                value=State.trig_func,
                on_change=State.set_trig_func,
            ),
            spacing="1",
            width="100%",
        ),
        labeled_input("Value (degrees for sin/cos/tan, ratio for inverse)", State.trig_value, State.set_trig_value),
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
        rx.heading("Solve ax^2 + bx + c = 0", size="5"),
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
        rx.callout("Use * for multiplication and ** for powers", color_scheme="blue"),
        labeled_input("Enter function", State.calc_input, State.set_calc_input),
        rx.button("Solve", on_click=State.solve_calculus, color_scheme="blue"),
        rx.cond(
            State.calc_error != "",
            rx.callout(State.calc_error, color_scheme="red"),
        ),
        rx.cond(
            State.calc_deriv != "",
            rx.vstack(
                rx.heading("The Derivative (f'(x))", size="4"),
                rx.katex("f'(x) = " + State.calc_deriv),
                rx.heading("The Integral (∫f(x) dx)", size="4"),
                rx.katex("\\int f(x)\\,dx = " + State.calc_integ),
                spacing="2",
                width="100%",
            ),
        ),
        spacing="4",
        width="100%",
    )


def stats() -> rx.Component:
    return rx.vstack(
        rx.heading("Statistics", size="5"),
        rx.text("Enter data separated by commas", color="gray"),
        rx.text_area(value=State.stats_raw, on_change=State.set_stats_raw, width="100%"),
        rx.button("Sort", on_click=State.solve_stats, color_scheme="blue"),
        rx.cond(
            State.stats_error != "",
            rx.callout(State.stats_error, color_scheme="red"),
        ),
        rx.cond(
            State.stats_mean != "",
            rx.vstack(
                rx.hstack(
                    rx.stat(rx.stat_label("Mean (Average)"), rx.stat_number(State.stats_mean)),
                    rx.stat(rx.stat_label("Median"), rx.stat_number(State.stats_median)),
                    rx.stat(rx.stat_label("Std Deviation"), rx.stat_number(State.stats_std)),
                    spacing="6",
                ),
                rx.hstack(
                    rx.stat(rx.stat_label("Minimum"), rx.stat_number(State.stats_min)),
                    rx.stat(rx.stat_label("Maximum"), rx.stat_number(State.stats_max)),
                    rx.stat(rx.stat_label("Length"), rx.stat_number(State.stats_len)),
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
                        rx.select(list(LENGTH_UNITS.keys()), value=State.len_from, on_change=State.set_len_from),
                        labeled_input("Value", State.len_value, State.set_len_value),
                        spacing="2",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("To:", size="2", color="gray"),
                        rx.select(list(LENGTH_UNITS.keys()), value=State.len_to, on_change=State.set_len_to),
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
                        rx.select(list(WEIGHT_UNITS.keys()), value=State.wt_from, on_change=State.set_wt_from),
                        labeled_input("Value", State.wt_value, State.set_wt_value),
                        spacing="2",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("To:", size="2", color="gray"),
                        rx.select(list(WEIGHT_UNITS.keys()), value=State.wt_to, on_change=State.set_wt_to),
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
                        rx.select(TEMP_UNITS, value=State.temp_from, on_change=State.set_temp_from),
                        labeled_input("Value", State.temp_value, State.set_temp_value),
                        spacing="2",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("To:", size="2", color="gray"),
                        rx.select(TEMP_UNITS, value=State.temp_to, on_change=State.set_temp_to),
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
                        rx.select(list(DATA_UNITS.keys()), value=State.data_from, on_change=State.set_data_from),
                        labeled_input("Value", State.data_value, State.set_data_value),
                        spacing="2",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("To:", size="2", color="gray"),
                        rx.select(list(DATA_UNITS.keys()), value=State.data_to, on_change=State.set_data_to),
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
