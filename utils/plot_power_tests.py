import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import sys


from utils.params_monte_carlo import (
    data_dir,
    str_beta_1,
    str_var_1,
    str_var_p,
)


def plot_power(which_test: str, str_coeff: str):
    df = pd.read_pickle(f"{data_dir}/df_test_{which_test}_results.pkl")
    df_sel = df[df.Parameter == "p_value"]
    true_coeff = f"true_{which_test}"
    dd = df_sel.groupby(["Method", true_coeff], as_index=False)["Value"].agg(
        lambda x: np.mean(x < 0.05)
    )
    dd.rename(columns={"Value": "Power"}, inplace=True)
    dd["true_coeff_case"] = dd[true_coeff].map(str)

    # print(dd)

    g = sns.FacetGrid(
        dd,
        col="Method",
        col_order=["FRAC(D)", "Corrected"],
        hue=true_coeff,
        sharey=True,
        margin_titles=True,
    )

    g.map(plt.axhline, y=0.05, ls="--", c="k")
    g.map(plt.bar, "true_coeff_case", "Power", width=0.6).set_axis_labels(
        f"True {str_coeff}", "Power"
    )

    g.set_titles(col_template="{col_name}")
    g.fig.subplots_adjust(top=0.8)

    test_what = r"$(H_0):$" + str_coeff + r"$=0$"
    g.fig.suptitle(f"Power of test of {test_what}")

    return g


def plot_joint_(df, coeff_colname):
    dd = df.groupby(["Method", "true_beta_1", "true_var_1"], as_index=False)[
        "Value"
    ].agg(lambda x: np.mean(x < 0.05))
    dd.rename(columns={"Value": "Power"}, inplace=True)
    dd["true_coeff_case"] = dd[coeff_colname].map(str)
    # print(f"{dd=}")
    g = sns.FacetGrid(
        dd,
        col="Method",
        col_order=["FRAC(D)", "Corrected"],
        hue="true_coeff_case",
        sharey=True,
        margin_titles=True,
    )
    if coeff_colname == "true_beta_1":
        str_coeff = str_beta_1
        other_str_coeff = str_var_1
    elif coeff_colname == "true_var_1":
        str_coeff = str_var_1
        other_str_coeff = str_beta_1
    else:
        sys.exit(f"{coeff_colname=} is not valid")

    g.map(plt.axhline, y=0.05, ls="--", c="k")
    g.map(plt.bar, "true_coeff_case", "Power", width=0.6).set_axis_labels(
        f"True {str_coeff}", "Power"
    )

    g.set_titles(col_template="{col_name}")
    g.fig.subplots_adjust(top=0.8)

    test_what = r"$(H_0):$" + str_beta_1 + " = " + str_var_1 + r"$\; =0$"
    g.fig.suptitle(f"Power of test of {test_what} when {other_str_coeff} = 0")

    return g


def plot_power_joint_1():
    df = pd.read_pickle(f"{data_dir}/df_test_joint_1_results.pkl")
    df_sel = df[df.Parameter == "p_value"]
    # print(df_sel)

    df_sel = df_sel[["true_beta_1", "true_var_1", "Value", "Method"]]

    df_sel_null = df_sel.query("true_beta_1 == 0.0 & true_var_1 == 0.0").copy()
    # print(f"{df_sel_null=}")
    df_sel_pos_beta_1 = df_sel.query("true_beta_1 > 0.0 & true_var_1 == 0.0").copy()
    df_sel_pos_var_1 = df_sel.query("true_beta_1 == 0.0 & true_var_1 > 0.0").copy()
    # print(f"{df_sel_pos_beta_1=}")
    # print(f"{df_sel_pos_var_1=}")

    df_beta_1 = pd.concat([df_sel_null, df_sel_pos_beta_1])
    g_beta_1 = plot_joint_(df_beta_1, "true_beta_1")

    df_var_1 = pd.concat([df_sel_null, df_sel_pos_var_1])
    g_var_1 = plot_joint_(df_var_1, "true_var_1")

    return g_beta_1, g_var_1


if __name__ == "__main__":

    plot_power("beta_1", str_beta_1)
    plot_power("var_1", str_var_1)
    plot_power("var_p", str_var_p)
    plot_power_joint_1()

    # plot_power_over_ident()
