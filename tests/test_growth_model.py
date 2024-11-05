"""Tests for growth model fitting."""

import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal

from growth_model import (
    add_better_fit_column,
    calculate_BIC,
    get_performance_metrics,
    gompertz_model,
    gompertz_model_metrics,
    richards_model,
    richards_model_metrics,
)


def test_richards_model():
    """Test that the equation produces expected result."""
    actual_population = richards_model(
        t=pd.Series([1.0, 2.0]),
        A=pd.Series([2.0, 3.0]),
        k=pd.Series([3.0, 4.0]),
        t0=pd.Series([4.0, 5.0]),
        A0=pd.Series([0.1, 0.4]),
    )
    expected_population = pd.Series([0.00024973992453493154, 0.00013872506058638806])
    assert_series_equal(actual_population, expected_population)


def test_gompertz_model():
    """Test that the equation produces expected result."""
    actual_population = gompertz_model(
        t=pd.Series([12.0, 53.2]),
        N_0=pd.Series([11.1, 41.4]),
        k=pd.Series([11.7, 41.8]),
        A=pd.Series([13.5, 12.4]),
    )
    expected_population = pd.Series([13.5, 12.4])
    assert_series_equal(actual_population, expected_population)


def test_calculate_BIC():
    """Test that the BIC formula function gives the correct value."""
    input_n = 2.5
    input_k = 3.5
    input_sse = 4.5
    actual_BIC = calculate_BIC(n=input_n, k=input_k, sse=input_sse)
    expected_BIC = 11.771176889838204
    assert actual_BIC == expected_BIC


def test_get_performance_metrics():
    """Test performance metric calculation gives expected result."""
    input_N_pred = pd.Series([1.1, 2.1, 3.2])
    input_N_data = pd.Series([1.0, 2.2, 3.2])
    input_n_parameters = 4
    input_n = 3
    expected_performance_metrics = {
        "R_2": 1.0027573529411764,
        "RMSE": 0.08164965809277268,
        "AIC": -3.736069016284432,
        "BIC": -2.123825528388286,
    }

    actual_performance_metrics = get_performance_metrics(
        input_N_pred, input_N_data, input_n_parameters, input_n
    )
    assert actual_performance_metrics == expected_performance_metrics


def test_get_optimal_parameters_gompertz():
    """Test that optimal parameters are right for Gompertz."""
    input_mtp = pd.DataFrame({"A1": [1.0, 2.0, 3.0, 4.0]})
    input_mtp.index = pd.Series([0.5, 1.0, 1.5, 1.7])
    input_growth_param = pd.DataFrame(
        {
            "L": 2.0,
            "k": 2.0,
            "t": 2.0,
            "A": 2.0,
        },
        index=["A1"],
    )
    expected_optimal_parameters = pd.DataFrame(
        {
            "N_0_opt": [1.0],
            "N_inf_opt": [3.6964208716242193],
            "alpha_opt": [0.94745358060056],
            "R_2": [1.1453892518001116],
            "RMSE": [0.7383831622202789],
            "AIC": [9.118838251569304],
            "BIC": [13.084052156086795],
        },
        index=["A1"],
    )
    actual_optimal_parameters = gompertz_model_metrics(input_mtp, input_growth_param)
    assert_frame_equal(actual_optimal_parameters, expected_optimal_parameters)


def test_get_optimal_parameters_richards():
    """Test that optimal parameters are right for Richards."""
    input_mtp = pd.DataFrame({"A1": [0.5, 4.0, 3.3, 1.7]})
    input_mtp.index = pd.Series([1.0, 2.0, 3.0, 4.0])
    input_growth_param = pd.DataFrame(
        {
            "L": 2.0,
            "k": 2.0,
            "t": 2.0,
            "A": 3.0,
        },
        index=["A1"],
    )
    expected_optimal_parameters = pd.DataFrame(
        {
            "A_opt": [2.374999996564483],
            "k_opt": [-4.174579638237476],
            "t0_opt": [196.41366289792106],
            "A0_opt": [124.14914730524701],
            "R_2": [1.5716746411483253],
            "RMSE": [1.366336342193971],
            "AIC": [16.04224108443251],
            "BIC": [19.393749350069893],
        },
        index=["A1"],
    )
    actual_optimal_parameters = richards_model_metrics(input_mtp, input_growth_param)
    assert_frame_equal(actual_optimal_parameters, expected_optimal_parameters)


def test_add_better_fit_column():
    """Test that column gets right value."""
    df_a = pd.DataFrame({"BIC": [3, 4, 5]})
    df_b = pd.DataFrame({"BIC": [4, 4, 4]})
    actual_df = add_better_fit_column(df_a, df_b["BIC"])
    expected_df = pd.DataFrame(
        {"BIC": [3, 4, 5], "Goodness of fit": ["Yes", "Equal", "No"]}
    )
    assert_frame_equal(actual_df, expected_df)
