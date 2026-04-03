import streamlit as st
import math
from datetime import datetime
import pytz

# 1. Setup
st.set_page_config(page_title="Britus International School", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1532187891246-1f3b0fe44383?auto=format&fit=crop&w=1920&q=80");
        background-size: cover;
    }
    .calculator-box {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 30px;
        border-radius: 20px;
        border: 4px solid #800000;
        box-shadow: 10px 10px 20px rgba(0,0,0,0.3);
    }
    .clock-style {
        background-color: #002147;
        color: white;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        width: 200px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Banner & Clock
st.image("britus_banner.png", use_container_width=True)

bahrain_tz = pytz.timezone('Asia/Bahrain')
st.markdown(f"<div class='clock-style'>🕒 {datetime.now(bahrain_tz).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# 3. Calculator Box
st.markdown('<div class="calculator-box">', unsafe_allow_html=True)
st.title("🧪 Reaction Rate Law & Order Determinator")

cols = st.columns(4)
trials = []
for i, col in enumerate(cols, 1):
    with col:
        st.markdown(f"### Trial {i}")
        a = st.number_input(f"Initial [A]", key=f"a{i}", format="%.4e", value=0.1)
        b = st.number_input(f"Initial [B]", key=f"b{i}", format="%.4e", value=0.1)
        r = st.number_input(f"Rate", key=f"r{i}", format="%.4e", value=0.001)
        trials.append({'a': a, 'b': b, 'rate': r})

if st.button("Calculate"):
    # (Your math logic)
    m = round(math.log(trials[1]['rate'] / trials[0]['rate']) / math.log(trials[1]['a'] / trials[0]['a']))
    n = round(math.log(trials[2]['rate'] / trials[0]['rate']) / math.log(trials[2]['b'] / trials[0]['b']))
    k = trials[0]['rate'] / ((trials[0]['a']**m) * (trials[0]['b']**n))
    
    st.balloons()
    st.success(f"Order A: {m} | Order B: {n}")
    st.info(f"Rate Constant (k): {k:.4e}")
    st.latex(rf"Rate = {k:.4e} \ [A]^{{{m}}} [B]^{{{n}}}")

st.markdown('</div>', unsafe_allow_html=True)
