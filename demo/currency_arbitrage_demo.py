from arbitrage import detect_arbitrage, best_exchange_path

# Currency exchange rates without arbitrage opportunities
currency_rates_without_arbitrage = {
    'GBP/USD': 1.35,
    'USD/GBP': 0.72,
    'USD/EUR': 0.83,
    'EUR/USD': 1.17,
    'GBP/EUR': 1.10,
    'EUR/GBP': 0.89,
    'USD/JPY': 108.0,
    'JPY/USD': 0.0091,
    'GBP/JPY': 145.0,
    }

# Convert EUR to JPY
start_currency = 'EUR'
end_currency = 'JPY'
exchange_rate, path = best_exchange_path(currency_rates_without_arbitrage, start_currency, end_currency)
if exchange_rate is not None:
    print(f"Best exchange path from {start_currency} to {end_currency}: {' -> '.join(path)} with an exchange rate of {exchange_rate:.4f}")
else:
    print(f"No exchange path found from {start_currency} to {end_currency}.")

# Currency exchange rates with arbitrage opportunities
currency_rates_with_arbitrage = {
    'GBP/USD': 1.37,
    'USD/GBP': 0.72,
    'USD/EUR': 0.84,
    'EUR/USD': 1.17,
    'GBP/EUR': 1.10,
    'EUR/GBP': 0.89,
    'USD/JPY': 108.0,
    'JPY/USD': 0.0091,
    'GBP/JPY': 150.0,
    }

# Check for arbitrage opportunities
arbitrage_cycle, profit_margin = detect_arbitrage(currency_rates_with_arbitrage)
if arbitrage_cycle:
    print(
        f"Arbitrage detected! Cycle: {' -> '.join(arbitrage_cycle)} "
        f"({profit_margin:.2%} profit)"
    )