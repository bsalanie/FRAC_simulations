import streamlit as st

from utils.params_monte_carlo import app_root

plots_dir = app_root / "asymptotic_plots"

uni_pi = "\N{GREEK SMALL LETTER PI}"
uni_S0 = "S\N{SUBSCRIPT ZERO}"

nmarkets = 5000


st.title("Asymptotic performance of FRAC estimators")
st.markdown(
    r"""
    We show the properties of the FRAC(D) and the corrected estimators
    in the many-market limit $T=\infty$:

    * the pseudo-true values to which they converge
    * for comparison, the semiparametric efficiency bounds.
    """
)

st.sidebar.markdown(
    r"""
    ### The simulation setup

    It is described in section 5 of Salanié-Wolak (2026).

    This is a discrete choice model on market-level data, with multinomial logit idiosyncratic preference shocks.

    It has one covariate: the log-price. The distribution of its random coefficients depends
    on an exogenous observed variable $D$ (the 'micromoment').

    The true values of the parameters are chosen so that the own price semi-elasticity is roughly -2
    and the outside good has a market share of 0.5 or 0.9.

    ### Special cases

    The *exogenous* models have price independent of product effects;
    the models *without a micromoment* have $D\equiv 0$.
    """
)

st.subheader("Notes on the graphs")
st.markdown(
    """
    The graphs show various simulation results as the variance of the random coefficient varies.

    The 95% confidence intervals shown are computed using the semiparametric efficiency bounds for 100 markets.

    Given the symmetry in the model, the cross-price semi-elasticities are the same for any two products;
    mean and dispersion are computed across markets.
    """
)


def plot_path(plot_type: str, nproducts: int, scenario: int, model: str, pi_num: int | None = None):
    plot_dir = plots_dir / f"J{nproducts}" / f"{model}_v{scenario}" / "figures_paper"
    T_str = f"T={nmarkets}" if pi_num is None else f"T={nmarkets}_pi{pi_num}"
    return plot_dir / f"{plot_type}_{model}_J={nproducts}_v{scenario}_{T_str}.png"


labels_plot_types = {
    "new_pseudo_vals": "Pseudo-true values",
    "new_semi_elast": "Semi-elasticities",
}
labels_scenarii = {4: f"{uni_S0} close to 0.9", 3: f"{uni_S0} close to 0.5"}
labels_models = {
    "endo_demog": "Endogenous, with a micromoment",
    "endo": "Endogenous, no micromoment",
    "exo_demog": "Exogenous, with a micromoment",
    "exo": "Exogenous, no micromoment",
}
labels_pi = {0: "0.25", 1: "0.5", 2: "1.0"}

plot_types = st.pills(
    "Plot type",
    options=list(labels_plot_types),
    selection_mode="multi",
    format_func=labels_plot_types.get,
    default=["new_pseudo_vals"],
)
scenarii = st.pills(
    "Market share of the zero good",
    options=list(labels_scenarii),
    selection_mode="multi",
    format_func=labels_scenarii.get,
    default=[4],
)
models = st.pills(
    "Model",
    options=list(labels_models),
    selection_mode="multi",
    format_func=labels_models.get,
    default=["endo_demog"],
)
J_vals = st.pills(
    "Number of products",
    [1, 2, 5, 10, 25, 50, 100],
    selection_mode="multi",
    default=[25],
)

pi_vals = []
if any("demog" in model for model in models):
    pi_vals = st.pills(
        f"Value of {uni_pi} (the mean coefficient of the micromoment)",
        options=list(labels_pi),
        selection_mode="multi",
        format_func=labels_pi.get,
        default=[1],
    )

paths = []
for plot_type in plot_types:
    for scenario in scenarii:
        for J in J_vals:
            for model in models:
                if "demog" in model:
                    for pi_num in pi_vals:
                        caption = f"{labels_models[model]}, J={J}, {labels_scenarii[scenario]}, {uni_pi}={labels_pi[pi_num]}"
                        paths.append((plot_path(plot_type, J, scenario, model, pi_num), caption))
                else:
                    caption = f"{labels_models[model]}, J={J}, {labels_scenarii[scenario]}"
                    paths.append((plot_path(plot_type, J, scenario, model), caption))

st.subheader("Your plots")
if not paths:
    st.info("Choose at least one option in each row to see plots.")
for path, caption in paths:
    st.image(path, caption=caption, alt=f"{caption}: {path.stem}")
