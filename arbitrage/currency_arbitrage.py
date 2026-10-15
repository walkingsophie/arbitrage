import numpy as np

def detect_arbitrage(exchange_rates):
    """
    Detects arbitrage opportunities in a given set of exchange rates.

    Parameters:
    exchange_rates (dict): A dictionary where keys are currency pairs (e.g., 'USD/EUR') 
                           and values are the corresponding exchange rates.

    Returns:
    list: A list of arbitrage opportunities found, each represented as a tuple 
          (currency_pair, profit_percentage).
    """
    arbitrage_opportunities = []

    # Convert exchange rates to a matrix for easier manipulation
    currencies = list(set([pair.split('/')[0] for pair in exchange_rates.keys()] + 
                          [pair.split('/')[1] for pair in exchange_rates.keys()]))
    
    num_currencies = len(currencies)
    rate_matrix = np.zeros((num_currencies, num_currencies))

    # Fill the rate matrix with the given exchange rates
    for i, currency_from in enumerate(currencies):
        for j, currency_to in enumerate(currencies):
            if i == j:
                rate_matrix[i][j] = 1.0  # Exchange rate to itself is 1
            else:
                pair = f"{currency_from}/{currency_to}"
                if pair in exchange_rates:
                    rate_matrix[i][j] = exchange_rates[pair]
                    rate_matrix[j][i] = 1 /exchange_rates[pair]
                else:
                    # If no direct exchange rate is available, set it to 0
                    rate_matrix[i][j] = 0.0

    # Use the Bellman-Ford algorithm to detect negative cycles (arbitrage opportunities)
    for start_currency in range(num_currencies):
        distances = np.full(num_currencies, np.inf)
        distances[start_currency] = 0

        for _ in range(num_currencies - 1):
            for u in range(num_currencies):
                for v in range(num_currencies):
                    if rate_matrix[u][v] > 0:  # Only consider valid exchange rates
                        new_distance = distances[u] - np.log(rate_matrix[u][v])
                        if new_distance < distances[v]:
                            distances[v] = new_distance

        # Check for negative cycles
        for u in range(num_currencies):
            for v in range(num_currencies):
                if rate_matrix[u][v] > 0:
                    new_distance = distances[u] - np.log(rate_matrix[u][v])
                    if new_distance < distances[v]:
                        profit_percentage = (np.exp(-new_distance) - 1) * 100
                        arbitrage_opportunities.append((f"{currencies[u]}/{currencies[v]}", profit_percentage))

    return arbitrage_opportunities

