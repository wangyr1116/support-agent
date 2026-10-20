import os
import requests
import json
from tool_specs import TOOL_SPECS
from tool_calling import execute_tool_call


def run_agent(question):
    if not isinstance(question, str):
        return {"ok": False, "data": None, "error": "问题必须是字符串"}

    question = question.strip()
    if not question:
        return {"ok": False, "data": None, "error": "问题不能为空"}

    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        return {"ok": False, "data": None, "error": "未找到DEEPSEEK_API_KEY"}

    # 后面保留现有 payload 和循环
    payload = {
        "model": "deepseek-flash",
        "thinking": {"type": "disabled"},
        "messages": [
            {
    "role": "system",
    "content": (
        "你是技术支持助手，目前只有两个只读工具："
        "get_ticket查询虚构工单的编号、标题和状态；"
        "search_docs检索本地FastAPI资料。"
        "查询工单必须使用get_ticket，解释FastAPI用法必须先使用search_docs。"
        "如果检索问题依赖工单内容，先查询工单，拿到结果后再检索。"
        "资料不足时明确说明，不补写没有依据的处理步骤。"
        "工具返回失败时如实说明，不编造结果。"
        "回答中的工单信息必须来自工单结果，技术说明必须依据检索片段。"
        "引用资料时写出检索结果中的source和chunk_id。"
        "你不能查询处理记录、修改工单或补充工单信息，不要承诺这些能力。"
        "最终回答保持简短：工单状态一行、相关资料最多三点，附来源和片段编号；不要复制整段代码。"
    ),
},
           {
    "role": "user",
    "content": (
        question
    ),
},
        ],
        "tools": TOOL_SPECS,  # 填空1：已有的工具说明列表
        "max_tokens": 1024,
    }

    max_rounds = 4
    max_tool_calls = 4
    tool_calls_used = 0   

    for round_no in range(1, max_rounds + 1):
        print(f"\n模型请求第 {round_no} 轮")

        try:
            response = requests.post(
                "https://api.deepseek.com/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json=payload,
                timeout=60,
            )
            response.raise_for_status()
            choice = response.json()["choices"][0]
            message = choice["message"]
        except requests.exceptions.RequestException as exc:
            return {
                "ok": False,
                "data": None,
                "error": f"模型请求失败：{type(exc).__name__}",
            }

        if choice.get("finish_reason") == "length":
            return {"ok": False, "data": None, "error": "模型输出达到长度上限"}

        payload["messages"].append(message)
        tool_calls = message.get("tool_calls") or []

        if not tool_calls:
            answer = message.get("content")
            if not isinstance(answer, str) or not answer.strip():
                return {"ok": False, "data": None, "error": "模型未返回有效回答"}

            return {"ok": True, "data": answer, "error": None}  # 填空1

        if round_no == max_rounds:
            return {"ok": False, "data": None, "error": "达到模型请求轮数上限，任务尚未完成"}
        for call in tool_calls:
            if tool_calls_used >= max_tool_calls:
                return {
                    "ok": False,
                    "data": None,
                    "error": "达到工具执行次数上限，任务尚未完成",
                }

            tool_calls_used += 1  
            function_info = call["function"]
            print("执行工具：", function_info["name"], function_info["arguments"])
            result = execute_tool_call(
                function_info["name"], function_info["arguments"]
            )
            print("工具结果：", result)
            payload["messages"].append({
                "role": "tool",
                "tool_call_id": call["id"],
                "content": json.dumps(result, ensure_ascii=False),
            })

def main():
    question = input("请输入你的问题：")
    agent_result = run_agent(question)
    if agent_result["ok"]:
        print("最终回答：", agent_result["data"])
    else:
        print("执行未完成：", agent_result["error"])


if __name__ == "__main__":
    main()
