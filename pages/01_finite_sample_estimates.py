import streamlit as st
import seaborn as sns
import pandas as pd

from utils.params_monte_carlo import (
    data_dir,
    headers_coeffs,
    str_coeffs,
    gamma_vals,
    var_xi_vals,
    sigma2_vals,
    basic_values,
    headers_demand_betas,
    headers_demand_sigmas,
    headers_supply,
)
from utils.plot_densities import plot_estimates


uni_sigma2 = "\N{GREEK SMALL LETTER SIGMA}\N{SUPERSCRIPT TWO}"


sns.set_context("notebook")
sns.set_style("whitegrid")

st.markdown("## Finite sample simulations:")
st.markdown("###\t\tFRAC and MPEC estimates")

st.sidebar.markdown(
    """
    ### The simulation setup:
    
    It is described in section 7 of Salani&eacute;-Wolak (2022);
    it adapts  Dub&eacute;-Fox-Su (*Eca* 2012).

    There are $T=50$ markets and $J=25$ products in each market, 
    and three observed product characteristics in addition to the price. 

    Instead of a reduced form price equation that induces correlation between price and product effects,
    we specify a cost side of the market and solve the first-order conditions for profit-maximization 
    to compute the market clearing prices.
    """
)


@st.cache(persist=True)
def load_results():
    df_results = pd.read_pickle(f"{data_dir}/df_results.pkl")
    # make pretty LaTeX names
    df_results["Parameter"] = df_results["Parameter"].map(
        {k: v for (k, v) in zip(headers_coeffs, str_coeffs)}
    )
    return df_results


df_results = load_results()

gamma_val = st.selectbox(
    "Choose a scale factor for the marginal cost:",
    gamma_vals,
    # default=[0.1],
)
# var_omega = st.selectbox("Choose a value for var_omega", var_omega_vals)
var_omega = 0.2
var_xi = st.selectbox(
    "Choose a value for the variance of the product effects:",
    var_xi_vals,
    # default=[0.5],
)
sigma2 = st.selectbox(
    "Choose a scale factor for the variance of the random coefficients:",
    sigma2_vals,
    # default=[0.5],
)

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
