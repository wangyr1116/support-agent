# 学习状态

更新：2026-10-20。

## 目标与约定

- 独立技术支持Agent学习项目：虚构工单查询与本地FastAPI资料检索，均只读，面向LLM应用实习准备。
- 核心代码与Git提交由用户完成，助手维护文档。中文通俗解释、完整小模块、适量填空。
- 用户容易混淆项目各文件的参数、返回值和同名变量，需用实际项目值逐步解释，不用无关基础例子替代项目梳理。
- 简单修改依据用户输出，不逐轮检查；错误、矛盾或关键阶段再定点核对。详见AGENTS.md。

## 当前实现

- tools.py：get_ticket查虚构工单；search_docs请求本地/search，统一ok/data/error返回。
- dispatcher.py：注册表、参数结构检查；tool_calling.py：JSON参数解析；tool_specs.py：工具说明。
- agent.py：requests调用DeepSeek，DEEPSEEK_API_KEY环境变量，deepseek-flash非思考模式。最多4轮模型请求，每轮输出上限1024；无工具调用则结束，第4轮仍有工具调用则不执行并报告未完成，截断和请求异常有出口。
- main()已支持终端输入单个问题并展示结果；run_agent(question)检查字符串及空白，执行流程并返回ok/data/error。成功data为回答字符串；已处理失败返回原因。仍打印过程日志，无工具总次数上限或完整响应结构校验。
- .venv使用Python 3.13.9，pyproject.toml声明requests。曾因WindowsApps入口无输出，通过Anaconda Python创建环境解决。

## 验证与理解

- 用户展示了单工单成功/不存在回传回答、同轮两工具组合、按前一轮结果继续检索的三轮正常结束。
- 用户实际触发过length出口；提高输出上限并限制回答长度后通过。
- 用户运行test_round_limit.py通过：模拟请求4次、实际本地工具3次，第4轮停止。助手读取确认断言，未重跑；每轮一个调用才有此工具次数。
- 用户能解释业务失败字典仍会回传、两工具不等于额外两次模型请求、无tool_calls会return结束。
- 已解释tool_call_id从服务返回call["id"]取得并回传。工具说明与实际参数、调用信息字典与真实函数仍需迁移巩固。
- 资料引用存在不等于充分支持每句话；422资料不等于工单根因。详细证据与未测项目见docs/validation.md。

## Git与当前下一步

- 用户已提交54c014c，保存有轮数上限的Agent、协议解析与文档；此前提交6a6b22b、7fcfd0a。
- 本批已完成终端输入、main/run_agent拆分、统一成功/失败返回；用户验证T1002真实查询、空格拒绝、更新后的上限失败字典及新增正常回答测试。最后两项为本地模拟，无付费模型请求。助手核对差异，未重复运行。
- 用户能正确区分未知工具、参数名错误在dispatcher拒绝，参数值类型错误在tools拒绝；曾误认为纯空格会请求模型，已实际验证并纠正。
- 本轮更新README、docs/validation与本文件，核心功能未改。待用户暂存agent.py、test_round_limit.py、test_agent_answer.py及三份文档，共6个文件并提交。
- 不继续增加测试文件。提交后优先巩固run_agent返回值与工具结果的区别，再按需求决定下一模块；不默认发布GitHub。
## 前置项目

- RAG第一阶段、GitHub发布、主页更新和置顶已完成，不重复检索诊断或上传。
- 原项目D:/llm-learning/rag-qa-system；https://github.com/wangyr1116/rag-qa-system。
- RAG用自身uv环境与既有/search，不改其main.py，不用既有留出评测调参。
