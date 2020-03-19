# target-csv

A [Singer](https://singer.io) target that writes data to CSV files.

## How to use it

`target-csv` works together with any other [Singer Tap] to move data from sources like [Braintree], [Freshdesk] and [Hubspot] to CSV-formatted files. It is commonly used for loading data into tools like Excel or simply storing a backup of the source data set.

### Install

We will use [`tap-exchangeratesapi`][Exchangeratesapi] to pull currency exchange rate data from a public data set as an example.

First, make sure Python 3 is installed on your system or follow these installation instructions for [Mac] or [Ubuntu].

It is recommended to install each Tap and Target in a separate Python virtual environment to avoid conflicting dependencies between any Taps and Targets.

```bash
 # Install tap-exchangeratesapi in its own virtualenv
python3 -m venv ~/.virtualenvs/tap-exchangeratesapi
source ~/.virtualenvs/tap-exchangeratesapi/bin/activate
pip install tap-exchangeratesapi
deactivate

# Install target-csv in its own virtualenv
python3 -m venv ~/.virtualenvs/target-csv
source ~/.virtualenvs/target-csv/bin/activate
pip install target-csv
deactivate
```

### Run

We can now run `tap-exchangeratesapi` and pipe the output to `target-csv`.

```bash
~/.virtualenvs/tap-exchangeratesapi/bin/tap-exchangeratesapi | ~/.virtualenvs/target-csv/bin/target-csv
```

The data will be written to a file called `exchange_rate-{timestamp}.csv` in your working directory.

```bash
› cat exchange_rate-{timestamp}.csv
AUD,BGN,BRL,CAD,CHF,CNY,CZK,DKK,GBP,HKD,HRK,HUF,IDR,ILS,INR,JPY,KRW,MXN,MYR,NOK,NZD,PHP,PLN,RON,RUB,SEK,SGD,THB,TRY,ZAR,EUR,USD,date
1.3023,1.8435,3.0889,1.3109,1.0038,6.869,25.47,7.0076,0.79652,7.7614,7.0011,290.88,13317.0,3.6988,66.608,112.21,1129.4,19.694,4.4405,8.3292,1.3867,50.198,4.0632,4.2577,58.105,8.9724,1.4037,34.882,3.581,12.915,0.9426,1.0,2017-02-24T00:00:00Z
```

### Optional Configuration

`target-csv` takes an optional configuration file that can be used to set formatting parameters like the delimiter - see [config.sample.json](config.sample.json) for examples. To run `target-csv` with the configuration file, use this command:

```bash
~/.virtualenvs/tap-exchangeratesapi/bin/tap-exchangeratesapi | ~/.virtualenvs/target-csv/bin/target-csv -c my-config.json
```

Config option **rewrite_headers** (default: `false`) can be used to rewrite the header of the csv-file(s) when the header is updated during the processing. This can happen when new fields are discovered during flattening of records. New discovered header fields are appended at the end of the header. Rewriting happens at the end of the stream, so no performance impact during streaming. Only the header is updated, other lines are copied as-is.

---

Copyright &copy; 2017 Stitch

[Singer Tap]: https://singer.io
[Braintree]: https://github.com/singer-io/tap-braintree
[Freshdesk]: https://github.com/singer-io/tap-freshdesk
[Hubspot]: https://github.com/singer-io/tap-hubspot
[Exchangeratesapi]: https://github.com/singer-io/tap-exchangeratesapi
[Mac]: http://docs.python-guide.org/en/latest/starting/install3/osx/
[Ubuntu]: https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-ubuntu-16-04