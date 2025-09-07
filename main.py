import json
from pathlib import Path
from importlib.metadata import version
from fastapi import FastAPI, HTTPException, Request, status, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from functools import wraps
import asyncio
from fastapi.websockets import WebSocketState
from core.registry import register_widget, WIDGETS, add_template, TEMPLATES
from core.config import config
from core.auth import get_current_user
from routes.charts import charts_router
from routes.equity_cn import equity_cn_router
from routes.equity_hk import equity_hk_router

app = FastAPI(title=config.title,
    description=config.description,
    version="0.1.2")

origins = [
    "https://pro.openbb.co",
    "http://localhost:1420"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Info": f"{config.description}"}

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy"}

app.include_router(
    charts_router,
    prefix="/charts",
)

app.include_router(
    equity_cn_router,
    prefix="/cn",
)
add_template("cn")

app.include_router(
    equity_hk_router,
    prefix="/hk",
)
add_template("hk")

# Apps configuration file for the OpenBB Workspace
# it contains the information and configuration about all the
# apps that will be displayed in the OpenBB Workspace
@app.get("/apps.json")
def get_apps():
    """Apps configuration file for the OpenBB Workspace
    
    Returns:
        JSONResponse: The contents of apps.json file
    """
    # Read and return the apps configuration file
    return list(TEMPLATES.values())

# Endpoint that returns the registered widgets configuration
# The WIDGETS dictionary is maintained by the registry.py helper
# which automatically registers widgets when using the @register_widget decorator
@app.get("/widgets.json")
def get_widgets():
    """Returns the configuration of all registered widgets
    
    The widgets are automatically registered through the @register_widget decorator
    and stored in the WIDGETS dictionary from registry.py
    Returns:
        dict: The configuration of all registered widgets
    Issue:
    Refer to the issue below for more details about authentication header
    https://github.com/OpenBB-finance/OpenBB/issues/7175
    """
    return WIDGETS

@register_widget({
    "name": "利润表",
    "description": "Financial statements that provide information about a company's revenues, expenses, and profits over a specific period.",
    "category": "Equity",
    "subcategory": "Financials",
    "widgetType": "individual",
    "widgetId": "income",
    "endpoint": "income",
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
            "description": "Ticker to get 利润表 for (Free tier: AAPL, MSFT, TSLA)",
            "optionsEndpoint": "/stock_tickers"
        },
        {
            "type": "text",
            "value": "annual",
            "paramName": "period",
            "label": "Period",
            "description": "Period to get statements from",
            "options": [
                {"value": "annual", "label": "Annual"},
                {"value": "quarter", "label": "Quarterly"},
                {"value": "ttm", "label": "TTM"}
            ]
        },
        {
            "type": "number",
            "paramName": "limit",
            "label": "Number of Statements",
            "value": "10",
            "description": "Number of statements to display"
        }
    ]
})
@app.get("/income")
def get_income(ticker: str, period: str, limit: int, token: str = Depends(get_current_user)):
    """Get 利润表"""
    from fin_data.financials import get_income
    return get_income(ticker, period, limit).to_dict(orient="records")

@register_widget({
    "name": "资产负债表",
    "description": "A financial statement that summarizes a company's assets, liabilities and shareholders' equity at a specific point in time.",
    "category": "Equity",
    "subcategory": "Financials",
    "type": "table",
    "widgetId": "balance",
    "endpoint": "balance",
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
            "description": "Ticker to get 资产负债表 for (Free tier: AAPL, MSFT, TSLA)",
            "optionsEndpoint": "/stock_tickers"
        },
        {
            "type": "text",
            "value": "annual",
            "paramName": "period",
            "label": "Period",
            "description": "Period to get statements from",
            "options": [
                {"value": "annual", "label": "Annual"},
                {"value": "quarter", "label": "Quarterly"},
                {"value": "ttm", "label": "TTM"}
            ]
        },
        {
            "type": "number",
            "paramName": "limit",
            "label": "Number of Statements",
            "value": "10",
            "description": "Number of statements to display"
        }
    ]
})
@app.get("/balance")
def get_balance(ticker: str, period: str, limit: int, token: str = Depends(get_current_user)):
    """Get 资产负债表"""
    from fin_data.financials import get_balance
    return get_balance(ticker, period, limit).to_dict(orient="records")

