import pandas as pd
from openbb import obb
from . import default_provider

def get_news(ticker: str, limit: int = 10)->pd.DataFrame:
    """Get latest news for a stock"""
    return obb.news.company(ticker, provider=default_provider).to_dataframe().head(limit)

def get_profile(ticker: str)->pd.DataFrame:
    """
    Get company profile
    """
    return obb.equity.profile(symbol=ticker, provider=default_provider).to_dataframe()

def get_historical_prices(
    ticker: str,
    interval: str,
    interval_multiplier: int,
    start_date: str,
    end_date: str
    )->pd.DataFrame:
    """
    Get historical prices
    """
    return obb.equity.price.historical(symbol=ticker, start_date=start_date, end_date=end_date, provider=default_provider).to_dataframe()