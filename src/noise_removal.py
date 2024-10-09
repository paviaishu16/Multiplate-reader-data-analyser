"""Functions related to noise removal based on blank wells."""

import logging

import pandas as pd


def normalize(data: pd.DataFrame) -> pd.DataFrame:
    """Normalize all value in dataframe except first column."""

    def normalize_column(s: pd.Series) -> pd.Series:  # type: ignore
        min_val = s.min()
        max_val = s.max()
        return (s - min_val) / (max_val - min_val)  # type: ignore

    data = data.apply(normalize_column)

    return data


def apply_loess_smoothing(
    data: pd.DataFrame,
    prev_weight: float = 0.8,
    cur_weight: float = 0.2,
) -> pd.DataFrame:
    """Apply smoothing to all but first column of a dataframe."""
    prev_data = data.shift(1)
    data.iloc[1:, 1:] = (
        cur_weight * data.iloc[1:, 1:] + prev_weight * prev_data.iloc[1:, 1:]
    )
    logging.debug("Data has been smoothed")
    return data
