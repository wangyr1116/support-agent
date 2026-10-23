import requests
# 全部是虚构工单，仅用于学习。
MOCK_TICKETS = {
    "T1001": {
        "ticket_id": "T1001",
        "title": "FastAPI 接口返回 422",
        "status": "处理中",
    },
    "T1002": {
        "ticket_id": "T1002",
        "title": "本地资料检索服务无法连接",
        "status": "待处理",
    },
}


def get_ticket(ticket_id):
    if not isinstance(ticket_id, str):
        return {"ok": False, "data": None, "error": "工单编号必须是字符串"}

    ticket_id = ticket_id.strip()  # 填空1：去掉字符串两端空白

    if not ticket_id:
        return {"ok": False, "data": None, "error": "工单编号不能为空"}

    ticket = MOCK_TICKETS.get(ticket_id)  # 填空2：按键取值，不存在时返回None

    if ticket is None:
        return {"ok": False, "data": None, "error": "工单不存在"}

    return {"ok": True, "data": ticket, "error": None}
def list_tickets(status):
    if not isinstance(status, str):
        return {"ok": False, "data": None, "error": "工单状态必须是字符串"}

    status = status.strip()

    if not status:
        return {"ok": False, "data": None, "error": "工单状态不能为空"}

    tickets = [ticket for ticket in MOCK_TICKETS.values() if ticket["status"] == status]

    return {"ok": True, "data": tickets, "error": None}


def search_docs(question, top_k=3):
    if not isinstance(question, str):
        return {"ok": False, "data": None, "error": "问题必须是字符串"}

    question = question.strip()
    if not question:
        return {"ok": False, "data": None, "error": "问题不能为空"}

    if type(top_k) is not int or not 1 <= top_k <= 10:
        return {"ok": False, "data": None, "error": "top_k必须是1到10的整数"}

    payload = {"question": question, "top_k": top_k}

    try:
        response = requests.post(
            "http://127.0.0.1:8000/search",
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        return {"ok": False, "data": None, "error": "资料检索请求超时"}
    except requests.exceptions.ConnectionError:
        return {"ok": False, "data": None, "error": "无法连接资料检索服务"}
    except requests.exceptions.JSONDecodeError:
        return {"ok": False, "data": None, "error": "资料检索服务未返回有效JSON"}
    except requests.exceptions.RequestException:
        return {"ok": False, "data": None, "error": "资料检索HTTP请求失败"}

    return {"ok": True, "data": data, "error": None}


if __name__ == "__main__":
    print(get_ticket(" T1001 "))
    print(get_ticket("T9999"))
    print(get_ticket("   "))
    print(get_ticket(1001))
    print(get_ticket(" T1002 "))
    result = search_docs(
        "Should I raise or return HTTPException?",
        top_k=2,
    )
    print(result)
    print(list_tickets("处理中"))
    print(list_tickets("待处理"))
    print(list_tickets(" 已关闭"))
    print(list_tickets("   "))
    print(list_tickets(123))
