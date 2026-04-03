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
        margin-bottom: 15px !important;
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
    div[data-baseweb="select"] {{ background-color: white !important; border-radius: 10px !important; }}
    input {{ color: black !important; text-shadow: none !important; font-weight: bold !important; }}
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

# 4. Expert Selection
st.markdown('<div class="unified-card">', unsafe_allow_html=True)
num_trials = st.selectbox("Select Number of Experimental Trials", options=[3, 4], index=1)
st.markdown('</div>', unsafe_allow_html=True)

# 5. Dynamic Input Layout
cols = st.columns(num_trials)
trials_data = []

for i, col in enumerate(cols, 1):
    with col:
        st.markdown(f'<div class="unified-card"><h3 style="margin: 0;">Trial {i}</h3></div>', unsafe_allow_html=True)
        a = st.number_input(f"Initial [A] (M)", key=f"a{i}", format="%.4e", value=0.1)
        b = st.number_input(f"Initial [B] (M)", key=f"b{i}", format="%.4e", value=0.1)
        r = st.number_input(f"Initial Rate (M/s)", key=f"r{i}", format="%.4e", value=0.001)
        trials_data.append({'a': a, 'b': b, 'rate': r})

# 6. Optimized Calculation Logic
st.markdown("<br>", unsafe_allow_html=True)
if st.button("Analyze Reaction Kinetics", type="primary", use_container_width=True):
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
            k = active_trials[0]['rate'] / ((active_trials[0]['a']**m) * (active_trials[0]['b']**n))
            
            units = {0: "M/s", 1: "s⁻¹", 2: "M⁻¹s⁻¹", 3: "M⁻²s⁻¹"}
            unit = units.get(overall_order, f"M^{1-overall_order}s⁻¹")

            st.balloons()
            # Result Display
            st.markdown('<div class="unified-card">', unsafe_allow_html=True)
            st.subheader("ANALYSIS COMPLETE")
            st.write(f"**Order for reactant A (m):** {m}")
            st.write(f"**Order for reactant B (n):** {n}")
            st.write(f"**Overall Reaction Order:** {overall_order}")
            st.write(f"**Rate Constant (k):** {k:.4e} {unit}")
            st.latex(rf"FINAL \ RATE \ LAW: Rate = {k:.4e} \ {unit} \ [A]^{{{m}}} [B]^{{{n}}}")
            st.markdown('</div>', unsafe_allow_html=True)

            # --- YOUR ORIGINAL SCIENTIFIC EXPLANATION RESTORED ---
            st.markdown('<div class="unified-card">', unsafe_allow_html=True)
            st.subheader("SCIENTIFIC CONCLUSION")
            
            explanation_text = (
                f"The rate is proportional to the concentration of A to the power of {m} and B to the power of {n}. "
                f"According to collision theory, increasing concentration means there are more particles per volume, "
                f"leading to more collisions and a faster rate. The value of k and its unit ({unit}) "
                f"reflect the specific speed and order of this reaction."
            )
            st.write(explanation_text)
            
            st.markdown("---")
            col_a, col_b = st.columns(2)
            with col_a:
                st.write(f"**For reactant A (Order {m}):**")
                st.write(f"- Doubling [A] increases the rate by a factor of {2**m}.")
                st.write(f"- Halving [A] decreases the rate by a factor of {2**m}.")
            with col_b:
                st.write(f"**For reactant B (Order {n}):**")
                st.write(f"- Doubling [B] increases the rate by a factor of {2**n}.")
                st.write(f"- Halving [B] decreases the rate by a factor of {2**n}.")
            st.markdown('</div>', unsafe_allow_html=True)
            
        else:
            st.error("Scientific Error: No constant concentration pairs found. Please check your experimental data.")

    except Exception as e:
        st.error(f"Input Error: Ensure all fields contain valid experimental numbers.")

st.markdown("<p style='text-align: center;'>Learning Without Limits - Science Department</p>", unsafe_allow_html=True)
