import streamlit as st
import math
import base64
from datetime import datetime
import pytz

# 1. SETUP & CONFIGURATION (Must be at the top)
st.set_page_config(page_title="Britus International School Bahrain", layout="wide")

def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except: return ""

# Background handling
bin_str = get_base64('my_background.jpg')

# 2. UI STYLING (Professional Navy & Maroon Theme)
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
    .trial-header {{
        background-color: rgba(0, 33, 71, 0.95) !important;
        padding: 15px !important;
        border-radius: 20px !important;
        border: 4px solid #800000 !important;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.6) !important;
        margin-bottom: 15px !important;
        width: 100% !important;
    }}
    .results-card {{
        background-color: rgba(0, 33, 71, 0.95) !important;
        padding: 30px !important;
        border-radius: 25px !important;
        border: 4px solid #800000 !important;
        box-shadow: 0px 15px 35px rgba(0,0,0,0.8) !important;
        margin-top: 30px !important;
    }}
    div[data-baseweb="input"] {{
        background-color: white !important;
        border-radius: 10px !important;
    }}
    div[data-baseweb="input"] * {{
        color: black !important;
        text-shadow: none !important;
    }}
    .stButton>button {{
        background-color: #800000 !important;
        color: white !important;
        border: 2px solid white !important;
        border-radius: 12px !important;
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

# 4. TRIAL INPUTS (3 Trials as per your design)
st.markdown("<br>", unsafe_allow_html=True)
cols = st.columns(3)
trials_data = []

for i, col in enumerate(cols, 1):
    with col:
        st.markdown(f'<div class="trial-header"><h3>Trial {i}</h3></div>', unsafe_allow_html=True)
        a = st.number_input(f"Initial [A] (M)", key=f"a{i}", format="%.4e", value=0.1)
        b = st.number_input(f"Initial [B] (M)", key=f"b{i}", format="%.4e", value=0.1)
        r = st.number_input(f"Initial Rate (M/s)", key=f"r{i}", format="%.4e", value=0.001)
        trials_data.append({'a': a, 'b': b, 'rate': r})

# 5. ANALYSIS LOGIC
st.markdown("<br>", unsafe_allow_html=True)
if st.button("ANALYZE KINETICS"):
    try:
        # Solving for m (where B is constant) and n (where A is constant)
        m, n = None, None
        
        # Calculate Order m
        if trials_data[0]['b'] == trials_data[1]['b']:
            m = round(math.log(trials_data[1]['rate'] / trials_data[0]['rate']) / math.log(trials_data[1]['a'] / trials_data[0]['a']))
        
        # Calculate Order n
        if trials_data[1]['a'] == trials_data[2]['a']:
            n = round(math.log(trials_data[2]['rate'] / trials_data[1]['rate']) / math.log(trials_data[2]['b'] / trials_data[1]['b']))

        if m is not None and n is not None:
            overall_order = m + n
            t1 = trials_data[0]
            k = t1['rate'] / ((t1['a']**m) * (t1['b']**n))
            
            st.balloons()
            st.markdown(f"""
            <div class="results-card">
                <h2>ANALYSIS COMPLETE</h2>
                <p><b>Order (m):</b> {m} | <b>Order (n):</b> {n} | <b>Rate Constant (k):</b> {k:.4e}</p>
                <hr style="border: 1px solid #800000;">
                <h3>SCIENTIFIC CONCLUSION</h3>
                <p>Collision theory dictates that for a reaction to occur, particles must collide with sufficient energy and correct orientation. 
                By increasing the concentration, the frequency of these collisions per unit of time increases, resulting in a higher rate.</p>
                <div style="display: flex; justify-content: space-around; margin-top: 20px;">
                    <div><b>Reactant A (Order {m})</b><br>Doubling [A] increases rate {2**m}x</div>
                    <div><b>Reactant B (Order {n})</b><br>Doubling [B] increases rate {2**n}x</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.latex(rf"Rate = [{k:.4e}] \ [A]^{{{m}}} [B]^{{{n}}}")
            
        else:
            st.error("Error: Ensure concentrations remain constant between trials to calculate orders.")
    except Exception as e:
        st.error(f"Calculation Error: {e}")

st.markdown("<p style='margin-top: 50px;'>Learning Without Limits - Science Department</p>", unsafe_allow_html=True)
