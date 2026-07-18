# Function Search

面向 PyTorch、Python 常用标准库、Python 后端开发的 **API 快速查询桌面软件**。

- 极速模糊搜索：SQLite FTS5 + RapidFuzz 混合检索
- 完整说明与可复制调用示例
- 可扩展 Provider 架构，支持自定义 JSON 数据集
- 一键打包 macOS `.app`

## 功能

| 数据源 | 说明 |
|--------|------|
| **PyTorch** | 运行时 introspection 自动采集 `torch.*` 公共 API、签名、docstring |
| **Python 常用** | 精选 builtins / json / pathlib / asyncio 等高频函数 |
| **Python 后端** | FastAPI / SQLAlchemy / Redis / Celery / pytest 等后端常用 API |

## 快速开始

### 1. 安装依赖

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

或手动安装：

```bash
cd function_search
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

**GUI 需要 tkinter（macOS Homebrew Python 默认不带）：**

```bash
brew install python-tk@3.14
```

### 2. 构建索引

```bash
# 完整索引（推荐，需安装 PyTorch）
python3 -m pip install torch
python3 -m function_search.build_index

# 或仅构建 Python + 后端数据（无需 torch）
python3 -m function_search.build_index --no-pytorch
```

索引输出：`src/function_search/data/functions.db`

### 3. 启动 GUI

```bash
function-search
# 或
python3 -m function_search.main gui
```

### 4. 命令行搜索

```bash
function-search search torch.nn.Linear --limit 5
function-search search json.dumps --provider python
```

### 5. AI 代码问答（LM Studio + GLM-4-32B）

推荐在 **16GB 内存** 设备上使用 `IQ3_XXS` 量化（约 12.8GB，同档位推理质量最佳）：

```bash
chmod +x scripts/setup_lm_studio.sh
./scripts/setup_lm_studio.sh

# 加载模型（建议 context 4096 以节省内存）
lms load bartowski/glm-4-32b-0414-gguf -c 4096 -y

# 启动 LM Studio 本地 API
lms server start
```

GUI 中切换到 **「AI 问答」** 标签页即可提问；命令行：

```bash
function-search ask "如何用 torch 定义两层全连接网络？"
function-search ask "FastAPI 怎么写依赖注入？" --provider backend
```

可选配置（`~/Library/Application Support/FunctionSearch/config.json`）：

```json
{
  "lm_studio_url": "http://localhost:1234/v1",
  "model": "glm-4-32b-0414",
  "context_results": 8,
  "temperature": 0.3,
  "max_tokens": 2048,
  "timeout": 180.0
}
```

## 扩展自定义函数库

在 `extensions/` 目录添加 JSON 文件即可，构建索引时自动合并：

```
extensions/
  myapi.json          # 函数数据
  myapi.meta.json     # 可选：id / display_name
```

`myapi.json` 单条记录格式：

```json
{
  "name": "my_helper",
  "full_name": "mylib.my_helper",
  "module": "mylib",
  "category": "function",
  "signature": "my_helper(value: str) -> str",
  "description": "函数说明",
  "example": "result = mylib.my_helper('demo')",
  "tags": ["custom"]
}
```

重新构建索引：

```bash
python3 -m function_search.build_index
```

### 编写代码级 Provider（高级扩展）

实现 `function_search.providers.base.Provider` 接口，并在 `providers/registry.py` 注册：

```python
from function_search.providers.base import Provider
from function_search.models import FunctionEntry

class MyProvider(Provider):
    @property
    def id(self) -> str:
        return "mylib"

    @property
    def display_name(self) -> str:
        return "我的函数库"

    def collect(self) -> list[FunctionEntry]:
        return [...]
```

## macOS 打包发布

```bash
chmod +x scripts/package_mac.sh
./scripts/package_mac.sh
```

产物路径：`dist/FunctionSearch.app`

> 打包前请确保已安装 `python-tk@3.14`，否则 PyInstaller 会跳过 tkinter，GUI 无法启动。

```bash
open dist/FunctionSearch.app
```

### 手动打包

```bash
python3 -m function_search.build_index
pyinstaller --noconfirm function_search.spec
```

## 搜索性能设计

1. **预构建 SQLite 索引**：启动时只读加载，无运行时 introspection 开销
2. **FTS5 全文检索**：对名称、签名、描述、标签建立倒排索引
3. **RapidFuzz 重排**：先缩小候选集，再模糊打分，毫秒级响应
4. **输入防抖 80ms**：避免每次按键全量计算

## 项目结构

```
function_search/
├── src/function_search/
│   ├── app.py                 # GUI（API 搜索 + AI 问答）
│   ├── qa_assistant.py        # 问答模块（检索上下文 + LM Studio）
│   ├── lm_studio_client.py    # LM Studio OpenAI 兼容客户端
│   ├── prompts.py             # 代码分析助手系统提示词
│   ├── config.py              # 用户配置（LM Studio 地址/模型）
│   ├── search_engine.py       # 搜索引擎 + 索引构建
│   ├── build_index.py         # 索引 CLI
│   ├── providers/             # 可扩展数据源
│   └── data/                  # JSON 数据集 + functions.db
├── extensions/                # 用户扩展数据
├── scripts/package_mac.sh     # Mac 打包脚本
├── function_search.spec       # PyInstaller 配置
└── tests/
```

## 测试

```bash
python3 -m pip install pytest
pytest -q
```

## 许可证

MIT
