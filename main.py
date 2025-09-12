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
import logging
from mysharelib.tools import setup_logger

setup_logger(__name__)
logger = logging.getLogger(__name__)

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


# Add back the endpoint to get available tickers
@app.get("/earnings_press_releases/tickers")
async def get_tickers(token: str = Depends(get_current_user)):
    """Get available tickers for earnings press releases"""
    return {}

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
            "optionsEndpoint": "/cn/tickers"
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
            "optionsEndpoint": "/cn/tickers"
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
            "optionsEndpoint": "/cn/tickers"
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