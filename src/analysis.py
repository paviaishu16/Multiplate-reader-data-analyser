"""Analyze preprocessed data for e.g. growth rate and growth parameters."""

import logging

import pandas as pd


def calculate_growth_rates(mtp_data: pd.DataFrame) -> pd.DataFrame:
    """Calculate growth rate between each value of each column.

    Args:
        mtp_data: DataFrame with time series' of MTP data.

    Return:
        A new DataFrame with the growth rate values.
    """
    growth_rate_data = mtp_data.copy()
    time_delta = growth_rate_data.index.to_series()
    time_delta = time_delta.diff()

    def calculate_column_growth_rate(s: pd.Series) -> pd.Series:  # type: ignore
        value_delta = s.diff()
        growth_rate = value_delta / time_delta
        growth_rate = growth_rate.fillna(0.0)
        return growth_rate

    growth_rate_data = growth_rate_data.apply(calculate_column_growth_rate)

    logging.debug("Calculated growth rate data.")

    return growth_rate_data


def extract_maximum_growth_rates(growth_rates: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Extract the ten largest growth rate values of each column.

    Extract the ten largest growth rate values of each column of the provided
    DataFrame and add timestamp as a separate column.

    Args:
        growth_rates: DataFrame with values for growth rate in each column.

    Return:
        A DataFrame with MultiIndex column, containing the ten largest
        growth rate values that was in each column in the original DataFrame
        as well as the associated timestamp.
    """

    def top_timestamps(col: pd.Series) -> pd.Series:  # type: ignore
        return (
            col.nlargest(10).index.to_series().reset_index(drop=True).astype("float64")
        )

    def top_growth_rates(col: pd.Series) -> pd.Series:  # type: ignore
        return col.nlargest(10).reset_index(drop=True)

    logging.debug("Extracted the top ten growth rate values for each column.")
    results = {
        "timestamps": growth_rates.apply(top_timestamps),
        "growth_rates": growth_rates.apply(top_growth_rates),
    }
    return results