# @app.get("/financial_metrics")
# def get_financial_metrics(ticker: str, period: str, limit: int, token: str = Depends(get_current_user)):
#     """Get financial metrics and ratios"""
#     return {}

@register_widget({
    "name": "现金流量表",
    "description": "Financial statements that provide information about a company's cash inflows and outflows over a specific period.",
    "category": "Equity",
    "subcategory": "Financials",
    "widgetType": "individual",
    "widgetId": "cash_flow",
    "endpoint": "cash_flow",
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
            "description": "Ticker to get 现金流量表 for (Free tier: AAPL, MSFT, TSLA)",
            "optionsEndpoint": "/stock_tickers"
        },
        {
            "type": "text",
            "value": "annual",
            "paramName": "period",
            "label": "Period",
            "description": "Period to get statements from",
            "options": [
                {"value": "annual", "label": "Annual"},
                {"value": "quarter", "label": "Quarterly"},
                {"value": "ttm", "label": "TTM"}
            ]
        },
        {
            "type": "number",
            "paramName": "limit",
            "label": "Number of Statements",
            "value": "10",
            "description": "Number of statements to display"
        }
    ]
})
@app.get("/cash_flow")
def get_cash_flow(ticker: str, period: str, limit: int, token: str = Depends(get_current_user)):
    """Get 现金流量表"""
    from fin_data.financials import get_cash_flow
    return get_cash_flow(ticker, period, limit).to_dict(orient="records")

@register_widget({
    "name": "基本信息",
    "description": "Get key company information including name, CIK, market cap, total employees, website URL, and more.",
    "category": "Equity",
    "subcategory": "Company Info",
    "type": "markdown",
    "widgetId": "company_facts",
    "endpoint": "company_facts",
    "gridData": {
        "w": 10,
        "h": 12
    },
    "data": {
        "table": {
            "showAll": True,
            "columns": [
                {"field": "fact", "headerName": "Fact", "width": 200},
                {"field": "value", "headerName": "Value", "width": 200}
            ]
        }
    },
    "params": [
        {
            "type": "endpoint",
            "paramName": "ticker",
            "label": "Symbol",
            "value": "600325",
            "description": "Ticker to get company facts for (Free tier: AAPL, MSFT, TSLA)",
            "optionsEndpoint": "/stock_tickers"
        }
    ]
})
@app.get("/company_facts")
def get_company_facts(
    ticker: str, 
    token: str = Depends(get_current_user)
    ):
    """Get company facts for a ticker"""
    from fin_data.profile import get_info
    return get_info(ticker).to_markdown()

# Add back the endpoint to get available tickers
@app.get("/earnings_press_releases/tickers")
async def get_tickers(token: str = Depends(get_current_user)):
    """Get available tickers for earnings press releases"""
    return {}

@app.get("/stock_tickers")
def get_stock_tickers(token: str = Depends(get_current_user)):
    """Get available stock tickers for free tier"""
    return [
        {"label": "华发股份", "value": "600325"},
        {"label": "中国石化", "value": "600028"},
        {"label": "招商银行", "value": "600036"},
        {"label": "招商蛇口", "value": "001979"},
        {"label": "美的集团", "value": "000333"},
        {"label": "中远海控", "value": "601919"},
        {"label": "中国石油", "value": "601857"},
        {"label": "招商蛇口", "value": "001979"},
        {"label": "中国联通", "value": "600050"},
        {"label": "中国移动", "value": "600941"},
        {"label": "中国电信", "value": "601728"},
        {"label": "中国人保", "value": "601319"},
        {"label": "大秦铁路", "value": "601006"},
        {"label": "物产中大", "value": "600704"},
        {"label": "国投电力", "value": "600886"},
        {"label": "辽港股份", "value": "601880"},
        {"label": "中信银行", "value": "601998"},
        {"label": "招商证券", "value": "600999"},
        {"label": "平安银行", "value": "000001"},
        {"label": "中国平安", "value": "601318"},
        {"label": "农业银行", "value": "601288"},
        {"label": "中国银行", "value": "601988"},
        {"label": "建设银行", "value": "601939"},
        {"label": "工商银行", "value": "601398"},
        {"label": "保利发展", "value": "600048"}
    ]

