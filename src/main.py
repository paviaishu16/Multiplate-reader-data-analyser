"""Starting point and main logic of application."""

import logging

from analysis import calculate_growth_rates, extract_maximum_growth_rates
from cli import CLI
from exceptions import MTPAnalyzerException
from noise_removal import (
    apply_loess_smoothing,
    normalize,
    normalize_blanked_data,
    remove_noise,
    separate_blanks,
)
from preprocessing import load_mtp_data, load_sample_table, validate_mtp_columns


def setup_logging(verbose: bool) -> None:
    """Set up configuration for logger with verbosity and format."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


def main() -> int:
    """Structure overall logic of application."""
    args = CLI.parse_args()
    setup_logging(args.verbose)
    try:
        data = load_mtp_data(args.raw_data_path)
        well_mapping = load_sample_table(args.sample_table_path)
        validate_mtp_columns(mtp_data=data, well_mapping=well_mapping)
        logging.debug("Preprocessing completed successfully.")

        data = normalize(data)
        data = apply_loess_smoothing(data)
        filled_wells, empty_wells = separate_blanks(data, well_mapping)
        blanked_data = remove_noise(filled_wells, empty_wells)
        normalized_blanked_data = normalize_blanked_data(blanked_data)
        logging.debug("Noise removal and normalization completed successfully.")

        growth_rates = calculate_growth_rates(normalized_blanked_data)
        max_growth_rates = extract_maximum_growth_rates(growth_rates)
        print(max_growth_rates)
    except MTPAnalyzerException as e:
        logging.error(
            f"MTPAnalyzer encountered an error: {str(e)}",
        )
        return 1

    return 0


if __name__ == "__main__":
    main()
