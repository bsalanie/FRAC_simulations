from PIL import Image
import streamlit as st
import seaborn as sns

from typing import List
from functools import partial

DATA_URL = "./variance_shares_plots"


sns.set_context("notebook")
sns.set_style("whitegrid")


st.markdown("## Finite sample simulations:")
st.markdown("###\t\tVariance decompositions")


st.sidebar.markdown(
    """
    **The simulation setup:**
    
    It is described in section 7 of Salani&eacute;-Wolak (2022);
    it adapts  Dub&eacute;-Fox-Su (*Eca* 2012).

    We show what accounts for the variation in market shares and in marginal costs 
    in our simulations.

    *For market shares:*
    * $V^D_1$ is the proportion of the variance that comes from the covariates and the (instrumented) prices
    * $V^D_2$ is the proportion that comes from the unobserved product effects
    * $V^D_3$ is due to the idiosyncratic factors.

    *For the (log-) marginal cost:*
    * $V^S_1$ is the proportion of the variance that comes from the covariates
    * $V^S_2$ is the proportion that comes from the unobserved product effects
    * $V^S_3$ is due to the idiosyncratic factors.
    """
)

st.markdown("### Notes on the graphs")

st.markdown(
    """
    The graphs show the average proportion of the variance across the 
    simulated samples. Each panel corresponds to a value of $\sigma^2$ and of the variance of the product effects.
    """
)

st.markdown(
    """
    You can choose to see the decomposition for demand and/or supply,
    the value of $\gamma_1$ (which indexes the strength of the supply-side
    instruments).
    """
)


@st.cache(persist=True)
def load_plot(plot_gamma: float, side: str):
    mside = side.lower()
    plot_dir = f"{DATA_URL}"
    plot_str = f"variance_shares_{mside}_g{gamma_val}"
    our_plot = Image.open(f"{plot_dir}/{plot_str}.png")
    return our_plot


options_gamma = ["0.1", "0.2"]

plot_gammas = st.multiselect(
    "Choose the value(s) of " + r"$\gamma_1$",
    options=options_gamma,
    default=["0.1"],
)

options_side = ["Demand", "Supply"]

plot_side = st.multiselect(
    "Choose the market side",
    options=options_side,
    default=["Demand"],
)


st.subheader("Here are your plots:")
for gamma_val in plot_gammas:
    for side in plot_side:
        plot_g = load_plot(gamma_val, side)
        st.image(plot_g)
