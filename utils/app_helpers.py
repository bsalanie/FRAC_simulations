"""Streamlit helpers shared by the app pages"""

import threading
from typing import Callable

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

from utils.params_monte_carlo import data_dir

# matplotlib is not thread-safe (its mathtext parser fails when used concurrently),
# and Streamlit runs each session in its own thread: we draw one figure at a time
_plot_lock = threading.RLock()


def set_plot_style() -> None:
    sns.set_context("notebook")
    sns.set_style("whitegrid")


@st.cache_data(max_entries=10)
def load_test_results(which_test: str) -> pd.DataFrame:
    """the simulated test results for one null hypothesis"""
    return pd.read_pickle(data_dir / f"df_test_{which_test}_results.pkl")


def show_grids(
    build: Callable[[], sns.FacetGrid | tuple[sns.FacetGrid, ...]], alt: str
) -> None:
    """build one or several seaborn grids and display them, holding the plot lock;
    then close their figures so they do not pile up in memory"""
    with _plot_lock:
        grids = build()
        if not isinstance(grids, tuple):
            grids = (grids,)
        for g in grids:
            st.pyplot(g.figure, alt=alt)
            plt.close(g.figure)
