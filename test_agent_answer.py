from unittest.mock import Mock, patch
import agent


if __name__ == "__main__":
    bad_cases = [
        ({}, "模型响应缺少有效choices"),
        ({"choices": []}, "模型响应缺少有效choices"),
        ({"choices": [{}]}, "模型响应缺少有效message"),
        ({"choices": ["hello", "world"]}, "模型候选必须是对象"),
    ]

    for body, expected_error in bad_cases:
        response = Mock()
        response.json.return_value = body

        with patch.dict("os.environ", {"DEEPSEEK_API_KEY": "test-only"}):
            with patch("agent.requests.post", return_value=response) as mock_post:
                with patch("agent.execute_tool_call") as mock_tool:
                    result = agent.run_agent("你好")

                    assert result == {
                        "ok": False,
                        "data": None,
                        "error": expected_error,
                        "tool_calls": [],
                    }
                    assert mock_post.call_count == 1
                    mock_tool.assert_not_called()

        print("异常响应验证通过：", expected_error)
    response = Mock()
    response.json.return_value = {
        "choices": [{
            "finish_reason": "stop",
            "message": {
                "role": "assistant",
                "content": "你好，我可以查询虚构工单和检索FastAPI资料。",
                "tool_calls": [],
            },
        }],
    }

    with patch.dict("os.environ", {"DEEPSEEK_API_KEY": "test-only"}):
        with patch("agent.requests.post", return_value=response) as mock_post:
            with patch("agent.execute_tool_call") as mock_tool:
                agent_result = agent.run_agent("你好")

                print("Agent返回值：", agent_result)
                assert agent_result == {
                    "ok": True,
                    "data": "你好，我可以查询虚构工单和检索FastAPI资料。",
                    "error": None,
                    "tool_calls": [],
                }
                assert mock_post.call_count == 1  # 填空：请求了几次？
                mock_tool.assert_not_called()
                print("正常回答返回值验证通过")