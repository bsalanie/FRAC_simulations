from PIL import Image
import streamlit as st
import seaborn as sns

from typing import List
from functools import partial

DATA_URL = "./asymptotic_plots"

uni_pi = "\N{GREEK SMALL LETTER PI}"
uni_S0 = "S\N{SUBSCRIPT ZERO}"

nmarkets = 5000

sns.set_context("notebook")
sns.set_style("whitegrid")


st.markdown(
    """
    ## Asymptotic performance of FRAC estimators
    
    We show the properties of the FRAC(D) and the corrected estimators
    in the many-market limit $T=\infty$:

    * the pseudo-true values to which they converge
    * for comparison, the semiparametric efficiency bounds.
    """
)

st.sidebar.subheader("The simulation setup:")
st.sidebar.markdown(
    """
    It is described in section 6 of Salani&eacute;-Wolak (2022).

    This is a discrete choice model on market-level data, with multinomial logit idiosyncratic preference shocks.
    
    It has one covariate: the log-price. The distribution of its random coefficients depends 
    on an exopgenous observed variable $D$  (the 'micromoment').

    The true values of the parameters are chosen  so that the own price semi-elasticity is roughly -2
    and the outside good has a market share of 0.5 or 0.9.
    """
)

st.sidebar.subheader("Special cases:")
st.sidebar.markdown(
    """
    The *exogenous* models have price independent of product effects;
    
    the models *without a micromoment* have $D\equiv 0$.
    """
)

st.markdown("### Notes on the graphs")
st.markdown(
    """
    The graphs show various simulation results as the variance of the random coefficient varies.

    The 95% confidence intervals shown are computed using the semiparametric efficiency bounds for 100 markets.
    """
)
st.write(
    """
    Given the symmetry in the model, the cross-price semi-elasticities are the same for any two products; "
    mean and dispersion are computed across markets.
    """
)


@st.cache(persist=True)
def load_plot(
    plot_type: str, nproducts: int, scenario: int, model: str, pi_num: int = None
):
    plot_dir = f"{DATA_URL}/J{nproducts}/{model}_v{scenario}/figures_paper"
    T_str = f"T={nmarkets}" if pi_num is None else f"T={nmarkets}_pi{pi_num}"
    plot_root = f"{plot_dir}/{plot_type}_{model}_" + f"J={nproducts}_v{scenario}"
    our_plot = Image.open(f"{plot_root}_{T_str}.png")
    return our_plot


labels_plot_types = ["Pseudo-true values", "Semi-elasticities"]

options_plot_types = ["new_pseudo_vals", "new_semi_elast"]


def format_f(s: str, list_s: List[str], list_labels: List[str]) -> str:
    for i, optn in enumerate(list_s):
        if s == optn:
            return list_labels[i]


plot_types = st.multiselect(
    "Choose the plot type:",
    options=options_plot_types,
    format_func=partial(
        format_f, list_s=options_plot_types, list_labels=labels_plot_types
    ),
    default=["new_pseudo_vals"],
)

options_scenarii = [4, 3]
S0_9 = f"{uni_S0} close to 0.9"
S0_5 = f"{uni_S0} close to 0.5"
labels_scenarii = [S0_9, S0_5]
scenarii = st.multiselect(
    "Choose the market share of the zero good:",
    options=options_scenarii,
    format_func=partial(
        format_f,
        list_s=options_scenarii,
        list_labels=labels_scenarii,
    ),
    default=[4],
)


options_models = ["endo_demog", "endo", "exo_demog", "exo"]
labels_models = [
    "Endogenous, with a micromoment",
    "Endogenous, no micromoment",
    "Exogenous, with a micromoment",
    "Exogenous, no micromoment",
]

models = st.multiselect(
    "Choose the model:",
    options=options_models,
    format_func=partial(
        format_f,
        list_s=options_models,
        list_labels=labels_models,
    ),
    default=["endo_demog"],
)

J_vals = st.multiselect(
    "Choose the number of products:", [1, 2, 5, 10, 25, 50, 100], default=[25]
)

options_pi = [0, 1, 2]
labels_pi = ["0.25", "0.5", "1.0"]

if "endo_demog" in models or "exo_demog" in models:
    pi_vals = st.multiselect(
        f"Choose the value of {uni_pi} (the mean coefficient of the micromoment)",
        options=options_pi,
        format_func=partial(format_f, list_s=options_pi, list_labels=labels_pi),
        default=[1],
    )

st.subheader("Here are your plots:")
for plot_type in plot_types:
    for scenario in scenarii:
        for J in J_vals:
            for model in models:
                if "demog" in model:
                    for pi_num in pi_vals:
                        plot_i = load_plot(plot_type, J, scenario, model, pi_num=pi_num)
                        st.image(plot_i)
                else:
                    plot_i = load_plot(plot_type, J, scenario, model)
                    st.image(plot_i)
