"""Tests related to noise removal based on blank wells."""

import pandas as pd
from pandas.testing import assert_frame_equal

from noise_removal import (
    apply_loess_smoothing,
    normalize,
    normalize_blanked_data,
    remove_noise,
    separate_blanks,
)


def test_separate_blanks():
    """Test the the correct columns are separated."""
    input_df = pd.DataFrame(
        {
            "A1": [1, 2],
            "A2": [3, 4],
            "A3": [5, 6],
            "A4": [7, 8],
        }
    )
    well_mapping = {
        "A1": "label1",
        "A2": "BLK",
        "A3": "label3",
        "A4": "BLK",
    }

    filled_wells, empty_wells = separate_blanks(input_df, well_mapping)
    assert len(filled_wells.columns) == 2
    assert "A1" in filled_wells.columns
    assert "A3" in filled_wells.columns
    assert len(empty_wells.columns) == 2
    assert "A2" in empty_wells.columns
    assert "A4" in empty_wells.columns


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


def test_remove_noise():
    """Test that output is correct when removing noise."""
    noise = pd.DataFrame(
        {
            "B1": [0.1, 0.2, 0.15],
            "B2": [0.3, 0.2, 0.1],
        }
    )
    noisy_data = pd.DataFrame(
        {
            "A1": [0.6, 0.7, 0.65],
            "A2": [0.9, 0.5, 0.7],
        }
    )
    expected_noisefree_data = pd.DataFrame(
        {
            "A1": [0.4, 0.5, 0.525],
            "A2": [0.7, 0.3, 0.575],
        }
    )

    actual_noisefree_data = remove_noise(noisy_data, noise)

    assert_frame_equal(actual_noisefree_data, expected_noisefree_data)


def test_normalize_blanked_data():
    """Test blanked data normalization produces expected output."""
    input_data = pd.DataFrame(
        {
            "A1": [-0.5, 0.2, 0.4],
            "A2": [-0.1, -0.1, 0.2],
        }
    )
    expected_renormalized_data = pd.DataFrame(
        {
            "A1": [0.00001, 0.7, 0.9],
            "A2": [0.00001, 0.00001, 0.3],
        }
    )
    actual_renormalized_data = normalize_blanked_data(input_data)
    assert_frame_equal(actual_renormalized_data, expected_renormalized_data)
