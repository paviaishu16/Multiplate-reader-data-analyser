"""Analyze preprocessed data."""

import pandas as pd


def calculate_slope(mtp_data: pd.DataFrame) -> pd.DataFrame:
    """Calculate slope between each value of each column.

    Args:
        mtp_data: DataFrame with time series' of MTP data.

    Return:
        A new DataFrame with the slope values.
    """
    slope_data = mtp_data.copy()
    time_delta = slope_data.index.to_series()
    time_delta = time_delta.diff()

    def calculate_column_slope(s: pd.Series) -> pd.Series:  # type: ignore
        value_delta = s.diff()
        slope = value_delta / time_delta
        slope = slope.fillna(0.0)
        return slope

    slope_data = slope_data.apply(calculate_column_slope)

    return slope_data
