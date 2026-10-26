from unittest.mock import patch
from fastapi.testclient import TestClient

from api import app


if __name__ == "__main__":
    client = TestClient(app)

    fake_result = {
        "ok": True,
        "data": "工单T1001目前处于处理中。",
        "error": None,
    }

    with patch("api.run_agent", return_value=fake_result) as mock_agent:
        response = client.post(
            "/ask",
            json={"question": "查询T1001的状态"},
        )

        assert response.status_code == 200#验证接口和agent正确连接
        assert response.json() == fake_result
        mock_agent.assert_called_once_with("查询T1001的状态")

    print("接口正常请求验证通过")