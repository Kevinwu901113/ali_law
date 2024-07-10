import json
import logging
from LLM import reply, parse_json_from_response
from propmt import GET_INFORMERTION_CLASS, QUESTION_CLASS
from handlers import *

# 配置日志记录
logging.basicConfig(level=logging.INFO)

def start(question):
    prompt = QUESTION_CLASS.format(question=question)
    initial_response = parse_json_from_response(reply(prompt))

    if not initial_response:
        logging.error("Failed to parse initial response")
        return None

    if initial_response.get("category_name") == "direct_answer":
        return reply(question)
    
    prompt = GET_INFORMERTION_CLASS.format(question=question)
    info_response = parse_json_from_response(reply(prompt))
    
    if not info_response:
        logging.error("Failed to parse information response")
        return None

    return process_info_response(info_response, question)

def process_info_response(response, question):
    info_number = response.get("information_number")
    if info_number in ["1", 1]:
        return handle_company_info(question)
    elif info_number in ["2", 2]:
        return handle_get_company_info(question, "上市公司简称")
    elif info_number in ["3", 3]:
        return handle_get_company_info(question, "公司简称")
    elif info_number in ["4", 4]:
        return handle_company_register_name(question)
    elif info_number in ["5", 5]:
        return handle_get_legal_document(question)
    elif info_number in ["6", 6]:
        return handle_get_court_info(question)
    elif info_number in ["7", 7]:
        return handle_get_court_info(question)
    elif info_number in ["8", 8]:
        return handle_get_lawfirm_info(question)
    elif info_number in ["9", 9]:
        return handle_get_address_info(question)
    elif info_number in ["10", 10]:
        return handle_get_address_info(question)
    elif info_number in ["11", 11]:
        return handle_get_temp_info(question)
    else:
        logging.warning(f"Unhandled information number: {info_number}")
        return None

def main():
    question = "91310000677833266F的公司全称是？该公司的涉案次数为？（起诉日期在2020年）作为被起诉人的次数及总金额为？"
    answer = start(question)
    if answer:
        print("Answer:", answer)
    else:
        logging.error("Failed to generate a valid answer")

if __name__ == "__main__":
    main()
