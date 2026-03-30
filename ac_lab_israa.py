# Virtual Physics Lab - AC Circuit
# Created by Israa Samara

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# الزمن
t = np.linspace(0, 0.1, 1000)

# القيم الابتدائية
Vmax = 10
f_init = 50
R_init = 10
L_init = 0.05
C_init = 0.0001

# دالة الحساب
def calculate(f, R, L, C):
    omega = 2 * np.pi * f
    XL = omega * L
    XC = 1 / (omega * C)
    Z = np.sqrt(R**2 + (XL - XC)**2)

    V = Vmax * np.sin(omega * t)
    I = (Vmax / Z) * np.sin(omega * t)

    return V, I

# رسم أولي
V, I = calculate(f_init, R_init, L_init, C_init)

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.35)

line_v, = plt.plot(t, V, label="Voltage")
line_i, = plt.plot(t, I, label="Current")

plt.legend()
plt.title("AC Virtual Lab - Israa Samara")

# Sliders
ax_freq = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_R = plt.axes([0.25, 0.2, 0.65, 0.03])
ax_L = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_C = plt.axes([0.25, 0.1, 0.65, 0.03])

s_freq = Slider(ax_freq, 'Frequency', 1, 200, valinit=f_init)
s_R = Slider(ax_R, 'Resistance', 1, 100, valinit=R_init)
s_L = Slider(ax_L, 'Inductance', 0.001, 0.1, valinit=L_init)
s_C = Slider(ax_C, 'Capacitance', 0.00001, 0.001, valinit=C_init)

# تحديث
def update(val):
    f = s_freq.val
    R = s_R.val
    L = s_L.val
    C = s_C.val

    V, I = calculate(f, R, L, C)

    line_v.set_ydata(V)
    line_i.set_ydata(I)

    fig.canvas.draw_idle()

s_freq.on_changed(update)
s_R.on_changed(update)
s_L.on_changed(update)
s_C.on_changed(update)

plt.show()