import streamlit as st
import math
import base64
from datetime import datetime
import pytz

# 1. Page Configuration
st.set_page_config(page_title="Britus International School Bahrain", layout="wide")

# 2. Function to load your local background image (my_background.jpg)
def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

# Apply Background Styling
bin_str = get_base64('my_background.jpg')
if bin_str:
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
        """, unsafe_allow_html=True)

# 3. White Font & High-Contrast CSS
st.markdown("""
    <style>
    /* Main container box with a darker tint to make white text pop */
    .calculator-container {
        background-color: rgba(0, 33, 71, 0.8); /* Britus Navy with transparency */
        padding: 40px;
        border-radius: 25px;
        border: 4px solid #800000; /* Britus Maroon */
        box-shadow: 0px 15px 35px rgba(0,0,0,0.7);
        margin-top: 10px;
    }
    
    /* FORCE WHITE FONT EVERYWHERE */
    h1, h2, h3, p, span, label, .stMarkdown {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    /* Style the Bahrain Clock */
    .clock-style {
        background-color: #800000;
        color: white;
        padding: 12px 25px;
        border-radius: 50px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 15px;
        border: 2px solid white;
    }

    /* Keep Input Boxes readable (Black text inside white boxes) */
    .stNumberInput input {
        color: black !important;
        background-color: white !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. Top School Banner
try:
    st.image("britus_banner.png", use_container_width=True)
except:
    st.warning("Banner 'britus_banner.png' not found. Please upload it to GitHub.")

# 5. Bahrain Clock
bahrain_tz = pytz.timezone('Asia/Bahrain')
now = datetime.now(bahrain_tz)
st.markdown(f"<div class='clock-style'>🕒 Bahrain Time: {now.strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# 6. Calculator Logic
st.markdown('<div class="calculator-container">', unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;'>🧪 Chemical Kinetics: Rate Law Determinator</h2>", unsafe_allow_html=True)
st.write("Enter your experimental data below. Scientific notation (e.g., **1.5e-3**) is supported.")

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
    
    # Calculation Logic
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

        st.success(f"Analysis Complete!")
        st.write(f"**Order of A:** {m} | **Order of B:** {n}")
        st.info(f"Rate Constant (k): {k:.4e} {unit}")
        st.latex(rf"Rate = {k:.4e} \ {unit} \ [A]^{{{m}}} [B]^{{{n}}}")
    else:
        st.error("Check data: Could not find constant concentrations between trials.")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-top: 20px;'><b>Learning Without Limits - Science Department</b></p>", unsafe_allow_html=True)
