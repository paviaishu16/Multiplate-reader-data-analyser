"""Functions for preprocessing Excel sheets."""

import logging

import pandas as pd

from exceptions import MTPAnalyzerException

COLUMNS_TO_REMOVE = ["T° Fluo50_k:450,530"]
TIME_COLUMN = "Time"


def start_experiment_from_zero(original_time: pd.Series) -> pd.Series:  # type: ignore
    """Adjust timeseries so that first value start from 0.5 hours.

    Takes a Series of str timestamps convertible to Timedelta and
    shifts it so that it starts at 30 minutes. Note that format will
    go from HH:MM:SS to just hours with one decimal.

    Args:
        original_time: The Series to shift.

    Returns:
        Original series shifted to start at 0.5 hours (in units of
        hours with one decimal)
    """
    new_time = pd.to_timedelta(original_time)
    new_time = new_time - (new_time[0] - pd.Timedelta(minutes=30))
    new_time_str = new_time.apply(format_time_as_hours)
    return new_time_str


def format_time_as_hours(time: pd.Timedelta) -> str:
    """Convert timedelta to hours, with one decimal, as string."""
    hours = time.total_seconds() / 3600
    return f"{hours:.1f}"


def load_mtp_data(path_to_raw_data: str) -> pd.DataFrame:
    """Read data from path and clean and format it."""
    try:
        data = pd.read_excel(path_to_raw_data, dtype={TIME_COLUMN: str})
    except ValueError as e:
        raise MTPAnalyzerException(
            f"Error attempting to read '{path_to_raw_data}' as Excel file: {str(e)}",
        )
    logging.debug(f"Read '{path_to_raw_data}' successfully as Excel file.")

    data = data.drop(columns=COLUMNS_TO_REMOVE)
    data = data.assign(
        # Modify the existing Time column to work in formulas
        Time=lambda x: start_experiment_from_zero(x[TIME_COLUMN]),
    )
    logging.debug("Reformatted 'Time' column of raw data.")

    return data


def load_sample_table(sample_table_path: str) -> dict[str, str]:
    """Load the sample table as DataFrame from provided path."""
    try:
        raw_data: pd.DataFrame = pd.read_excel(sample_table_path, index_col=0, header=0)
    except ValueError as e:
        raise MTPAnalyzerException(
            f"Error attempting to read '{sample_table_path}' as Excel file: {str(e)}",
        )
    logging.debug(f"Read '{sample_table_path}' successfully as Excel file.")

    well_mapping: dict[str, str] = {}
    for row_index in raw_data.index.tolist():
        for column_index in raw_data.columns.tolist():
            well_index = f"{row_index}{column_index}"
            well_mapping[well_index] = raw_data.at[row_index, column_index]

    logging.debug(
        "Generated mapping dictionary for well indices and content of wells."
    )

    return well_mapping
