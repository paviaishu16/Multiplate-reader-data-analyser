# MTP Data Analyzer

A project for analyzing data from MTPs.

## Usage

Requires: Python>=3.12.

First, clone this repository.

Second, install dependencies:

```console
$ pip install -r requirements.txt
```

Third, run the script from the repository root, providing your source files (raw
data and well map):

```console
$ python.exe src\main.py C:\User\username\path\to\your\raw_data.xlsx --sample-table sample-table.xlsx
```

On Linux, the command might be slightly different, more like this format:

```console
$ python3 src/main.py path/to/your/raw_data.xlsx --sample-table sample-table.xlsx
```

