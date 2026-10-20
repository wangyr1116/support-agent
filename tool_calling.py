import json

from dispatcher import dispatch_tool


def execute_tool_call(name, arguments_json):
    if not isinstance(arguments_json, str):
        return {"ok": False, "data": None, "error": "工具参数文本必须是字符串"}

    try:
        arguments = json.loads(arguments_json)  # 填空1：解析JSON文本
    except json.JSONDecodeError:
        return {"ok": False, "data": None, "error": "工具参数不是有效JSON"}

    return dispatch_tool(name, arguments)  # 填空2：传入解析后的值


if __name__ == "__main__":
    calls = [
        ("get_ticket", '{"ticket_id": "T1001"}'),
        ("get_ticket", '{"ticket_id": "T1002"}'),
        ("get_ticket", '{"ticket_id":'),
        ("get_ticket", '["T1001"]'),
        ("get_ticket", '{"ticket_id": 1001}'),
        ("search_docs", '{"question": "HTTPException", "top_k": 0}'),
    ]

    for name, arguments_json in calls:
        result = execute_tool_call(name, arguments_json)
        print(result)