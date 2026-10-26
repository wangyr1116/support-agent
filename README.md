# Support Agent

## HTTP接口（本地开发）

在项目虚拟环境安装依赖后，设置DEEPSEEK_API_KEY，再启动：

```bat
python -m pip install -e .
python -m uvicorn api:app --host 127.0.0.1 --port 8001 --reload
```

浏览器访问 http://127.0.0.1:8001/docs ，向POST /ask提交 `{"question":"查询T1001的状态，只查工单，不需要检索资料。"}`。正常输入会调用付费模型；仅查工单无需启动RAG。资料查询仍依赖8000端口的RAG服务。

接口复用run_agent，使用同步def路由，返回ok/data/error。缺少question由请求校验拒绝；空白字符串由Agent返回失败字典。已处理的Agent失败目前仍以HTTP 200返回，业务是否成功看ok；未处理异常可能产生HTTP 500。

接口模拟测试：

```bat
python -m pip install httpx
python test_api.py
```

测试替换api.run_agent，检查调用参数、次数及响应字典，无需启动服务或调用模型。当前环境使用httpx可通过，但Starlette发出弃用警告；其本地源码优先导入httpx2，并兼容回退httpx。尚未迁移或验证httpx2。本项目尚未锁定完整依赖版本。

2026-10-26用户已验证/docs请求、空白输入、缺少字段及真实T1001回答；原有模拟测试用户报告通过。接口目前不返回工具执行记录，无自定义网页。

只读技术支持 Agent 学习原型：DeepSeek选择工具，本地Python执行工具并回传结果；模型可以根据前一轮结果继续检索，再生成回答。所有工单均为虚构数据，不支持修改工单或查询处理记录。

## 工具与流程

| 工具 | 输入 | 数据来源 |
| --- | --- | --- |
| get_ticket | ticket_id，例如T1001 | tools.py中的虚构工单字典 |
| list_tickets | status，例如待处理 | 同一虚构工单字典，返回匹配列表 |
| search_docs | question、可选top_k（1–10，默认3） | 本地RAG的POST /search |

工具统一返回包含ok、data、error的字典。查询失败也可回传模型，由模型说明失败原因。

```text
用户问题 + 工具说明 → DeepSeek
    → 工具名称与JSON参数文本
    → 参数解析 → 注册表分发 → 本地执行
    → 带tool_call_id的结果消息 → DeepSeek继续决策或回答
```

示例问题：先查询T1001，再根据工单标题检索FastAPI资料。已观察到的路径为第1轮查工单、第2轮检索、第3轮回答。模型选择、检索结果与措辞可能变化。

## 环境准备（Windows CMD）

需要Python 3.13或以上，本机使用Python 3.13.9。首次在项目目录执行：

```bat
cd /d D:\llm-learning\support-agent
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e .
```

已有.venv时只需激活。若python被WindowsApps别名遮挡，使用实际Python可执行文件的完整路径创建环境；本机曾使用 `D:\ProgramData\anaconda3\python.exe -m venv .venv`。

两个项目各用自己的环境；Agent不安装RAG的向量检索依赖。依赖范围见pyproject.toml，当前没有锁文件，不保证不同时间安装的依赖版本完全相同。

## 启动RAG（窗口一）

