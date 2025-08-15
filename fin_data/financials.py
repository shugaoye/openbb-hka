import pandas as pd
from openbb import obb
from . import default_provider

def get_balance(ticker: str, period: str, limit: int) -> pd.DataFrame:
    """
    Get balance sheet
    """
    balance_df = obb.equity.fundamental.balance(symbol=ticker, period=period, limit=limit, provider=default_provider).to_dataframe().head(limit)
    return balance_df[["period_ending", "fiscal_period", "股东权益", "总负债", "总资产"]]

def get_cash_flow(ticker: str, period: str, limit: int) -> pd.DataFrame:
    """
    Get cash flow
    """
    cash_flow_df = obb.equity.fundamental.cash(symbol=ticker, period=period, limit=limit, provider=default_provider).to_dataframe().head(limit)
    return cash_flow_df[["period_ending", "fiscal_period","营业性现金流","投资性现金流","融资性现金流"]]

def get_income(ticker: str, period: str, limit: int) -> pd.DataFrame:
    """
    Get income statement
    """
    income_df = obb.equity.fundamental.income(symbol=ticker, period=period, limit=limit, provider=default_provider).to_dataframe()
    return income_df[["总营收","净利润"]].head(limit)