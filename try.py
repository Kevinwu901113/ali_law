import requests
import logging
import os

# 配置日志记录
logging.basicConfig(level=logging.INFO)

# 从环境变量中获取API密钥
API_KEY = os.getenv('API_KEY', 'DD588018ADCC373065941C2E935D04595E3C9CA65F8873A3')

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_KEY}'
}
domain = "comm.chatglm.cn"

def api(data, type):
    url = f"https://{domain}/law_api/s1_b/{type}"
    try:
        rsp = requests.post(url, json=data, headers=headers)
        rsp.raise_for_status()  # 检查响应状态码
        return rsp.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return {"error": "Request failed"}

if __name__ == "__main__":
    try1 = api({"query_conds": {"关联公司": "上海晨光文具股份有限公司"}, "need_fields": []}, "get_legal_document_list")
    print(try1)