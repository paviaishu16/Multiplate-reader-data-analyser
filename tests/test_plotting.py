"""Test functions for constructing plots."""

import base64

import pandas as pd

from plotting import create_all_plots, create_timeseries_plot_with_models


def test_create_timeseries_plot_with_models():
    """Test that single plot image is created."""
    input_observed_data = pd.Series(
        {"A1": [5.5, 15.5, 19.2, 20.3, 50.5, 72.2]},
        index=[0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
    )
    input_gompertz_metrics = pd.Series(
        {
            "N_0_opt": 4.511152,
            "N_inf_opt": 1.397241,
            "alpha_opt": 0.031169,
            "R_2": -0.342961,
            "RMSE": 0.333926,
            "AIC": 409.544346,
            "BIC": 108.340329,
        }
    )
    input_richards_metrics = pd.Series(
        {
            "A_opt": 1.607220,
            "k_opt": 0.110140,
            "t0_opt": 13.314109,
            "A0_opt": 0.244298,
            "R_2": 0.857320,
            "RMSE": 0.108843,
            "AIC": 86.450596,
            "BIC": -211.776687,
        },
    )
    plot = create_timeseries_plot_with_models(
        input_observed_data,
        input_gompertz_metrics,
        input_richards_metrics,
        "A1",
    )

    assert len(plot) != 0
    try:
        base64.b64decode(plot)
    except Exception:
        assert False


def test_create_all_plots():
    """Test that multiple plot images are created."""
    input_observed_data = pd.DataFrame(
        {
            "A1": [4.5, 19.5, 29.2, 90.3, 50.5, 72.2],
            "A2": [5.5, 15.5, 19.2, 20.3, 50.5, 72.2],
        }
    )
    input_observed_data.index = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

    input_gompertz_metrics = pd.DataFrame(
        {
            "N_0_opt": [4.511152, 4.2],
            "N_inf_opt": [1.397241, 3.1],
            "alpha_opt": [0.031169, 2.0],
            "R_2": [-0.342961, 1.1],
            "RMSE": [0.333926, 1.1],
            "AIC": [409.544346, 4.0],
            "BIC": [108.340329, 2.0],
        },
        index=["A1", "A2"],
    )
    input_richards_metrics = pd.DataFrame(
        {
            "A_opt": [1.607220, 2.1],
            "k_opt": [0.110140, 1.3],
            "t0_opt": [13.314109, 3.0],
            "A0_opt": [0.244298, 1.1],
            "R_2": [0.857320, 1.2],
            "RMSE": [0.108843, 1.1],
            "AIC": [86.450596, 1.1],
            "BIC": [-211.776687, 3.0],
        },
        index=["A1", "A2"],
    )
    plots = create_all_plots(
        input_observed_data,
        input_gompertz_metrics,
        input_richards_metrics,
    )

    assert len(plots) == 2
    assert len(plots["A1"]) != 0
    assert len(plots["A2"]) != 0
    try:
        base64.b64decode(plots["A1"])
    except Exception:
        assert False
    try:
        base64.b64decode(plots["A2"])
    except Exception:
        assert False
