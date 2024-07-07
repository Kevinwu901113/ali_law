import logging
import re
from LLM import reply, parse_json_from_response
from api import api
from propmt import COMPANY_NAME_CLASS, GET_KEY_CLASS

def handle_company_info(question):
    prompt = COMPANY_NAME_CLASS.format(question=question)
    response = parse_json_from_response(reply(prompt))
    
    if not response:
        return None

    question_type = response.get("question_type")
    if question_type == "company_info":
        return reply(question)
    elif question_type == "law_info":
        return reply(question)
    else:
        logging.warning(f"Unhandled question type: {question_type}")
        return None

def handle_get_company_info(question, key):
    prompt = GET_KEY_CLASS.format(question=question, key=key)
    key_value = reply(prompt)
    if not key_value:
        logging.error("Failed to get key value from reply")
        return None

    data = {
        "query_conds": {"公司简称": key_value},
        "need_fields": []
    }
    return api_with_retries(data, "get_company_info")

def handle_company_register_name(question):
    company_id = extract_company_id(question)
    data = {
        "query_conds": {"统一社会信用代码": company_id},
        "need_fields": ["公司名称"]
    }
    company_info = api_with_retries(data, "get_company_register_name")
    if not company_info or 'error' in company_info:
        logging.error("Failed to get company register name")
        return None

    # 获取公司的涉案次数
    data = {
        "query_conds": {
            "统一社会信用代码": company_id,
            "起诉日期": {"$gte": "2020-01-01", "$lte": "2020-12-31"}
        },
        "need_fields": ["案号"]
    }
    lawsuit_info = api_with_retries(data, "get_legal_document_list")
    if not lawsuit_info or 'error' in lawsuit_info:
        logging.error("Failed to get legal document info")
        return None

    # 获取作为被起诉人的次数及总金额
    data = {
        "query_conds": {
            "被告": {"$regex": company_info["公司名称"]},
            "起诉日期": {"$gte": "2020-01-01", "$lte": "2020-12-31"}
        },
        "need_fields": ["案号", "涉案金额"]
    }
    defendant_info = api_with_retries(data, "get_legal_abstract")
    if not defendant_info or 'error' in defendant_info:
        logging.error("Failed to get defendant info")
        return None

    total_amount = sum([case["涉案金额"] for case in defendant_info if "涉案金额" in case])

    # 生成最终回答
    final_answer = (
        f"{company_id}的公司全称是：{company_info['公司名称']}。\n"
        f"该公司的涉案次数为：{len(lawsuit_info)}。\n"
        f"作为被起诉人的次数为：{len(defendant_info)}，总金额为：{total_amount}。"
    )

    return final_answer

def handle_get_legal_document(question):
    # 示例处理逻辑
    company_id = extract_company_id(question)
    data = {
        "query_conds": {"统一社会信用代码": company_id},
        "need_fields": ["案号", "文书类型", "涉案金额"]
    }
    legal_docs = api_with_retries(data, "get_legal_document_list")
    if not legal_docs or 'error' in legal_docs:
        logging.error("Failed to get legal document list")
        return None

    return legal_docs

def handle_get_court_info(question):
    # 示例处理逻辑
    return

def handle_get_lawfirm_info(question):
    # 示例处理逻辑
    return

def handle_get_address_info(question):
    # 示例处理逻辑
    return

def handle_get_temp_info(question):
    # 示例处理逻辑
    return

def extract_company_id(question):
    match = re.search(r"(\d{15,18}[0-9Xx])", question)
    return match.group(1) if match else None

def api_with_retries(data, api_type, retries=3):
    for attempt in range(retries):
        try:
            response = api(data, api_type)
            if response and "error" not in response:
                return response
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed: {e}")
    return {"error": f"Failed after {retries} attempts"}
