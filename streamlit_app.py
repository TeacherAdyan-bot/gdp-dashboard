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

# Background image handling - ensure 'my_background.jpg' is in your repository
bin_str = get_base64('my_background.jpg')

# 2. SYSTEMATIC BRANDING CSS (Fixes alignment and card symmetry)
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
    }}
    h1, h2, h3, p, span, label, [data-testid="stWidgetLabel"] {{
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,1) !important;
        text-align: center !important;
    }}
    .unified-card {{
        background-color: rgba(0, 33, 71, 0.9) !important;
        padding: 25px !important;
        border-radius: 25px !important;
        border: 4px solid #800000 !important;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.7) !important;
        margin-bottom: 20px !important;
        width: 100% !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }}
    /* SYSTEMATIC DROPDOWN FIX: Forces the box to stay inside the navy container */
    div[data-baseweb="select"] {{
        background-color: white !important;
        border-radius: 10px !important;
        width: 100% !important;
        max-width: 600px !important; /* Prevents awkward stretching on wide screens */
        margin: 0 auto !important;
    }}
    div[data-baseweb="select"] * {{
        color: black !important;
        font-weight: bold !important;
        text-shadow: none !important;
    }}
    /* Trial Input Boxes */
    div[data-baseweb="input"] {{
        background-color: white !important;
        border-radius: 10px !important;
    }}
    div[data-baseweb="input"] * {{
        color: black !important;
        font-weight: bold !important;
        text-shadow: none !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. BRANDING & CLOCK
try:
    st.image("britus_banner.png", use_container_width=True)
except: pass

bahrain_tz = pytz.timezone('Asia/Bahrain')
st.markdown(f"<div style='background-color:#800000; color:white; padding:8px 20px; border-radius:50px; font-weight:bold; border:2px solid white; margin:0 auto 20px auto; display:table;'>🕒 {datetime.now(bahrain_tz).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# Main Title
st.markdown('<div class="unified-card"><h1 style="margin: 0;">🧪 Chemical Kinetics: Rate Law Determinator</h1></div>', unsafe_allow_html=True)

# 4. FIXED SELECTION CARD (Text and Dropdown centered together)
st.markdown('<div class="unified-card">', unsafe_allow_html=True)
st.markdown('<h3 style="margin: 0; padding-bottom: 15px;">Select Number of Experimental Trials</h3>', unsafe_allow_html=True)
num_trials = st.selectbox(
    "Select Number of Experimental Trials", 
    options=[3, 4], 
    index=1, 
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# 5. DYNAMIC TRIAL INPUTS
cols = st.columns(num_trials)
trials_data = []

for i, col in enumerate(cols, 1):
    with col:
        st.markdown(f'<div class="unified-card"><h3 style="margin: 0;">Trial {i}</h3></div>', unsafe_allow_html=True)
        a = st.number_input(f"Initial [A] (M)", key=f"a{i}", format="%.4e", value=0.1)
        b = st.number_input(f"Initial [B] (M)", key=f"b{i}", format="%.4e", value=0.1)
        r = st.number_input(f"Initial Rate (M/s)", key=f"r{i}", format="%.4e", value=0.001)
        trials_data.append({'a': a, 'b': b, 'rate': r})

# 6. CALCULATION LOGIC & SCIENTIFIC CONCLUSION
st.markdown("<br>", unsafe_allow_html=True)
if st.button("Analyze Reaction Kinetics", type="primary", use_container_width=True):
    try:
        m, n = None, None
        active_trials = trials_data[:num_trials]

        # Order for A
        for i in range(num_trials):
            for j in range(num_trials):
                if i != j and active_trials[i]['b'] == active_trials[j]['b'] and active_trials[i]['a'] != active_trials[j]['a']:
                    m = round(math.log(active_trials[j]['rate'] / active_trials[i]['rate']) / math.log(active_trials[j]['a'] / active_trials[i]['a']))
                    break
            if m is not None: break

        # Order for B
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
            st.markdown('<div class="unified-card">', unsafe_allow_html=True)
            st.subheader("ANALYSIS COMPLETE:")
            st.write(f"Order for reactant A (m): {m}")
            st.write(f"Order for reactant B (n): {n}")
            st.write(f"Rate Constant (k): {k:.4e} {unit}")
            
            st.markdown("---")
            st.subheader("SCIENTIFIC CONCLUSION:")
            st.write(f"The rate is proportional to [A]^{m} and [B]^{n}. According to collision theory, "
                     f"increasing concentration leads to more collisions and a faster rate.")
            
            # Show doubling logic
            c_a, c_b = st.columns(2)
            with c_a:
                st.write(f"**Reactant A (Order {m})**")
                st.write(f"Doubling [A] increases rate {2**m}x")
            with c_b:
                st.write(f"**Reactant B (Order {n})**")
                st.write(f"Doubling [B] increases rate {2**n}x")

            st.markdown("---")
            st.latex(rf"Rate = {k:.4e} \ {unit} \ [A]^{{{m}}} [B]^{{{n}}}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        else:
            st.error("Error: Could not find appropriate trials to determine orders.")
    except Exception as e:
        st.error(f"Calculation Error: {e}")

# 7. FOOTER
st.markdown("<p style='text-align: center;'>Learning Without Limits - Science Department</p>", unsafe_allow_html=True)
