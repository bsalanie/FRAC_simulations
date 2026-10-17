# FRAC_simulations

A Streamlit app that shows the Monte Carlo simulation results for the FRAC
(Fast, Robust, and Approximately Correct) estimation method of Salanié and Wolak (2026),
as reported in sections 5 and 6 and Appendix E of the paper.

## What the app shows

The app has a main page and four pages:

1. **Finite sample estimates**: the distributions of the FRAC and MPEC estimates
   for a "macro-BLP" model adapted from Dubé, Fox and Su (*Econometrica* 2012),
   with $T=50$ markets and $J=25$ products per market. You choose the scale factor
   of the marginal cost, the variance of the product effects, and the scale of the
   variance of the random coefficients.
2. **Finite sample tests**: power curves and p-value distributions of specification
   tests of $\beta_1=0$, $\sigma_1^2=0$, $\beta_1=\sigma_1^2=0$, and $\sigma_p^2=0$.
3. **Finite sample variance decompositions**: the shares of the variance of market
   shares and of log marginal costs due to covariates, unobserved product effects,
   and idiosyncratic factors.
4. **Asymptotic performance**: the pseudo-true values and semi-elasticities of the
   FRAC(D) and corrected estimators in the many-market limit, with 95% confidence
   intervals from the semiparametric efficiency bounds. You choose the market share
   of the outside good, the model (endogenous or exogenous prices, with or without
   a micromoment), and the number of products.

## Running the app locally

The app has been tested with Python 3.13.5.

```bash
uv sync
uv run treamlit run main_page.py
```

## Repository layout

- `main_page.py`: the app's landing page
- `pages/`: the four pages of the app
- `utils/`: simulation parameters and plotting functions
  - `read_monte_carlo_estimates.py` and `read_monte_carlo_tests.py` rebuild the data
    files in `Latest_Data/` from the raw simulation output (not included in this repository)
- `Latest_Data/`: pickled pandas DataFrames with the finite sample estimates and tests
- `variance_shares_plots/`: figures for the variance decompositions page
- `asymptotic_plots/`: figures for the asymptotic performance page
