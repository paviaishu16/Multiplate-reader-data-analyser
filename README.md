# MTP Data Analyzer

MTP Data Analyzer is a program for analyzing data from MTPs. It
will perform curve fitting according to both the Richards model and Gompertz
model.

By default, you will get a HTML report as the output artifact of the program.
This will contain plots with the fitted curves and observed data, as well as
tables with parameter optimization data.

Optionally, you can receive an Excel sheet with data from the analysis.

## Dependencies

You need Python 3.12 or greater. You can see what your version is with:

```console
$ python3 --version
```

Then, make sure all the dependencies are installed:

```console
$ pip install -r requirements.txt
```

> [!TIP]
> It might be a good idea to install the dependencies (and run the script) in a
> virtual environment.

## Running it

First, make sure you have installed the [dependencies](#Dependencies).

Second, make sure you have the required source files. This is the raw data from the MTP,
and a "Sample Table" which maps well positions loaded in the MTP to their content.

[Here](https://github.com/paviaishu16/Multiplate-reader-data-analyser/blob/88beff3e59bf7d32aa06a5519471dcbfb630a766/tests/example_data/Raw%20data.xlsx)
is an example of what the raw data file can look like and
[here](https://github.com/paviaishu16/Multiplate-reader-data-analyser/blob/88beff3e59bf7d32aa06a5519471dcbfb630a766/tests/example_data/Sample%20Table.xlsx)
is an example of what the Sample Table can look like.

Provide the path to the raw data as a positional argument to the script and the Sample Table path as the value to the option `--sample-table`. Like this in Windows:

```console
$ python.exe src\main.py C:\User\username\path\to\your\raw_data.xlsx --sample-table sample-table.xlsx
```

And like this on Linux:

```console
$ python3 src/main.py path/to/your/raw_data.xlsx --sample-table sample-table.xlsx
```

This should produce a HTML page at `exports/report.html`. You can open it in
your browser and it will show you plots and parameters optimization data.

If you want the Excel sheet with optimization data as well, add the
`--export-growth-data` option to the command.

## FAQ

**Q: What do I do if the command fails with `ModuleNotFoundError: No module
named X`?**

Most likely you forgot to install the [dependencies](#Dependencies). If doing
that doesn't help, [report an
issue](https://github.com/paviaishu16/Multiplate-reader-data-analyser/issues/new/choose),

**Q: What does the HTML report look like?**

See an example [here](https://paviaishu16.github.io/Multiplate-reader-data-analyser/).
