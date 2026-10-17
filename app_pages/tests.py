import streamlit as st

from utils.app_helpers import set_plot_style, show_grid
from utils.params_monte_carlo import str_beta_1, str_var_1, str_var_p
from utils.plot_power_tests import plot_power, plot_power_joint_1
from utils.plot_var_select import plot_pvalues, plot_pvalues_joint_1

set_plot_style()

uni_beta_1 = "\N{GREEK SMALL LETTER BETA}\N{SUBSCRIPT ONE}"
uni_var_1 = "\N{GREEK SMALL LETTER SIGMA}\N{SUBSCRIPT ONE}\N{SUPERSCRIPT TWO}"
uni_var_p = "\N{GREEK SMALL LETTER SIGMA}ₚ\N{SUPERSCRIPT TWO}"


st.title("Finite sample simulations")
st.header("Specification tests")

st.sidebar.markdown(
    """
    ### The simulation setup

    It is described in section 6 of Salanié-Wolak (2026);
    it adapts Dubé-Fox-Su (*Eca* 2012).

    The tests reported here use scale factors (0.1, 0.5, 0.5).

    For each null hypothesis, we show the power curve of a test of nominal size 5%,
    and the distribution of the p-values.

    An ideal test would have power 0.05 under the null, and one under the alternative;
    the distribution of the p-values would be uniform on [0,1] under the null,
    and a Dirac mass at 0 under the alternative.
    """
)
beta_1_is_0 = uni_beta_1 + "=0"
var_1_is_0 = uni_var_1 + "=0"
var_p_is_0 = uni_var_p + "=0"
joint_1 = uni_beta_1 + "=" + var_1_is_0

hypotheses = {
    beta_1_is_0: ("beta_1", str_beta_1),
    var_1_is_0: ("var_1", str_var_1),
    joint_1: (0, 0),
    var_p_is_0: ("var_p", str_var_p),
}

hypo_names = list(hypotheses.keys())

which_tests = st.pills(
    "Null hypotheses",
    hypo_names,
    selection_mode="multi",
    default=[hypo_names[0]],
)

plot_labels = {"power": "Power curve", "pvalues": "Distribution of p-values"}
which_plots = st.pills(
    "Plots",
    list(plot_labels),
    selection_mode="multi",
    format_func=plot_labels.get,
    default=["power"],
)

if not which_tests or not which_plots:
    st.info("Choose at least one null hypothesis and one plot.")

for hypo in which_tests:
    if hypo == joint_1:
        if "power" in which_plots:
            for g in plot_power_joint_1():
                show_grid(g, alt=f"Power of the test of {hypo}")
        if "pvalues" in which_plots:
            for g in plot_pvalues_joint_1():
                show_grid(g, alt=f"Distribution of the p-values of the test of {hypo}")
    else:
        vals = hypotheses[hypo]
        if "power" in which_plots:
            show_grid(plot_power(*vals), alt=f"Power of the test of {hypo}")
        if "pvalues" in which_plots:
            show_grid(
                plot_pvalues(*vals, only_2siv=True),
                alt=f"Distribution of the p-values of the test of {hypo}",
            )
