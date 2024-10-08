"""Starting point and main logic of application."""

import logging

from analysis import calculate_slope
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

        data = normalize(data)
        data = apply_loess_smoothing(data)

        filled_wells, empty_wells = separate_blanks(data, well_mapping)
        blanked_data = remove_noise(filled_wells, empty_wells)
        normalized_blanked_data = normalize_blanked_data(blanked_data)
        slope_data = calculate_slope(normalized_blanked_data)
        print(slope_data)
    except MTPAnalyzerException as e:
        logging.error(
            f"MTPAnalyzer encountered an error preprocessing data: {str(e)}",
        )
        return 1
    logging.debug("Preprocessing completed successfully.")

    return 0


if __name__ == "__main__":
    main()
