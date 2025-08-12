import pandas as pd
from openbb import obb
from . import default_provider

def get_balance(ticker: str, period: str, limit: int) -> pd.DataFrame:
    """
    Get balance sheet
    """
    return obb.equity.fundamental.balance(symbol=ticker, period=period, limit=limit, provider=default_provider).to_dataframe().head(limit)

def get_cash_flow(ticker: str, period: str, limit: int) -> pd.DataFrame:
    """
    Get cash flow
    """
    return obb.equity.fundamental.cash(symbol=ticker, period=period, limit=limit, provider=default_provider).to_dataframe().head(limit)

def get_income(ticker: str, period: str, limit: int) -> pd.DataFrame:
    """
    Get income statement
    """
    return obb.equity.fundamental.income(symbol=ticker, period=period, limit=limit, provider=default_provider).to_dataframe().head(limit)