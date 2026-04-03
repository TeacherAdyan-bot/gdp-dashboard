import streamlit as st
import math
import base64
from datetime import datetime
import pytz

# 1. Page Configuration
st.set_page_config(page_title="Britus International School Bahrain", layout="wide")

# 2. Function to load your background image
def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except: return None

bin_str = get_base64('my_background.jpg')

# 3. STRONGER CSS (Forces Title inside and forces White color)
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str if bin_str else ""}");
        background-size: cover;
        background-attachment: fixed;
    }}
    
    /* This is your boundary box */
    .calculator-container {{
        background-color: rgba(0, 33, 71, 0.9); /* Dark Navy */
        padding: 40px;
        border-radius: 30px;
        border: 5px solid #800000; /* Maroon Border */
        box-shadow: 0px 20px 40px rgba(0,0,0,0.8);
        margin-top: 20px;
        text-align: center;
        color: white !important; /* Force children to be white */
    }}

    /* TARGETING THE TITLE SPECIFICALLY INSIDE THE BOX */
    .calculator-container h1, .calculator-container p, .calculator-container h3, .calculator-container label {{
        color: #FFFFFF !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,1); /* Strong shadow for visibility */
    }}

    .clock-style {{
        background-color: #800000;
        color: white;
        padding: 10px 25px;
        border-radius: 50px;
        font-weight: bold;
        display: inline-block;
        border: 2px solid white;
    }}

    /* Input boxes remain white with black text for typing */
    .stNumberInput input {{
        color: black !important;
        background-color: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. Banner & Clock (Top of page)
try:
    st.image("britus_banner.png", use_container_width=True)
except:
    st.error("Check GitHub for 'britus_banner.png'")

bahrain_tz = pytz.timezone('Asia/Bahrain')
st.markdown(f"<div class='clock-style'>🕒 {datetime.now(bahrain_tz).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# 5. THE BOX (Open the box)
st.markdown('<div class="calculator-container">', unsafe_allow_html=True)

# THE TITLE IS NOW WRITTEN IN HTML INSIDE THE DIV
st.markdown("<h1 style='color: white;'>🧪 Chemical Kinetics: Rate Law Determinator</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: white;'>Enter your experimental data to calculate reaction orders and k.</p>", unsafe_allow_html=True)

st.write("---") # Visual separator inside the box

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
        # Math remains the same
        m = round(math.log(trials[1]['rate'] / trials[0]['rate']) / math.log(trials[1]['a'] / trials[0]['a']))
        n = round(math.log(trials[2]['rate'] / trials[0]['rate']) / math.log(trials[2]['b'] / trials[0]['b']))
        k = trials[0]['rate'] / ((trials[0]['a']**m) * (trials[0]['b']**n))
        st.balloons()
        st.success("Analysis Complete!")
        st.latex(rf"Rate = {k:.4e} \ [A]^{{{m}}} [B]^{{{n}}}")
    except:
        st.error("Ensure constant concentrations between trials.")

st.markdown('</div>', unsafe_allow_html=True) # Closes the box

# 6. Footer
st.markdown("<p style='text-align: center; color: white; margin-top: 20px;'>Learning Without Limits - Science Department</p>", unsafe_allow_html=True)
