import streamlit as st

st.title("Fast, Robust, and Approximately Correct")
st.subheader("Monte Carlo simulation results on the FRAC method of Salanié-Wolak 2026")
st.markdown(
    """
    This app shows detailed results of the simulations reported in sections 5 and 6
    and Appendix E of the paper:

    1. the distribution of the FRAC and MPEC estimates for a reasonably realistic 'macro-BLP' model,
    2. specification tests,
    3. variance decompositions of market shares and costs,
    4. and the asymptotic properties of FRAC in the many-market limit.

    Use the sidebar to move between pages.
    """
)
