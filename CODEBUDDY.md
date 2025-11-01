# CODEBUDDY.md This file provides guidance to CodeBuddy Code when working with code in this repository.

Project purpose
- Backend FastAPI application providing OpenBB Workspace "A‑Shares" and "H‑Shares" dashboards backed by OpenBB, AKShare, and Tushare data providers.

Core workflows and commands
- Environment setup (uv)
  - Install uv (see https://docs.astral.sh/uv/). Then:
    - uv sync
- Run the API (auto-reload):
  - uv run uvicorn main:app --reload
- Linting:
  - Ruff is present via dependencies; if installed globally/in venv, run: ruff check .
- Tests:
  - uv run pytest
  - Run a single test file: uv run pytest tests/test_main.py
  - Run a single test by node id: uv run pytest tests/test_main.py::test_get_apps
- Docker:
  - Build: docker build -t openbb-hka:<version> .
  - Run (compose): docker compose up

High-level architecture
- Application entrypoint: FastAPI app in main.py:17-21; CORS setup in main.py:21-32. Health/root endpoints in main.py:34-41.
- Routing modules registered in main.py:43-68
  - TradingView UDF: routes/tradingview.py (prefix /udf)
  - Chart data: routes/charts.py (prefix /charts)
  - A‑share endpoints and widgets: routes/equity_cn.py (prefix /cn)
  - H‑share endpoints and widgets: routes/equity_hk.py (prefix /hk)
  - Copilot/agent SSE endpoints: routes/agents.py (prefix /a)
- Widget/Template registry: core/registry.py
  - @register_widget decorator registers widget metadata at import time into WIDGETS, keyed by endpoint (core/registry.py:34-46,41-46).
  - add_template(name) loads JSON from templates/<name>.json into TEMPLATES (core/registry.py:50-76). main.py calls add_template("cn") and add_template("hk") to expose via GET /apps.json (main.py:75-86).
  - GET /widgets.json serves the accumulated widget configs (main.py:88-103).
  - load_agent_config() loads templates/agents.json and is served at GET /agents.json (main.py:70-73; core/registry.py:84-113).
- Configuration: core/config.py loads env via dotenv and constructs AppConfig (core/models.py) requiring:
  - AGENT_HOST_URL, APP_API_KEY, OPENROUTER_API_KEY (required)
  - FMP_API_KEY, AKSHARE_API_KEY (validators require values)
  Note: missing or empty values raise validation errors at app import time (core/models.py:25-57).
- Authentication: routes commonly depend on core.auth.get_current_user (e.g., routes/equity_cn.py:10,46,122,195,267,454,533,590). Ensure APP_API_KEY is set appropriately for auth flow.
- Financial data layer: fin_data/* uses openbb‑akshare/openbb‑tushare helpers to fetch profiles, financials, prices (e.g., routes/equity_cn.py:124-128,197-200,269-272,457-459,535-536,593-594).
- Agent/Copilot integration: routes/agents.py streams SSE responses for two paths:
  - POST /a/openrouter/query delegates to core.agent.execution_loop (routes/agents.py:21-27; core/agent.py)
  - POST /a/chatglm/query composes OpenAI chat calls and optionally injects recent widget data; streams MessageChunkSSE.

Conventions and integration points
- Templates:
  - templates/cn.json, templates/hk.json define the two Workspace apps; templates/agents.json defines Copilot config consumed by /agents.json.
- Widget endpoints:
  - Decorate FastAPI route handlers with @register_widget and set a unique "endpoint"; this auto-populates /widgets.json for Workspace discovery.
- CORS origins are limited to https://pro.openbb.co and http://localhost:1420 (main.py:21-32).

Common developer tasks
- Add a new dashboard widget:
  - Create a FastAPI route under routes/equity_cn.py or routes/equity_hk.py (or a new router), decorate with @register_widget including metadata (endpoint, params, gridData, etc.). The widget becomes visible via /widgets.json once the module is imported by main.py.
- Add a new Workspace app template:
  - Create templates/<name>.json and call add_template("<name>") in main.py to include it in /apps.json.
- Update agent behavior:
  - Modify templates/agents.json for Copilot catalog; or update core/agent.py and routes/agents.py for server-side behaviors.

Testing
- Minimal pytest suite exists (tests/). Example test ensures /apps.json backing data isn’t empty (tests/test_main.py:1-8). Extend with endpoint unit tests using TestClient.

Notes pulled from README
- Requires configuring $HOME/.openbb_platform/user_settings.json with akshare_api_key for Xueqiu access.
- Environment variables can be loaded via .env (see README). Keys commonly referenced: AGENT_HOST_URL, APP_API_KEY, OPENROUTER_API_KEY, FMP_API_KEY.

Gotchas
- AppConfig validators will raise at import time if required env vars or FMP/AKShare keys are missing; supply them in .env for local dev.
- Some endpoints depend on mysharelib and openbb_akshare; ensure dependencies from requirements.txt are present (uv sync).
