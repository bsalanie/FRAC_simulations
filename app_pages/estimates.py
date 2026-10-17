import pandas as pd
import streamlit as st

from utils.app_helpers import set_plot_style, show_grids
from utils.params_monte_carlo import (
    basic_values,
    data_dir,
    gamma_vals,
    headers_coeffs,
    headers_demand_betas,
    headers_demand_sigmas,
    headers_supply,
    sigma2_vals,
    str_coeffs,
    var_xi_vals,
)
from utils.plot_densities import plot_estimates

set_plot_style()

st.title("Finite sample simulations")
st.header("FRAC and MPEC estimates")


st.sidebar.markdown(
    """
    ### The simulation setup

    It is described in section 6 of Salanié-Wolak (2026);
    it adapts Dubé-Fox-Su (*Eca* 2012).

    There are $T=50$ markets and $J=25$ products in each market,
    and three observed product characteristics in addition to the price.

    Instead of a reduced form price equation that induces correlation between price and product effects,
    we specify a cost side of the market and solve the first-order conditions for profit-maximization
    to compute the market clearing prices.
    """
)


@st.cache_data(persist="disk")
def load_results():
    df_results = pd.read_pickle(data_dir / "df_results.pkl")
    # make pretty LaTeX names
    df_results["Parameter"] = df_results["Parameter"].map(
        {k: v for (k, v) in zip(headers_coeffs, str_coeffs)}
    )
    return df_results


with st.container(horizontal=True):
    gamma_val = st.segmented_control(
        "Scale factor for the marginal cost",
        gamma_vals,
        default=gamma_vals[0],
        required=True,
    )
    var_xi = st.segmented_control(
        "Variance of the product effects",
        var_xi_vals,
        default=var_xi_vals[0],
        required=True,
    )
    sigma2 = st.segmented_control(
        "Scale factor for the variance of the random coefficients",
        sigma2_vals,
        default=sigma2_vals[0],
        required=True,
    )
var_omega = 0.2

df_results = load_results()

subcase = (sigma2, gamma_val, var_xi, var_omega)

# plots for the mean coefficients of demand
st.subheader("Distribution of the estimates of the mean coefficients of demand")
true_vals = [basic_values[j] for j in headers_demand_betas]
show_grids(
    lambda: plot_estimates(df_results, subcase, "means_betas", true_vals),
    alt="Densities of the estimates of the mean coefficients of demand",
)

# plots for the variances of the coefficients of demand
st.subheader(
    "Distribution of the estimates of the variances of the coefficients of demand"
)
true_vals = [
    basic_values[j] * sigma2 / basic_values["var_1"] for j in headers_demand_sigmas
]
show_grids(
    lambda: plot_estimates(df_results, subcase, "variances_betas", true_vals),
    alt="Densities of the estimates of the variances of the coefficients of demand",
)

# plots for the coefficients of supply
st.subheader("Distribution of the estimates of the coefficients of supply")
true_vals = [basic_values["gamma_0"]] + [
    basic_values[j] * gamma_val / basic_values["gamma_1"] for j in headers_supply[1:]
]
show_grids(
    lambda: plot_estimates(df_results, subcase, "gammas", true_vals),
    alt="Densities of the estimates of the coefficients of supply",
)
