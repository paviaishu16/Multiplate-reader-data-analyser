import argparse
import sys

import pandas as pd

__author__ = "Simon"
__version__ = "0.1.0"
__licence__ = "MIT"

COLUMNS_TO_REMOVE = ["T° Fluo50_k:450,530"]
TIME_COLUMN = "Time"


class MTPAnalyzerException(Exception):
    """Base class for exceptions for this app."""

    pass


class CLI:

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(
            description="An app to analyze and generate graphs from raw MTP data"
        )

        parser.add_argument(
            "raw_data_path",
            help="Path to xlsx file with raw MTP data",
        )

        parser.add_argument(
            "-t",
            "--sample-table",
            action="store",
            help="Path to xlsx file with well labels",
            dest="sample_table_path",
        )

        parser.add_argument(
            "--version",
            action="version",
            version=f"Version {__version__}",
        )

        return parser.parse_args()


def start_experiment_from_zero(original_time: pd.Series) -> pd.Series:
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


def format_time_as_hours(time: pd.Timedelta) -> pd.Timedelta:
    """Convert timedelta to hours, with one decimal, as string."""
    hours = time.total_seconds() / 3600
    return f"{hours:.1f}"


def preprocess_data(path_to_raw_data: str) -> pd.DataFrame:
    """Read data from path and clean and format it."""
    try:
        data = pd.read_excel(path_to_raw_data, dtype={TIME_COLUMN: str})
    except ValueError as e:
        raise MTPAnalyzerException(
            f"Error attempting to read '{path_to_raw_data}' as Excel file: {str(e)}",
        )

    data = data.drop(columns=COLUMNS_TO_REMOVE)
    data = data.assign(
        # Modify the existing Time column to work in formulas
        Time=lambda x: start_experiment_from_zero(x[TIME_COLUMN]),
    )

    return data


def main() -> int:
    """Main entrypoint of application."""
    args = CLI.parse_args()
    try:
        data = preprocess_data(args.raw_data_path)
    except MTPAnalyzerException as e:
        print(
            f"MTPAnalyzer encountered an error preprocessing data: {str(e)}",
            file=sys.stderr,
        )
        return 1

    print(data.head())
    return 0


if __name__ == "__main__":
    main()
