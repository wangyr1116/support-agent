TOOL_SPECS = [#工具规格列表 / 工具描述清单
    {
        "type": "function",
        "function": {
            "name": "get_ticket",
            "description": "按工单编号查询虚构工单的标题和处理状态。只读，不修改工单。",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "string",
                        "description": "工单编号，例如T1001。",
                    },
                },
                "required": ["ticket_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_docs",
            "description": "检索本地FastAPI资料，用于查找接口用法和错误处理说明。",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "要检索的问题。"},
                    "top_k": {"type": "integer", "minimum": 1, "maximum": 10},
                },
                "required": ["question"],
                "additionalProperties": False,
            },
        },
    },
    {
       "type": "function",
                "function": {
                    "name": "list_tickets",
                    "description": "按状态筛选本地虚构工单，返回匹配工单列表。无匹配时返回空列表。只读，不修改工单。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string", "description": "要筛选的工单状态。"},
                        },
                        "required": ["status"],
                        "additionalProperties": False,
                    },
                },
    }
]

if __name__ == "__main__":
    import json

    print("工具数量：", len(TOOL_SPECS))
    print("第一个工具：", TOOL_SPECS[0]["function"]["name"])
    print("第二个工具必填参数：",
          TOOL_SPECS[1]["function"]["parameters"]["required"])
    print(json.dumps(TOOL_SPECS[0], ensure_ascii=False, indent=2))
