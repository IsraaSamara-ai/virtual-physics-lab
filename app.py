import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# إعداد الصفحة
st.set_page_config(page_title="معمل الفيزياء الافتراضي", layout="wide")
st.title("🔌 معمل الفيزياء الافتراضي - دوائر التيار المتردد والترانزستور")
st.markdown("### إعداد: إسراء سمارة")

# الشريط الجانبي للتحكم
st.sidebar.header("⚙️ إعدادات الدائرة")
circuit_type = st.sidebar.selectbox(
    "نوع الدائرة",
    ["دائرة RC (مقاومة - مكثف)", "دائرة RL (مقاومة - ملف)", "دائرة RLC (رنان)", "ترانزستور BJT"]
)

# متغيرات مشتركة
R = st.sidebar.slider("المقاومة R (Ω)", 100, 10000, 1000, step=100)
C = st.sidebar.slider("السعة C (µF)", 0.1, 100.0, 10.0) * 1e-6
L = st.sidebar.slider("المحاثة L (mH)", 1, 100, 10) * 1e-3

f = np.linspace(10, 1000, 500)
w = 2 * np.pi * f

# الدوائر
if circuit_type.startswith("دائرة RC"):
    st.header("📈 دائرة RC - استجابة التردد")
    Xc = 1 / (w * C)
    Z = np.sqrt(R**2 + Xc**2)
    phase = -np.arctan(Xc / R)
    gain = 1 / np.sqrt(1 + (w * R * C)**2)

    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots()
        ax.semilogx(f, 20 * np.log10(gain))
        ax.set_xlabel("التردد (Hz)")
        ax.set_ylabel("الكسب (dB)")
        ax.grid(True)
        st.pyplot(fig)
    with col2:
        fig, ax = plt.subplots()
        ax.semilogx(f, np.degrees(phase))
        ax.set_xlabel("التردد (Hz)")
        ax.set_ylabel("زاوية الطور (درجة)")
        ax.grid(True)
        st.pyplot(fig)

elif circuit_type.startswith("دائرة RL"):
    st.header("📈 دائرة RL - استجابة التردد")
    XL = w * L
    Z = np.sqrt(R**2 + XL**2)
    phase = np.arctan(XL / R)
    gain = 1 / np.sqrt(1 + (w * L / R)**2)

    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots()
        ax.semilogx(f, 20 * np.log10(gain))
        ax.set_xlabel("التردد (Hz)")
        ax.set_ylabel("الكسب (dB)")
        ax.grid(True)
        st.pyplot(fig)
    with col2:
        fig, ax = plt.subplots()
        ax.semilogx(f, np.degrees(phase))
        ax.set_xlabel("التردد (Hz)")
        ax.set_ylabel("زاوية الطور (درجة)")
        ax.grid(True)
        st.pyplot(fig)

elif circuit_type.startswith("دائرة RLC"):
    st.header("📈 دائرة RLC متسلسلة")
    XL = w * L
    Xc = 1 / (w * C)
    Z = np.sqrt(R**2 + (XL - Xc)**2)
    phase = np.arctan2((XL - Xc), R)
    I_norm = 1 / Z
    I_norm = I_norm / np.max(I_norm)

    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots()
        ax.semilogx(f, 20 * np.log10(I_norm))
        ax.set_xlabel("التردد (Hz)")
        ax.set_ylabel("التيار الطبيعي (dB)")
        ax.grid(True)
        ax.set_title("منحنى الرنين")
        st.pyplot(fig)
    with col2:
        fig, ax = plt.subplots()
        ax.semilogx(f, np.degrees(phase))
        ax.set_xlabel("التردد (Hz)")
        ax.set_ylabel("زاوية الطور (درجة)")
        ax.grid(True)
        st.pyplot(fig)

    fo = 1 / (2 * np.pi * np.sqrt(L * C))
    st.info(f"**تردد الرنين النظري:** {fo:.1f} Hz")

else:  # ترانزستور
    st.header("🔬 خصائص الترانزستور ثنائي القطب (BJT) - النوع NPN")
    Vce = np.linspace(0, 10, 100)
    IB_values = [10, 20, 50, 100, 150]  # µA
    beta = 100

    fig, ax = plt.subplots(figsize=(8, 6))
    for IB in IB_values:
        IB_A = IB * 1e-6
        Ic = beta * IB_A * np.ones_like(Vce)
        saturation = np.minimum(Vce / 0.5, 1)
        Ic = Ic * saturation
        ax.plot(Vce, Ic * 1000, label=f"Iᵦ = {IB} µA", linewidth=2)
    ax.set_xlabel("VCE (V)")
    ax.set_ylabel("IC (mA)")
    ax.set_title("منحنيات خرج الترانزستور (NPN)")
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    st.pyplot(fig)

    st.markdown("""
    **ملاحظات تعليمية:**  
    - **منطقة القطع:** IC = 0 (عند VCE صغير جداً و IB = 0).  
    - **المنطقة الفعالة (Active):** IC = β × IB، منحنى مستقر.  
    - **منطقة الإشباع (Saturation):** IC لا يزيد رغم زيادة IB (يستخدم في التبديل).
    """)

