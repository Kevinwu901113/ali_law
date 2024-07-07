import json
from LLM import reply,prase_json_from_response
from propmt import GET_INFORMERTION_CLASS,QUESTION_CLASS,COMPANY_NAME_CLASS,GET_KEY_CLASS
from api import api

def start(response,question):
    if response["information_number"]=="1" or response["information_number"]==1:
        prompt=COMPANY_NAME_CLASS.format(question=question)
        response= prase_json_from_response(reply(prompt))
        if response["question_type"]=="company_info":
            return
        elif response["question_type"]=="law_info":
            return
        else:
            return  #除了类型1以外，其他类型涉及到的接口数量较少，可以不需要再做判断
    elif response["information_number"]=="2" or response["information_number"]==2: #涉及get_company_info
        key="上市公司简称"
        prompt=GET_KEY_CLASS.format(question=question,key=key)
        key=reply(prompt)
        data={
            "query_conds":  {"公司简称": f"{key}"},
            "need_fields": []
        }
        return api(data,"get_company_info")
    elif response["information_number"]=="3" or response["information_number"]==3: #涉及get_company_info
        return
    elif response["information_number"]=="4" or response["information_number"]==4: #涉及get_company_register_name
        return
    elif response["information_number"]=="5" or response["information_number"]==5: #涉及get_legal_document、get_legal_abstract、get_xzgxf_info
        return
    elif response["information_number"]=="6" or response["information_number"]==6: #涉及get_court_info、get_court_code
        return
    elif response["information_number"]=="7" or response["information_number"]==7: #涉及get_court_code
        return
    elif response["information_number"]=="8" or response["information_number"]==8: #涉及get_lawfirm_info、get_lawfirm_log
        return
    elif response["information_number"]=="9" or response["information_number"]==9: #涉及get_address_info
        return
    elif response["information_number"]=="10" or response["information_number"]==10: #涉及get_address_code
        return
    elif response["information_number"]=="11" or response["information_number"]==11: #涉及get_temp_info
        return

question="我想要联系上海妙可蓝多食品科技股份有限公司的法人代表，请问他的名字是什么？"
prompt=QUESTION_CLASS.format(question=question)
response = prase_json_from_response(reply(prompt))
if response["category_name"] == "direct_answer":
    answer = reply(question)
else:
    prompt=GET_INFORMERTION_CLASS.format(question=question)
    response = prase_json_from_response(reply(prompt))
    info=start(response,question)    #api返回的信息
    #判断api返回信息是否足够回答问题，不足够则将info和quuestion合并再进行判断，直到获取到足够信息，判断标准是info中包含的字段是否超过问题目标信息
    #最后将info和question交给模型生成答案
    
   