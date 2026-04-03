import streamlit as st
import math
import base64
from datetime import datetime
import pytz

# 1. Page Configuration
st.set_page_config(page_title="Britus International School Bahrain", layout="wide")

# 2. Background Loader
def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except: return ""

bin_str = get_base64('my_background.jpg')

# 3. EXPERT CSS: This styles the actual Streamlit "Main" area directly
st.markdown(f"""
    <style>
    /* Sets the background for the whole page */
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
    }}

    /* THE FIX: Style the Streamlit "Block Container" to be your Navy/Red box */
    [data-testid="stVerticalBlock"] > div:nth-child(2) {{
        background-color: rgba(0, 33, 71, 0.9) !important;
        padding: 50px !important;
        border-radius: 30px !important;
        border: 5px solid #800000 !important;
        box-shadow: 0px 20px 40px rgba(0,0,0,0.8) !important;
    }}

    /* FORCE ALL TEXT TO BE WHITE */
    /* Target labels, headers, and plain text */
    h1, h2, h3, p, span, label, [data-testid="stWidgetLabel"] {{
        color: white !important;
        text-align: center !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,1) !important;
    }}

    /* Centering the Banner */
    [data-testid="stImage"] {{
        display: flex;
        justify-content: center;
    }}

    /* The Bahrain Clock styling */
    .clock-style {{
        background-color: #800000;
        color: white;
        padding: 10px 25px;
        border-radius: 50px;
        font-weight: bold;
        border: 2px solid white;
        margin: 0 auto 20px auto;
        display: table;
    }}

    /* Input box text stays black for typing visibility */
    input {{
        color: black !important;
        text-align: left !important;
        text-shadow: none !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. Top Banner
try:
    st.image("britus_banner.png", use_container_width=True)
except:
    pass

# 5. Bahrain Clock
bahrain_tz = pytz.timezone('Asia/Bahrain')
st.markdown(f"<div class='clock-style'>🕒 {datetime.now(bahrain_tz).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# 6. CONTENT (Everything here will automatically be inside the box)
st.title("🧪 Chemical Kinetics: Rate Law Determinator")
st.write("Calculate Reaction Orders and Rate Constants effortlessly.")
st.divider()

# Trial Input Grid
cols = st.columns(4)
trials = []
for i, col in enumerate(cols, 1):
    with col:
        st.subheader(f"Trial {i}")
        a = st.number_input(f"Initial [A] (M)", key=f"a{i}", format="%.4e", value=0.1)
        b = st.number_input(f"Initial [B] (M)", key=f"b{i}", format="%.4e", value=0.1)
        r = st.number_input(f"Initial Rate", key=f"r{i}", format="%.4e", value=0.001)
        trials.append({'a': a, 'b': b, 'rate': r})

st.write("") # Padding
if st.button("Calculate Results", type="primary"):
    try:
        # Standard chemical kinetics logic
        m = round(math.log(trials[1]['rate'] / trials[0]['rate']) / math.log(trials[1]['a'] / trials[0]['a']))
        n = round(math.log(trials[2]['rate'] / trials[0]['rate']) / math.log(trials[2]['b'] / trials[0]['b']))
        k = trials[0]['rate'] / ((trials[0]['a']**m) * (trials[0]['b']**n))
        
        st.balloons()
        st.success(f"Successfully Determined!")
        st.write(f"Order of A: **{m}** | Order of B: **{n}**")
        st.latex(rf"Rate = {k:.4e} \ [A]^{{{m}}} [B]^{{{n}}}")
    except:
        st.error("Error: Please check your data. Ensure constant concentrations exist between trials.")

# 7. Footer
st.divider()
st.markdown("Learning Without Limits - Science Department")
