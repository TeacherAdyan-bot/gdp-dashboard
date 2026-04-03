import streamlit as st
import math
import base64
from datetime import datetime
import pytz

# 1. Page Configuration
st.set_page_config(page_title="Britus International School Bahrain", layout="wide")

# 2. Function to load your background
def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

# Apply Background
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

# 3. CSS for the Box and White Fonts
st.markdown("""
    <style>
    .calculator-container {
        background-color: rgba(0, 33, 71, 0.85); /* Navy Box */
        padding: 40px;
        border-radius: 25px;
        border: 4px solid #800000; /* Maroon Border */
        box-shadow: 0px 15px 35px rgba(0,0,0,0.7);
        margin-top: 10px;
    }
    
    /* Force white text for all headers and labels */
    h1, h2, h3, p, span, label, .stMarkdown {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    .clock-style {
        background-color: #800000;
        color: white;
        padding: 10px 20px;
        border-radius: 50px;
        font-weight: bold;
        display: inline-block;
        border: 2px solid white;
        margin-bottom: 20px;
    }

    .stNumberInput input {
        color: black !important;
        background-color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. Banner & Clock
try:
    st.image("britus_banner.png", use_container_width=True)
except:
    st.warning("Banner not found.")

bahrain_tz = pytz.timezone('Asia/Bahrain')
st.markdown(f"<div class='clock-style'>🕒 {datetime.now(bahrain_tz).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# 5. THE BOX (Title is now INSIDE)
st.markdown('<div class="calculator-container">', unsafe_allow_html=True)

# This line is now moved inside the container
st.markdown("<h1 style='text-align:center;'>🧪 Chemical Kinetics: Rate Law Determinator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Enter your experimental data below.</p>", unsafe_allow_html=True)
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
        k = trials[3]['rate'] / ((trials[3]['a']**m) * (trials[3]['b']**n))
        st.success(f"Analysis Complete! m={m}, n={n}")
        st.latex(rf"Rate = {k:.4e} \ [A]^{{{m}}} [B]^{{{n}}}")
    else:
        st.error("Constant concentration trials not found.")

st.markdown('</div>', unsafe_allow_html=True) # Closes the box

# 6. Footer
st.markdown("<p style='text-align: center; margin-top: 20px;'><b>Learning Without Limits - Science Department</b></p>", unsafe_allow_html=True)
