import streamlit as st

from utils.params_monte_carlo import str_beta_1
from utils.plot_var_select import plot_pvalues


st.markdown("# Finite sample simulations")
st.sidebar.markdown("# Finite sample simulations")

plot_pvalues("beta_1", str_beta_1)
