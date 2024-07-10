from zhipuai import ZhipuAI
import json
import requests

client = ZhipuAI(api_key="33dcd2e786c4567b9f97a3ac9d38dad0.RMsTbtFmlmtq8zFa") # 请填写您自己的APIKey
domain = "comm.chatglm.cn"

def get_company_name(response_message):
    response_json = response_message.tool_calls[0].function.arguments    # 解析response中返回的JSON字符串
    response_dict = json.loads(response_json)
    company_name = response_dict['company_name']
    return company_name

def get_key(response_message):
    response_json = response_message.tool_calls[0].function.arguments    # 解析response中返回的JSON字符串
    response_dict = json.loads(response_json)
    key = response_dict['key']
    return key

def get_value(response_message):
    table = {ord(f):ord(t) for f,t in zip(
     u'，。！？【】（）％＃＠＆１２３４５６７８９０',
     u',.!?[]()%#@&1234567890')}
    response_json = response_message.tool_calls[0].function.arguments    # 解析response中返回的JSON字符串
    response_dict = json.loads(response_json)
    value = response_dict['value']
    value = value.translate(table)
    return value

def get_case_num(response_message):
    table = {ord(f):ord(t) for f,t in zip(
     u'，。！？【】（）％＃＠＆１２３４５６７８９０',
     u',.!?[]()%#@&1234567890')}
    response_json = response_message.tool_calls[0].function.arguments    # 解析response中返回的JSON字符串
    response_dict = json.loads(response_json)
    case_num = response_dict['case_num']
    case_num = case_num.translate(table)
    return case_num

def get_company_info(company_name):
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

def search_company_name_by_info(key,value):
    data = {
        "key": key,
        "value": value
    }
    url = f"https://{domain}/law_api/search_company_name_by_info"
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer DD588018ADCC373065941C2E935D04595E3C9CA65F8873A3'
    }
    rsp = requests.post(url, json=data, headers=headers)
    return rsp.json()

def get_company_register(company_name):
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

def search_company_name_by_register(key,value):
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

def get_sub_company_info(company_name):
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

def search_company_name_by_sub_info(key,value):
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

def get_legal_document(case_num):
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

def search_case_num_by_legal_document(key,value):
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