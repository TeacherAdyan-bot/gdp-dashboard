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
    except:
        return ""

bin_str = get_base64('my_background.jpg')

# 2. CSS (FINAL CLEAN VERSION)
st.markdown(f"""
<style>
.stApp {{
    background-image: url("data:image/png;base64,{bin_str}");
    background-size: cover;
    background-attachment: fixed;
}}

/* TEXT ONLY */
h1, h2, h3, h4, p, span {{
    color: white !important;
    text-align: center !important;
}}

/* NAVY BOXES */
.trial-header {{
    background-color: rgba(0, 33, 71, 0.95);
    padding: 15px;
    border-radius: 20px;
    border: 4px solid #800000;
    margin-bottom: 15px;
}}

.results-card {{
    background-color: rgba(0, 33, 71, 0.95);
    padding: 30px;
    border-radius: 25px;
    border: 4px solid #800000;
    margin-top: 30px;
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
}}

/* INPUTS FIX */
input {{
    color: black !important;
}}

div[data-baseweb="select"] span {{
    color: black !important;
}}

/* BUTTON */
.stButton>button {{
    background-color: #800000;
    color: white;
    border-radius: 12px;
    font-size: 1.1rem;
    width: 100%;
}}
</style>
""", unsafe_allow_html=True)

# 3. HEADER
try:
    st.image("britus_banner.png", use_container_width=True)
except:
    pass

# CLOCK (FIXED COLOR)
bahrain_tz = pytz.timezone('Asia/Bahrain')
st.markdown(
    f"<div style='background-color:#800000; color:white; padding:8px 25px; border-radius:50px; font-weight:bold; border:2px solid white; margin:0 auto 20px auto; display:table;'>🕒 {datetime.now(bahrain_tz).strftime('%H:%M:%S')}</div>",
    unsafe_allow_html=True
)

st.markdown('<div class="trial-header"><h1>🧪 Chemical Kinetics: Rate Law Determinator</h1></div>', unsafe_allow_html=True)

# 4. TRIAL SELECTION
st.markdown("### Select Number of Experimental Trials")
num_trials = st.selectbox("Trials", options=[3, 4], index=1, label_visibility="collapsed")

# 5. INPUTS
cols = st.columns(num_trials)
trials_data = []

for i, col in enumerate(cols, 1):
    with col:
        st.markdown(f'<div class="trial-header"><h3>Trial {i}</h3></div>', unsafe_allow_html=True)
        a = st.number_input(f"[A] (M)", key=f"a{i}", value=0.1)
        b = st.number_input(f"[B] (M)", key=f"b{i}", value=0.1)
        r = st.number_input(f"Rate (M/s)", key=f"r{i}", value=0.001)
        trials_data.append({'a': a, 'b': b, 'rate': r})

# 6. ANALYSIS
if st.button("ANALYZE KINETICS"):
    try:
        m, n = None, None
        active = trials_data

        # FIND m
        for i in range(num_trials):
            for j in range(num_trials):
                if i != j and active[i]['b'] == active[j]['b'] and active[i]['a'] != active[j]['a']:
                    m = round(math.log(active[j]['rate']/active[i]['rate']) /
                              math.log(active[j]['a']/active[i]['a']))
                    break
            if m is not None:
                break

        # FIND n
        for i in range(num_trials):
            for j in range(num_trials):
                if i != j and active[i]['a'] == active[j]['a'] and active[i]['b'] != active[j]['b']:
                    n = round(math.log(active[j]['rate']/active[i]['rate']) /
                              math.log(active[j]['b']/active[i]['b']))
                    break
            if n is not None:
                break

        if m is not None and n is not None:
            overall = m + n
            t = active[-1]
            k = t['rate'] / ((t['a']**m)*(t['b']**n))

            result_html = f"""
            <div class="results-card">

            <h2>🧪 ANALYSIS COMPLETE</h2>

            <h3>🔢 Determined Values</h3>
            <p>
            Order of A (m) = <b>{m}</b><br>
            Order of B (n) = <b>{n}</b><br>
            Overall Order = <b>{overall}</b><br>
            Rate Constant (k) = <b>{k:.2e} M<sup>{1-overall}</sup>s<sup>-1</sup></b>
            </p>

            <h3>⚗️ Rate Equation</h3>
            <p><b>Rate = {k:.2e} [A]<sup>{m}</sup> [B]<sup>{n}</sup></b></p>

            <h3>🧠 Scientific Explanation</h3>
            <p>
            According to collision theory, increasing concentration increases the number of particles per unit volume,
            leading to more frequent effective collisions.
            </p>

            <p>
            <b>Reactant A:</b> doubling [A] → rate ×{2**m}<br>
            <b>Reactant B:</b> doubling [B] → rate ×{2**n}
            </p>

            <p>
            Since the overall order is <b>{overall}</b>, the reaction depends strongly on concentration,
            especially reactant B.
            </p>

            <h3>📌 Conclusion</h3>
            <p>
            Reactant B has a greater influence on the reaction rate than reactant A.
            </p>

            </div>
            """

            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                st.markdown(result_html, unsafe_allow_html=True)

        else:
            st.error("Could not determine reaction orders.")

    except Exception as e:
        st.error(f"Error: {e}")