# رسم الدائرة
st.header("⚡ مخطط الدائرة الكهربائية")
def draw_circuit(ax, circuit_type):
    ax.clear()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    if circuit_type.startswith("دائرة RC"):
        ax.add_patch(Rectangle((0.5, 2.5), 0.8, 1, fill=None, edgecolor='black'))
        ax.text(0.9, 3, "V", fontsize=12)
        ax.plot([1.5, 2.5], [3, 3], 'k-')
        ax.add_patch(Rectangle((2, 2.5), 0.5, 1, fill=None, edgecolor='black'))
        ax.text(2.25, 3, "R", fontsize=12)
        ax.plot([3, 4], [3, 3], 'k-')
        ax.plot([4, 4.5], [2.5, 3.5], 'k-')
        ax.plot([4.5, 5], [3, 3], 'k-')
        ax.text(4.2, 2.5, "C", fontsize=12)
        ax.plot([5, 5.5], [3, 3], 'k-')
        ax.plot([5.25, 5.75], [3, 2.5], 'k-')
        ax.plot([5.25, 5.75], [3, 3.5], 'k-')
        ax.text(6, 3, "GND", fontsize=10)

    elif circuit_type.startswith("دائرة RL"):
        ax.add_patch(Rectangle((0.5, 2.5), 0.8, 1, fill=None, edgecolor='black'))
        ax.text(0.9, 3, "V", fontsize=12)
        ax.plot([1.5, 2.5], [3, 3], 'k-')
        ax.add_patch(Rectangle((2, 2.5), 0.5, 1, fill=None, edgecolor='black'))
        ax.text(2.25, 3, "R", fontsize=12)
        ax.plot([3, 3.5], [3, 3], 'k-')
        for i in range(3):
            ax.plot([3.5 + i*0.2, 3.7 + i*0.2], [2.7, 3.3], 'k-')
            ax.plot([3.5 + i*0.2, 3.7 + i*0.2], [3.3, 2.7], 'k-')
        ax.plot([4.1, 5], [3, 3], 'k-')
        ax.text(4, 2.5, "L", fontsize=12)
        ax.plot([5, 5.5], [3, 3], 'k-')
        ax.plot([5.25, 5.75], [3, 2.5], 'k-')
        ax.plot([5.25, 5.75], [3, 3.5], 'k-')

    elif circuit_type.startswith("دائرة RLC"):
        ax.add_patch(Rectangle((0.5, 2.5), 0.8, 1, fill=None, edgecolor='black'))
        ax.text(0.9, 3, "V", fontsize=12)
        ax.plot([1.5, 2.5], [3, 3], 'k-')
        ax.add_patch(Rectangle((2, 2.5), 0.5, 1, fill=None, edgecolor='black'))
        ax.text(2.25, 3, "R", fontsize=12)
        ax.plot([3, 3.5], [3, 3], 'k-')
        for i in range(3):
            ax.plot([3.5 + i*0.2, 3.7 + i*0.2], [2.7, 3.3], 'k-')
            ax.plot([3.5 + i*0.2, 3.7 + i*0.2], [3.3, 2.7], 'k-')
        ax.plot([4.1, 4.5], [3, 3], 'k-')
        ax.plot([4.5, 5], [3, 3], 'k-')
        ax.plot([5, 5.5], [2.5, 3.5], 'k-')
        ax.plot([5.5, 6], [3, 3], 'k-')
        ax.text(5.2, 2.5, "C", fontsize=12)
        ax.plot([6, 6.5], [3, 3], 'k-')
        ax.plot([6.25, 6.75], [3, 2.5], 'k-')
        ax.plot([6.25, 6.75], [3, 3.5], 'k-')

    else:  # ترانزستور
        ax.add_patch(Rectangle((0.5, 2.5), 0.8, 1, fill=None, edgecolor='black'))
        ax.text(0.9, 3, "Vcc", fontsize=10)
        ax.plot([1.5, 3], [3, 3], 'k-')
        ax.add_patch(Rectangle((2.5, 2.5), 0.5, 1, fill=None, edgecolor='black'))
        ax.text(2.75, 3, "Rc", fontsize=10)
        ax.plot([3, 4], [3, 3], 'k-')
        ax.plot([3.5, 3.5], [2, 3.5], 'k-')
        ax.plot([3.5, 4], [3.5, 3.5], 'k-')
        ax.plot([3.5, 3], [3.5, 3], 'k-')
        ax.plot([3, 3.5], [3, 3.5], 'k-')
        ax.text(3.2, 3.7, "Q1", fontsize=12)
        ax.plot([3.5, 4], [2, 2], 'k-')
        ax.plot([3.75, 4.25], [2, 1.5], 'k-')
        ax.plot([3.75, 4.25], [2, 2.5], 'k-')
        ax.text(4.5, 2, "GND", fontsize=10)

fig_circ, ax_circ = plt.subplots(figsize=(8, 4))
draw_circuit(ax_circ, circuit_type)
st.pyplot(fig_circ)

st.markdown("---")
st.markdown("**📘 ملاحظة:** استخدم القوائم الجانبية لتغيير قيم المكونات وشاهد تأثيرها على المخططات والرسوم البيانية.")