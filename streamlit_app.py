import streamlit as st
import math
import base64
from datetime import datetime
import pytz

# 1. Setup
st.set_page_config(page_title="Britus International School Bahrain", layout="wide")

def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except: return ""

bin_str = get_base64('my_background.jpg')

# 2. Expert CSS
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
    }}

    /* Global White Font Force */
    h1, h2, h3, p, span, label, [data-testid="stWidgetLabel"] {{
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,1) !important;
        text-align: center !important;
    }}

    /* The Unified Box Style */
    .unified-card {{
        background-color: rgba(0, 33, 71, 0.9) !important;
        padding: 20px !important;
        border-radius: 25px !important;
        border: 4px solid #800000 !important;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.7) !important;
        margin-bottom: 10px !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }}

    .clock-style {{
        background-color: #800000;
        color: white;
        padding: 8px 20px;
        border-radius: 50px;
        font-weight: bold;
        border: 2px solid white;
        margin: 0 auto 20px auto;
        display: table;
    }}

    input {{
        color: black !important;
        text-shadow: none !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. Banner & Clock
try:
    st.image("britus_banner.png", use_container_width=True)
except: pass

bahrain_tz = pytz.timezone('Asia/Bahrain')
st.markdown(f"<div class='clock-style'>🕒 {datetime.now(bahrain_tz).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# 4. THE TITLE BOX FIX
# We put the text INSIDE the div string so Streamlit cannot separate them
st.markdown("""
    <div class="unified-card">
        <h1 style="margin: 0; padding: 10px;">🧪 Chemical Kinetics: Rate Law Determinator</h1>
    </div>
    """, unsafe_allow_html=True)

# 5. THE TRIALS FIX
cols = st.columns(4)
trials = []

for i, col in enumerate(cols, 1):
    with col:
        # Step A: Create the box WITH the Trial Title inside it
        st.markdown(f"""
            <div class="unified-card">
                <h3 style="margin: 0;">Trial {i}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        # Step B: Inputs appear immediately below the box
        a = st.number_input(f"Initial [A] (M)", key=f"a{i}", format="%.4e", value=0.1)
        b = st.number_input(f"Initial [B] (M)", key=f"b{i}", format="%.4e", value=0.1)
        r = st.number_input(f"Initial Rate", key=f"r{i}", format="%.4e", value=0.001)
        trials.append({'a': a, 'b': b, 'rate': r})

# 6. Logic
st.markdown("<br>", unsafe_allow_html=True)
if st.button("Calculate Reaction Order", type="primary", use_container_width=True):
    try:
        m = round(math.log(trials[1]['rate'] / trials[0]['rate']) / math.log(trials[1]['a'] / trials[0]['a']))
        n = round(math.log(trials[2]['rate'] / trials[0]['rate']) / math.log(trials[2]['b'] / trials[0]['b']))
        k = trials[0]['rate'] / ((trials[0]['a']**m) * (trials[0]['b']**n))
        st.balloons()
        st.success(f"Results: m={m}, n={n}")
        st.latex(rf"Rate = {k:.4e} \ [A]^{{{m}}} [B]^{{{n}}}")
    except:
        st.error("Check experimental data.")

st.markdown("<p style='text-align: center;'>Learning Without Limits - Science Department</p>", unsafe_allow_html=True)
