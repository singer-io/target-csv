# target-csv

Writes [Singer](https://singer.io) data to CSV files.

## Install

Requires Python 3

```bash
› pip install target-csv
```

## Use

target-csv takes two types of input:

1. An optional config file
2. A stream of Singer-formatted data on stdin

The config file can be used to set formatting parameters for the csv,
like the delimiter - see [config.sample.json](config.sample.json) for
examples.

It can be run as follows:

```bash
› tap-some-api | target-csv --config config.json
```

where `tap-some-api` is a program that writes Singer-formatted data to
stdout. [Singer.io](https://www.singer.io) contains a directory of
such programs - called "Taps."

---

Copyright &copy; 2017 Stitch
