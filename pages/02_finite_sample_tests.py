import streamlit as st
import seaborn as sns

from utils.params_monte_carlo import str_beta_1, str_var_1, str_var_p
from utils.plot_var_select import plot_pvalues, plot_pvalues_joint_1
from utils.plot_power_tests import plot_power, plot_power_joint_1


sns.set_context("notebook")
sns.set_style("whitegrid")

uni_beta_1 = "\N{GREEK SMALL LETTER BETA}\N{SUBSCRIPT ONE}"
uni_var_1 = "\N{GREEK SMALL LETTER SIGMA}\N{SUBSCRIPT ONE}\N{SUPERSCRIPT TWO}"
uni_var_p = "\N{GREEK SMALL LETTER SIGMA}\u209a\N{SUPERSCRIPT TWO}"


st.sidebar.markdown(
    """
    ### The simulation setup:
    
    It is described in section 7 of Salani&eacute;-Wolak (2022);
    it adapts  Dub&eacute;-Fox-Su (*Eca* 2012).

    The tests reported here use scale factors (0.1, 0.5, 0.5).

    For each null hypothesis, we show the power curve of a test of nominal size 5%, and the distribution of the p-values.

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

which_tests = st.multiselect(
    "Choose one or more null hypotheses",
    hypo_names,
    default=[hypo_names[0]],
)

which_plots = st.multiselect(
    "Plot the power curve and/or the distribution of pvalues",
    ["power", "pvalues"],
    default=["power"],
)


for hypo in which_tests:
    if hypo == joint_1:
        if "power" in which_plots:
            g_beta_1, g_var_1 = plot_power_joint_1()
            st.pyplot(g_beta_1)
            st.pyplot(g_var_1)
        if "pvalues" in which_plots:
            g_beta_1, g_var_1 = plot_pvalues_joint_1()
            st.pyplot(g_beta_1)
            st.pyplot(g_var_1)
    else:
        vals = hypotheses[hypo]
        if "power" in which_plots:
            g = plot_power(*vals)
            st.pyplot(g)
        if "pvalues" in which_plots:
            g = plot_pvalues(*vals, only_2siv=True)
            st.pyplot(g)
