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

# 2. TOTAL UI OVERRIDE (CSS)
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
    .branded-card {{
        background-color: rgba(0, 33, 71, 0.95) !important;
        padding: 30px !important;
        border-radius: 20px !important;
        border: 4px solid #800000 !important;
        box-shadow: 0px 15px 35px rgba(0,0,0,0.8) !important;
        margin: 20px auto !important;
        width: 90% !important;
    }}
    div[data-baseweb="select"], div[data-baseweb="input"] {{
        background-color: white !important;
        border-radius: 8px !important;
        border: 2px solid #800000 !important;
    }}
    div[data-baseweb="select"] *, div[data-baseweb="input"] * {{
        color: black !important;
        text-shadow: none !important;
        font-weight: bold !important;
    }}
    .stButton>button {{
        background-color: #800000 !important;
        color: white !important;
        border: 2px solid white !important;
        border-radius: 10px !important;
        font-weight: bold !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. BRANDING & CLOCK
try:
    st.image("britus_banner.png", use_container_width=True)
except: pass

bahrain_tz = pytz.timezone('Asia/Bahrain')
st.markdown(f"<div style='background-color:#800000; color:white; padding:8px 25px; border-radius:50px; font-weight:bold; border:2px solid white; margin:0 auto 20px auto; display:table;'>🕒 {datetime.now(bahrain_tz).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# 4. TITLE & SELECTION
st.markdown('<div class="branded-card">', unsafe_allow_html=True)
st.markdown('<h1 style="margin-bottom: 25px;">🧪 Chemical Kinetics Determinator</h1>', unsafe_allow_html=True)
st.markdown('<p style="font-size: 1.2rem;">Select Number of Experimental Trials</p>', unsafe_allow_html=True)
num_trials = st.selectbox("Trials", options=[3, 4], index=1, label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# 5. DYNAMIC TRIAL INPUTS
cols = st.columns(num_trials)
trials_data = []

for i, col in enumerate(cols, 1):
    with col:
        st.markdown(f'<div class="branded-card" style="padding: 15px !important; width: 100% !important;">', unsafe_allow_html=True)
        st.markdown(f'<h3>Trial {i}</h3>', unsafe_allow_html=True)
        a = st.number_input(f"Initial [A]", key=f"a{i}", format="%.4e", value=0.1)
        b = st.number_input(f"Initial [B]", key=f"b{i}", format="%.4e", value=0.1)
        r = st.number_input(f"Rate", key=f"r{i}", format="%.4e", value=0.001)
        trials_data.append({'a': a, 'b': b, 'rate': r})
        st.markdown('</div>', unsafe_allow_html=True)

# 6. CALCULATION & FULL NAVY BOX RESULTS
st.markdown("<br>", unsafe_allow_html=True)
if st.button("RUN SCIENTIFIC ANALYSIS", use_container_width=True):
    try:
        m, n = None, None
        active_trials = trials_data[:num_trials]

        # Calculation logic for orders m and n
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
            
            units = {0: "M/s", 1: "s⁻¹", 2: "M⁻¹s⁻¹", 3: "M⁻²s⁻¹"}
            unit = units.get(overall_order, f"M^{1-overall_order}s⁻¹")

            st.balloons()
            
            # START OF FULL NAVY BOX FOR ANSWERS
            st.markdown('<div class="branded-card">', unsafe_allow_html=True)
            st.markdown('<h2>ANALYSIS COMPLETE</h2>', unsafe_allow_html=True)
            st.markdown(f"**Order (m):** {m} | **Order (n):** {n} | **Rate Constant (k):** {k:.4e} {unit}")
            
            st.markdown('<hr style="border: 1px solid #800000;">', unsafe_allow_html=True)
            st.markdown('<h3>SCIENTIFIC CONCLUSION</h3>', unsafe_allow_html=True)
            st.write("According to collision theory, increasing concentration leads to more frequent successful collisions.")
            
            # Side-by-Side Explanation
            c1, c2 = st.columns(2)
            with c1:
                st.write(f"**Reactant A (Order {m})**")
                st.write(f"Doubling [A] increases rate {2**m}x")
            with c2:
                st.write(f"**Reactant B (Order {n})**")
                st.write(f"Doubling [B] increases rate {2**n}x")

            # Final LaTeX Equation (k in brackets, no units)
            st.markdown("<br>", unsafe_allow_html=True)
            st.latex(rf"Rate = [{k:.4e}] \ [A]^{{{m}}} [B]^{{{n}}}")
            st.markdown('</div>', unsafe_allow_html=True)
            # END OF NAVY BOX
            
        else:
            st.error("Error: Could not find trials with constant concentrations.")
    except Exception as e:
        st.error(f"Input Error: {e}")

st.markdown("<p style='margin-top: 50px;'>Learning Without Limits - Science Department</p>", unsafe_allow_html=True)
