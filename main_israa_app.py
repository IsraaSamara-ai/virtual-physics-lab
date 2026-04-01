import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("⚡ مختبر إسراء الفيزيائي")

tab1, tab2 = st.tabs(["AC", "Diode"])

with tab1:
    A = st.slider("Amplitude", 0.1, 10.0, 1.0)
    f = st.slider("Frequency", 1.0, 100.0, 5.0)

    t = np.linspace(0, 1, 1000)
    y = A * np.sin(2 * np.pi * f * t)

    fig, ax = plt.subplots()
    ax.plot(t, y)
    ax.grid()

    st.pyplot(fig)

with tab2:
    V = st.slider("Voltage", 0.0, 5.0, 0.5)

    if V > 0.7:
        st.success("يمر التيار")
    else:
        st.error("لا يمر التيار")