"""Functions related to noise removal based on blank wells."""

import pandas as pd


def normalize(data: pd.DataFrame) -> pd.DataFrame:
    """Normalize all value in dataframe except first column."""

    def normalize_column(s: pd.Series) -> pd.Series:  # type: ignore
        min_val = s.min()
        max_val = s.max()
        return (s - min_val) / (max_val - min_val)  # type: ignore

    data = data.apply(normalize_column)

    return data
