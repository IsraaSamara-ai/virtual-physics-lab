# AC Virtual Lab PRO
# Created by Israa Samara

import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# -----------------------
# الحسابات
# -----------------------
def calculate():
    f = freq.get()
    R = res.get()
    L = ind.get()
    C = cap.get()

    omega = 2 * np.pi * f
    XL = omega * L
    XC = 1 / (omega * C)
    Z = np.sqrt(R**2 + (XL - XC)**2)

    t = np.linspace(0, 0.1, 1000)
    V = 10 * np.sin(omega * t)
    I = (10 / Z) * np.sin(omega * t)

    # تحديث الرسم
    ax.clear()
    ax.plot(t, V, label="Voltage")
    ax.plot(t, I, label="Current")
    ax.legend()
    ax.set_title("AC Circuit - Israa Samara")

    canvas.draw()

    # عرض معلومات
    info.set(f"XL={XL:.2f} | XC={XC:.2f} | Z={Z:.2f}")

    # كشف الرنين
    if abs(XL - XC) < 0.5:
        resonance.set("🔥 Resonance State")
    else:
        resonance.set("")

# -----------------------
# واجهة البرنامج
# -----------------------
root = tk.Tk()
root.title("Virtual Physics Lab - Israa Samara")
root.geometry("900x600")

# Sliders
freq = tk.DoubleVar(value=50)
res = tk.DoubleVar(value=10)
ind = tk.DoubleVar(value=0.05)
cap = tk.DoubleVar(value=0.0001)

ttk.Label(root, text="Frequency").pack()
ttk.Scale(root, from_=1, to=200, variable=freq, command=lambda x: calculate()).pack()

ttk.Label(root, text="Resistance").pack()
ttk.Scale(root, from_=1, to=100, variable=res, command=lambda x: calculate()).pack()

ttk.Label(root, text="Inductance").pack()
ttk.Scale(root, from_=0.001, to=0.1, variable=ind, command=lambda x: calculate()).pack()

ttk.Label(root, text="Capacitance").pack()
ttk.Scale(root, from_=0.00001, to=0.001, variable=cap, command=lambda x: calculate()).pack()

# معلومات
info = tk.StringVar()
ttk.Label(root, textvariable=info, foreground="blue").pack()

resonance = tk.StringVar()
ttk.Label(root, textvariable=resonance, foreground="red").pack()

# الرسم
fig, ax = plt.subplots(figsize=(5, 3))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# زر تحديث
ttk.Button(root, text="Update", command=calculate).pack()

# تشغيل أولي
calculate()

root.mainloop()