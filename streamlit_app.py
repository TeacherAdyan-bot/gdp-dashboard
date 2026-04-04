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

# 2. UI OVERRIDE (Expert CSS for Full Containment)
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
        margin-bottom: 15px !important;
    }}
    /* The Master Container */
    .results-card {{
        background-color: rgba(0, 33, 71, 0.95) !important;
        padding: 40px !important;
        border-radius: 25px !important;
        border: 4px solid #800000 !important;
        box-shadow: 0px 15px 35px rgba(0,0,0,0.8) !important;
        width: 100% !important;
        display: block !important;
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
    /* Style for the selectbox label */
    .stSelectbox label p {{
        font-size: 1.2rem !important;
        font-weight: bold !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. BRANDING
try:
    st.image("britus_banner.png", use_container_width=True)
except: pass

bahrain_tz = pytz.timezone('Asia/Bahrain')
st.markdown(f"<div style='background-color:#800000; color:white; padding:8px 25px; border-radius:50px; font-weight:bold; border:2px solid white; margin:0 auto 20px auto; display:table;'>🕒 {datetime.now(bahrain_tz).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

st.markdown('<div class="trial-header"><h1>🧪 Chemical Kinetics: Rate Law Determinator</h1></div>', unsafe_allow_html=True)

# 4. TRIAL SELECTION & INPUTS
# Added the Dropdown box here
num_trials = st.selectbox("Select Number of Trials:", options=[3, 4], index=0)

cols = st.columns(num_trials)
trials_data = []
for i, col in enumerate(cols, 1):
    with col:
        st.markdown(f'<div class="trial-header"><h3>Trial {i}</h3></div>', unsafe_allow_html=True)
        a = st.number_input(f"Initial [A] (M)", key=f"a{i}", format="%.4e", value=0.1)
        b = st.number_input(f"Initial [B] (M)", key=f"b{i}", format="%.4e", value=0.1)
        r = st.number_input(f"Initial Rate (M/s)", key=f"r{i}", format="%.4e", value=0.001)
        trials_data.append({'a': a, 'b': b, 'rate': r})

# 5. INTEGRATED ANALYSIS & OUTPUT
st.markdown("<br>", unsafe_allow_html=True)
if st.button("RUN SCIENTIFIC ANALYSIS"):
    try:
        m, n = None, None
        
        # Order Calculation Logic
        # We look for two trials where B is constant to find m (order of A)
        # We look for two trials where A is constant to find n (order of B)
        
        # Expert logic to find constant pairs automatically
        for i in range(len(trials_data)):
            for j in range(i + 1, len(trials_data)):
                # Finding m: [B] is constant, [A] changes
                if trials_data[i]['b'] == trials_data[j]['b'] and trials_data[i]['a'] != trials_data[j]['a']:
                    m = round(math.log(trials_data[j]['rate'] / trials_data[i]['rate']) / math.log(trials_data[j]['a'] / trials_data[i]['a']))
                # Finding n: [A] is constant, [B] changes
                if trials_data[i]['a'] == trials_data[j]['a'] and trials_data[i]['b'] != trials_data[j]['b']:
                    n = round(math.log(trials_data[j]['rate'] / trials_data[i]['rate']) / math.log(trials_data[j]['b'] / trials_data[i]['b']))

        if m is not None and n is not None:
            overall_order = m + n
            k = trials_data[0]['rate'] / ((trials_data[0]['a']**m) * (trials_data[0]['b']**n))
            
            # Unit Mapping
            units = {0: "M/s", 1: "s⁻¹", 2: "M⁻¹s⁻¹", 3: "M⁻²s⁻¹"}.get(overall_order, "M⁻ⁿs⁻¹")

            st.balloons()
            
            st.markdown(f"""
            <div class="results-card">
                <h2>ANALYSIS COMPLETE</h2>
                <p style="font-size: 1.2rem;">
                    <b>Order (m):</b> {m} | <b>Order (n):</b> {n} | <b>Rate Constant (k):</b> {k:.4e} {units}
                </p>
                <hr style="border: 1px solid #800000; margin: 25px 0;">
                <h3>SCIENTIFIC CONCLUSION</h3>
                <p>
              According to collision theory, a chemical reaction occurs only when reacting particles collide with sufficient kinetic energy and 
              a favorable orientation. By increasing the concentration of reactants, the number of particles per unit volume increases, 
              leading to a higher frequency of effective collisions and a faster reaction rate.
                </p>
                <div style="display: flex; justify-content: space-around; margin: 25px 0; font-weight: bold;">
                    <div>Reactant A (Order {m})<br>Doubling [A] increases rate {2**m}x</div>
                    <div>Reactant B (Order {n})<br>Doubling [B] increases rate {2**n}x</div>
                </div>
                <div style="margin-top: 35px; background: rgba(255,255,255,0.08); padding: 25px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.2);">
                    <p style="margin-bottom: 10px; font-weight: bold; color: #800000 !important;">FINAL RATE LAW:</p>
                    <p style="font-size: 1.8rem; font-family: 'Times New Roman', serif;">
                        <i>Rate</i> = [{k:.4e}] [A]<sup>{m}</sup> [B]<sup>{n}</sup>
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Error: Could not determine orders. Ensure your data includes trials where one concentration remains constant while the other changes.")
    except Exception as e:
        st.error(f"Analysis Error: {e}")

st.markdown("<p style='margin-top: 50px;'>Learning Without Limits - Science Department</p>", unsafe_allow_html=True)
