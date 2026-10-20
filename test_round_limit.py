from unittest.mock import Mock, patch
import agent


def make_response(number):
    response = Mock()
    response.json.return_value = {
        "choices": [{
            "finish_reason": "tool_calls",
            "message": {
                "role": "assistant",
                "content": None,
                "tool_calls": [{
                    "id": f"test_call_{number}",
                    "type": "function",
                    "function": {
                        "name": "get_ticket",
                        "arguments": '{"ticket_id": "T1001"}',
                    },
                }],
            },
        }],
    }
    return response


if __name__ == "__main__":
    responses = [make_response(n) for n in range(1, 5)]

    with patch.dict("os.environ", {"DEEPSEEK_API_KEY": "test-only"}):
        with patch("agent.requests.post", side_effect=responses) as mock_post:
            with patch(
                "agent.execute_tool_call", wraps=agent.execute_tool_call
            ) as tracked_tool:
                agent_result = agent.run_agent("查询T1001的进度，并检索相关FastAPI资料。")
                print("Agent返回值：", agent_result)
                assert agent_result == {
                    "ok": False,
                    "data": None,
                    "error": "达到模型请求轮数上限，任务尚未完成",
                }
                print("模拟模型请求次数：", mock_post.call_count)
                print("实际工具执行次数：", tracked_tool.call_count)
                assert mock_post.call_count == 4  # 填空1 大模型调用最多4次
                assert tracked_tool.call_count == 3  # 填空2 工具调用轮数最多3轮    
                print("轮数上限验证通过")
    responses = [make_response(n) for n in range(1, 3)]

    for response in responses:
        message = response.json.return_value["choices"][0]["message"]
        first_call = message["tool_calls"][0]
        message["tool_calls"] = [
            {
                **first_call,
                "id": f"{first_call['id']}_{i}",
            }
            for i in range(3)
        ]
#一轮调用3次
    with patch.dict("os.environ", {"DEEPSEEK_API_KEY": "test-only"}):
        with patch("agent.requests.post", side_effect=responses) as mock_post:
            with patch(
                "agent.execute_tool_call", wraps=agent.execute_tool_call
            ) as tracked_tool:
                agent_result = agent.run_agent("查询T1001")

                assert mock_post.call_count == 2
                assert tracked_tool.call_count == 4
                assert agent_result == {
                    "ok": False,
                    "data": None,
                    "error": "达到工具执行次数上限，任务尚未完成",
                }
                print("工具次数上限验证通过：请求2次，工具执行4次")