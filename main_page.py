import streamlit as st

st.set_page_config(page_title="FRAC simulations", page_icon=":material/insights:")

pg = st.navigation(
    {
        "": [
            st.Page("app_pages/home.py", title="Home", icon=":material/home:"),
        ],
        "Finite sample": [
            st.Page(
                "app_pages/estimates.py",
                title="Estimates",
                icon=":material/area_chart:",
            ),
            st.Page(
                "app_pages/tests.py",
                title="Specification tests",
                icon=":material/rule:",
            ),
            st.Page(
                "app_pages/variance_decompositions.py",
                title="Variance decompositions",
                icon=":material/pie_chart:",
            ),
        ],
        "Many-market limit": [
            st.Page(
                "app_pages/asymptotic_performance.py",
                title="Asymptotic performance",
                icon=":material/trending_flat:",
            ),
        ],
    }
)
pg.run()