资料查询依赖独立项目 [rag-qa-system](https://github.com/wangyr1116/rag-qa-system)，不会自动启动。以下使用本机现有目录，其他机器请替换路径并先完成原项目的环境准备。

```bat
cd /d D:\llm-learning\rag-qa-system
uv sync --locked
set "RAG_DOCUMENT_DIR=knowledge\fastapi_expanded"
set "RAG_CHUNKING=markdown_tokens"
uv run uvicorn app.main:app --reload
```

等待Application startup complete并保持窗口运行。工具请求http://127.0.0.1:8000/search，只检索资料，不调用RAG生成接口。单独查工单无需启动RAG。

## 运行Agent（窗口二）

```bat
cd /d D:\llm-learning\support-agent
.venv\Scripts\activate
set "DEEPSEEK_API_KEY=替换为自己的真实密钥"
python agent.py
```

只在本地终端设置密钥，不提交到Git。代码读取环境变量，不自动加载.env；关闭CMD后需要重新设置。

当前使用deepseek-flash非思考模式，运行会发送付费API请求。运行后在终端输入问题并按回车，例如“查询T1002的进度”。每次运行处理一个问题，不保留跨次运行的对话。空白输入在请求模型前被拒绝。

## 终止规则

- 最多4次模型请求，每次输出上限1024 tokens。
- 无工具调用且回答有效时返回成功字典；空回答返回失败字典。
- 第4轮仍要求调用工具时，不执行该轮工具，并报告任务尚未完成。
- 输出因长度限制截断时停止，不执行该轮工具。
- 捕获HTTP请求相关异常后返回包含异常类别的失败字典。

请求轮数不等于工具次数：一轮可能包含多个工具。每次run_agent运行最多尝试执行4次工具，准备执行第5次时返回失败；失败的工具尝试也计数。用满次数后模型仍可直接回答。当前没有自动重试。

## 本地验证

```bat
python test_round_limit.py
python test_agent_answer.py
```

这两个脚本以模拟响应替换模型网络请求，并临时设置假密钥；上限测试仍执行真实的本地工单查询。无需真实密钥或RAG，不产生模型请求费用。

预期模拟请求4次、工具执行3次，第4轮停止，末尾输出“轮数上限验证通过”。这里工具执行3次，是因为第一个场景每轮仅包含一个调用。第二个场景每轮提出3个调用，预期模型请求2次、工具实际执行4次，在第5次尝试前停止并返回工具次数上限错误。

正常回答测试预置一条回复，验证模型请求1次、工具执行0次，并返回正确的成功字典；不评价真实模型回答质量。

其他学习入口：`python dispatcher.py`、`python tool_calling.py`、`python tool_specs.py`，当前演示不需要模型。`python tools.py`包含本地RAG请求，服务未启动时返回连接失败。

## 文件职责

| 文件 | 职责 |
| --- | --- |
| agent.py | main接收输入并展示结果；run_agent执行流程并返回字典 |
| tool_specs.py | 给模型阅读的工具说明 |
| tool_calling.py | JSON参数文本解析 |
| dispatcher.py | 注册表、参数结构检查、函数调用 |
| tools.py | 虚构工单查询、本地资料检索 |
| test_round_limit.py | 无付费请求的轮数上限及失败返回值验证 |
| test_agent_answer.py | 正常回答、成功返回值与提前结束验证 |

## 验证与限制

已验证场景见 [验证记录](docs/validation.md)。

这是学习原型：未全面处理模型响应结构异常；引用支持仍由人工核对；检索资料不等于确认实际工单根因；提示词不能保证回答始终符合要求。尚未验证全新机器部署、并发或长期稳定运行。

## 从Python调用

```python
from agent import run_agent

agent_result = run_agent("查询T1002的进度")
```

此调用需要环境变量密钥，通常会产生模型请求费用。正常完成返回 `{"ok": True, "data": "回答文字", "error": None}`；可处理的失败返回 `{"ok": False, "data": None, "error": "原因"}`。run_agent仍会打印轮数和工具过程日志，最终结果由调用者展示。

Agent的ok表示流程产出了有效回答，不代表工单存在或回答事实已自动核验。工具的data是业务数据，Agent的data是回答字符串。未知响应结构等未处理异常仍可能抛出，不能保证所有异常都转换为失败字典。


## 按状态查询工单

输入：列出所有待处理的工单。已验证模型选择list_tickets并返回T1002，不需要RAG。status需为字符串，去除两端空白后不能为空。无匹配时返回ok=True、data=[]；数据来自虚构工单字典，不来自FastAPI资料。
