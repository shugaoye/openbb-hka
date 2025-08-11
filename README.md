# FinAnalyzer

OpenBB with AKShare and Tushare backend

1. Install all the required libraries

```bash
uv venv
# Linux/macOS
source .venv/bin/activate

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Windows (CMD)
.\.venv\Scripts\activate.bat
```

2. Install required packages

```bash
uv install
# Or
uv pip install -r requirements.txt
```



3. Run the custom backend

```bash
uv run uvicorn main:app --reload
```

4. Go into [OpenBB](httpc://pro.openbb.co), into the Data Connectors tab to  be more specific.

5. Add a new custom backend, with https://pro.openbb.co/app/data-connectors?modal=data-connectors&dcTab=backend as follows.



That's it, now you can access data from that widget.
