import streamlit as st
import math
import base64
from datetime import datetime
import pytz

# 1. SETUP & CONFIGURATION
st.set_page_config(page_title="Britus International School Bahrain", layout="wide")

def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except: return ""

# Background image handling
bin_str = get_base64('my_background.jpg')

# 2. UI OVERRIDE (CSS)
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
    }}
    h1, h2, h3, h4, p, span, div, label {{
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,1) !important;
        text-align: center !important;
    }}
    /* Standard Navy Box for Trial Headers */
    .trial-header {{
        background-color: rgba(0, 33, 71, 0.95) !important;
        padding: 15px !important;
        border-radius: 20px !important;
        border: 4px solid #800000 !important;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.6) !important;
        margin-bottom: 15px !important;
        width: 100% !important;
    }}
    /* NEW: High-Contrast White Results Card */
    .results-card {{
        background-color: rgba(255, 255, 255, 0.98) !important;
        padding: 35px !important;
        border-radius: 15px !important;
        border: 4px solid #800000 !important;
        box-shadow: 0px 15px 35px rgba(0,0,0,0.8) !important;
        margin-top: 30px !important;
        width: 100% !important;
    }}
    /* Black Text for White Card */
    .results-card h2, .results-card h3, .results-card p, .results-card b, .results-card div {{
        color: #000000 !important;
        text-shadow: none !important;
    }}
    /* Input Styling */
    div[data-baseweb="input"], div[data-baseweb="select"] {{
        background-color: white !important;
        border-radius: 10px !important;
        border: 2px solid #800000 !important;
    }}
    div[data-baseweb="input"] *, div[data-baseweb="select"] * {{
        color: black !important;
        text-shadow: none !important;
        font-weight: bold !important;
    }}
    .stButton>button {{
        background-color: #800000 !important;
        color: white !important;
        border: 2px solid white !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        width: 100% !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. BRANDING & CLOCK
try:
    st.image("britus_banner.png", use_container_width=True)
except: pass

bahrain_tz = pytz.timezone('Asia/Bahrain')
st.markdown(f"<div style='background-color:#800000; color:white; padding:8px 25px; border-radius:50px; font-weight:bold; border:2px solid white; margin:0 auto 20px auto; display:table;'>🕒 {datetime.now(bahrain_tz).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

st.markdown('<div class="trial-header"><h1>🧪 Chemical Kinetics: Rate Law Determinator</h1></div>', unsafe_allow_html=True)

# 4. TRIAL SELECTION
st.markdown("### Select Number of Experimental Trials")
num_trials = st.selectbox("Trials", options=[3, 4], index=1, label_visibility="collapsed")

# 5. DYNAMIC TRIAL INPUTS
st.markdown("<br>", unsafe_allow_html=True)
cols = st.columns(num_trials)
trials_data = []

for i, col in enumerate(cols, 1):
    with col:
        st.markdown(f'<div class="trial-header"><h3>Trial {i}</h3></div>', unsafe_allow_html=True)
        a = st.number_input(f"Initial [A] (M)", key=f"a{i}", format="%.4e", value=0.1)
        b = st.number_input(f"Initial [B] (M)", key=f"b{i}", format="%.4e", value=0.1)
        r = st.number_input(f"Initial Rate (M/s)", key=f"r{i}", format="%.4e", value=0.001)
        trials_data.append({'a': a, 'b': b, 'rate': r})

# 6. CALCULATION & WHITE BOX OUTPUT
st.markdown("<br>", unsafe_allow_html=True)
if st.button("ANALYZE KINETICS"):
    try:
        m, n = None, None
        active_trials = trials_data[:num_trials]

        for i in range(num_trials):
            for j in range(num_trials):
                if i != j and active_trials[i]['b'] == active_trials[j]['b'] and active_trials[i]['a'] != active_trials[j]['a']:
                    m = round(math.log(active_trials[j]['rate'] / active_trials[i]['rate']) / math.log(active_trials[j]['a'] / active_trials[i]['a']))
                    break
            if m is not None: break

        for i in range(num_trials):
            for j in range(num_trials):
                if i != j and active_trials[i]['a'] == active_trials[j]['a'] and active_trials[i]['b'] != active_trials[j]['b']:
                    n = round(math.log(active_trials[j]['rate'] / active_trials[i]['rate']) / math.log(active_trials[j]['b'] / active_trials[i]['b']))
                    break
            if n is not None: break

        if m is not None and n is not None:
            overall_order = m + n
            t_last = active_trials[-1]
            k = t_last['rate'] / ((t_last['a']**m) * (t_last['b']**n))
            
            units_map = {0: "M/s", 1: "s⁻¹", 2: "M⁻¹s⁻¹", 3: "M⁻²s⁻¹"}
            unit_display = units_
