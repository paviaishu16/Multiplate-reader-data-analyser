"""Starting point and main logic of application."""

import logging

from exceptions import MTPAnalyzerException
from preprocessing import load_mtp_data, load_sample_table
from cli import CLI


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
    except MTPAnalyzerException as e:
        logging.error(
            f"MTPAnalyzer encountered an error preprocessing data: {str(e)}",
        )
        return 1
    logging.debug("Preprocessing completed successfully.")

    well_mapping = load_sample_table(args.sample_table_path)
    print(data.head())
    print(well_mapping)
    return 0


if __name__ == "__main__":
    main()
