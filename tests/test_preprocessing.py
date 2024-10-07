import os

import pandas as pd
import pytest

from preprocessing import format_time_as_hours, preprocess_data
from exceptions import MTPAnalyzerException


def test_preprocess_data():
    """Test preprocessing data produces expected DataFrame."""
    path_to_test_file = os.path.join("tests", "example_data", "Raw data.xlsx")
    actual_data = preprocess_data(path_to_test_file)
    assert actual_data.shape == (145, 49)
    assert actual_data.columns[0] == "Time"

    # Spot check
    assert actual_data.iat[0, 0] == "0.5"
    assert actual_data.iat[4, 0] == "2.5"
    assert actual_data.iat[2, 3] == 97


def test_preprocess_data_with_non_excel_file():
    """Test preprocessing data when fed non-Excel file."""
    path_to_bad_file = os.path.join("tests", "example_data", "no-data.txt")
    with pytest.raises(MTPAnalyzerException) as exception_info:
        preprocess_data(path_to_bad_file)

    assert "no-data.txt' as Excel file: Excel file format" in str(exception_info.value)


def test_format_time_as_hours():
    """Test that timedeltas can be converted to str as expected."""
    test_cases = [(pd.Timedelta(minutes=30), "0.5")]
    for timedelta_input, expected_output in test_cases:
        assert format_time_as_hours(timedelta_input) == expected_output
