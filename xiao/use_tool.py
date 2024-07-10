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
        url = f"https://{domain}/law_api/{using_tool}"
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer DD588018ADCC373065941C2E935D04595E3C9CA65F8873A3'
        }
        rsp = requests.post(url, json=data, headers=headers)

        if rsp.json()!=[] and isinstance(rsp.json(), list):
            print(rsp.json())
            company_names = [company["公司名称"] for company in rsp.json()] 
            return search2("get_company_info",value,company_names)
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
        url = f"https://{domain}/law_api/{using_tool}"
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer DD588018ADCC373065941C2E935D04595E3C9CA65F8873A3'
        }
        rsp = requests.post(url, json=data, headers=headers)
        if rsp.json()!=[] and isinstance(rsp.json(), list):
            company_names = [company["公司名称"] for company in rsp.json()] 
            return search2("get_company_info",value,company_names)
    elif using_tool == "get_sub_company_info":
        company_name = response_dict["company_name"]    # 获取公司名称
        data = {
        "company_name": company_name
        }
    elif using_tool == "search_company_name_by_sub_info":
        key = response_dict["key"]
        value = response_dict["value"]
        #value=value.translate(table)
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
        if rsp.json()!=[] and isinstance(rsp.json(), list):
            print(rsp.json())
            company_names = [company["公司名称"] for company in rsp.json()] 
            return search2("get_sub_company_info",value,company_names)
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
        url = f"https://{domain}/law_api/{using_tool}"
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer DD588018ADCC373065941C2E935D04595E3C9CA65F8873A3'
        }
        rsp = requests.post(url, json=data, headers=headers)
        print(rsp.json())
        if rsp.json()!=[] and isinstance(rsp.json(), list):
            company_names = [company["案号"] for company in rsp.json()] 
            return search2("get_legal_document",value,company_names)                  
    else:
        pass
    
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

def search2(using_tool,value,company_names):
    ans=[]   
    if len(company_names)!=0:   
        f=len(company_names)
        if using_tool=="get_sub_company_info":
            s=f"{value}一共包含{f}家子公司，下列是{value}与子公司之间的关联信息，关联上市公司就是母公司，（包括关联上市公司股票代码、关联上市公司股票简称、关联上市公司全称、上市公司关系、上市公司参股比例、上市公司投资金额、公司名称）"
        if using_tool=="get_company_info":
            s=f"{value}一共包含{f}家公司，下列是该公司的信息（公司名称、简称、英文名称、关联证券、公司代码、曾用简称、所属市场、所属行业、上市日期、法人代表、总经理、董秘 、邮政编码 、注册地址 、办公地址 、联系电话 、传真 、官方网址 、电子邮箱 、入选指数 、主营业务 、经营范围 、机构简介 、每股面值 、首发价格 、首发募资净额 、首发主承销商）和注册信息（公司名称、登记状态、统一社会信用代码、注册资本、成立日期、省份、城市、区县、注册号、组织机构代码、参保人数、企业类型、曾用名）"
        if using_tool=="get_legal_document":
            s=f"{value}一共涉及{f}个法律文书信息，下列是该公司设计法律文书的信息，包括标题、案号、文书类型、原告、被告、原告律师、被告律师、案由、审理法条依据、涉案金额、判决结果、胜诉方、文件名"
        ans.append([s])   
    for company_name in company_names:
            if using_tool!="get_legal_document":
                data={
                    "company_name": company_name
                }
            else:
                data={
                    "case_num": company_name
                }
            
            url = f"https://{domain}/law_api/{using_tool}"
            headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer DD588018ADCC373065941C2E935D04595E3C9CA65F8873A3'
            }
            rsp = requests.post(url, json=data, headers=headers)
            data1=rsp.json()

            if isinstance(data1, dict) and '判决结果' in data1:  
                del data1['判决结果']
            if isinstance(data1, dict) and '文件名' in data1:  
                del data1['文件名']
            if isinstance(data1, dict) and '机构简介' in data1:  
                del data1['机构简介']
            if isinstance(data1, dict) and '经营范围' in data1:  
                del data1['经营范围']
            ans.append(data1)
            if using_tool=="get_company_info":
                url = f"https://{domain}/law_api/get_company_register"
                rsp = requests.post(url, json=data, headers=headers)
                ans.append(rsp.json())

            
    return ans
                

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
    tem=[]
    using_tool = "search_company_name_by_info"
    keys =["简称","英文名称" ,"曾用简称","所属市场","所属行业"]
    for key in keys:        
        value=value.translate(table)
        t=search1(using_tool,key,value)
        if t!=[] and t!="查询失败，大概率是因为没有按照规范使用接口，如果确定自己没有问题，请咨询管理员。":
            tem.append(t)
        if tem!=[]:

            company_names = [company["公司名称"] for company in tem[0]] 
            ans.append(search2("get_company_info",value,company_names) )
            
    using_tool = "search_company_name_by_sub_info"
    keys =["关联上市公司股票简称","关联上市公司全称"]
    tem=[]
    for key in keys:        
        value=value.translate(table)
        t=search1(using_tool,key,value)
        if t!=[] and t!="查询失败，大概率是因为没有按照规范使用接口，如果确定自己没有问题，请咨询管理员。":
            # print(t)
            tem.append(t)   
        # print(tem)
        if tem!=[]:
            company_names = [company["公司名称"] for company in tem[0]]   
            if len(company_names)!=0:   
                f=len(company_names)
                s=f"{value}一共包含{f}家子公司，下列是{value}与子公司之间的关联信息，关联上市公司就是母公司，（包括关联上市公司股票代码、关联上市公司股票简称、关联上市公司全称、上市公司关系、上市公司参股比例、上市公司投资金额、公司名称）"
                ans.append([s])   
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
                
           
    print(ans) 
    return ans
