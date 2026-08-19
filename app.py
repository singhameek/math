import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
import sympy as sp
import pandas as pd
from scipy import stats


st.set_page_config(layout="wide")
st.set_page_config(page_title="Math", page_icon="+")
st.title("Math Solver")

mode = st.sidebar.selection("Select Mode", ["Single Equation", "Simultaneous", "Trig", "Quadratics", "Calculus", "Stats", "Unit Conversion"])

if mode == "Single Equation":
    st.header("Solve $ax +b = c$")
    a = st.number_input("Value for a", value=0.0, key="a1")
    b = st.number_input("Value for b", value=0.0, key="b1")
    c = st.number_input("Value for c", value=0.0, key="b1")

    if st.button("Solve", key="btn_single"):
        if a == 0:
            st.error("a cannot be 0")
        else:
            x=(c-b)/a
            st.success(f"Result: $x = {round(x,4)}")

elif mode == "Simultaneous":
    st.header("Solve $ax+by=c$ and $dx+ey=f$")

    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("a", value=0.0, key="a2")
        b = st.number_input("b", value = 0.0, key="b2")
        c = st.number_input("c", value =0.0, key="c2")

    with col2:
        d = st.number_input("d", value=0.0, key="d2")
        e = st.number_input("e", value=0.0, key="e2")
        f = st.number_input("f", value=0.0, key ="f2")

    if st.button("Solve", key="btn_sim"):
        D = (a*e)-(b*d)

        if D != 0:
            x_res = ((c*e)-(b*f))/D
            y_res = ((a*f)-(c*d))/D
            st.success(f"Results: $x = {round(x_res, 4)}$, $y = {round(y_res, 4)}$")

            fig, ax = plt.subplots(figsizw=(8,8))
            limit = max(abs(x_res), abs(y_res), 10) + 2
            x_vals = np.linspace(-limit, limit, 400)

            ax.spines['left'].set_position('zero')
            ax.spines['bottom'].set_position('zero')
            ax.spines['right'].set_color('none')
            ax.spines['top'].set_color('none')


            if b != 0:
                y1 = (c-a*x_vals)/b
                ax.plot(x_vals, y1, label=f'Line 1: {a}x + {b}y = {c}')
            else:
                ax.axvline(x=c/a, color='blue', label=f'line 1: {a}x = {c}')

            ax.plot(x_res, y_res, 'ro', markersize=10, label='Intersection', zorder=5)

            ax.set_xlim(-limit, limit)
            ax.set_ylim(-limit, limit)
            ax.set_aspect('equal')
            ax.grid(True, linestyle='--', alpha = 0.5)
            ax.legend(loc='upper right')

            st.pyplot(fig)

elif mode == "Trig":
    st.header("Solve Trig Functions")
    trigfunc = st.selectbox("Choose function", ["sine", "cosine", "tangent", "inverse sine", "inverse cosine", "inverse tangent"])
    value = st.number_input("Value (Degrees for sin/cos/tan, ratio for inverse)", value = 0.0, key = "value")

    if st.button("Solve", key = "btn_trig"):
        if trigfunc == "sine":
            result = math.sin(math.radians(value))
            st.success(f"Result: {round(result, 4)}")

        elif trigfunc == "cosine":
            result = math.cos(math.radians(value))
            st.success(f"Result: {round(result, 4)}")

        elif trigfunc == "tangent":
            result = math.tan(math.radians(value))
            st.success(f"Result: {round(result, 4)}")

        elif trigfunc == "inverse sine":
            if -1<= value <=1:
                result_deg = math.degrees(math.acos(value))
                st.success(f"Result: {round(result_deg, 4)}")
            else:
                st.error("Value must be between 1 and -1")

        elif trigfunc == "inverse cosine":
            if -1<= value <=1:
                result_deg = math.degrees(math.acos(value))
                st.success(f"Result: {round(result_deg, 4)}")
            else:
                st.error("Value must be between 1 and -1")

        elif trigfunc == "inverse tangent":
            result_deg = math.degrees(math.atan(value))
            st.success(f"Result: {round(result_deg, 4)}")

        