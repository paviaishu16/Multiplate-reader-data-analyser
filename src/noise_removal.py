"""Functions related to noise removal based on blank wells."""

import logging

import pandas as pd

BLANK_LABEL = "BLK"


def separate_blanks(
    original_data: pd.DataFrame,
    well_mapping: dict[str, str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split a dataframe into two, based on if well is a blank."""
    is_filled = [well_mapping[x] != BLANK_LABEL for x in original_data.columns]
    filled_wells = original_data.copy().loc[:, is_filled]

    is_blank = [well_mapping[x] == BLANK_LABEL for x in original_data.columns]
    empty_wells = original_data.copy().loc[:, is_blank]

    return filled_wells, empty_wells


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
    data.iloc[1:, :] = (
        cur_weight * data.iloc[1:, :] + prev_weight * prev_data.iloc[1:, :]
    )
    logging.debug("Data has been smoothed")
    return data


def remove_noise(filled_wells: pd.DataFrame, blank_wells: pd.DataFrame) -> pd.DataFrame:
    """Use blank well data to remove noise from filled well data.

    Args:
        filled_wells: DataFrame with data for wells with content in
            them. (The content that the experiment is done on).
        blank_wells: DataFrame with data from empty wells.

    Return:
        The blanked version of the filled wells.
    """
    average_noise = blank_wells.mean(axis="columns")
    return filled_wells.sub(average_noise, axis="index")


def normalize_blanked_data(blanked_data: pd.DataFrame) -> pd.DataFrame:
    """Normalize blanked data, so that it is above 0 and at most 2.

    The blanked data will have been normalized before being blanked,
    but the blanking process may make some values negative. The
    smallest value of each column will be removed from that column.
    All zeroes will be changed to a small positive value (0.00001)

    Args:
        blanked_data: The blanked data to normalize.

    Return:
        The renormalized blanked data.
    """

    def shift_column_values_down_to_zero(s: pd.Series) -> pd.Series:  # type: ignore
        """Perform the normalization for a single column."""
        return (s - s.min()).replace(0.0, 0.00001)  # type: ignore

    return blanked_data.apply(shift_column_values_down_to_zero)
