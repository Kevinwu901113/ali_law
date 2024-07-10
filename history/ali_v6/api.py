from zhipuai import ZhipuAI
import json
import requests

client = ZhipuAI(api_key="33dcd2e786c4567b9f97a3ac9d38dad0.RMsTbtFmlmtq8zFa") # 请填写您自己的APIKey
domain = "comm.chatglm.cn"

def get_company_info(response_message):
    company_name = response_message['公司名称']
    data = {
        "company_name": company_name
    }
    url = f"https://{domain}/law_api/get_company_info"
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer DD588018ADCC373065941C2E935D04595E3C9CA65F8873A3'
    }
    rsp = requests.post(url, json=data, headers=headers)
    return rsp.json()

def search_company_name_by_info(response_message):
    company_name = response_message['公司名称']
    data = {
        "key": "公司名称",
        "value": company_name
    }
    url = f"https://{domain}/law_api/search_company_name_by_info"
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer DD588018ADCC373065941C2E935D04595E3C9CA65F8873A3'
    }
    rsp = requests.post(url, json=data, headers=headers)
    return rsp.json()

def get_company_register(response_message):
    company_name = response_message['公司名称']
    data = {
        "company_name": company_name
    }
    url = f"https://{domain}/law_api/get_company_register"
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer DD588018ADCC373065941C2E935D04595E3C9CA65F8873A3'
    }
    rsp = requests.post(url, json=data, headers=headers)
    return rsp.json()

def search_company_name_by_register(response_message):
    key = response_message['key']
    value = response_message['value']
    data = {
        "key": key,
        "value": value
    }
    url = f"https://{domain}/law_api/search_company_name_by_register"
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer DD588018ADCC373065941C2E935D04595E3C9CA65F8873A3'
    }
    rsp = requests.post(url, json=data, headers=headers)
    return rsp.json()

def get_sub_company_info(response_message):
    company_name = response_message['公司名称']
    data = {
        "company_name": company_name
    }
    url = f"https://{domain}/law_api/get_sub_company_info"
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer DD588018ADCC373065941C2E935D04595E3C9CA65F8873A3'
    }
    rsp = requests.post(url, json=data, headers=headers)
    return rsp.json()

def search_company_name_by_sub_info(response_message):
    key = response_message['key']
    value = response_message['value']
    data = {
        "key": key,
        "value": value
    }
    url = f"https://{domain}/law_api/search_company_name_by_sub_info"
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer DD588018ADCC373065941C2E935D04595E3C9CA65F8873A3'
    }
    rsp = requests.post(url, json=data, headers=headers)
    return rsp.json()

def get_legal_document(response_message):
    case_num = response_message['案号']
    data = {
        "case_num": case_num,
    }
    url = f"https://{domain}/law_api/get_legal_document"
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer DD588018ADCC373065941C2E935D04595E3C9CA65F8873A3'
    }
    rsp = requests.post(url, json=data, headers=headers)
    return rsp.json()

def search_case_num_by_legal_document(response_message):
    key = response_message['key']
    value = response_message['value']
    data = {
        "key": key,
        "value": value,
    }
    url = f"https://{domain}/law_api/search_case_num_by_legal_document"
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer DD588018ADCC373065941C2E935D04595E3C9CA65F8873A3'
    }
    rsp = requests.post(url, json=data, headers=headers)
    return rsp.json()