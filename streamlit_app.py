# streamlit_app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="AC Virtual Lab ULTRA", layout="wide")

st.title("⚡ AC Virtual Lab ULTRA")
st.caption("Created by Israa Samara")

# Sliders for user inputs
col1, col2, col3, col4 = st.columns(4)
with col1:
    f = st.slider("Frequency (Hz)", 1.0, 200.0, 50.0, 0.1)
with col2:
    R = st.slider("Resistance (Ω)", 1.0, 100.0, 10.0, 0.1)
with col3:
    L = st.slider("Inductance (H)", 0.001, 0.1, 0.05, 0.001)
with col4:
    C = st.slider("Capacitance (F)", 0.00001, 0.001, 0.0001, 0.00001, format="%.5f")

# Compute circuit parameters
omega = 2 * np.pi * f
XL = omega * L
XC = 1 / (omega * C)
Z = np.sqrt(R**2 + (XL - XC)**2)
phase_deg = np.degrees(np.arctan((XL - XC) / R)) if R != 0 else 90.0

# Time vector for plotting (0 to 0.1 s)
t = np.linspace(0, 0.1, 1000)
V = 10 * np.sin(omega * t)
I = (10 / Z) * np.sin(omega * t - np.arctan((XL - XC) / R))

# Create figure
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(t, V, label="Voltage (V)", linewidth=2)
ax.plot(t, I, label="Current (A)", linewidth=2)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.legend()
ax.grid(True)

# Dynamic background color based on circuit behavior
if abs(XL - XC) < 0.5:
    ax.set_facecolor("#ffe6e6")
    resonance_msg = "🔥 Resonance!"
elif XL > XC:
    ax.set_facecolor("#e6f0ff")
    resonance_msg = "Inductive Circuit"
else:
    ax.set_facecolor("#e6ffe6")
    resonance_msg = "Capacitive Circuit"

ax.set_title(f"AC Circuit: {resonance_msg}")

# Show plot in Streamlit
st.pyplot(fig)

# Display circuit info
info_text = f"""
**XL** = {XL:.2f} Ω | **XC** = {XC:.2f} Ω | **Z** = {Z:.2f} Ω  
**Phase Shift** = {phase_deg:.2f}° | **Resonance** = {resonance_msg}
"""
st.markdown(info_text)

# Buttons for extra features
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("💾 Save Plot"):
        fig.savefig("ac_lab_plot.png")
        st.success("Plot saved as 'ac_lab_plot.png'")
with col_btn2:
    if st.button("🧪 Student Mode"):
        st.info("🔬 **Student Mode:** Experiment with frequency, inductance, and capacitance. Observe resonance when XL ≈ XC and note the phase relationship between voltage and current.")

# Footer
st.caption("Virtual Physics Lab - AC Circuit Simulator")
