from arbitrage import detect_arbitrage, best_exchange_path

currency_rates = {
    'GBP/USD': 1.38,
    'USD/GBP': 0.72,
    'USD/EUR': 0.85,
    'EUR/USD': 1.18,
    'GBP/EUR': 1.11,
    'EUR/GBP': 0.90,
    'USD/JPY': 110.0,
    'JPY/USD': 0.0091,
    'JPY/GBP': 0.0067,
    'GBP/JPY': 150.0,
    }

# Check for arbitrage opportunities
arbitrage_cycle = detect_arbitrage(currency_rates)
if arbitrage_cycle:
    print(f"Arbitrage detected! Cycle: {' -> '.join(arbitrage_cycle)}")

# Convert EUR to JPY
start_currency = 'EUR'
end_currency = 'JPY'
exchange_rate, path = best_exchange_path(currency_rates, start_currency, end_currency)
print(f"Best exchange path from {start_currency} to {end_currency}: {' -> '.join(path)} with an exchange rate of {exchange_rate:.4f}")