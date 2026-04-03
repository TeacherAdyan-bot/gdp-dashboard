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

# 2. Expert CSS (Branding & Global Styles)
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
    /* Style for the Dropdown */
    div[data-baseweb="select"] {
        background-color: white !important;
        border-radius: 10px !important;
    }
    input { color: black !important; text-shadow: none !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. Header & Clock
try:
    st.image("britus_banner.png", use_container_width=True)
except: pass

bahrain_tz = pytz.timezone('Asia/Bahrain')
st.markdown(f"<div class='clock-style'>🕒 {datetime.now(bahrain_tz).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

st.markdown("""
    <div class="unified-card">
        <h1 style="margin: 0; padding: 10px;">🧪 Chemical Kinetics: Rate Law Determinator</h1>
    </div>
    """, unsafe_allow_html=True)

# --- 4. EXPERT DROPDOWN SELECTION ---
st.markdown('<div class="unified-card">', unsafe_allow_html=True)
num_trials = st.selectbox(
    "Select Number of Experimental Trials",
    options=[3, 4],
    index=1,  # Defaults to 4
    help="Choose 3 or 4 trials based on your lab data."
)
st.markdown('</div>', unsafe_allow_html=True)

# 5. Experimental Trials (Dynamic Layout)
cols = st.columns(num_trials)
trials = []

for i, col in enumerate(cols, 1):
    with col:
        st.markdown(f'<div class="unified-card"><h3 style="margin: 0;">Trial {i}</h3></div>', unsafe_allow_html=True)
        a = st.number_input(f"Initial [A] (M)", key=f"a{i}", format="%.4e", value=0.1)
        b = st.number_input(f"Initial [B] (M)", key=f"b{i}", format="%.4e", value=0.1)
        r = st.number_input(f"Initial Rate (M/s)", key=f"r{i}", format="%.4e", value=0.001)
        trials.append({'a': a, 'b': b, 'rate': r})

# 6. Calculation Logic
st.markdown("<br>", unsafe_allow_html=True)
if st.button("Analyze Reaction Kinetics", type="primary", use_container_width=True):
    try:
        m, n = None, None

        # Search through selected number of trials to find m
        for i in range(num_trials):
            for j in range(num_trials):
                if i != j and trials[i]['b'] == trials[j]['b'] and trials[i]['a'] != trials[j]['a']:
                    m = round(math.log(trials[j]['rate'] / trials[i]['rate']) / math.log(trials[j]['a'] / trials[i]['a']))
                    break
            if m is not None: break

        # Search through selected number of trials to find n
        for i in range(num_trials):
            for j in range(num_trials):
                if i != j and trials[i]['a'] == trials[j]['a'] and trials[i]['b'] != trials[j]['b']:
                    n = round(math.log(trials[j]['rate'] / trials[i]['rate']) / math.log(trials[j]['b'] / trials[i]['b']))
                    break
            if n is not None: break

        if m is not None and n is not None:
            overall_order = m + n
            t_ref = trials[0]
            k = t_ref['rate'] / ((t_ref['a']**m) * (t_ref['b']**n))
            
            units = {0: "M/s", 1: "s⁻¹", 2: "M⁻¹s⁻¹", 3: "M⁻²s⁻¹"}
            unit = units.get(overall_order, f"M^{1-overall_order}s⁻¹")

            st.balloons()
            st.markdown('<div class="unified-card">', unsafe_allow_html=True)
            st.subheader("ANALYSIS COMPLETE")
            st.write(f"**Order for A (m):** {m} | **Order for B (n):** {n}")
            st.write(f"**Overall Order:** {overall_order}")
            st.latex(rf"Rate = {k:.4e} \ {unit} \ [A]^{{{m}}} [B]^{{{n}}}")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="unified-card">', unsafe_allow_html=True)
            st.subheader("SCIENTIFIC CONCLUSION")
            st.write(f"The rate is proportional to [A]^{m} and [B]^{n}. According to collision theory, increasing concentration increases particles per volume, leading to more collisions. The unit ({unit}) reflects the overall order {overall_order}.")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.write(f"**Reactant A (Order {m}):**")
                st.write(f"- Doubling [A] factor: {2**m}x")
                st.write(f"- Halving [A] factor: {2**m}x")
            with col_b:
                st.write(f"**Reactant B (Order {n}):**")
                st.write(f"- Doubling [B] factor: {2**n}x")
                st.write(f"- Halving [B] factor: {2**n}x")
            st.markdown('</div>', unsafe_allow_html=True)
            
        else:
            st.error("Scientific Error: Could not find trials with constant concentrations. Check your data.")

    except Exception as e:
        st.error("Input Error: Ensure all fields contain valid experimental numbers.")

st.markdown("<p style='text-align: center;'>Learning Without Limits - Science Department</p>", unsafe_allow_html=True)
