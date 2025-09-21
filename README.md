# How to Build A-Share and H-Share Analysis Dashboards Using OpenBB Workspace

openbb-hka is an OpenBB Workspace application that provides templates and components for building analysis dashboards for A-shares and H-shares. It uses openbb-akshare and openbb-tushare as data sources.

Prior to this project, I released OpenBB extensions for AKShare and Tushare data sources. A common question has been: Why develop these extensions, and what is the core value of OpenBB? I attempted to address these in the article *" Introduction to OpenBB and How to Use It to Aid Financial Data Analysis of China A-share and Hong Kong Stocks"*, but truly understanding OpenBB's design philosophy still requires hands-on experience.

Another frequent point of confusion is whether OpenBB has a front-end interface and how to use it. OpenBB Workspace is, in fact, the front-end platform. It allows users to build customized data analysis dashboards. For specific markets such as A-shares and H-shares, we can develop dedicated OpenBB Workspace applications with tailored analytical components — openbb-hka is one such application designed for building dashboards for A-share and H-share analysis.

## Comparison Between OpenBB Workspace Apps and Dashboards

| **Apps**                                          | **Dashboards**                    |
| ------------------------------------------------------- | --------------------------------------- |
| Pre-configured templates with specific analytical goals | Blank canvas for custom configuration   |
| Widgets come with pre-linked parameters                 | Manual parameter configuration required |
| Include curated prompt libraries                        | Start with no predefined prompts        |
| Designed by domain experts for specific workflows       | General-purpose analytical workspace    |

## Environment Setup

# FinApp

Your dashboard for China market. Built using OpenBB workspace with data from AKShare and Tushare.

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
