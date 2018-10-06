# CSV Parser

The parser will parse all CSV files found in the folder specified in the **config.yaml** file.

Usage (any of):

    python sbury
    python sbury/__main__.py

The default location is "tests/test_csvs"

All files will be parsed to the required specifications, and have the file name, and the parsed contents, printed to the screen.


Additional (test) Files have been added, which allows for processing of multiple rows of data,
* data with different naming conventions, i.e. Mon, TUe-Thu
* Missing Dates (i.e. only Mon-Tue, Thu-Fri)
* Missing Data (i.e. no value for Mon)


Tests can be run with pytest:

    In your terminal, cd into the sbury directory and run:
    
    >> python -m pytest



>> Tested on Windows 10, Python 3.6.5, with a venv

