from unittest.mock import Mock, patch
import agent


if __name__ == "__main__":
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
                }
                assert mock_post.call_count == 1  # 填空：请求了几次？
                mock_tool.assert_not_called()
                print("正常回答返回值验证通过")