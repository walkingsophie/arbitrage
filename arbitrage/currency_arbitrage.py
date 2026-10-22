import numpy as np
import warnings
import math

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
    currencies = sorted(
        {currency for pair in exchange_rates for currency in pair.split('/')}
    )
    
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

    arbitrage_cycle, _ = detect_arbitrage(exchange_rates)
    if arbitrage_cycle:
        warnings.warn(
            "Arbitrage detected in exchange rates; no finite best exchange path exists.",
            UserWarning,
        )
        return None, []  # Arbitrage detected, no valid path

    rate_matrix, currencies = exchange_rate_to_matrix(exchange_rates)
    num_currencies = len(currencies)

    if start_currency not in currencies or end_currency not in currencies:
        return None, []

    # Initialize distances and previous nodes
    distances = np.full(num_currencies, -np.inf)
    previous = [None] * num_currencies

    start_index = currencies.index(start_currency)
    end_index = currencies.index(end_currency)

    distances[start_index] = 0  # Start from the start_currency

    # Relax edges up to num_currencies - 1 times, using only paths from the prior pass.
    for _ in range(num_currencies - 1):
        next_distances = distances.copy()
        next_previous = previous.copy()
        for i in range(num_currencies):
            for j in range(num_currencies):
                if rate_matrix[i][j] > 0 and distances[i] > -np.inf:
                    candidate = distances[i] + np.log(rate_matrix[i][j])
                    if candidate > next_distances[j]:
                        next_distances[j] = candidate
                        next_previous[j] = i
        if np.array_equal(next_distances, distances):
            break
        distances = next_distances
        previous = next_previous

    # Reconstruct the best path
    path = []
    current = end_index
    while current is not start_index:
        if previous[current] is None:
            return None, []  # No path exists
        path.append(currencies[current])
        current = previous[current]
    path.append(currencies[start_index])
    path.reverse()

    return math.exp(distances[end_index]), path

def detect_arbitrage(exchange_rates):
    """
    Detects if there is an arbitrage opportunity in the given exchange rates.

    Parameters:
    exchange_rates (dict): A dictionary where keys are currency pairs (e.g., 'USD/EUR') 
                           and values are the corresponding exchange rates.

    Returns:
    tuple: A tuple containing the list of currencies involved in the arbitrage cycle, if any, and the profit margin.
           Returns an empty list and 0 if no arbitrage is detected.
    """
    rate_matrix, currencies = exchange_rate_to_matrix(exchange_rates)
    num_currencies = len(currencies)

    # Convert rates to log space for Bellman-Ford algorithm
    log_rate_matrix = np.full_like(rate_matrix, np.inf)
    positive_rates = rate_matrix > 0
    log_rate_matrix[positive_rates] = -np.log(rate_matrix[positive_rates])

    # Initialize distances and predecessors
    distances = np.zeros(num_currencies)
    predecessors = [None] * num_currencies

    # Initializing all distances to zero is equivalent to adding a super-source,
    # so cycles are detected even in disconnected components.
    updated_currency = None
    for _ in range(num_currencies):
        updated_currency = None
        for i in range(num_currencies):
            for j in range(num_currencies):
                if (log_rate_matrix[i][j] < np.inf
                        and distances[i] + log_rate_matrix[i][j] < distances[j] - 1e-12):
                    distances[j] = distances[i] + log_rate_matrix[i][j]
                    predecessors[j] = i
                    updated_currency = j
        if updated_currency is None:
            return [], 0

    # Follow predecessors into the cycle, then reverse the predecessor chain.
    current = updated_currency
    for _ in range(num_currencies):
        current = predecessors[current]

    cycle = [current]
    next_currency = predecessors[current]
    while next_currency != current:
        cycle.append(next_currency)
        next_currency = predecessors[next_currency]
    cycle.append(current)
    cycle.reverse()

    cycle_log_rate = sum(
        log_rate_matrix[source][target]
        for source, target in zip(cycle, cycle[1:])
    )
    profit_margin = math.exp(-cycle_log_rate) - 1
    return [currencies[index] for index in cycle], profit_margin