@register_widget({
    "name": "相关新闻",
    "description": "Get recent news articles for stocks, including headlines, publish dates, and article summaries.",
    "category": "Equity",
    "subcategory": "News",
    "type": "table",
    "widgetId": "stock_news",
    "endpoint": "stock_news",
    "gridData": {
        "w": 40,
        "h": 8
    },
    "data": {
        "table": {
            "showAll": True,
            "columnsDefs": [
                {"field": "date", "headerName": "Date", "width": 180, "cellDataType": "text", "pinned": "left"},
                {"field": "title", "headerName": "Title", "width": 300, "cellDataType": "text"},
                {"field": "source", "headerName": "Source", "width": 150, "cellDataType": "text"},
                {"field": "author", "headerName": "Author", "width": 150, "cellDataType": "text"},
                {"field": "sentiment", "headerName": "Sentiment", "width": 120, "cellDataType": "text"},
                {"field": "url", "headerName": "URL", "width": 200, "cellDataType": "text"}
            ]
        }
    },
    "params": [
        {
            "type": "endpoint",
            "paramName": "ticker",
            "label": "Symbol",
            "value": "600325",
            "description": "Stock ticker to get news for (Free tier: AAPL, MSFT, TSLA)",
            "multiSelect": False,
            "optionsEndpoint": "/stock_tickers"
        },
        {
            "type": "number",
            "paramName": "limit",
            "label": "Number of Articles",
            "value": "10",
            "description": "Maximum number of news articles to display"
        }
    ]
})
@app.get("/stock_news")
async def get_stock_news(ticker: str = Query(..., description="Stock ticker"), 
                         limit: int = 10, token: str = Depends(get_current_user)):
    """Get news articles for a stock"""
    from fin_data.profile import get_news
    return get_news(ticker, limit).to_dict(orient="records")

@register_widget({
    "name": "历史股价",
    "description": "Get historical price data for stocks with customizable intervals and date ranges.",
    "category": "Equity",
    "subcategory": "Prices",
    "type": "table",
    "widgetId": "stock_prices_historical",
    "endpoint": "stock_prices_historical",
    "gridData": {
        "w": 40,
        "h": 8
    },
    "data": {
        "table": {
            "enableCharts": True,
            "showAll": False,
            "chartView": {
                "enabled": True,
                "chartType": "line"
            },
            "columnsDefs": [
                {"field": "date", "headerName": "Date", "width": 180, "chartDataType": "time"},
                {"field": "open", "headerName": "Open", "width": 120, "cellDataType": "number"},
                {"field": "high", "headerName": "High", "width": 120, "cellDataType": "number"},
                {"field": "low", "headerName": "Low", "width": 120, "cellDataType": "number"},
                {"field": "close", "headerName": "Close", "width": 120, "chartDataType": "series"},
                {"field": "volume", "headerName": "Volume", "width": 120, "cellDataType": "number"}
            ]
        }
    },
    "params": [
        {
            "type": "endpoint",
            "paramName": "ticker",
            "label": "Symbol",
            "value": "600325",
            "description": "Stock ticker to get historical prices for (Free tier: AAPL, MSFT, TSLA)",
            "optionsEndpoint": "/stock_tickers"
        },
        {
            "type": "text",
            "value": "day",
            "paramName": "interval",
            "label": "Interval",
            "description": "Time interval for prices",
            "options": [
                {"value": "minute", "label": "Minute"},
                {"value": "day", "label": "Day"},
                {"value": "week", "label": "Week"},
                {"value": "month", "label": "Month"},
                {"value": "year", "label": "Year"}
            ]
        },
        {
            "type": "number",
            "paramName": "interval_multiplier",
            "label": "Interval Multiplier",
            "value": "1",
            "description": "Multiplier for the interval (e.g., 5 for every 5 minutes)"
        },
        {
            "type": "date",
            "paramName": "start_date",
            "label": "Start Date",
            "value": "2024-01-01",
            "description": "Start date for historical data"
        },
        {
            "type": "date",
            "paramName": "end_date",
            "label": "End Date",
            "value": "2024-03-20",
            "description": "End date for historical data"
        }
    ]
})
@app.get("/stock_prices_historical")
def get_stock_prices_historical(
    ticker: str,
    interval: str,
    interval_multiplier: int,
    start_date: str,
    end_date: str, 
    token: str = Depends(get_current_user)
):
    """Get historical stock prices"""
    from fin_data.profile import get_historical_prices
    stock_prices = get_historical_prices(ticker, interval, interval_multiplier, start_date, end_date)
    return stock_prices.reset_index().to_dict(orient="records")

