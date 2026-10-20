import os
import requests
import json
from tool_specs import TOOL_SPECS
from tool_calling import execute_tool_call


def main():
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("未找到 DEEPSEEK_API_KEY，请先设置环境变量")
        return

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
        "请先查询T1001的进度，再根据查到的工单标题检索相关FastAPI资料，"
        "简要说明资料中有哪些相关信息。"
    ),
},
        ],
        "tools": TOOL_SPECS,  # 填空1：已有的工具说明列表
        "max_tokens": 1024,
    }

    max_rounds = 4

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
            print("模型请求失败：", type(exc).__name__)
            return

        if choice.get("finish_reason") == "length":
            print("模型输出达到长度上限，本次停止，未执行本轮工具")
            return

        payload["messages"].append(message)
        tool_calls = message.get("tool_calls") or []

        if not tool_calls:
            print("最终回答：", message.get("content") or "模型未返回有效回答")
            return

        if round_no == max_rounds:
            print("已达到模型请求轮数上限，本轮工具未执行，任务尚未完成")
            return

        for call in tool_calls:
            function_info = call["function"]
            print("执行工具：", function_info["name"], function_info["arguments"])
            result = execute_tool_call(
                function_info["name"], function_info["arguments"]
            )
            print("工具结果：", result)
            payload["messages"].append({
                "role": "tool",
                "tool_call_id": call["id"],  # 填空2：这次调用的编号
                "content": json.dumps(result, ensure_ascii=False),
            })

if __name__ == "__main__":
    main()