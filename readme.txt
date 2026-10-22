# Arbitrage

`arbitrage` is a small Python package that attempts to find arbitrage loops and best exchange paths given a dictionary of currency exchange rates.

Each dictionary key is a directed currency pair such as `"USD/GBP"`; its value is the exchange rate from the first currency to the second.

NumPy is used to find the best exchange paths and detect arbitrage cycles.
## Installation

From inside the `root_directory` directory, install the package in editable mode:

```sh
python -m pip install -e .
```

The required dependencies are specified in `pyproject.toml` and will be installed automatically.

## Examples of use

Find the best exchange path from USD to GBP:

```python
from arbitrage import best_exchange_path

rates = {
    "USD/EUR": 0.9,
    "EUR/GBP": 0.8,
    "USD/GBP": 0.7,
}

rate, path = best_exchange_path(rates, "USD", "GBP")
print(path)  # ['USD', 'EUR', 'GBP']
print(f"{rate:.2f}")  # 0.72
```

Detect an arbitrage cycle. The rates below produce an 8% gain when exchanging
USD to EUR to GBP and back to USD:

```python
from arbitrage import detect_arbitrage

rates = {
    "USD/EUR": 0.9,
    "EUR/GBP": 0.8,
    "GBP/USD": 1.5,
}

cycle, profit_margin = detect_arbitrage(rates)
if cycle:
    print(" -> ".join(cycle))  # EUR -> GBP -> USD -> EUR
    print(f"{profit_margin:.0%}")  # 8%
```

If the exchange rates contain an arbitrage cycle, `best_exchange_path` warns
and returns `(None, [])` because there is no finite best rate.

## Demonstration

The complete demonstration can be run from the root directory using:

```sh
python demo/currency_arbitrage_demo.py
```