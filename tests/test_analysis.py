"""Test data analysis functions."""

import pandas as pd
from pandas.testing import assert_frame_equal

from analysis import calculate_slope


def test_calculate_slope():
    """Tets that slope gets calculated correctly."""
    input_data = pd.DataFrame(
        {
            "Time": [1.0, 3.0, 5.0, 9.0],
            "A1": [2.0, 4.0, 10.0, 6.0],
        }
    )
    input_data = input_data.set_index("Time")

    expected_slope_data = pd.DataFrame(
        {
            "Time": [1.0, 3.0, 5.0, 9.0],
            "A1": [0.0, 1.0, 3.0, -1.0],
        }
    )
    expected_slope_data = expected_slope_data.set_index("Time")

    actual_slope_data = calculate_slope(input_data)

    assert_frame_equal(actual_slope_data, expected_slope_data)
