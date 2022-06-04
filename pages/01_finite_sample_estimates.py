import streamlit as st
import seaborn as sns
import pandas as pd

from utils.params_monte_carlo import (
    data_dir,
    headers_coeffs,
    str_coeffs,
    gamma_vals,
    var_xi_vals,
    var_omega_vals,
    sigma2_vals,
    basic_values,
    headers_demand_betas,
    headers_demand_sigmas,
    headers_supply,
)
from utils.plot_densities import plot_estimates


sns.set_context("notebook")
sns.set_style("whitegrid")

st.markdown("## Finite sample simulations:")
st.markdown("###\t\tFRAC and MPEC estimates")
st.sidebar.subheader("Using FRAC as per Salani&eacute;-Wolak (2022)")


@st.cache(persist=True)
def load_results():
    df_results = pd.read_pickle(f"{data_dir}/df_results.pkl")
    # make pretty LaTeX names
    df_results["Parameter"] = df_results["Parameter"].map(
        {k: v for (k, v) in zip(headers_coeffs, str_coeffs)}
    )
    return df_results


df_results = load_results()

gamma_val = st.selectbox("Choose a value for gamma", gamma_vals)
# var_omega = st.selectbox("Choose a value for var_omega", var_omega_vals)
var_omega = 0.2
var_xi = st.selectbox("Choose a value for var_xi", var_xi_vals)
sigma2 = st.selectbox("Choose a value for sigma2", sigma2_vals)

subcase = (sigma2, gamma_val, var_xi, var_omega)

# plots for the mean coefficients of demand
true_vals = [basic_values[j] for j in headers_demand_betas]
g = plot_estimates(
    df_results,
    subcase,
    "means_betas",
    true_vals,
)
st.markdown("#### Distribution of the estimates of the mean coefficients of demand:")
st.pyplot(g)

# plots for the variances of the coefficients of demand
true_vals = [
    basic_values[j] * sigma2 / basic_values["var_1"] for j in headers_demand_sigmas
]
g = plot_estimates(
    df_results,
    subcase,
    "variances_betas",
    true_vals,
)
st.markdown(
    "#### Distribution of the estimates of the variances of the coefficients of demand:"
)

st.pyplot(g)
# plots for the coefficients of supply
true_vals = [basic_values["gamma_0"]] + [
    basic_values[j] * gamma_val / basic_values["gamma_1"] for j in headers_supply[1:]
]
g = plot_estimates(
    df_results,
    subcase,
    "gammas",
    true_vals,
)
st.markdown("#### Distribution of the estimates of the coefficients of supply:")

st.pyplot(g)
# # plots for the variance shares of demand
# true_vals = [basic_values[j] for j in headers_varianceshares_demand]
# plot_estimates(
#     df_results,
#     subcase,
#     "variance_shares_demand",
#     true_vals,
#     plots_dir / "plots_variance_shares",
# )
# # plots for the variance shares of supply
# true_vals = [basic_values[j] for j in headers_varianceshares_supply]
# plot_estimates(
#     df_results,
#     subcase,
#     "variance_shares_supply",
#     true_vals,
#     plots_dir / "plots_variance_shares",
# )
