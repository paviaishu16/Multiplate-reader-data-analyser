"""Functions relating to fitting the Richards and Gompertz models.

Fit curve and determine goodness of fit using Richards and Gompertz
models for timeseries of well data.
"""

from typing import Any

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit  # type: ignore

MAXFEV = 2000


def gompertz_model(
    t: np.ndarray,  # type: ignore
    N_0: pd.Series,  # type: ignore
    A: pd.Series,  # type: ignore
    k: pd.Series,  # type: ignore
) -> pd.Series:  # type: ignore
    """Gompertz equation for calculating population size.

    Args:
        t: Traditionally t in the formula. Time points/independent
           variable.
        N_0: Traditionally N_0 in the formula. Initial population.
        A: Traditionally N_inf in the formula. Asymptotic maximum
           population.
        k: Traditionally alpha in the formula. The maximum growth rate
           seen between 20 and 48 hours into the experiment.

    Return:
        Series or single value of population at given timepoints t.
    """
    population_size = N_0 * np.exp(np.log(A / N_0) * 1 - np.exp(-k * t))
    return population_size  # type: ignore


def richards_model(
    t: np.ndarray,  # type: ignore
    A: pd.Series,  # type: ignore
    k: pd.Series,  # type: ignore
    t0: pd.Series,  # type: ignore
    A0: pd.Series,  # type: ignore
    nu: float = 1.5,
) -> pd.Series:  # type: ignore
    """Get population given time and parameters using Richards model.

    Args:
        t: Timepoint or Series of timepoints for which to determine
           the population.
        A: Asymptotic max population. The highest value found for a
           given well.
        k: Maximum growth rate. Highest slope (growth) found for given
           well.
        t0: Inflection point. The timepoint of k.
        A0: Initial population size (called N_0 in Gompertz)
        nu: Shape parameter. Defaults to 1.5.

    Return:
        Series or single value of population at given timepoints t.
    """
    Q = ((A / A0) ** nu) - 1
    return A * (1 + Q * np.exp(-k * (t - t0))) ** (-1 / nu)  # type: ignore


def calculate_BIC(n: float, k: float, sse: float) -> float:
    """Calculate Bayesian Information Criterion."""
    log_likelihood = -n / 2 * (np.log(2 * np.pi * (sse / n)) + 1)
    bic = k * np.log(n) - 2 * log_likelihood
    return bic  # type: ignore


def get_performance_metrics(
    N_pred: pd.Series,  # type: ignore
    N_data: np.ndarray,  # type: ignore
    n_parameters: int,
    n: int,
) -> dict[str, float]:
    """Calcluate R-squared, RMSE, AIC and BIC for model fit.

    Args:
        N_pred: Population values predicted by the model.
        N_data: Observed population values.
        n_parameters: Number of parameters of used model.
        n: Number of data records.
    """
    residuals = N_pred - N_data
    SS_res = np.sum(residuals**2)
    SS_tot = np.sum(N_data - np.mean(N_data) ** 2)

    R_2 = 1 - SS_res / SS_tot
    RMSE = np.sqrt(np.mean(residuals**2))
    AIC = n * np.log(np.mean(SS_res)) + 2 * n_parameters
    BIC = calculate_BIC(n=n, k=n_parameters, sse=SS_res)

    return {"R_2": R_2, "RMSE": RMSE, "AIC": AIC, "BIC": BIC}


def gompertz_model_metrics(
    mtp_data: pd.DataFrame,
    growth_parameters: pd.DataFrame,
) -> pd.DataFrame:
    """Get optimal parameters and performance metrics for Gompertz.

    Args:
        mtp_data: Cleaned up data.
        growth_parameters: L, k, t, and A values for each mtp data
                           column.

    Return:
        Dataframe with optimal parameters for Gompertz model and
        performance metrics.
    """
    t_data = mtp_data.index.to_numpy()

    all_model_metrics: list[dict[str, Any]] = []

    for well_index in mtp_data.columns:
        N_data = mtp_data[well_index].to_numpy()

        p_opt, p_cov = curve_fit(
            gompertz_model,
            t_data,
            N_data,
            p0=[
                mtp_data.loc[mtp_data.index[0], well_index],
                growth_parameters.loc[well_index, "A"],
                growth_parameters.loc[well_index, "k"],
            ],
            bounds=([0.0, 0.0, 0.0], [np.inf, np.inf, np.inf]),
            maxfev=MAXFEV,
        )

        N_pred = gompertz_model(t_data, *p_opt)

        N_0_opt, N_inf_opt, alpha_opt = p_opt
        well_model_metrics = {
            "N_0_opt": N_0_opt,
            "N_inf_opt": N_inf_opt,
            "alpha_opt": alpha_opt,
        }

        well_model_metrics.update(
            get_performance_metrics(
                N_pred=N_pred,
                N_data=N_data,
                n_parameters=3,
                n=len(t_data),
            )
        )
        all_model_metrics.append(well_model_metrics)

    model_metrics_df = pd.DataFrame(all_model_metrics)
    model_metrics_df.index = mtp_data.columns
    return model_metrics_df


def richards_model_metrics(
    mtp_data: pd.DataFrame,
    growth_parameters: pd.DataFrame,
) -> pd.DataFrame:
    """Get optimal parameters and performance metrics for Richards.

    Args:
        mtp_data: Cleaned up data.
        growth_parameters: L, k, t, and A values for each mtp data
                           column.

    Return:
        Dataframe with optimal parameters for Richards model and
        performance metrics.
    """
    t_data = mtp_data.index.to_numpy()

    all_model_metrics: list[dict[str, Any]] = []

    for well_index in mtp_data.columns:
        N_data = mtp_data[well_index].to_numpy()

        p_opt, p_cov = curve_fit(
            richards_model,
            t_data,
            N_data,
            p0=[
                growth_parameters.loc[well_index, "A"],
                growth_parameters.loc[well_index, "k"],
                growth_parameters.loc[well_index, "t"],
                mtp_data.loc[mtp_data.index[0], well_index],
            ],
            maxfev=MAXFEV,
        )
        N_pred = richards_model(t_data, *p_opt)

        A_opt, k_opt, t0_opt, A0_opt = p_opt
        well_model_metrics = {
            "A_opt": A_opt,
            "k_opt": k_opt,
            "t0_opt": t0_opt,
            "A0_opt": A0_opt,
        }

        well_model_metrics.update(
            get_performance_metrics(
                N_pred=N_pred,
                N_data=N_data,
                n_parameters=4,
                n=len(t_data),
            )
        )
        all_model_metrics.append(well_model_metrics)

    model_metrics_df = pd.DataFrame(all_model_metrics)
    model_metrics_df.index = mtp_data.columns
    return model_metrics_df
