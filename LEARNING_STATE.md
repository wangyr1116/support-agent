# 学习状态

更新：2026-10-13。

- 目标：独立技术支持Agent，两个只读工具为资料检索与模拟工单查询；练习模型工具选择、参数校验、结果回传、终止与失败出口。
- 前置RAG阶段已完成固定融合接入、单题真实生成与引用核查、独立目录启动复现；2026-10-13核实原项目最新提交d1902b4。项目已发布https://github.com/wangyr1116/rag-qa-system，origin已配置；助手实际通过浏览器确认公开代码与最新展示README。用户GitHub主页已更新且置顶RAG，Support Agent标为规划中。具体证据和限制见D:/llm-learning/rag-qa-system/docs/experiments.md。
- 已解释引用标签存在与原文支持答案的区别；用户最后能正确复述该区别，仍需后续迁移判断。小样本检索成绩的结论边界由助手纠正，不视为已独立掌握。
- 当前已实现 tools.py 的 get_ticket 与 search_docs，使用虚构工单和本地 RAG，统一成功/失败字典；已建立 .venv（用户报告 Python 3.13.9），尚无 Git 仓库，未调用模型。
- 2026-10-10至12日暂停Agent并巩固RAG：token/向量维度、平方L2/FAISS、BM25/RRF、评测边界、引用校验和服务生命周期。用户已完成/config与/search两个小修改；/search新增请求数量与实际数量已由助手实际请求核验。用户称已理解FastAPI创建应用并注册lifespan的关系，未做独立回忆验收，后续穿插复习，不认定全面掌握。
- 2026-10-13用户要求继续，助手判断可转Agent作为新增功能主线，不必等满两周；核心Python和RAG原理持续穿插。当时 tools.py 与 pyproject.toml 尚不存在；现两个工具与 pyproject.toml 均已创建。
- 用户确认每周15–25小时后，助手综合建议先1–2周RAG巩固，达到独立解释/小修改验收再恢复Agent为唯一新增功能主线；相关理论和Python/算法始终穿插。详细安排见原RAG项目docs/learning_plan.md，不同时扩两个项目。
- 恢复Agent后的首步：用户创建pyproject.toml与tools.py，实现get_ticket读取虚构工单，验证存在、不存在及纯空白编号，统一返回成功/失败字典。
- 下一步：实现 dispatcher.py 的工具名称分发与参数结构校验，再加入模型工具协议；当前阶段由人调用函数，尚无自主工具选择。
- 核心代码和Git提交由用户完成；中文通俗解释、中等颗粒度支架。项目约定见AGENTS.md。
- 衔接：本轮用户要的是GitHub个人主页展示，没有简历；RAG发布、主页更新与置顶均已由用户完成，助手已实际核验。现在适合新开Agent带教会话，以本目录为工作目录，先读AGENTS.md和本文件；不要继续要求上传RAG或重复巩固整套RAG。
- Agent具体场景：技术支持助手，按自然语言需求查虚构工单状态与FastAPI资料，可组合两个工具处理“查工单进度并解释相关接口用法”；不处理真实企业工单，不把工具函数单独可运行称完整Agent完成。用户要求函数解释更细，穿插Python基础、最小输入返回示例，记录于AGENTS.md。
- 用户GitHub账号wangyr1116，主页展示已完成；LTNtorch为fork，不当作独立项目。历史首步（现已完成）：先用约15–40行、两处填空的get_ticket模拟查询，详解字典嵌套、参数、isinstance、strip、get、return与直接运行/导入区别。完成后读取本地代码并验收，再接RAG/search只读工具；此时才准备依赖和Git初始化，不宣称已有完整Agent。

- 2026-10-13 get_ticket 模块完成：助手读取确认 strip/get 与五次调用，此前实际运行四种输入通过；用户在 .venv 中贴出存在、不存在、空白、非字符串、带空格 T1002 共五项成功输出。WindowsApps python 入口无输出，通过 Anaconda Python 创建 .venv 后解决。T1002 状态为待处理，用户曾误写预处理，已纠正，不认定完全掌握嵌套取值。
- search_docs 已实现，pyproject.toml 声明 requests。用户贴出成功检索（请求2条、实际2条）和服务不可达结果；助手读取确认实现，并在 .venv 实际验证 top_k=True/0 被拒绝。用户能指出参数检查后的 return 阻止请求发送；bool/int 关系已解释，尚未独立迁移验收。助手原支架 JSON 异常捕获顺序已纠正，用户修改后读取确认；演示 top_k 已恢复2。超时、HTTP错误、非JSON分支尚未实际触发验证。原 RAG 使用自身 uv 环境，不改 main.py、不重跑检索诊断。


- 本轮带教下一步：新建 dispatcher.py，工具白名单映射、名称/参数字典检查、signature.bind 检查缺失或多余参数，再通过 **arguments 调用；支架由用户完成，尚未实现。之后准备 Git 忽略与首个提交（用户执行），再接模型工具协议。


- dispatcher 模块：用户贴出六项符合预期的输出（成功、未知工具、缺参数、编号类型错误、top_k越界、多余参数）。用户正确预测多余 verbose 参数在 signature.bind 处拒绝；本轮依据用户输出验收，未读取或重跑 dispatcher.py。已解释注册表 get 返回函数对象。下一步由用户创建 .gitignore、初始化 Git、检查暂存范围并首次提交，之后接模型工具协议。用户要求降低重复本地核查频率，已加入 AGENTS.md。

