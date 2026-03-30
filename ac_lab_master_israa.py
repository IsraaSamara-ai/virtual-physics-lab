# AC Virtual Lab MASTER
# Created by Israa Samara

import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import cv2

# -----------------------
# القيم
# -----------------------
freq = 50
R = 10
L = 0.05
C = 0.0001

t = np.linspace(0, 0.1, 1000)

# -----------------------
# إنشاء نافذة
# -----------------------
root = tk.Tk()
root.title("AC Lab MASTER - Israa Samara")
root.geometry("1100x700")

# -----------------------
# الرسم
# -----------------------
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6,6))

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# -----------------------
# حساب
# -----------------------
def compute():
    global freq, R, L, C
    omega = 2*np.pi*freq

    XL = omega*L
    XC = 1/(omega*C)
    Z = np.sqrt(R**2 + (XL-XC)**2)

    V = 10*np.sin(omega*t)
    phi = np.arctan((XL-XC)/R)
    I = (10/Z)*np.sin(omega*t - phi)

    return V, I, phi, XL, XC

# -----------------------
# رسم الدارة
# -----------------------
def draw_circuit(e_pos):
    ax2.clear()

    # رسم الأسلاك
    ax2.plot([0,10],[0,0], linewidth=3)
    
    # إلكترونات (نقاط متحركة)
    x = (e_pos % 10)
    ax2.scatter(x, 0, s=100)

    ax2.set_xlim(0,10)
    ax2.set_ylim(-1,1)
    ax2.set_title("Electron Motion in Circuit")
    ax2.axis('off')

# -----------------------
# التحديث (أنيميشن)
# -----------------------
frames = []
def update(frame):
    V, I, phi, XL, XC = compute()

    # رسم الموجات
    ax1.clear()
    ax1.plot(t, V, label="Voltage")
    ax1.plot(t, I, label="Current")
    ax1.legend()
    ax1.set_title(f"Phase Difference = {np.degrees(phi):.2f}°")

    # رسم الإلكترونات
    draw_circuit(frame)

    # حفظ إطار للفيديو
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    frames.append(image)

# -----------------------
# تشغيل الأنيميشن
# -----------------------
ani = FuncAnimation(fig, update, frames=100, interval=50)

# -----------------------
# حفظ فيديو
# -----------------------
def save_video():
    height, width, _ = frames[0].shape
    out = cv2.VideoWriter("ac_experiment.mp4",
                          cv2.VideoWriter_fourcc(*'mp4v'),
                          20, (width, height))

    for f in frames:
        out.write(f)

    out.release()
    print("Video saved!")

# -----------------------
# تحكم
# -----------------------
def update_values(val):
    global freq, R, L, C
    freq = s_freq.get()
    R = s_R.get()
    L = s_L.get()
    C = s_C.get()

# Sliders
s_freq = tk.Scale(root, from_=1, to=200, orient='horizontal', label="Frequency", command=update_values)
s_freq.set(50)
s_freq.pack()

s_R = tk.Scale(root, from_=1, to=100, orient='horizontal', label="Resistance", command=update_values)
s_R.set(10)
s_R.pack()

s_L = tk.Scale(root, from_=0.001, to=0.1, resolution=0.001, orient='horizontal', label="Inductance", command=update_values)
s_L.set(0.05)
s_L.pack()

s_C = tk.Scale(root, from_=0.00001, to=0.001, resolution=0.00001, orient='horizontal', label="Capacitance", command=update_values)
s_C.set(0.0001)
s_C.pack()

# زر حفظ فيديو
ttk.Button(root, text="Save Video", command=save_video).pack()

canvas.draw()
root.mainloop()