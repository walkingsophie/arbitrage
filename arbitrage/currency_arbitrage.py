import numpy as np
import warnings

def exchange_rate_to_matrix(exchange_rates):
    """
    Converts a dictionary of exchange rates into a matrix representation.

    Parameters:
    exchange_rates (dict): A dictionary where keys are currency pairs (e.g., 'USD/EUR') 
                           and values are the corresponding exchange rates.

    Returns:
    np.ndarray: A 2D numpy array representing the exchange rate matrix.
    list: A list of unique currencies corresponding to the rows and columns of the matrix.
    """
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
                else:
                    # If no direct exchange rate is available, set it to 0
                    rate_matrix[i][j] = 0.0

    return rate_matrix, currencies  

def exchange_matrix_to_dict(rate_matrix, currencies):
    """
    Converts a matrix representation of exchange rates back into a dictionary.

    Parameters:
    rate_matrix (np.ndarray): A 2D numpy array representing the exchange rate matrix.
    currencies (list): A list of unique currencies corresponding to the rows and columns of the matrix.

    Returns:
    dict: A dictionary where keys are currency pairs (e.g., 'USD/EUR') 
          and values are the corresponding exchange rates.
    """
    exchange_rates = {}
    num_currencies = len(currencies)

    for i in range(num_currencies):
        for j in range(num_currencies):
            if i != j and rate_matrix[i][j] > 0:
                pair = f"{currencies[i]}/{currencies[j]}"
                exchange_rates[pair] = rate_matrix[i][j]

    return exchange_rates

def best_exchange_path(exchange_rates, start_currency, end_currency):
    """
    Finds the best exchange path from start_currency to end_currency using the given exchange rates.

    Parameters:
    exchange_rates (dict): A dictionary where keys are currency pairs (e.g., 'USD/EUR') 
                           and values are the corresponding exchange rates.
    start_currency (str): The currency to start from.
    end_currency (str): The currency to end at.

    Returns:
    tuple: A tuple containing the best exchange rate and the path taken as a list of currencies.
           If no path exists, returns (None, []).
    """

    if detect_arbitrage(exchange_rates) != []:
        warnings.warn("Arbitrage detected in exhange rates, thus there may be paths that yield infinite profit. Returning None for best exchange path.", UserWarning)
        return None, []  # Arbitrage detected, no valid path

    rate_matrix, currencies = exchange_rate_to_matrix(exchange_rates)
    num_currencies = len(currencies)

    # Create a mapping from currency to index
    currency_index = {currency: index for index, currency in enumerate(currencies)}

    if start_currency not in currency_index or end_currency not in currency_index:
        return None, []  # Invalid currencies

    start_index = currency_index[start_currency]
    end_index = currency_index[end_currency]

    # Use Dijkstra's algorithm to find the best path
    distances = np.full(num_currencies, -np.inf)
    distances[start_index] = 1.0  # Start with an exchange rate of 1
    previous = [None] * num_currencies

    for _ in range(num_currencies - 1):
        for i in range(num_currencies):
            for j in range(num_currencies):
                if rate_matrix[i][j] > 0 and distances[i] * rate_matrix[i][j] > distances[j]:
                    distances[j] = distances[i] * rate_matrix[i][j]
                    previous[j] = i

    # Reconstruct the path
    path = []
    current_index = end_index
    while current_index is not None:
        path.append(currencies[current_index])
        current_index = previous[current_index]

    path.reverse()

    if distances[end_index] == -np.inf:
        return None, []  # No path found

    return distances[end_index], path

def detect_arbitrage(exchange_rates):
    """
    Detects if there is an arbitrage opportunity in the given exchange rates.

    Parameters:
    exchange_rates (dict): A dictionary where keys are currency pairs (e.g., 'USD/EUR') 
                           and values are the corresponding exchange rates.

    Returns:
    list: A list of currencies involved in the arbitrage cycle, if any. 
          Returns an empty list if no arbitrage is detected.
    """
    rate_matrix, currencies = exchange_rate_to_matrix(exchange_rates)
    num_currencies = len(currencies)

    # Use the Bellman-Ford algorithm to detect negative cycles
    log_rate_matrix = -np.log(rate_matrix + 1e-10)  # Use log to convert multiplication to addition

    distances = np.full(num_currencies, np.inf)
    distances[0] = 0  # Start from the first currency

    for _ in range(num_currencies - 1):
        for i in range(num_currencies):
            for j in range(num_currencies):
                if distances[i] + log_rate_matrix[i][j] < distances[j]:
                    distances[j] = distances[i] + log_rate_matrix[i][j]

    # Check for negative cycles
    for i in range(num_currencies):
        for j in range(num_currencies):
            if distances[i] + log_rate_matrix[i][j] < distances[j]:
                # Arbitrage detected, reconstruct the cycle
                cycle = []
                visited = set()
                current_index = j
                while current_index not in visited:
                    visited.add(current_index)
                    cycle.append(currencies[current_index])
                    current_index = np.argmin(log_rate_matrix[current_index])  # Move to the next currency in the cycle
                cycle.append(currencies[current_index])  # Close the cycle
                return cycle[::-1]  # Return the cycle in correct order

    return []  # No arbitrage detected