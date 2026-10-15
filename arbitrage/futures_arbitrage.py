###
## Calculates arbitrage opportinities for futures
###

class Future:
    def __init__(self, price, expiration):
        self.price = price
        self.expiration = expiration

def detect_arbitrage(futures, current_price, interest_rate=0):
    """
    Detects arbitrage opportunities in a given set of futures prices.

    Parameters:
    futures (list): A list of Future objects representing different futures contracts.
    current_price (float): The current price of the underlying asset.

    Returns:
    list: A list of arbitrage opportunities found, each represented as a tuple 
          (future_expiration, profit_percentage, strategy).
    """
    arbitrage_opportunities = []

    for future in futures:

        # Calculate the theoretical price based on the current price and time to expiration

        theoretical_price = current_price * (1 + interest_rate) ** future.expiration

        if future.price < theoretical_price:
            profit_percentage = ((theoretical_price - future.price) / future.price) * 100
            arbitrage_opportunities.append((future.expiration, profit_percentage, "Buy Future, Sell Spot"))

        if future.price > theoretical_price:
            profit_percentage = ((future.price - theoretical_price) / theoretical_price) * 100
            arbitrage_opportunities.append((future.expiration, profit_percentage, "Sell Future, Buy Spot"))

    return arbitrage_opportunities