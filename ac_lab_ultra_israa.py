# AC Virtual Lab ULTRA
# Created by Israa Samara

import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import winsound

# -----------------------
# الحساب
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
    I = (10 / Z) * np.sin(omega * t - np.arctan((XL - XC)/R))

    phi = np.degrees(np.arctan((XL - XC)/R))

    # رسم
    ax.clear()
    ax.plot(t, V, label="Voltage", linewidth=2)
    ax.plot(t, I, label="Current", linewidth=2)

    ax.legend()
    ax.set_title("AC Circuit Lab - Israa Samara")

    # لون ديناميكي
    if abs(XL - XC) < 0.5:
        ax.set_facecolor("#ffe6e6")
        winsound.Beep(1000, 200)
        resonance.set("🔥 Resonance!")
    elif XL > XC:
        ax.set_facecolor("#e6f0ff")
        resonance.set("Inductive Circuit")
    else:
        ax.set_facecolor("#e6ffe6")
        resonance.set("Capacitive Circuit")

    canvas.draw()

    info.set(f"XL={XL:.2f} | XC={XC:.2f} | Z={Z:.2f} | Phase={phi:.2f}°")

# -----------------------
# حفظ صورة
# -----------------------
def save_plot():
    fig.savefig("experiment_result.png")
    messagebox.showinfo("Saved", "Image saved successfully!")

# -----------------------
# وضع الطالب
# -----------------------
def student_mode():
    messagebox.showinfo("Student Mode",
        "🔬 جرّبي:\n"
        "- زيادة التردد\n"
        "- ملاحظة الرنين\n"
        "- مقارنة التيار والجهد")

# -----------------------
# واجهة
# -----------------------
root = tk.Tk()
root.title("Virtual Physics Lab ULTRA - Israa Samara")
root.geometry("1000x700")

freq = tk.DoubleVar(value=50)
res = tk.DoubleVar(value=10)
ind = tk.DoubleVar(value=0.05)
cap = tk.DoubleVar(value=0.0001)

# Sliders
for text, var, frm, to in [
    ("Frequency", freq, 1, 200),
    ("Resistance", res, 1, 100),
    ("Inductance", ind, 0.001, 0.1),
    ("Capacitance", cap, 0.00001, 0.001)
]:
    ttk.Label(root, text=text).pack()
    ttk.Scale(root, from_=frm, to=to, variable=var, command=lambda x: calculate()).pack()

info = tk.StringVar()
ttk.Label(root, textvariable=info, foreground="blue").pack()

resonance = tk.StringVar()
ttk.Label(root, textvariable=resonance, foreground="red").pack()

# الرسم
fig, ax = plt.subplots(figsize=(6,4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# أزرار
ttk.Button(root, text="Update", command=calculate).pack()
ttk.Button(root, text="Save Image", command=save_plot).pack()
ttk.Button(root, text="Student Mode", command=student_mode).pack()

calculate()
root.mainloop()