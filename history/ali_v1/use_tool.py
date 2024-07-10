import requests
import json
domain = "comm.chatglm.cn"

def tool_use_response(response_choices):
   #调用函数
    response_json = response_choices[0].message.tool_calls[0].function.arguments    # 解析response中返回的JSON字符串
    response_dict = json.loads(response_json)
    using_tool = response_choices[0].message.tool_calls[0].function.name    # 获取工具名称

    if using_tool == "search_company_name_by_info":
        key = response_dict["key"]
        value = response_dict["value"]
        data = {
            "key": key,
            "value": value
        }
    elif using_tool == "get_company_info":
        company_name = response_dict["company_name"]    # 获取公司名称
        data = {
        "company_name": company_name
        }
    elif using_tool == "get_company_register":
        company_name = response_dict["company_name"]    # 获取公司名称
        data = {
        "company_name": company_name
        }
    elif using_tool == "search_company_name_by_register":
        key = response_dict["key"]
        value = response_dict["value"]
        data = {
        "key": key,
        "value": value
        }
    elif using_tool == "get_sub_company_info":
        company_name = response_dict["company_name"]    # 获取公司名称
        data = {
        "company_name": company_name
        }
    elif using_tool == "search_company_name_by_sub_info":
        key = response_dict["key"]
        value = response_dict["value"]
        data = {
        "key": key,
        "value": value
        }
    elif using_tool == "get_legal_document":
        case_num = response_dict["case_num"]
        data = {
        "case_num": case_num
        }
    elif using_tool == "search_case_num_by_legal_document":
        key = response_dict["key"]
        value = response_dict["value"]
        data = {
        "key": key,
        "value": value
        }
    else:
        pass
    url = f"https://{domain}/law_api/{using_tool}"
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer DD588018ADCC373065941C2E935D04595E3C9CA65F8873A3'
    }
    rsp = requests.post(url, json=data, headers=headers)
    return rsp.json()

