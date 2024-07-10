import requests
import json

domain = "comm.chatglm.cn"

def tool_use_response(response_message):
   #调用函数
    response_json = response_message.tool_calls[0].function.arguments    # 解析response中返回的JSON字符串
    response_dict = json.loads(response_json)
    using_tool = response_message.tool_calls[0].function.name    # 获取工具名称
    table = {ord(f):ord(t) for f,t in zip(
     u'，。！？【】（）％＃＠＆１２３４５６７８９０',
     u',.!?[]()%#@&1234567890')}
    if using_tool == "search_company_name_by_info":
        key = response_dict["key"]
        value = response_dict["value"]
        value=value.translate(table)
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
        value=value.translate(table)
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
        value=value.translate(table)
        data = {
        "key": key,
        "value": value
        }
    elif using_tool == "get_legal_document":
        case_num = response_dict["case_num"]
        case_num=case_num.translate(table)
        data = {
        "case_num": case_num
        }
    elif using_tool == "search_case_num_by_legal_document":
        key = response_dict["key"]
        value = response_dict["value"]
        value=value.translate(table)
        data = {
        "key": key,
        "value": value
        }
    elif using_tool == "get_all_connect_company":
        company_names=response_dict["company_name"]
        print(company_names)
        a=[]
        if isinstance(company_names, tuple) or isinstance(company_names,list):
            for company_name in company_names:
                data={
                    "company_name": company_name
                }
                print(company_name)
                url = f"https://{domain}/law_api/get_sub_company_info"
                headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer DD588018ADCC373065941C2E935D04595E3C9CA65F8873A3'
                }
                rsp = requests.post(url, json=data, headers=headers)
                a.append(rsp.json())
                print(a)
            return a
        else:
            data={
                    "company_name": company_names
                }
            print(company_names)
            url = f"https://{domain}/law_api/get_sub_company_info"
            headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer DD588018ADCC373065941C2E935D04595E3C9CA65F8873A3'
            }
            rsp = requests.post(url, json=data, headers=headers)
            return(rsp.json())           
    else:
        pass
    if using_tool!="get_all_connect_company":
        url = f"https://{domain}/law_api/{using_tool}"
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer DD588018ADCC373065941C2E935D04595E3C9CA65F8873A3'
        }
        rsp = requests.post(url, json=data, headers=headers)
        if rsp.json()==[]:
            t=tool_use_response_correct(response_message)
            return t
        else:
            return rsp.json()

def search1(using_tool,key,value):    
    data = {
        "key": key,
        "value": value
    }
    url = f"https://{domain}/law_api/{using_tool}"
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer DD588018ADCC373065941C2E935D04595E3C9CA65F8873A3'
    }
    
    rsp = requests.post(url, json=data, headers=headers)
    
    return rsp.json()


def tool_use_response_correct(response_message):
   #调用函数
    response_json = response_message.tool_calls[0].function.arguments    # 解析response中返回的JSON字符串
    response_dict = json.loads(response_json)
    using_tool = response_message.tool_calls[0].function.name 
    if  using_tool=="get_legal_document":
        value= response_dict["case_num"]
    elif using_tool[:3]=="get":
        value= response_dict["company_name"]
    else:
        value= response_dict["value"]
    
    table = {ord(f):ord(t) for f,t in zip(
     u'，。！？【】（）％＃＠＆１２３４５６７８９０',
     u',.!?[]()%#@&1234567890')}
    ans=[]
    using_tool = "search_company_name_by_info"
    keys =["简称","英文名称" ,"曾用简称","所属市场","所属行业"]
    for key in keys:        
        value=value.translate(table)
        t=search1(using_tool,key,value)
        if t!=[] and t!="查询失败，大概率是因为没有按照规范使用接口，如果确定自己没有问题，请咨询管理员。":
            ans.append(t)
    using_tool = "search_company_name_by_sub_info"
    keys =["关联上市公司股票简称","关联上市公司全称"]
    for key in keys:        
        value=value.translate(table)
        t=search1(using_tool,key,value)
        if t!=[] and t!="查询失败，大概率是因为没有按照规范使用接口，如果确定自己没有问题，请咨询管理员。":
            # print(t)
            ans.append(t)   
    # print(ans) 
    return ans
