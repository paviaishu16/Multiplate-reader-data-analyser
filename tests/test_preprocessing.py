"""Tests for preprocessing functionality."""

import os

import pandas as pd
import pytest

from exceptions import MTPAnalyzerException
from preprocessing import (
    format_time_as_hours,
    load_mtp_data,
    load_sample_table,
    validate_mtp_columns,
)

EMPTY_FILE_PATH = os.path.join("tests", "example_data", "no-data.txt")
EXAMPLE_MTP_DATA_PATH = os.path.join("tests", "example_data", "Raw data.xlsx")
EXAMPLE_SAMPLE_TABLE_PATH = os.path.join("tests", "example_data", "Sample Table.xlsx")


def test_load_mtp_data():
    """Test loading MTP data produces expected DataFrame."""
    actual_data = load_mtp_data(EXAMPLE_MTP_DATA_PATH)
    assert actual_data.shape == (145, 49)
    assert actual_data.columns[0] == "Time"

    # Spot check
    assert actual_data.iat[0, 0] == "0.5"
    assert actual_data.iat[4, 0] == "2.5"
    assert actual_data.iat[2, 3] == 97


def test_load_mtp_data_with_non_excel_file():
    """Test loading MTP data when fed non-Excel file."""
    with pytest.raises(MTPAnalyzerException) as exception_info:
        load_mtp_data(EMPTY_FILE_PATH)

    assert "no-data.txt' as Excel file: Excel file format" in str(exception_info.value)


def test_load_sample_table_with_non_excel_file():
    """Test loading MTP data when fed non-Excel file."""
    with pytest.raises(MTPAnalyzerException) as exception_info:
        load_mtp_data(EMPTY_FILE_PATH)

    assert "no-data.txt' as Excel file: Excel file format" in str(exception_info.value)


def test_format_time_as_hours():
    """Test that timedeltas can be converted to str as expected."""
    test_cases = [(pd.Timedelta(minutes=30), "0.5")]
    for timedelta_input, expected_output in test_cases:
        assert format_time_as_hours(timedelta_input) == expected_output


def test_load_sample_table():
    """Test that well mapping looks as expected when loaded normally."""
    actual_well_mapping = load_sample_table(EXAMPLE_SAMPLE_TABLE_PATH)

    expected_well_mapping = {
        "A1": "SPL1",
        "A2": "SPL3",
        "A3": "SPL5",
        "A4": "SPL7",
        "A5": "SPL9",
        "A6": "SPL11",
        "A7": "WT",
        "A8": "WT",
        "B1": "SPL1",
        "B2": "SPL3",
        "B3": "SPL5",
        "B4": "SPL7",
        "B5": "SPL9",
        "B6": "SPL11",
        "B7": "WT",
        "B8": "WT",
        "C1": "SPL1",
        "C2": "SPL3",
        "C3": "SPL5",
        "C4": "SPL7",
        "C5": "SPL9",
        "C6": "SPL11",
        "C7": "WT",
        "C8": "WT",
        "D1": "SPL2",
        "D2": "SPL4",
        "D3": "SPL6",
        "D4": "SPL8",
        "D5": "SPL10",
        "D6": "SPL12",
        "D7": "WT",
        "D8": "BLK",
        "E1": "SPL2",
        "E2": "SPL4",
        "E3": "SPL6",
        "E4": "SPL8",
        "E5": "SPL10",
        "E6": "SPL12",
        "E7": "WT",
        "E8": "BLK",
        "F1": "SPL2",
        "F2": "SPL4",
        "F3": "SPL6",
        "F4": "SPL8",
        "F5": "SPL10",
        "F6": "SPL12",
        "F7": "WT",
        "F8": "BLK",
    }

    assert actual_well_mapping == expected_well_mapping


def test_validate_mtp_columns():
    """Test that good data passes."""
    mtp_data = load_mtp_data(EXAMPLE_MTP_DATA_PATH)
    well_mapping = load_sample_table(EXAMPLE_SAMPLE_TABLE_PATH)

    # Test fails if this function raises an exception
    validate_mtp_columns(mtp_data, well_mapping)


def test_validate_mtp_columns_well_number_mismatch(caplog):
    """Test that we get a warning when size mismatches.

    Test that we get a warning when size of sample table doesn't match
    MTP data.
    """
    mtp_data = load_mtp_data(EXAMPLE_MTP_DATA_PATH)
    well_mapping = load_sample_table(EXAMPLE_SAMPLE_TABLE_PATH)

    mtp_data = mtp_data.drop(columns=["B1"])

    validate_mtp_columns(mtp_data, well_mapping)

    assert "number of wells in the sample table doesn't match" in caplog.text


def test_validate_mtp_columns_exception_on_missing_label(caplog):
    """Test that exception is raised when column label is missing.

    Test that an exception is raised when we don't find a label for a
    column. All MTP data columns should have a label assigned in the
    Sample Table.
    """
    mtp_data = load_mtp_data(EXAMPLE_MTP_DATA_PATH)
    well_mapping = load_sample_table(EXAMPLE_SAMPLE_TABLE_PATH)

    # Keep the _number_ of columns accurate, but make one label missing
    well_mapping["X"] = well_mapping["B1"]
    well_mapping.pop("B1")

    with pytest.raises(MTPAnalyzerException) as e:
        validate_mtp_columns(mtp_data, well_mapping)

    assert "Well index B1 in MTP data doesn't seem to exist in Sample" in caplog.text
    assert "one column in MTP data was not found in Sample Table" in str(e.value)
