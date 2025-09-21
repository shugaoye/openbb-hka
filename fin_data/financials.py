import pandas as pd
from openbb import obb
from . import default_provider

def get_balance(ticker: str, period: str, limit: int) -> pd.DataFrame:
    """
    Get balance sheet
    """
    from mysharelib.tools import normalize_symbol

    symbol_b, symbol_f, market = normalize_symbol(ticker)
    balance_df = obb.equity.fundamental.balance(symbol=symbol_b, period=period, limit=limit, provider=default_provider).to_dataframe().head(limit)
    if market  == "HK":
        if "股东权益合计" in balance_df.columns:
            return balance_df[["period_ending", "股东权益合计", "总负债", "总资产"]]
        else:
            return balance_df[["period_ending", "总权益", "总负债", "总资产"]]
    else:
        return balance_df[["period_ending", "fiscal_period", "股东权益", "总负债", "总资产"]]

def get_cash_flow(ticker: str, period: str, limit: int) -> pd.DataFrame:
    """
    Get cash flow
    """
    from mysharelib.tools import normalize_symbol

    symbol_b, symbol_f, market = normalize_symbol(ticker)
    cash_flow_df = obb.equity.fundamental.cash(symbol=symbol_b, period=period, limit=limit, provider=default_provider).to_dataframe().head(limit)
    if market  == "HK":
        return cash_flow_df
    else:
        return cash_flow_df[["period_ending", "fiscal_period","营业性现金流","投资性现金流","融资性现金流"]]

def get_income(ticker: str, period: str, limit: int) -> pd.DataFrame:
    """
    Get income statement
    """
    from mysharelib.tools import normalize_symbol

    symbol_b, symbol_f, market = normalize_symbol(ticker)

    income_df = obb.equity.fundamental.income(symbol=symbol_b, period=period, limit=limit, provider=default_provider).to_dataframe()
    if market  == "HK":
        if "经营收入总额" in income_df.columns:
            return income_df[["period_ending",'经营收入总额','股东应占溢利']].head(limit)
        else:
            return income_df[["period_ending",'营业额','股东应占溢利']].head(limit)
    else:
        if "总营收" in income_df.columns:
        # Column exists
            return income_df[["period_ending","fiscal_period","总营收","净利润"]].head(limit)
        elif "OPERATE_INCOME" in income_df.columns:
            new_df = income_df[["period_ending","fiscal_period","OPERATE_INCOME","净利润"]]
            new_df = new_df.rename(columns={"OPERATE_INCOME": "总营收"})
            return new_df.head(limit)
        else:
            raise ValueError("Neither '总营收' nor 'OPERATE_INCOME' found in the DataFrame columns.")