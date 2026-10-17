"""Streamlit helpers shared by the app pages"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

from utils.params_monte_carlo import data_dir


def set_plot_style() -> None:
    sns.set_context("notebook")
    sns.set_style("whitegrid")


@st.cache_data(max_entries=10)
def load_test_results(which_test: str) -> pd.DataFrame:
    """the simulated test results for one null hypothesis"""
    return pd.read_pickle(data_dir / f"df_test_{which_test}_results.pkl")


def show_grid(g: sns.FacetGrid, alt: str) -> None:
    """display a seaborn grid, then close its figure so it does not pile up in memory"""
    st.pyplot(g.figure, alt=alt)
    plt.close(g.figure)
