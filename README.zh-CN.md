# 如何使用 OpenBB Workspace 搭建A股和港股分析面板

openbb-hka 是一款基于 OpenBB Workspace 的应用，提供搭建A股与港股分析面板的模板与组件，数据源依托于 openbb-akshare 和 openbb-tushare。

在此之前，我已发布基于 AKShare 和 Tushare 的 OpenBB 数据源扩展。很多用户提出这样的疑问：为何要开发这些扩展？OpenBB 的核心价值是什么？我在《OpenBB 介绍及其在A股与港股金融数据分析中的应用》一文中尝试回应了这些问题，但真正理解 OpenBB 的设计理念，仍需结合实际使用体验。

另一个常见困惑是：OpenBB 是否具备前端界面？应如何使用？事实上，OpenBB Workspace 正是其前端实现。通过该平台，用户可搭建定制化的数据分析面板。针对特定市场（如A股和港股），我们能够开发专用的 OpenBB Workspace 应用，集成相关分析组件——openbb-hka 正是这样一个为构建A股和港股分析面板而设计的应用。

## OpenBB Workspace 应用与面板对比

| **应用（Apps）**             | **面板（Dashboards）**   |
| ---------------------------------- | ------------------------------ |
| 提供具备特定分析功能的预配置模板   | 支持自由配置的空白画布         |
| 组件已预置关联参数，开箱即用       | 需手动配置参数                 |
| 内置精选提示词库，提升分析效率     | 初始不包含预设提示，需自行构建 |
| 由领域专家设计，适用于特定工作流程 | 作为通用型分析工作空间使用     |

## 环境设置

### API Key

AKShare虽然是使用的免费数据，但是如果用到雪球的数据，还是需要API Key的。需要在文件 `$HOME/.openbb_platform/user_settings.json`里设置 `akshare_api_key`如下：

```json
{
    "credentials": {
        "akshare_api_key": "your {xq_a_token}"
    },
    "preferences": {},
    "defaults": {
        "commands": {}
    }
}
```

### 环境变量

虽然上面设置了API Key，但是一部分的设置还是需要通过环境变量来完成。环境变量的设置可以参考文件 `env.example`。或者根据 `env.example`生成你的 `.env`文件。

| 变量               | 说明                              |
| ------------------ | --------------------------------- |
| AGENT_HOST_URL     | 目前可以为空                      |
| APP_API_KEY        | 可以生成自己的JWT token来认证链接 |
| DATA_FOLDER_PATH   | 目前可以为空                      |
| OPENROUTER_API_KEY | 目前可以为空                      |
| FMP_API_KEY        | 目前可以为空                      |

### 安装 `uv`

依赖管理使用的是 `uv`。如果系统没有，需要自行安装。安装好后，运行下列命令来同步环境。

```bash
uv sync
```

### 运行

通过下面的命令来运行。

```bash
uv run uvicorn main:app --reload
```

## Docker

```bash
docker build -t openbb-hka:0.2.4 .
docker compose up
```

## Google
