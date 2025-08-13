import pandas as pd
from openbb import obb
from . import default_provider

def get_balance(ticker: str, period: str, limit: int) -> pd.DataFrame:
    """
    Get balance sheet
    """
    balance_df = obb.equity.fundamental.balance(symbol=ticker, period=period, limit=limit, provider=default_provider).to_dataframe().head(limit)
    return balance_df[["period_ending", "fiscal_period", "totalEquity", "totalDebt", "totalAssets"]]

def get_cash_flow(ticker: str, period: str, limit: int) -> pd.DataFrame:
    """
    Get cash flow
    """
    cash_flow_df = obb.equity.fundamental.cash(symbol=ticker, period=period, limit=limit, provider=default_provider).to_dataframe().head(limit)
    return cash_flow_df[["period_ending", "fiscal_period","TOTAL_OPERATE_INFLOW","TOTAL_OPERATE_OUTFLOW","NETCASH_OPERATE","TOTAL_INVEST_INFLOW","TOTAL_INVEST_OUTFLOW","NETCASH_INVEST","TOTAL_FINANCE_INFLOW","TOTAL_FINANCE_OUTFLOW","NETCASH_FINANCE"]]

def get_income(ticker: str, period: str, limit: int) -> pd.DataFrame:
    """
    Get income statement
    """
    income_df = obb.equity.fundamental.income(symbol=ticker, period=period, limit=limit, provider=default_provider).to_dataframe()
    return income_df[["TOTAL_OPERATE_INCOME","TOTAL_OPERATE_INCOME_YOY","PARENT_NETPROFIT","PARENT_NETPROFIT_YOY"]].head(limit)