import streamlit as st
import math
import base64
from datetime import datetime
import pytz

# 1. Page Configuration
st.set_page_config(page_title="Britus International School Bahrain", layout="wide")

# 2. Function to load your local background image (my_background.jpg)
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Try to load your background file
try:
    bin_str = get_base64('my_background.jpg')
    bg_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(bg_style, unsafe_allow_html=True)
except:
    st.markdown("<style>.stApp {background-color: #f0f2f6;}</style>", unsafe_allow_html=True)

# 3. Custom Styling for the Calculator & Clock
st.markdown("""
    <style>
    .calculator-container {
        background-color: rgba(255, 255, 255, 0.97);
        padding: 35px;
        border-radius: 25px;
        border: 5px solid #800000; /* Britus Maroon */
        box-shadow: 0px 15px 35px rgba(0,0,0,0.5);
        margin-top: 10px;
    }
    .clock-style {
        background-color: #002147; /* Britus Dark Blue */
        color: white;
        padding: 12px 25px;
        border-radius: 50px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
        border: 2px solid white;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. Top Banner (britus_banner.png)
try:
    st.image("britus_banner.png", use_container_width=True)
except:
    st.error("Missing 'britus_banner.png' in your GitHub folder.")

# 5. Bahrain Clock
bahrain_tz = pytz.timezone('Asia/Bahrain')
now = datetime.now(bahrain_tz)
st.markdown(f"<div class='clock-style'>🕒 Bahrain Time: {now.strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# 6. Calculator Content
st.markdown('<div class="calculator-container">', unsafe_allow_html=True)
st.markdown("<h2 style='color:#002147; text-align:center;'>🧪 Chemical Kinetics: Rate Law Determinator</h2>", unsafe_allow_html=True)
st.write("---")

cols = st.columns(4)
trials = []
for i, col in enumerate(cols, 1):
    with col:
        st.markdown(f"### Trial {i}")
        a = st.number_input(f"Initial [A] (M)", key=f"a{i}", format="%.4e", value=0.1)
        b = st.number_input(f"Initial [B] (M)", key=f"b{i}", format="%.4e", value=0.1)
        r = st.number_input(f"Initial Rate", key=f"r{i}", format="%.4e", value=0.001)
        trials.append({'a': a, 'b': b, 'rate': r})

if st.button("Calculate Reaction Order & k"):
    m, n = None, None
    
    # Math Logic to find m and n
    for i in range(4):
        for j in range(4):
            if i != j and trials[i]['b'] == trials[j]['b'] and trials[i]['a'] != trials[j]['a']:
                m = round(math.log(trials[j]['rate'] / trials[i]['rate']) / math.log(trials[j]['a'] / trials[i]['a']))
                break
        if m is not None: break

    for i in range(4):
        for j in range(4):
            if i != j and trials[i]['a'] == trials[j]['a'] and trials[i]['b'] != trials[j]['b']:
                n = round(math.log(trials[j]['rate'] / trials[i]['rate']) / math.log(trials[j]['b'] / trials[i]['b']))
                break
        if n is not None: break

    if m is not None and n is not None:
        st.balloons()
        overall = m + n
        k = trials[3]['rate'] / ((trials[3]['a']**m) * (trials[3]['b']**n))
        units = {0: "M/s", 1: "s⁻¹", 2: "M⁻¹s⁻¹", 3: "M⁻²s⁻¹"}
        unit = units.get(overall, f"M^{1-overall}s⁻¹")

        st.success(f"Analysis Complete! Order A: {m} | Order B: {n} | Overall: {overall}")
        st.info(f"Rate Constant (k): {k:.4e} {unit}")
        st.latex(rf"Rate = {k:.4e} \ {unit} \ [A]^{{{m}}} [B]^{{{n}}}")
    else:
        st.error("Error: Check your concentration data for constant values.")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white; margin-top: 15px;'><b>Learning Without Limits - Science Department</b></p>", unsafe_allow_html=True)
