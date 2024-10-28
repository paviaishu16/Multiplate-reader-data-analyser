"""Functions for constructing plots."""

import os

import matplotlib.pyplot as plt  # type: ignore
import pandas as pd

from exceptions import MTPAnalyzerException
from growth_model import gompertz_model, richards_model

FIGURE_SIZE = 10, 6


def create_timeseries_plot_with_models(
    observed_data: pd.Series,  # type: ignore
    gompertz_parameters: pd.Series,  # type: ignore
    richards_parameters: pd.Series,  # type: ignore
    well_index: str,
    dest_path: str,
) -> None:
    """Create an individual plot showing model and observed population.

    Args:
        observed_data: Timeseries, with time as index.
        gompertz_parameters: Optimal parameters after curve fit to
                             Gompertz model.
        richards_parameters: Optimal parameters after curve fit to
                             Richards model.
        dest_path: Where to save the plot to.
    """
    plt.style.use("ggplot")

    fix, ax = plt.subplots(figsize=FIGURE_SIZE)

    t_data = observed_data.index.to_numpy()
    gompertz_prediction = gompertz_model(
        t=t_data,
        N_0=gompertz_parameters.at["N_0_opt"],
        A=gompertz_parameters.at["N_inf_opt"],
        k=gompertz_parameters.at["alpha_opt"],
    )
    richards_prediction = richards_model(
        t=t_data,
        A=richards_parameters.at["A_opt"],
        k=richards_parameters.at["k_opt"],
        t0=richards_parameters.at["t0_opt"],
        A0=richards_parameters.at["A0_opt"],
    )

    ax.plot(t_data, observed_data, label="Observed data")
    ax.plot(t_data, gompertz_prediction, label="Gompertz model")
    ax.plot(t_data, richards_prediction, label="Richards model")

    ax.set_title(f"Observed and predicted data for well {well_index}")
    ax.set_xlabel("Time (hours)")
    ax.set_ylabel("Population")
    ax.grid(True, linestyle="--", alpha=0.7)
    ax.legend()

    plt.savefig(dest_path, dpi=300)
    plt.close()


def create_all_plots(
    observed_data: pd.DataFrame,
    gompertz_parameters: pd.DataFrame,
    richards_parameters: pd.DataFrame,
    dest_dir: str = "plots",
) -> None:
    """Create plots for all wells in DataFrame.

    Create plots for all wells in DataFrame, with model and observed
    data.

    Args:
        observed_data: Timeseries, with time as index.
        gompertz_parameters: Optimal parameters after curve fit to
                             Gompertz model.
        richards_parameters: Optimal parameters after curve fit to
                             Richards model.
        dest_dir: Directory in which to save the plots.
    """
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    def ensure_series(col: pd.Series | pd.DataFrame) -> pd.Series:  # type: ignore
        if not isinstance(col, pd.Series):
            raise MTPAnalyzerException(f"Duplicated well index: {col.index}")
        return col

    for well_index in observed_data.columns:
        create_timeseries_plot_with_models(
            observed_data.loc[:, well_index],
            ensure_series(gompertz_parameters.loc[well_index, :]),
            ensure_series(richards_parameters.loc[well_index, :]),
            well_index,
            os.path.join(dest_dir, well_index),
        )
