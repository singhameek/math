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