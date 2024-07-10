import json
from api import *
domain = "comm.chatglm.cn"

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

def tool_use_response(response_message):
    using_tool = response_message.tool_calls[0].function.name 
    if  using_tool=="get_legal_document":
        value= get_case_num(response_message)
    elif using_tool[:3]=="get":
        value= get_company_name(response_message)
    else:
        value= get_value(response_message)
    
    table = {ord(f):ord(t) for f,t in zip(
     u'，。！？【】（）％＃＠＆１２３４５６７８９０',
     u',.!?[]()%#@&1234567890')}
    ans=[]
    tmp=[]
    if using_tool == "search_company_name_by_info":
        keys =["简称","英文名称" ,"曾用简称","所属市场","所属行业"]
        for key in keys:        
            value=value.translate(table)
            t=search1(using_tool,key,value)
            if t!=[] and t!="查询失败，大概率是因为没有按照规范使用接口，如果确定自己没有问题，请咨询管理员。":
                ans.extend(t)
    elif using_tool == "search_company_name_by_sub_info":
        keys =["关联上市公司股票简称","关联上市公司全称"]
        for key in keys:        
            value=value.translate(table)
            t=search1(using_tool,key,value)
            if t!=[] and t!="查询失败，大概率是因为没有按照规范使用接口，如果确定自己没有问题，请咨询管理员。":
                tmp.extend(t)
            company_names = [company["公司名称"] for company in tmp]         
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
                    ans.append(rsp.json())
    elif using_tool == "search_company_name_by_register":
        keys = ["统一社会信用代码","注册资本","注册号","曾用名","企业类型","组织机构代码"]
        for key in keys:        
            value=value.translate(table)
            t=search1(using_tool,key,value)
            if t!=[] and t!="查询失败，大概率是因为没有按照规范使用接口，如果确定自己没有问题，请咨询管理员。":
                tmp.extend(t)
            company_names = [company["公司名称"] for company in tmp]
            for company_name in company_names:
                data={
                    "company_name": company_name
                }
                print(company_name)
                url = f"https://{domain}/law_api/get_company_register"
                headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer DD588018ADCC373065941C2E935D04595E3C9CA65F8873A3'
                }
                rsp = requests.post(url, json=data, headers=headers)
                ans.append(rsp.json())
    print(ans) 
    return ans