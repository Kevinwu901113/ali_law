import requests
import json
from api import *

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
        key = get_key(response_message)
        value = get_value(response_message)
        value=value.translate(table)
        data = {
            "key": key,
            "value": value
        }
        rsp = search_company_name_by_info(key, value)
    elif using_tool == "get_company_info":
        company_name = get_company_name(response_message)    # 获取公司名称
        data = {
        "company_name": company_name
        }
        rsp = get_company_info(company_name)
    elif using_tool == "get_company_register":
        company_name = get_company_name(response_message)    # 获取公司名称
        data = {
        "company_name": company_name
        }
        rsp = get_company_register(company_name)
    elif using_tool == "search_company_name_by_register":
        key = get_key(response_message)
        value = get_value(response_message)
        value=value.translate(table)
        data = {
        "key": key,
        "value": value
        }
        rsp = search_company_name_by_register(key, value)
    elif using_tool == "get_sub_company_info":
        company_name = get_company_name(response_message)    # 获取公司名称
        data = {
        "company_name": company_name
        }
        rsp = get_sub_company_info(company_name)
    elif using_tool == "search_company_name_by_sub_info":
        key = get_key(response_message)
        value = get_value(response_message)
        value=value.translate(table)
        rsp=search_company_name_by_sub_info(key,value)
       
        company_names = [company["公司名称"] for company in rsp] 
        a=[]
        for company_name in company_names:
                a.append(get_sub_company_info(company_name))
                print(company_name)
                a.append(rsp.json())
        print(a)        
        return a        
    elif using_tool == "get_legal_document":
        case_num = response_dict["case_num"]
        case_num=case_num.translate(table)
        data = {
        "case_num": case_num
        }
        rsp = get_legal_document(case_num)
    elif using_tool == "search_case_num_by_legal_document":
        key = response_dict["key"]
        value = response_dict["value"]
        value=value.translate(table)
        data = {
        "key": key,
        "value": value
        }        
        rsp = search_case_num_by_legal_document(key, value)          
    else:
        pass
    
    if rsp==[]:
        t=tool_use_response_correct(response_message)
        return t
    else:
        return rsp

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
        value= get_case_num(response_message)
    elif using_tool[:3]=="get":
        value= get_company_name(response_message)
    else:
        value= get_value(response_message)
    
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
    tem=[]
    for key in keys:        
        value=value.translate(table)
        t=search1(using_tool,key,value)
        if t!=[] and t!="查询失败，大概率是因为没有按照规范使用接口，如果确定自己没有问题，请咨询管理员。":
            # print(t)
            # tem.append(t)   
            tem.extend(t)
        company_names = [company["公司名称"] for company in tem]         
        for company_name in company_names:
                print(company_name)
                rsp = get_sub_company_info(company_name)
                ans.append(rsp)
                
           
    print(ans) 
    return ans
