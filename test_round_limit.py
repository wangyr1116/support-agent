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
                agent.main()

                print("模拟模型请求次数：", mock_post.call_count)
                print("实际工具执行次数：", tracked_tool.call_count)
                assert mock_post.call_count == 4  # 填空1 大模型调用最多4次
                assert tracked_tool.call_count == 3  # 填空2 工具调用轮数最多3轮    
                print("轮数上限验证通过")