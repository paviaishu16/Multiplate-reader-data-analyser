import argparse

__author__ = "Simon"
__version__ = "0.1.0"
__licence__ = "MIT"


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
            "--version",
            action="version",
            version=f"Version {__version__}",
        )

        return parser.parse_args()


def main():
    args = CLI.parse_args()
    print(args)


if __name__ == "__main__":
    main()
