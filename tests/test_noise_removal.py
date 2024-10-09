"""Tests related to noise removal based on blank wells."""

import pandas as pd
from pandas.testing import assert_frame_equal

from noise_removal import normalize


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