@register_widget({
    "name": "Earnings Press Releases",
    "description": "Get earnings-related press releases for companies, including URL, publish date, and full text.",
    "category": "Equity",
    "subcategory": "Earnings",
    "type": "markdown",
    "widgetId": "earnings_press_releases",
    "endpoint": "earnings_press_releases",
    "gridData": {
        "w": 40,
        "h": 8
    },
    "params": [
        {
            "type": "endpoint",
            "paramName": "ticker",
            "label": "Symbol",
            "value": "600325",
            "description": "Company ticker to get earnings press releases for",
            "multiSelect": False,
            "optionsEndpoint": "/stock_tickers"
        }
    ]
})
@app.get("/earnings_press_releases")
async def get_earnings_press_releases(ticker: str = Query(..., description="Company ticker"), 
                                      token: str = Depends(get_current_user)):
    """Get earnings press releases for a company"""
    return {}

@register_widget({
    "name": "Insider Trades",
    "description": "Get insider trading activity for stocks, including transaction details, shares traded, and transaction values.",
    "category": "Equity",
    "subcategory": "Trading",
    "type": "table",
    "widgetId": "insider_trades",
    "endpoint": "insider_trades",
    "gridData": {
        "w": 40,
        "h": 8
    },
    "data": {
        "table": {
            "showAll": True,
            "columnsDefs": [
                {"field": "transaction_date", "headerName": "Date", "width": 180, "cellDataType": "text", "pinned": "left"},
                {"field": "insider_name", "headerName": "Insider", "width": 200, "cellDataType": "text"},
                {"field": "transaction_type", "headerName": "Type", "width": 120, "cellDataType": "text"},
                {"field": "shares", "headerName": "Shares", "width": 120, "cellDataType": "number"},
                {"field": "price", "headerName": "Price", "width": 120, "cellDataType": "number"},
                {"field": "value", "headerName": "Value", "width": 150, "cellDataType": "number"},
                {"field": "ownership_type", "headerName": "Ownership", "width": 150, "cellDataType": "text"}
            ]
        }
    },
    "params": [
        {
            "type": "endpoint",
            "paramName": "ticker",
            "label": "Symbol",
            "value": "600325",
            "description": "Stock ticker to get insider trades for (Free tier: AAPL, MSFT, TSLA)",
            "optionsEndpoint": "/stock_tickers"
        },
        {
            "type": "number",
            "paramName": "limit",
            "label": "Number of Trades",
            "value": "50",
            "description": "Maximum number of insider trades to display"
        }
    ]
})

@app.get("/insider_trades")
async def get_insider_trades(ticker: str = Query(..., description="Stock ticker"), 
                             limit: int = 50, 
                             token: str = Depends(get_current_user)):
    """Get insider trading activity for a stock"""
    return {}

