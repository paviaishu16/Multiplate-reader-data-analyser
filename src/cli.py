import argparse
from version import __version__


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
            "-v",
            "--verbose",
            help="Log verbosely if used (show debug messages)",
            action="store_true",
        )

        parser.add_argument(
            "--version",
            action="version",
            version=f"Version {__version__}",
        )

        return parser.parse_args()
