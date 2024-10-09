"""Tests related to noise removal based on blank wells."""

import pandas as pd
from pandas.testing import assert_frame_equal

from noise_removal import apply_loess_smoothing, normalize


def test_normalize():
    """Test that values are normalized as expected."""
    input_data = pd.DataFrame(
        {
            "A1": [500.0, 750.0, 1000.0, 1000.0, 1000.0],
        },
    )
    expected_normalized_data = pd.DataFrame(
        {
            "A1": [0.0, 0.5, 1.0, 1.0, 1.0],
        }
    )
    actual_normalized_data = normalize(input_data)
    assert_frame_equal(actual_normalized_data, expected_normalized_data)


def test_loess_smoothing():
    """Test that values are smoothed as expected."""
    input_data = pd.DataFrame(
        {
            "Time": [0.5, 1.0, 1.5, 2.0, 2.5],
            "A1": [5.0, 10.0, 100.0, 100.0, 200.0],
            "A2": [5.0, 10.0, 100.0, 100.0, 400.0],
        }
    )
    expected_smoothed_data = pd.DataFrame(
        {
            "Time": [0.5, 1.0, 1.5, 2.0, 2.5],
            "A1": [5.0, 6.0, 28.0, 100.0, 120.0],
            "A2": [5.0, 6.0, 28.0, 100.0, 160.0],
        }
    )
    actual_smoothed_data = apply_loess_smoothing(input_data)
    assert_frame_equal(actual_smoothed_data, expected_smoothed_data)