@app.get("/institutional_investors")
async def get_institutional_investors(token: str = Depends(get_current_user)):
    """Get list of available institutional investors"""
    return {}

@register_widget({
    "name": "Institutional Ownership by Investor",
    "description": "Get institutional ownership data showing holdings of major investors like Berkshire Hathaway, BlackRock, and Vanguard.",
    "category": "Equity",
    "subcategory": "Ownership",
    "type": "table",
    "widgetId": "institutional_ownership_by_investor",
    "endpoint": "institutional_ownership_by_investor",
    "gridData": {
        "w": 40,
        "h": 8
    },
    "data": {
        "table": {
            "showAll": True,
            "columnsDefs": [
                {"field": "ticker", "headerName": "Symbol", "width": 120, "cellDataType": "text", "pinned": "left"},
                {"field": "company_name", "headerName": "Company", "width": 200, "cellDataType": "text"},
                {"field": "shares", "headerName": "Shares", "width": 150, "cellDataType": "number"},
                {"field": "value", "headerName": "Value", "width": 150, "cellDataType": "number"},
                {"field": "weight", "headerName": "Weight %", "width": 120, "cellDataType": "number"},
                {"field": "report_date", "headerName": "Report Date", "width": 180, "cellDataType": "text"}
            ]
        }
    },
    "params": [
        {
            "type": "endpoint",
            "paramName": "investor",
            "label": "Investor",
            "value": "BERKSHIRE_HATHAWAY_INC",
            "description": "Institutional investor name",
            "optionsEndpoint": "/institutional_investors",
            "style": {
                "popupWidth": 450
            }
        },
        {
            "type": "number",
            "paramName": "limit",
            "label": "Number of Holdings",
            "value": "100",
            "description": "Maximum number of holdings to display"
        }
    ]
})

@app.get("/institutional_ownership_by_investor")
async def get_institutional_ownership_by_investor(
    investor: str = Query(..., description="Institutional investor name"),
    limit: int = 100, 
    token: str = Depends(get_current_user)
):
    """Get institutional ownership data for an investor"""
    return {}

@register_widget({
    "name": "Institutional Ownership by Ticker",
    "description": "Get institutional ownership data showing which institutions hold a specific stock.",
    "category": "Equity",
    "subcategory": "Ownership",
    "type": "table",
    "widgetId": "institutional_ownership_by_ticker",
    "endpoint": "institutional_ownership_by_ticker",
    "gridData": {
        "w": 40,
        "h": 8
    },
    "data": {
        "table": {
            "showAll": True,
            "columnsDefs": [
                {"field": "investor", "headerName": "Investor", "width": 250, "cellDataType": "text", "pinned": "left"},
                {"field": "shares", "headerName": "Shares", "width": 150, "cellDataType": "number"},
                {"field": "value", "headerName": "Value", "width": 150, "cellDataType": "number"},
                {"field": "weight", "headerName": "Weight %", "width": 120, "cellDataType": "number"},
                {"field": "report_date", "headerName": "Report Date", "width": 180, "cellDataType": "text"}
            ]
        }
    },
    "params": [
        {
            "type": "endpoint",
            "paramName": "ticker",
            "label": "Symbol",
            "value": "600325",
            "description": "Stock ticker to get institutional ownership for (Free tier: AAPL, MSFT, TSLA)",
            "optionsEndpoint": "/stock_tickers"
        },
        {
            "type": "number",
            "paramName": "limit",
            "label": "Number of Holdings",
            "value": "100",
            "description": "Maximum number of institutional holders to display"
        }
    ]
})

@app.get("/institutional_ownership_by_ticker")
async def get_institutional_ownership_by_ticker(
    ticker: str = Query(..., description="Stock ticker"),
    limit: int = 100, 
    token: str = Depends(get_current_user)
):
    """Get institutional ownership data for a stock"""
    return {}