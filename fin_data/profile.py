import pandas as pd
from openbb import obb
from . import default_provider

def get_news(ticker: str, limit: int = 10)->pd.DataFrame:
    """Get latest news for a stock"""
    return obb.news.company(ticker, provider=default_provider).to_dataframe().head(limit)

def get_info(ticker: str)->pd.DataFrame:
    """
    获取A股基本信息
    """
    from mysharelib.tools import normalize_symbol

    _, symbol_f, _ = normalize_symbol(ticker)

    df_base = obb.equity.fundamental.metrics(symbol=symbol_f, provider=default_provider).to_dataframe().T
    return df_base[0]

def get_profile(ticker: str)->pd.DataFrame:
    """
    Get company profile
    """
    from mysharelib.tools import get_timestamp
    profile_df = obb.equity.profile(symbol=ticker, provider=default_provider).to_dataframe()
    profile_df=profile_df[["symbol", "公司名称", "公司简介", "主要范围", "成立日期", "上市日期"]]
    profile_df['成立日期']=pd.to_datetime(get_timestamp(profile_df['成立日期']), unit='s').date()
    profile_df.set_index('symbol', inplace=True)
    return profile_df

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