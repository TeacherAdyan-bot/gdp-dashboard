import streamlit as st
import math
import base64
from datetime import datetime
import pytz

# 1. Page Config
st.set_page_config(page_title="Britus International School Bahrain", layout="wide")

# 2. Background Image Loader
def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except: return None

bin_str = get_base64('my_background.jpg')

# 3. THE "FORCE WHITE" CSS
# This targets every possible text element in Streamlit and turns it white.
st.markdown(f"""
    <style>
    /* 1. The Background */
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str if bin_str else ""}");
        background-size: cover;
        background-attachment: fixed;
    }}

    /* 2. FORCE WHITE COLOR ON EVERYTHING */
    /* Targetting headers, paragraphs, labels, and general text */
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, h1, h2, h3, p, span, label {{
        color: white !important;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.8) !important;
    }}

    /* 3. The Central Container Box */
    .main-box {{
        background-color: rgba(0, 33, 71, 0.85); /* Dark Navy Transparent */
        padding: 50px;
        border-radius: 30px;
        border: 5px solid #800000; /* Britus Maroon */
        box-shadow: 0px 15px 40px rgba(0,0,0,0.7);
        text-align: center;
        margin-bottom: 20px;
    }}

    /* 4. Clock Styling */
    .clock-style {{
        background-color: #800000;
        color: white;
        padding: 10px 25px;
        border-radius: 50px;
        font-weight: bold;
        display: inline-block;
        border: 2px solid white;
        margin-bottom: 20px;
    }}

    /* 5. Keep inputs readable (Black text on white background) */
    input {{
        color: black !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. Top Banner & Clock
try:
    st.image("britus_banner.png", use_container_width=True)
except:
    st.warning("Upload 'britus_banner.png' to GitHub to see the logo.")

bahrain_tz = pytz.timezone('Asia/Bahrain')
st.markdown(f"<div class='clock-style'>🕒 {datetime.now(bahrain_tz).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# 5. THE CONTENT BOX (Title is now INSIDE)
st.markdown('<div class="main-box">', unsafe_allow_html=True)

# Centered White Title
st.markdown("<h1 style='text-align: center; color: white;'>🧪 Chemical Kinetics: Rate Law Determinator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white;'>Enter experimental data to calculate reaction orders (m, n) and rate constant (k).</p>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.2)'>", unsafe_allow_html=True)

# Calculator Grid
cols = st.columns(4)
trials = []
for i, col in enumerate(cols, 1):
    with col:
        st.markdown(f"### Trial {i}")
        a = st.number_input(f"Initial [A] (M)", key=f"a{i}", format="%.4e", value=0.1)
        b = st.number_input(f"Initial [B] (M)", key=f"b{i}", format="%.4e", value=0.1)
        r = st.number_input(f"Rate", key=f"r{i}", format="%.4e", value=0.001)
        trials.append({'a': a, 'b': b, 'rate': r})

if st.button("Calculate Results"):
    try:
        # Example calculation (A changes, B constant for trial 0 & 1)
        m = round(math.log(trials[1]['rate'] / trials[0]['rate']) / math.log(trials[1]['a'] / trials[0]['a']))
        # Example calculation (B changes, A constant for trial 0 & 2)
        n = round(math.log(trials[2]['rate'] / trials[0]['rate']) / math.log(trials[2]['b'] / trials[0]['b']))
        k = trials[0]['rate'] / ((trials[0]['a']**m) * (trials[0]['b']**n))
        
        st.balloons()
        st.success("Calculation Completed!")
        st.write(f"**Order of A (m):** {m} | **Order of B (n):** {n}")
        st.latex(rf"Rate = {k:.4e} \ [A]^{{{m}}} [B]^{{{n}}}")
    except:
        st.error("Please verify data points. Ensure at least two trials have a constant concentration for one reactant.")

st.markdown('</div>', unsafe_allow_html=True) # Closes the main-box

# 6. Footer
st.markdown("<p style='text-align: center; color: white;'>Learning Without Limits - Science Department</p>", unsafe_allow_html=True)
