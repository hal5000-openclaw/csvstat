# csvstat

Summarize a CSV file from the command line. Python 3, standard library only.

Per column: inferred type (int/float/text), non-empty count, empty count,
unique count, min/max/mean for numeric columns, top 3 values for text columns.

## Install

No dependencies. Copy `csvstat.py` or run it from a checkout.

## Usage

    python3 csvstat.py FILE [-d DELIM] [--json]

Use `-` as FILE to read stdin. `-d '\t'` selects tab.

Example (`sample.csv`):

    $ python3 csvstat.py sample.csv
    name (text)
      non-empty: 4  empty: 0  unique: 4
      top: ann (1), bob (1), cy (1)
    age (int)
      non-empty: 3  empty: 1  unique: 3
      min: 25  max: 41  mean: 32
    score (float)
      non-empty: 3  empty: 1  unique: 3
      min: 1.5  max: 3.0  mean: 2.333
    city (text)
      non-empty: 4  empty: 0  unique: 2
      top: Oslo (3), Rome (1)

`--json` prints the same data as a JSON array.

## Tests

    python3 -m unittest discover -s tests

## License

MIT
