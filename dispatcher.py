from inspect import signature
from tools import get_ticket, search_docs


TOOL_FUNCTIONS = {
    "get_ticket": get_ticket,
    "search_docs": search_docs,
}


def dispatch_tool(name, arguments):
    if not isinstance(name, str):
        return {"ok": False, "data": None, "error": "工具名称必须是字符串"}

    function = TOOL_FUNCTIONS.get(name) 
    if function is None:
        return {"ok": False, "data": None, "error": "未知工具"}

    if not isinstance(arguments, dict):
        return {"ok": False, "data": None, "error": "工具参数必须是字典"}

    if any(not isinstance(key, str) for key in arguments):
        return {"ok": False, "data": None, "error": "参数名必须是字符串"}

    try:
        signature(function).bind(**arguments)
    except TypeError:
        return {"ok": False, "data": None, "error": "工具参数缺失或包含多余参数"}

    return function(**arguments) 


if __name__ == "__main__":
    print(dispatch_tool("get_ticket", {"ticket_id": "T1001"}))
    print(dispatch_tool("delete_ticket", {"ticket_id": "T1001"}))
    print(dispatch_tool("get_ticket", {}))
    print(dispatch_tool("get_ticket", {"ticket_id": 1001}))
    print(dispatch_tool("search_docs", {"question": "HTTPException", "top_k": 0}))
    print(dispatch_tool("get_ticket", {"ticket_id": "T1002", "extra_param": 123}))