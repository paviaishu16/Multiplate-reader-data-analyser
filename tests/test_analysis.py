"""Test data analysis functions."""

import pandas as pd
from pandas.testing import assert_frame_equal

from analysis import (
    calculate_growth_rates,
    extract_growth_parameters,
    extract_maximum_growth_rates,
)


def test_calculate_growth_rate():
    """Tets that growth_rate gets calculated correctly."""
    input_data = pd.DataFrame(
        {
            "Time": [1.0, 3.0, 5.0, 9.0],
            "A1": [2.0, 4.0, 10.0, 6.0],
        }
    )
    input_data = input_data.set_index("Time")

    expected_growth_rate_data = pd.DataFrame(
        {
            "Time": [1.0, 3.0, 5.0, 9.0],
            "A1": [0.0, 1.0, 3.0, -1.0],
        }
    )
    expected_growth_rate_data = expected_growth_rate_data.set_index("Time")

    actual_growth_rate_data = calculate_growth_rates(input_data)

    assert_frame_equal(actual_growth_rate_data, expected_growth_rate_data)


def test_extract_maximum_growth_rate():
    """Test that you really get the ten largest growth grates."""
    input_growth_rate = pd.DataFrame(
        {
            "A1": [
                0.0,
                -0.03012,
                -0.09271,
                0.091977,
                -0.13225,
                -0.29147,
                -0.17590,
                0.454498,
                0.155854,
                -0.17952,
                -0.10952,
                0.230918,
                0.126764,
                -0.19954,
                0.162511,
            ],
            "A2": [
                0.0,
                0.035321,
                0.269074,
                0.411489,
                -0.33875,
                0.095516,
                -0.42673,
                0.561835,
                -0.08195,
                0.220475,
                -0.30343,
                -0.05810,
                0.34993,
                -0.1048,
                -0.1976,
            ],
        }
    )
    expected_growth_rates = pd.DataFrame(
        {
            "A1": [
                0.454498,
                0.230918,
                0.162511,
                0.155854,
                0.126764,
                0.091977,
                0.0,
                -0.03012,
                -0.09271,
                -0.10952,
            ],
            "A2": [
                0.561835,
                0.411489,
                0.34993,
                0.269074,
                0.220475,
                0.095516,
                0.035321,
                0.0,
                -0.0581,
                -0.08195,
            ],
        }
    )
    expected_timestamps = pd.DataFrame(
        {
            "A1": [7.0, 11.0, 14.0, 8.0, 12.0, 3.0, 0.0, 1.0, 2.0, 10.0],
            "A2": [7.0, 3.0, 12.0, 2.0, 9.0, 5.0, 1.0, 0.0, 11.0, 8.0],
        }
    )

    actual_max_growth_rate = extract_maximum_growth_rates(input_growth_rate)

    assert_frame_equal(actual_max_growth_rate["growth_rates"], expected_growth_rates)
    assert_frame_equal(actual_max_growth_rate["timestamps"], expected_timestamps)


def test_get_growth_parameters():
    """Test that you get the expected growth parameters from good input."""
    input_growth_rates = {
        "growth_rates": pd.DataFrame(
            {
                "A1": [1.0, 2.0, 3.0, 9.0, 4.0],
                "A2": [3.0, 5.0, 6.0, 2.0, 99.0],
            }
        ),
        "timestamps": pd.DataFrame(
            {
                "A1": [10.0, 20.0, 30.0, 40.0, 50.0],
                "A2": [13.0, 82.0, 23.0, 44.0, 36.0],
            }
        ),
    }
    input_blank_data = pd.DataFrame(
        {
            "A1": [423.0, 234.0, 554.0, 634.0, 234.0],
            "A2": [4515.0, 6631.0, 643.0, 45.0, 12.0],
        }
    )

    actual_growth_parameters = extract_growth_parameters(
        input_growth_rates,
        input_blank_data,
    )

    expected_growth_parameters = pd.DataFrame(
        {
            "L": [50.0, 82.0],
            "k": [9.0, 99.0],
            "t": [40.0, 36.0],
            "A": [634.0, 6631.0],
        },
        index=["A1", "A2"],
    )

    assert_frame_equal(actual_growth_parameters, expected_growth_parameters)
