from fastapi import APIRouter, HTTPException
import plotly.graph_objects as go
import pandas as pd
from typing import List
import json
import asyncio
import numpy as np
from openbb import obb
from core.registry import register_widget
from core.plotly_config import (
    apply_config_to_figure, 
    get_chart_colors,
    create_base_layout
)

charts_router = APIRouter()

@charts_router.get("/candles")
@register_widget({
    "name": "k线图",
    "description": "股价k线图",
    "category": "Equity",
    "type": "chart",
    "endpoint": "charts/candles",
    "widgetId": "charts/candles",
    "gridData": {
        "w": 40,
        "h": 20
    },
    "source": "AKShare",
    "params": [
        {
            "type": "endpoint",
            "paramName": "ticker",
            "label": "Symbol",
            "value": "600001.SH",
            "description": "Stock ticker (e.g., 600001.SH for Shanghai Stock Exchange)",
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
            "value": "2024-08-01",
            "description": "Start date for historical data"
        },
        {
            "type": "date",
            "paramName": "end_date",
            "label": "End Date",
            "value": "2025-08-31",
            "description": "End date for historical data"
        }
    ],
    "data": {"chart": {"type": "candlestick"}},
})
async def get_charts_candles(
    ticker: str,
    interval: str,
    interval_multiplier: int,
    start_date: str,
    end_date: str
):
    from mysharelib.tools import get_valid_date
    start_dt = get_valid_date(start_date)
    end_dt = get_valid_date(end_date)
    data = obb.equity.price.historical(symbol=ticker, start_date=start_dt, end_date=end_dt, provider="akshare").to_dataframe()
    theme: str = "dark"
    # Get chart colors based on theme
    colors = get_chart_colors(theme)

    figure = go.Figure(
        layout=create_base_layout(
            x_title="Date",
            y_title="Price",
            y_dtype="$,.4f",
            theme=theme
        )
    )
    # Add candlestick chart second so it appears on top
    figure.add_candlestick(
        x=data.index,
        open=data['open'],
        high=data['high'],
        low=data['low'],
        close=data['close'],
        name="Price",
        increasing_line_color=colors['positive'],
        decreasing_line_color=colors['negative']
    )
    # Update layout to include secondary y-axis for volume
    figure.update_layout(
        yaxis=dict(
            rangemode="nonnegative",
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor="lightgrey"
        ),
    )
    # Apply the standard configuration to the figure with theme
    figure = apply_config_to_figure(figure, theme=theme)

    # Convert figure to JSON with the config
    figure_json = figure.to_json()
    figure_dict = json.loads(figure_json)
    
    return figure_dict
