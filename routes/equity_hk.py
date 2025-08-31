from fastapi import APIRouter, HTTPException
from core.registry import register_widget
import pandas as pd
from typing import List
import json
import asyncio
import numpy as np

equity_hk_router = APIRouter()

@register_widget({
    "name": "FinApp HK Equity",
    "description": "A FinApp widget",
    "type": "markdown",
    "endpoint": "hk/info",
    "gridData": {"w": 12, "h": 4},
})
@equity_hk_router.get("/info")
def info():
    """Returns a markdown widget"""
    return "# FinApp HK Equity\nThis is a markdown widget for HK Equity."