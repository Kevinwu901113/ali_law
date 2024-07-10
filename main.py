import json
from LLM import reply,prase_json_from_response
from propmt import GET_INFORMERTION_CLASS,QUESTION_CLASS,COMPANY_NAME_CLASS,GET_KEY_CLASS,GET_KEY1_CLASS,GET_KEY2_CLASS,QUESTION_NAME_CLASS,ANSWER_CLASS
from api import api,match1

def start(response,question):
    key=["公司代码","所属市场","所属行业","成立日期","上市日期","法人代表","总经理","董秘","邮政编码","注册地址","办公地址","联系电话","传真","官网","邮箱","首发募资净额","首发主承销商","统一社会信用代码","注册资本","注册号","组织机构代码","参保人数","行业一级","限高","限制高消费"]
    key_company={"公司代码","所属市场","所属行业","成立日期","上市日期","法人代表","总经理","董秘","邮政编码","注册地址","办公地址","联系电话","传真","官网","邮箱","首发募资净额","首发主承销商"}
    key_register={"统一社会信用代码","注册资本","注册号","组织机构代码","参保人数","行业一级"}
    key_xzgx={"限高","限制高消费"}
    key1=["关联公司","标题","案号","文书类型","原告","被告","原告律师事务所","被告律师事务所","案由","涉案金额","判决结果","日期","摘要","限高","限制高消费"]
    key_law={"关联公司","标题","案号","文书类型","原告","被告","原告律师事务所","被告律师事务所","案由","涉案金额","判决结果","日期"}
    if response["information_number"]=="1" or response["information_number"]==1:
        prompt=COMPANY_NAME_CLASS.format(question=question)
        response= prase_json_from_response(reply(prompt))
        name="公司名称"
        prompt=GET_KEY_CLASS.format(question=question,k=name)
        name=prase_json_from_response(reply(prompt))["information"]   
        print(name)     
        if response["question_type"]=="company_info":    
            prompt=GET_KEY1_CLASS.format(question=question)                  
            fields=list(prase_json_from_response(reply(prompt)))
            fields=match1(fields,key)
            
            print(fields)
            ans=[]
            if set(fields) & key_company != {}:
                data={
                    "query_conds":  {"公司名称": f"{name}"},
                    "need_fields": list(set(fields) & key_company)
                }
                ans.append(api(data,"get_company_info"))
            if set(fields) & key_register != {}:
                data={
                    "query_conds":  {"公司名称": f"{name}"},
                    "need_fields": list(set(fields) & key_company)
                }
                ans.append(api(data,"get_company_register"))
            if set(fields) & key_xzgx != {}:
                data={
                    "query_conds":  {"限制高消费企业名称": f"{name}"},
                    "need_fields": []
                }
                ans.append(api(data,"get_xzgxf_info_list"))
            return ans
        elif response["question_type"]=="law_info":
            data={
                    "query_conds":  {"关联公司": f"{name}"},
                    "need_fields": []
                }
            return api(data,"get_legal_document_list")
        else:
            data={
                "query_conds":  {"公司名称": f"{name}"},
                "need_fields": []
            }
            t= api(data,"get_sub_company_info")
            if t!={}:
                return t
            else:
                data={
                "query_conds":  {"关联上市公司全称": f"{name}"},
                "need_fields": []
                }
                t= api(data,"get_sub_company_info_list")
              #除了类型1以外，其他类型涉及到的接口数量较少，可以不需要再做判断
    elif response["information_number"]=="2" or response["information_number"]==2: #涉及get_company_info
        key="上市公司简称"
        prompt=GET_KEY_CLASS.format(question=question,k=key)
        key=prase_json_from_response(reply(prompt))["information"]
        data={
            "query_conds":  {"公司简称": f"{key}"},
            "need_fields": []
        }
        return api(data,"get_company_info")
    elif response["information_number"]=="3" or response["information_number"]==3: #涉及get_company_info
        key="上市公司代码"
        prompt=GET_KEY_CLASS.format(question=question,k=key)
        key=prase_json_from_response(reply(prompt))["information"]
        data={
            "query_conds":  {"公司代码": f"{key}"},
            "need_fields": []
        }
        return api(data,"get_company_info")
    elif response["information_number"]=="4" or response["information_number"]==4: #涉及get_company_register_name
        key="统一社会信用代码"
        prompt=GET_KEY_CLASS.format(question=question,k=key)
        key=prase_json_from_response(reply(prompt))["information"]
        data={
            "query_conds":  {"统一社会信用代码": f"{key}"},
            "need_fields": []
        }
        return api(data,"get_company_register_name")
    elif response["information_number"]=="5" or response["information_number"]==5: #涉及get_legal_document、get_legal_abstract、get_xzgxf_info
        name="案号"
        prompt=GET_KEY_CLASS.format(question=question,k=name)
        name=prase_json_from_response(reply(prompt))["information"]
        prompt=GET_KEY2_CLASS.format(question=question)                  
        fields=list(prase_json_from_response(reply(prompt))["information"])
        fields=match1(fields,key1)
        ans=[]
        if set(fields) & key_law != {}:
            data={
                "query_conds":  {"案号": f"{name}"},
                "need_fields": list(set(fields) & key_law)
            }
            ans.append(api(data,"get_legal_document"))
        if set(fields) & {"摘要"} != {}:
            data={
                "query_conds":  {"案号": f"{name}"},
                "need_fields": []
            }
            ans.append(api(data,"get_legal_abstract"))
        if set(fields) & key_xzgx != {}:
            data={
                "query_conds":  {"案号": f"{name}"},
                "need_fields": []
            }
            ans.append(api(data,"get_xzgxf_info"))
        return ans
    elif response["information_number"]=="6" or response["information_number"]==6: #涉及get_court_info、get_court_code
        key="法院名称"
        prompt=GET_KEY_CLASS.format(question=question,k=key)
        key=prase_json_from_response(reply(prompt))["information"]
        data={
            "query_conds":  {"法院名称": f"{key}"},
            "need_fields": []
        }
        ans=[]
        ans.append(api(data,"get_court_info"))
        ans.append(api(data,"get_court_code"))
        return ans
    elif response["information_number"]=="7" or response["information_number"]==7: #涉及get_court_code
        key="法院代字"
        prompt=GET_KEY_CLASS.format(question=question,k=key)
        key=prase_json_from_response(reply(prompt))["information"]
        data={
            "query_conds":  {"法院代字": f"{key}"},
            "need_fields": []
        }
        return api(data,"get_court_code")
    elif response["information_number"]=="8" or response["information_number"]==8: #涉及get_lawfirm_info、get_lawfirm_log
        key="律师事务所名称"
        prompt=GET_KEY_CLASS.format(question=question,k=key)
        key=prase_json_from_response(reply(prompt))["information"]
        data={
            "query_conds":  {"律师事务所名称": f"{key}"},
            "need_fields": []
        }
        ans=[]
        ans.append(api(data,"get_lawfirm_info"))
        ans.append(api(data,"get_lawfirm_log"))
        return ans
    elif response["information_number"]=="9" or response["information_number"]==9: #涉及get_address_info
        key="地址信息"
        prompt=GET_KEY_CLASS.format(question=question,k=key)
        key=prase_json_from_response(reply(prompt))["information"]
        data={
            "query_conds": {"地址": f"{key}"},
            "need_fields":[]
        }
        return api(data,"get_address_info")
    elif response["information_number"]=="10" or response["information_number"]==10: #涉及get_address_code
        key="省市区名称"
        prompt=GET_KEY_CLASS.format(question=question,k=key)
        key=prase_json_from_response(reply(prompt))["information"]
        key="{"+key+"}"
        data={
            "query_conds":key,
            "need_fields":[]
        }
        return api(data,"get_address_code")
    elif response["information_number"]=="11" or response["information_number"]==11: #涉及get_temp_info
        key="省市名称和日期"
        prompt=GET_KEY_CLASS.format(question=question,k=key)
        key=prase_json_from_response(reply(prompt))["information"]
        key="{"+key+"}"
        data={
            "query_conds":key,
            "need_fields":[]
        }
        return api(data,"get_temp_info")

question="91310000677833266F的公司全称是？该公司的涉案次数为？（起诉日期在2020年）作为被起诉人的次数及总金额为？"
prompt=QUESTION_CLASS.format(question=question)
response = prase_json_from_response(reply(prompt))
if response["category_name"] == "direct_answer":
    answer = reply(question)
else:
    prompt=QUESTION_NAME_CLASS.format(question=question)
    question_list=prase_json_from_response(reply(prompt))
    print(question_list["question"])
    ans=""
    for question in list(question_list["question"]):      
        question=ans+question
        print("question:"+question)
        prompt=GET_INFORMERTION_CLASS.format(question=question)
        response = prase_json_from_response(reply(prompt))
        info=start(response,question)    #api返回的信息
        print(info)
        prompt=ANSWER_CLASS.format(question=question,fact1=info)
        t=prase_json_from_response(reply(prompt))["answer"]
        ans=ans+t
        print("ans:"+ans)
    print(ans)