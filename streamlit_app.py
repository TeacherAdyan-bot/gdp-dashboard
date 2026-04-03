import streamlit as st
import math
import base64
from datetime import datetime
import pytz

# 1. Page Configuration
st.set_page_config(page_title="Britus International School Bahrain", layout="wide")

# 2. Background Loader
def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except: return ""

bin_str = get_base64('my_background.jpg')

# 3. GLOBAL CSS: This forces the box and white text everywhere
st.markdown(f"""
    <style>
    /* Background Image */
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
    }}

    /* THE UNIFIED BOX: Forces everything inside to stay together */
    .unified-card {{
        background-color: rgba(0, 33, 71, 0.9) !important;
        padding: 30px !important;
        border-radius: 20px !important;
        border: 5px solid #800000 !important;
        box-shadow: 0px 15px 30px rgba(0,0,0,0.8) !important;
        margin-bottom: 25px !important;
        text-align: center !important;
    }}

    /* FORCE WHITE FONT: Targets every text element known to Streamlit */
    h1, h2, h3, p, span, label, [data-testid="stWidgetLabel"], .stMarkdown {{
        color: #FFFFFF !important;
        text-align: center !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,1) !important;
    }}

    /* Clock Styling */
    .clock-style {{
        background-color: #800000;
        color: white;
        padding: 10px 25px;
        border-radius: 50px;
        font-weight: bold;
        border: 2px solid white;
        margin: 0 auto 20px auto;
        display: table;
    }}

    /* Inputs stay black for typing clarity */
    input {{
        color: black !important;
        text-shadow: none !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. Banner & Clock
try:
    st.image("britus_banner.png", use_container_width=True)
except:
    pass

bahrain_tz = pytz.timezone('Asia/Bahrain')
st.markdown(f"<div class='clock-style'>🕒 {datetime.now(bahrain_tz).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# 5. TITLE BOX (Forced Inside)
# We use a single markdown block for the div AND the text to prevent separation
st.markdown("""
    <div class="unified-card">
        <h1 style="margin:0;">🧪 Chemical Kinetics: Rate Law Determinator</h1>
        <p style="margin-top:10px;">Learning Without Limits - Science Department</p>
    </div>
    """, unsafe_allow_html=True)

# 6. TRIAL BOXES (All Same Style)
cols = st.columns(4)
trials = []

for i, col in enumerate(cols, 1):
    with col:
        # Wrapping the trial input inside the unified box
        st.markdown('<div class="unified-card">', unsafe_allow_html=True)
        st.markdown(f"### Trial {i}")
        a = st.number_input(f"Initial [A] (M)", key=f"a{i}", format="%.4e", value=0.1)
        b = st.number_input(f"Initial [B] (M)", key=f"b{i}", format="%.4e", value=0.1)
        r = st.number_input(f"Initial Rate", key=f"r{i}", format="%.4e", value=0.001)
        trials.append({'a': a, 'b': b, 'rate': r})
        st.markdown('</div>', unsafe_allow_html=True)

# 7. Calculation Button
if st.button("Calculate Reaction Order", type="primary", use_container_width=True):
    try:
        # Standard logic for Method of Initial Rates
        m = round(math.log(trials[1]['rate'] / trials[0]['rate']) / math.log(trials[1]['a'] / trials[0]['a']))
        n = round(math.log(trials[2]['rate'] / trials[0]['rate']) / math.log(trials[2]['b'] / trials[0]['b']))
        k = trials[0]['rate'] / ((trials[0]['a']**m) * (trials[0]['b']**n))
        
        st.balloons()
        st.success("Calculations Successful!")
        st.write(f"Order A: **{m}** | Order B: **{n}**")
        st.latex(rf"Rate = {k:.4e} \ [A]^{{{m}}} [B]^{{{n}}}")
    except:
        st.error("Error: Please check trial data for constant concentrations.")
