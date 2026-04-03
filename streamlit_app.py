import streamlit as st
import math

# Page setup
st.set_page_config(page_title="Rate Law Determinator", page_icon="🧪")

st.title("🧪 Reaction Rate Law & Order Determinator")
st.write("Enter your experimental data below. Use scientific notation like **2e-3** for small numbers.")

# Organizing inputs into 4 columns for 4 trials
cols = st.columns(4)
trials = []

for i, col in enumerate(cols, 1):
    with col:
        st.markdown(f"### Trial {i}")
        a = st.number_input(f"Initial [A] (M)", key=f"a{i}", format="%.4e", value=0.1)
        b = st.number_input(f"Initial [B] (M)", key=f"b{i}", format="%.4e", value=0.1)
        r = st.number_input(f"Initial Rate", key=f"r{i}", format="%.4e", value=0.001)
        trials.append({'a': a, 'b': b, 'rate': r})

if st.button("Calculate Reaction Order & k"):
    m, n = None, None

    # Logic to find m (A) where B is constant
    for i in range(4):
        for j in range(4):
            if i != j and trials[i]['b'] == trials[j]['b'] and trials[i]['a'] != trials[j]['a']:
                m = round(math.log(trials[j]['rate'] / trials[i]['rate']) / math.log(trials[j]['a'] / trials[i]['a']))
                break
        if m is not None: break

    # Logic to find n (B) where A is constant
    for i in range(4):
        for j in range(4):
            if i != j and trials[i]['a'] == trials[j]['a'] and trials[i]['b'] != trials[j]['b']:
                n = round(math.log(trials[j]['rate'] / trials[i]['rate']) / math.log(trials[j]['b'] / trials[i]['b']))
                break
        if n is not None: break

    if m is not None and n is not None:
        overall = m + n
        t4 = trials[3]
        k = t4['rate'] / ((t4['a']**m) * (t4['b']**n))
        
        # Determine Units
        units = {0: "M/s", 1: "s⁻¹", 2: "M⁻¹s⁻¹", 3: "M⁻²s⁻¹"}
        unit = units.get(overall, f"M^{1-overall}s⁻¹")

        # --- Display Results ---
        st.success("## Analysis Results")
        c1, c2, c3 = st.columns(3)
        c1.metric("Order of A (m)", m)
        c2.metric("Order of B (n)", n)
        c3.metric("Overall Order", overall)
        
        st.info(f"**Rate Constant (k):** {k:.4e} {unit}")

        st.subheader("Scientific Explanation")
        st.write(f"The rate is proportional to $[A]^{m}$ and $[B]^{n}$. According to **Collision Theory**, increasing concentration increases the number of particles per volume, leading to more frequent collisions.")
        st.write(f"- For **A** (Order {m}): Doubling concentration increases rate by {2**m}x.")
        st.write(f"- For **B** (Order {n}): Doubling concentration increases rate by {2**n}x.")
        
        st.latex(rf"Rate = {k:.4e} \ {unit} \ [A]^{{{m}}} [B]^{{{n}}}")
    else:
        st.error("Error: Could not find trials with constant concentrations. Please check your data table.")
