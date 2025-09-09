from fastapi import APIRouter, HTTPException
from core.registry import register_widget
import pandas as pd
from typing import List
import json
import asyncio
import numpy as np
from fastapi import Depends

from core.auth import get_current_user

equity_cn_router = APIRouter()

@register_widget({
    "name": "A股财务指标",
    "description": "获取A股的财务指标",
    "category": "Equity",
    "subcategory": "Financials",
    "type": "table",
    "widgetId": "financial_data",
    "endpoint": "cn/financial_data",
    "gridData": {
        "w": 80,
        "h": 12
    },
    "data": {
        "table": {
            "showAll": True
        }
    },
    "params": [
        {
            "type": "endpoint",
            "paramName": "ticker",
            "label": "Symbol",
            "value": "600325",
            "description": "Stock ticker",
            "optionsEndpoint": "/stock_tickers"
        }
    ]
})
@equity_cn_router.get("/financial_data")
def get_financial_data(
    ticker: str
):
    """Get historical stock prices"""
    from openbb_akshare.utils.ak_compare_company_facts import fetch_compare_company
    from mysharelib.tools import normalize_symbol

    _, symbol_f, _ = normalize_symbol(ticker)

    df_comparison = fetch_compare_company(symbol_f)
    return df_comparison.to_dict(orient="records")
