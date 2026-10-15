import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from arbitrage.currency_arbitrage import detect_arbitrage

currency_rates = {
    'USD/EUR': 0.85,
    'USD/JPY': 110.0,
    'EUR/JPY': 130.0,
    }

arbitrage_opportunities = detect_arbitrage(currency_rates)
print(arbitrage_opportunities)