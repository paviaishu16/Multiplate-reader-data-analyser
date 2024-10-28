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


def extract_growth_parameters(
    growth_rates: dict[str, pd.DataFrame],
    blank_data: pd.DataFrame,
    lag_time_threshold: int,
) -> pd.DataFrame:
    """Extract growth parameters from data.

    Args:
        data:

    Return:
        DataFrame with growth parameter name as index and growth
        parameter value as columns. Parameters are extracted
        independently for each column, and each column preserves its
        name. The extracted parameters are:

            - L: Lag time.
            - k: Maximum growth rate in well.
            - t: Inflection point.
            - A: Asymptotic maximum population.
    """
    ts = growth_rates["timestamps"]
    gr = growth_rates["growth_rates"]

    lag_time = ts.where(ts > lag_time_threshold).agg("min")

    maxidx = gr.where((ts >= 20) & (ts <= 48)).idxmax()
    max_growth_rate = pd.Series({col: gr.at[idx, col] for col, idx in maxidx.items()})
    inflection_point = pd.Series({col: ts.at[idx, col] for col, idx in maxidx.items()})

    as_max_pop = blank_data.agg("max")

    growth_parameters = pd.concat(
        [lag_time, max_growth_rate, inflection_point, as_max_pop],
        axis=1,
    )
    growth_parameters.columns = pd.Index(["L", "k", "t", "A"])

    return growth_parameters


def get_replicates_average(data: pd.DataFrame, names: dict[str, str]) -> pd.DataFrame:
    """Reduce df to average of wells with same sample."""
    data = data.rename(columns=names)
    data = data.T.groupby(by=data.columns).mean().T
    return data
