if st.button("ANALYZE KINETICS"):
    # (Your calculation logic for m, n, and k here)
    
    if m is not None and n is not None:
        st.balloons()
        
        # Combine everything into ONE HTML string
        result_html = f"""
        <div class="results-card">
            <h2 style="color: #800000 !important; margin-bottom: 20px;">ANALYSIS COMPLETE</h2>
            <p style="font-size: 1.2rem;">
                <b>Order (m):</b> {m} | <b>Order (n):</b> {n} | <b>Rate Constant (k):</b> {k:.4e} {unit_display}
            </p>
            <hr style="border: 1px solid #800000; margin: 25px 0;">
            <h3 style="color: #800000 !important;">SCIENTIFIC CONCLUSION</h3>
            <p>
                Collision theory dictates that for a reaction to occur, particles must collide with sufficient energy 
                and correct orientation. By increasing the concentration, the frequency of these collisions per 
                unit of time increases, which directly results in a higher reaction rate.
            </p>
            <div style="display: flex; justify-content: space-around; margin-top: 30px; font-weight: bold;">
                <div>Reactant A (Order {m})<br>Doubling [A] increases rate {2**m}x</div>
                <div>Reactant B (Order {n})<br>Doubling [B] increases rate {2**n}x</div>
            </div>
        </div>
        """
        st.markdown(result_html, unsafe_allow_html=True)
        
        # Display LaTeX immediately after the white box
        st.latex(rf"Rate = [{k:.4e}] \ [A]^{{{m}}} [B]^{{{n}}}")
