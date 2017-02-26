# target-csv

A [Singer](https://singer.io) target that writes data to CSV files.

## How to use it

`target-csv` works together with any other [Singer Tap] to move data
from sources like [Braintree], [Freshdesk] and [Hubspot] to
CSV-formatted files. It is commonly used for loading data into tools
like Excel or simply storing a backup of the source data set.

### Install and Run

First, make sure Python 3 is installed on your system or follow these
installation instructions for [Mac](python-mac) or
[Ubuntu](python-ubuntu).

`target-csv` can be run with any [Singer Tap], but we'll use
[`tap-fixerio`][Fixerio] - which pulls currency exchange rate data
from a public data set - as an example.

These commands will install `tap-fixerio` and `target-csv` with pip,
and then run `tap-fixerio`, piping its output to `target-csv`:

```bash
› pip install target-csv
› pip install tap-fixerio
› tap-fixerio | target-csv
```

The data will be written to a file called `exchange_rate.csv` in your
working directory.

If you're using a different Tap, substitute `tap-fixerio` in the final
command above to the command used to run your Tap.

### Optional Configuration

`target-csv` takes an optional configuration file that can be used to
set formatting parameters like the delimiter - see
[config.sample.json](config.sample.json) for examples. To run
`target-csv` with the configuration file, use this command:

```bash
› tap-fixerio | target-csv -c my-config.json
```

---

Copyright &copy; 2017 Stitch

[Singer Tap]: https://singer.io
[Braintree]: https://github.com/singer-io/tap-braintree
[Freshdesk]: https://github.com/singer-io/tap-freshdesk
[Hubspot]: https://github.com/singer-io/tap-hubspot
[Fixerio]: https://github.com/singer-io/tap-fixerio
[python-mac]: http://docs.python-guide.org/en/latest/starting/install3/osx/
[python-ubuntu]: https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-ubuntu-16-04