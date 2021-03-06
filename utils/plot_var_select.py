import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import sys


from utils.params_monte_carlo import (
    data_dir,
    str_beta_1,
    str_var_1,
)


def plot_diag_(*args, **kwargs):
    x = np.arange(0, 1, 0.01)
    y = x
    plt.plot(y, x, c="k", ls=":")


def plot_pvalues(which_test: str, str_coeff: str, only_2siv: bool = False):
    df = pd.read_pickle(f"{data_dir}/df_test_{which_test}_results.pkl")
    df_sel = df[df.Parameter == "p_value"]
    # print(df_sel)
    true_coeff = f"true_{which_test}"
    if only_2siv:
        df_sel = df_sel[df_sel["Method"] == "FRAC(D)"]
        df_sel = df_sel[[true_coeff, "Value"]]
    else:
        df_sel = df_sel[["Method", true_coeff, "Value"]]
    df_sel.rename(columns={true_coeff: str_coeff}, inplace=True)

    if only_2siv:
        g = sns.FacetGrid(
            df_sel,
            hue=str_coeff,
            col=str_coeff,  # for each subplot column,
            col_wrap=2,
            sharex=True,
            margin_titles=True,
        )
    else:
        g = sns.FacetGrid(
            df_sel,
            row="Method",  # for each subplot row
            hue="Method",
            col=str_coeff,  # for each subplot column,
            sharex=True,
            margin_titles=True,
        )

    g.map(plt.axhline, y=0.05, ls="--", c="k")
    g.map(plt.axvline, x=0.05, ls="--", c="k")
    # g.map(plt.axhline, y=1, ls='--', c='k')
    g.map(sns.ecdfplot, "Value")
    g.map(plot_diag_)
    g = g.set(xlim=(-0.05, 1.05), ylim=(-0.05, 1.05))
    if not only_2siv:
        g.set_titles(row_template="{row_name}")
    g.set_titles(col_template="True " + str_coeff + " = {col_name}")
    g.fig.subplots_adjust(top=0.9)

    test_what = r"$(H_0):$" + str_coeff + r"$=0$"
    g.fig.suptitle(f"Testing {test_what}")

    return g


def plot_pvalues_joint_(df_sel, coeff_colname):
    if coeff_colname == "true_beta_1":
        str_coeff = str_beta_1
        other_str_coeff = str_var_1
    elif coeff_colname == "true_var_1":
        str_coeff = str_var_1
        other_str_coeff = str_beta_1
    else:
        sys.exit(f"{coeff_colname=} is not valid")
    g = sns.FacetGrid(
        df_sel,
        hue=str_coeff,
        col=str_coeff,
        col_wrap=2,
        sharex=True,
        sharey=True,
        margin_titles=True,
    )

    g.map(plt.axhline, y=0.05, ls="--", c="k")
    g.map(plt.axvline, x=0.05, ls="--", c="k")
    g.map(plt.axhline, y=1, ls="--", c="k")
    g.map(sns.ecdfplot, "Value")
    g.map(plot_diag_)
    g = g.set(xlim=(-0.05, 1.05), ylim=(-0.05, 1.05))
    g.set_titles(col_template="True " + str_coeff + " = {col_name}")
    g.set_titles(row_template="{row_name}")

    g.fig.subplots_adjust(top=0.9)
    test_what = r"$(H_0):$" + str_beta_1 + r"$=$" + str_var_1 + r"$=0$"
    g.fig.suptitle(f"Testing {test_what} when {other_str_coeff} = 0")

    return g


def plot_pvalues_joint_1():
    df = pd.read_pickle(f"{data_dir}/df_test_joint_1_results.pkl")
    df_sel = df[(df.Parameter == "p_value") & (df.Method == "FRAC(D)")]

    df_sel = df_sel[["true_beta_1", "true_var_1", "Value"]]

    # print(df_sel.groupby(["true_beta_1", "true_var_1"]).count())

    df_sel_null = df_sel.query("true_beta_1 == 0.0 & true_var_1 == 0.0").copy()
    # print(f"{df_sel_null=}")
    df_sel_pos_beta_1 = df_sel.query("true_beta_1 > 0.0 & true_var_1 == 0.0").copy()
    df_sel_pos_var_1 = df_sel.query("true_beta_1 == 0.0  & true_var_1 > 0.0").copy()
    # print(f"{df_sel_pos_beta_1=}")
    # print(f"{df_sel_pos_var_1=}")

    for dd in [df_sel_null, df_sel_pos_beta_1, df_sel_pos_var_1]:
        dd.rename(
            columns={"true_beta_1": str_beta_1, "true_var_1": str_var_1}, inplace=True
        )

    df_beta_1 = pd.concat((df_sel_null, df_sel_pos_beta_1))
    g_beta_1 = plot_pvalues_joint_(df_beta_1, "true_beta_1")

    df_var_1 = pd.concat((df_sel_null, df_sel_pos_var_1))
    g_var_1 = plot_pvalues_joint_(df_var_1, "true_var_1")

    return g_beta_1, g_var_1


# if __name__ == "__main__":

#     plot_pvalues("beta_1", str_beta_1)
#     plot_pvalues("beta_1", str_beta_1, only_2siv=True)
#     plot_pvalues("var_1", str_var_1)
#     plot_pvalues("var_1", str_var_1, only_2siv=True)
#     plot_pvalues("var_p", str_var_p)
#     plot_pvalues("var_p", str_var_p, only_2siv=True)
#     plot_pvalues_joint_1()

#     # plot_pvalues_over_ident()
