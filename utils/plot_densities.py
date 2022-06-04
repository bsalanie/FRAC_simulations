""" plotting the densities of the estimates, Seaborn version"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


from utils.params_monte_carlo import (
    mkdir_if_needed_,
    coeff_subsets,
    data_dir,
    plots_dir,
    basic_values,
    headers_demand_betas,
    headers_demand_sigmas,
    headers_supply,
    headers_varianceshares_demand,
    headers_varianceshares_supply,
    gamma_vals,
    var_xi_vals,
    var_omega_vals,
    sigma2_vals,
    headers_coeffs,
    str_coeffs,
)


def select_data(df, subcase, coeff_subset):
    """extract the results for a subcase and a subset of parameters"""
    sigma2, gamma_val, var_xi, var_omega = subcase
    crit1 = df["sigma2"] == sigma2
    crit2 = df["var_xi"] == var_xi
    crit3 = df["var_omega"] == var_omega
    crit4 = df["gamma"] == gamma_val
    sel_cond = crit1 & crit2 & crit3 & crit4
    if coeff_subset == "All":
        select_df = df[sel_cond]
    else:
        subset_str_coeffs, methods_coeffs = coeff_subsets[coeff_subset]
        crit5 = df["Parameter"].isin(subset_str_coeffs)
        crit6 = df["Method"].isin(methods_coeffs)
        select_df = df[sel_cond & crit5 & crit6]
    return select_df


def plot_estimates(df, subcase, coeff_subset, true_vals):
    """plots densities of a subset of estimates for a subcase"""
    select_df = select_data(df, subcase, coeff_subset)
    n_coeffs = len(coeff_subsets[coeff_subset][0])
    sigma2, gamma_val, var_xi, var_omega = subcase

    d = {"ls": ["-", "--", "-.", ":"]}

    g = sns.FacetGrid(
        select_df,
        col="Parameter",
        col_wrap=3,
        hue="Method",
        hue_kws=d,
        sharex=False,
        margin_titles=True,
    )
    g.map(sns.kdeplot, "Estimate")
    g.set_titles(col_template="{col_name}")

    if (
        "variance_shares" not in coeff_subset
    ):  # we add vertical lines for the true values
        # dict of line positions
        lines_true = {}
        for i in range(n_coeffs):
            lines_true[i] = true_vals[i]
        # flatten axes into a 1-d array
        axes = g.axes.flatten()
        # iterate through the axes to add line  to each plot
        for i, ax in enumerate(axes):
            ax.axvline(lines_true[i], ls="--", c="purple")
            # ax.set_xlim(xlims[icol])
    else:
        # flatten axes into a 1-d array
        axes = g.axes.flatten()
        # iterate through the axes to add [0, 1] x range  to each plot
        for i, ax in enumerate(axes):
            ax.set_xlim((0.0, 1.0))

    g.set(yticks=[], xlabel="")  # set y ticks to blank
    g.despine(left=True)  # remove 'spines'

    # g.fig.subplots_adjust(top=0.85)
    g.fig.suptitle(
        "For "
        + r"$\sigma^2=$"
        + f"{sigma2}, "
        + r"$\sigma_\xi^2=$"
        + f"{var_xi}, "
        + r"$\gamma=$"
        + f"{gamma_val}, "
        + r"$\sigma_\omega^2=$"
        + f"{var_omega}",
        y=1.03,
    )

    g.add_legend()

    return g
