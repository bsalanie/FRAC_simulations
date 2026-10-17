import streamlit as st

from utils.params_monte_carlo import app_root

plots_dir = app_root / "variance_shares_plots"


st.title("Finite sample simulations")
st.header("Variance decompositions")


st.sidebar.markdown(
    """
    ### The simulation setup

    It is described in section 6 of Salanié-Wolak (2026);
    it adapts Dubé-Fox-Su (*Eca* 2012).

    We show what accounts for the variation in market shares and in marginal costs
    in our simulations (as in Appendix E of Salanié-Wolak 2026).

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

st.subheader("Notes on the graphs")

st.markdown(
    r"""
    The graphs show the average proportion of the variance across the
    simulated samples. Each panel corresponds to a value of $\sigma^2$ and of the variance of the product effects.

    You can choose to see the decomposition for demand and/or supply,
    and the value of $\gamma_1$ (which indexes the strength of the supply-side
    instruments).
    """
)


with st.container(horizontal=True):
    plot_gammas = st.pills(
        r"Value(s) of $\gamma_1$",
        options=["0.1", "0.2"],
        selection_mode="multi",
        default=["0.1"],
    )
    plot_sides = st.pills(
        "Market side",
        options=["Demand", "Supply"],
        selection_mode="multi",
        default=["Demand"],
    )


if not plot_gammas or not plot_sides:
    st.info(r"Choose at least one value of $\gamma_1$ and one market side.")

for gamma_val in plot_gammas:
    for side in plot_sides:
        st.image(
            plots_dir / f"variance_shares_{side.lower()}_g{gamma_val}.png",
            alt=f"Variance decomposition for {side.lower()}, gamma_1 = {gamma_val}",
        )
