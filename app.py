import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# إعداد الصفحة
st.set_page_config(page_title="AC Lab - Israa Samara", layout="wide")

# ثيم داكن
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at center, #0f172a, #020617);
    color: white;
}
h1, h2 {
    color: #38bdf8;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# عنوان
st.title("⚡ AC Circuit Interactive Lab")
st.write("By Israa Samara")

# تحكم من اليسار
st.sidebar.header("🎮 التحكم")

f = st.sidebar.slider("Frequency", 1, 200, 50)
R = st.sidebar.slider("Resistance", 1, 100, 10)
L = st.sidebar.slider("Inductance", 0.001, 0.1, 0.05)
C = st.sidebar.slider("Capacitance", 0.00001, 0.001, 0.0001)

# حسابات
t = np.linspace(0, 0.1, 1000)
omega = 2 * np.pi * f

XL = omega * L
XC = 1 / (omega * C)
Z = np.sqrt(R**2 + (XL - XC)**2)

V = 10 * np.sin(omega * t)
phi = np.arctan((XL - XC) / R)
I = (10 / Z) * np.sin(omega * t - phi)

# رسم
fig, ax = plt.subplots()

ax.plot(t, V, label="Voltage")
ax.plot(t, I, linestyle="dashed", label="Current")

ax.legend()
ax.set_title("Voltage vs Current")

st.pyplot(fig)

# شرح
st.subheader("🧠 التحليل")

if XL > XC:
    st.success("⚡ الدارة حثية — التيار متأخر")
elif XC > XL:
    st.warning("⚡ الدارة سعوية — التيار متقدم")
else:
    st.info("🔥 رنين")

st.write(f"زاوية الطور: {np.degrees(phi):.2f}°")