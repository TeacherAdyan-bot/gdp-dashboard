import streamlit as st
import math
import base64
from datetime import datetime
import pytz

# 1. SETUP
st.set_page_config(page_title="Britus International School Bahrain", layout="wide")

def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except: return ""

bin_str = get_base64('my_background.jpg')

# 2. CSS (Added overflow:hidden and display:inline-block to force containment)
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
    .results-card {{
        background-color: rgba(0, 33, 71, 0.95) !important;
        padding: 40px !important;
        border-radius: 25px !important;
        border: 4px solid #800000 !important;
        box-shadow: 0px 15px 35px rgba(0,0,0,0.8) !important;
        width: 100% !important;
        display: block !important;
        overflow: hidden !important;
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
    }}
    /* This forces Streamlit's internal latex div to respect the parent color */
    .stLatex div {{
        color: white !important;
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

# 4. INPUTS
cols = st.columns(3)
trials_data = []
for i, col in enumerate(cols, 1):
    with col:
        st.markdown(f'<div class="trial-header"><h3>Trial {i}</h3></div>', unsafe_allow_html=True)
        a = st.number_input(f"Initial [A] (M)", key=f"a{i}", format="%.4e", value=0.1)
        b = st.number_input(f"Initial [B] (M)", key=f"b{i}", format="%.4e", value=0.1)
        r = st.number_input(f"Initial Rate (M/s)", key=f"r{i}", format="%.4e", value=0.001)
        trials_data.append({'a': a, 'b': b, 'rate': r})

# 5. THE TRICK: THE CONTAINER PLACEHOLDER
# We create the container BEFORE the button is clicked.
results_container = st.container()

if st.button("RUN SCIENTIFIC ANALYSIS"):
    try:
        m, n = None, None
        if trials_data[0]['b'] == trials_data[1]['b']:
            m = round(math.log(trials_data[1]['rate'] / trials_data[0]['rate']) / math.log(trials_data[1]['a'] / trials_data[0]['a']))
        if trials_data[1]['a'] == trials_data[2]['a']:
            n = round(math.log(trials_data[2]['rate'] / trials_data[1]['rate']) / math.log(trials_data[2]['b'] / trials_data[1]['b']))

        if m is not None and n is not None:
            overall_order = m + n
            k = trials_data[0]['rate'] / ((trials_data[0]['a']**m) * (trials_data[0]['b']**n))
            units = {0: "M/s", 1: "s⁻¹", 2: "M⁻¹s⁻¹", 3: "M⁻²s⁻¹"}.get(overall_order, "M⁻ⁿs⁻¹")

            st.balloons()
            
            # Use the placeholder to wrap EVERYTHING
            with results_container:
                # Top part of box
                st.markdown(f"""
                <div class="results-card">
                    <h2>ANALYSIS COMPLETE</h2>
                    <p style="font-size: 1.1rem;"><b>Order (m):</b> {m} | <b>Order (n):</b> {n} | <b>Rate Constant (k):</b> {k:.4e} {units}</p>
                    <hr style="border: 1px solid #800000; margin: 20px 0;">
                    <h3>SCIENTIFIC CONCLUSION</h3>
                    <p>Collision theory dictates that for a reaction to occur, particles must collide with sufficient energy and correct orientation. 
                    By increasing the concentration, the frequency of these collisions per unit of time increases, resulting in a higher rate.</p>
                """, unsafe_allow_html=True)
                
                # The Equation (Now inside the 'with' block)
                st.latex(rf"Rate = [{k:.4e}] \ [A]^{{{m}}} [B]^{{{n}}}")
                
                # Close the box
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("Error: Constant concentration not found between trials.")
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("<p style='margin-top: 50px;'>Learning Without Limits - Science Department</p>", unsafe_allow_html=True)
