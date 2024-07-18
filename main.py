import json
from LLM import reply,prase_json_from_response
from propmt import GET_INFORMERTION_CLASS,QUESTION_CLASS,COMPANY_NAME_CLASS,GET_KEY_CLASS,GET_KEY1_CLASS,GET_KEY2_CLASS,QUESTION_NAME_CLASS,ANSWER_CLASS,GET_KEY3_CLASS,ANSWER1_CLASS,ANSWER2_CLASS,ANSWER3_CLASS,LAWSUIT_CLASS
from api import api,match1,report,generate_lawsuit_info

def start(response,question,prompt1):
    key=["公司代码","所属市场","所属行业","成立日期","上市日期","法人代表","总经理","董秘","邮政编码","注册地址","办公地址","联系电话","传真","官网","邮箱","首发募资净额","首发主承销商","统一社会信用代码","注册资本","注册号","组织机构代码","参保人数","行业一级","限高","限制高消费"]
    key_company={"公司代码","所属市场","所属行业","成立日期","上市日期","法人代表","总经理","董秘","邮政编码","注册地址","办公地址","联系电话","传真","官网","邮箱","首发募资净额","首发主承销商"}
    key_register={"统一社会信用代码","注册资本","注册号","组织机构代码","参保人数","行业一级","注册地址"}
    key_xzgx={"限高","限制高消费"}
    key1=["关联公司","标题","案号","文书类型","原告","被告","原告律师事务所","被告律师事务所","案由","涉案金额","判决结果","日期","摘要","限高","限制高消费"]
    key_law={"关联公司","标题","案号","文书类型","原告","被告","原告律师事务所","被告律师事务所","案由","涉案金额","判决结果","日期"}
    print("information_number:"+str(response["information_number"]))
    answ=[]
    if response["information_number"]=="1" or response["information_number"]==1:
        prompt=COMPANY_NAME_CLASS.format(question=question)
        response= prase_json_from_response(reply(prompt))
        nam="公司名称"
        prompt=prompt1.format(question=question,k=nam)
        nam=prase_json_from_response(reply(prompt))["information"]   
        print(nam)
        
        for  name in list(nam):
            if response["question_type"]=="company_info":    
                prompt=GET_KEY1_CLASS.format(question=question)                  
                fields=list(prase_json_from_response(reply(prompt))["information"])
                print("fields: "+str(fields))
                fields=match1(fields,key)            
                print("fields: "+str(fields))
                ans=[]
                if set(fields) & key_company:
                    data={
                        "query_conds":  {"公司名称": f"{name}"},
                        "need_fields": list(set(fields) & key_company)
                    }
                    ans.append(api(data,"get_company_info"))
                if set(fields) & key_register:
                    t1=list(set(fields) & key_register)
                    if "注册地址" in t1:
                        t1.remove("注册地址")
                        t1.append("企业地址")
                    data={
                        "query_conds":  {"公司名称": f"{name}"},
                        "need_fields": t1
                    }
                    ans.append(api(data,"get_company_register"))
                if set(fields) & key_xzgx:
                    data={
                        "query_conds":  {"限制高消费企业名称": f"{name}"},
                        "need_fields": []
                    }
                    ans.append(api(data,"get_xzgxf_info_list"))
                if ans !=[[]] and ans !=[]:
                    answ.append(ans)
                
            elif response["question_type"]=="law_info":
                data={
                        "query_conds":  {"关联公司": f"{name}"},
                        "need_fields": ["关联公司","标题","案号","文书类型","原告","被告","原告律师事务所","被告律师事务所","案由","涉案金额","日期","文件名"]
                    }
                ans=api(data,"get_legal_document_list")
                tem=ans
                if  ans!=[]:
                    prompt=ANSWER2_CLASS.format(question=question)
                    an=prase_json_from_response(reply(prompt))
                    print(an)
                    if an["涉案金额"]!="":
                        for t in range(len(ans)):
                            ans[t]["涉案金额"] = ans[t]["涉案金额"].replace("千", "*1e3")
                            ans[t]["涉案金额"] = ans[t]["涉案金额"].replace("万", "*1e4")
                            ans[t]["涉案金额"] = ans[t]["涉案金额"].replace("亿", "*1e8")
                        if "-" in an["涉案金额"]:
                            tt=an["涉案金额"].split("-")
                            ans=[t for t in ans if t["涉案金额"]!='-' and t["涉案金额"]!='' and eval(an["涉案金额"])!=0 and float(tt[0])<eval(t["涉案金额"]) and float(tt[1])>eval(t["涉案金额"])]
                        else:
                            ans=[t for t in ans if t["涉案金额"]!='-' and t["涉案金额"]!='' and eval(an["涉案金额"])!=0 and float(an["涉案金额"])<=eval(t["涉案金额"])]
                            
                    ans=[t for t in ans if an["原告"] in t["原告"] and an["被告"] in t["被告"] and an["原告律师事务所"] in t["原告律师事务所"] and an["被告律师事务所"] in t["被告律师事务所"] and an["立案时间"] in t["案号"] and an["审理日期"] in t["日期"] and an["案由"] in t["案由"]]
                    num=0
                    if ans !=[]:
                        if isinstance(ans,dict):
                            num=ans["涉案金额"]
                            p=f"一共有1起满足条件的涉及案件,投资总金额为{num}元"
                        else:
                            for t in ans:
                                t["涉案金额"] = t["涉案金额"].replace("千", "*1e3")
                                t["涉案金额"] = t["涉案金额"].replace("万", "*1e4")
                                t["涉案金额"] = t["涉案金额"].replace("亿", "*1e8")
                                if t["涉案金额"]!='-' and t["涉案金额"]!='':
                                    num=num+eval(t["涉案金额"])
                            p=f"一共有{len(ans)}起满足条件的涉及案件，涉案总金额为{num}元"
                        
                        
                        answ.append(p)
                        answ.append(ans)
                    else:
                        if tem!=[]:
                            answ.append(tem)
                    print(answ)

            else:
                data={
                    "query_conds":  {"公司名称": f"{name}"},
                    "need_fields": []
                }
                t= api(data,"get_sub_company_info")
                if t!=[]:
                    answ.append(t)
                else:
                    data={
                    "query_conds":  {"关联上市公司全称": f"{name}"},
                    "need_fields": []
                    }
                    ans=api(data,"get_sub_company_info_list")
                    
                    if ans!=[]:
                        prompt=ANSWER3_CLASS.format(question=question)
                        an=prase_json_from_response(reply(prompt))
                        print(an)
                        
                        if an["投资金额"]!="":
                            for t in range(len(ans)):
                                
                                ans[t]["上市公司投资金额"] =ans[t]["上市公司投资金额"].replace("千", "*1e3")
                                ans[t]["上市公司投资金额"] = ans[t]["上市公司投资金额"].replace("万", "*1e4")
                                ans[t]["上市公司投资金额"] = ans[t]["上市公司投资金额"].replace("亿", "*1e8")
                                
                            ans=[t for t in ans if t["上市公司投资金额"]!='-' and t["上市公司投资金额"]!='' and eval(t["上市公司投资金额"])!=0 and float(an["投资金额"])<=eval(t["上市公司投资金额"])]
                        if an["参股比例"]!="":                            
                            ans=[t for t in ans if t["上市公司参股比例"]!='-' and t["上市公司参股比例"]!='' and float(an["参股比例"])<=eval(t["上市公司参股比例"])]
                            
                        num=0
                        print(ans)
                        if isinstance(ans, dict):
                            num=ans["上市公司投资金额"]
                            p=f"一共有1家满足条件的子公司，投资总金额为{num}元"
                        else:
                            for t in ans:
                                t["上市公司投资金额"] =t["上市公司投资金额"].replace("千", "*1e3")
                                t["上市公司投资金额"] = t["上市公司投资金额"].replace("万", "*1e4")
                                t["上市公司投资金额"] = t["上市公司投资金额"].replace("亿", "*1e8")
                                if t["上市公司投资金额"]!='-' and t["上市公司投资金额"]!='':
                                    num=num+eval(t["上市公司投资金额"])
                            p=f"一共有{len(ans)}家满足条件的子公司，投资总金额为{num}元"
                        
                        
                        answ.append(p)  
                        answ.append(ans)
                        
                #除了类型1以外，其他类型涉及到的接口数量较少，可以不需要再做判断
    elif response["information_number"]=="2" or response["information_number"]==2: #涉及get_company_info
        key="上市公司简称"
        prompt=prompt1.format(question=question,k=key)
        key=prase_json_from_response(reply(prompt))["information"]
        ans=[]
        for kkk in list(key):
            data={
                "query_conds":  {"公司简称": f"{kkk}"},
                "need_fields": []
            }
            t=api(data,"get_company_info")
            if t !=[]:
                answ.append(t)
    elif response["information_number"]=="3" or response["information_number"]==3: #涉及get_company_info
        key="上市公司代码"
        prompt=prompt1.format(question=question,k=key)
        key=prase_json_from_response(reply(prompt))["information"]
        for kkk in list(key):
            data={
                "query_conds":  {"公司代码": f"{kkk}"},
                "need_fields": []
            }
            t=api(data,"get_company_info")
            if t !=[]:
                answ.append(t)
    elif response["information_number"]=="4" or response["information_number"]==4: #涉及get_company_register_name
        key="统一社会信用代码"
        prompt=prompt1.format(question=question,k=key)
        key=prase_json_from_response(reply(prompt))["information"]
        print("统一社会信用代码"+str(key))
        for kkk in list(key):
            data={
                "query_conds":  {"统一社会信用代码": f"{kkk}"},
                "need_fields": []
            }
            t=api(data,"get_company_register_name")
            if t !=[]:
                answ.append(t)
    elif response["information_number"]=="5" or response["information_number"]==5: #涉及get_legal_document、get_legal_abstract、get_xzgxf_info
        if "法院" in question:
            response["information_number"]=7            
            answ.append(start(response,question,prompt1))
        nam="案号"
        prompt=prompt1.format(question=question,k=nam)
        nam=prase_json_from_response(reply(prompt))["information"]
        for name in list(nam):
            prompt=GET_KEY2_CLASS.format(question=question)                  
            fields=list(prase_json_from_response(reply(prompt))["information"])
            fields=match1(fields,key1)
            ans=[]
            if set(fields) & key_law:
                if len(name)>5:
                    name=list(name)
                    name[0]='('
                    name[5]=')'
                    name=''.join(name)
                data={
                    "query_conds":  {"案号": f"{name}"},
                    "need_fields": list(set(fields) & key_law)
                }
                ans.append(api(data,"get_legal_document"))
            if set(fields) & {"摘要"}:
                if len(name)>5:
                    name=list(name)
                    name[0]='（'
                    name[5]='）'
                    name=''.join(name)
                data={
                    "query_conds":  {"案号": f"{name}"},
                    "need_fields": []
                }
                ans.append(api(data,"get_legal_abstract"))
            if set(fields) & key_xzgx:
                if len(name)>5:
                    name=list(name)
                    name[0]='（'
                    name[5]='）'
                    name=''.join(name)
                data={
                    "query_conds":  {"案号": f"{name}"},
                    "need_fields": []
                }
                ans.append(api(data,"get_xzgxf_info"))
            if ans !=[[]] and ans !=[]:
                answ.append(ans)
    elif response["information_number"]=="6" or response["information_number"]==6: #涉及get_court_info、get_court_code
        key="法院名称"
        prompt=prompt1.format(question=question,k=key)
        key=prase_json_from_response(reply(prompt))["information"]
        for kkk in list(key):
            data={
                "query_conds":  {"法院名称": f"{kkk}"},
                "need_fields": []
            }
            ans=[]
            ans.append(api(data,"get_court_info"))
            ans.append(api(data,"get_court_code"))
            if ans !=[] and ans !=[[]]:
                answ.append(ans)
    elif response["information_number"]=="7" or response["information_number"]==7: #涉及get_court_code
        key="法院代字"
        prompt=prompt1.format(question=question,k=key)
        key=prase_json_from_response(reply(prompt))["information"]
        for kkk in list(key):
            data={
                "query_conds":  {"法院代字": f"{kkk}"},
                "need_fields": []
            }
            t=api(data,"get_court_code")
            if t!=[]:
                answ.append(t)
    elif response["information_number"]=="8" or response["information_number"]==8: #涉及get_lawfirm_info、get_lawfirm_log
        key="律师事务所名称"
        prompt=prompt1.format(question=question,k=key)
        key=prase_json_from_response(reply(prompt))["information"]
        for kkk in list(key):
            data={
                "query_conds":  {"律师事务所名称": f"{kkk}"},
                "need_fields": []
            }
            ans=[]
            ans.append(api(data,"get_lawfirm_info"))
            ans.append(api(data,"get_lawfirm_log"))
            if ans !=[] and ans !=[[]]:
                answ.append(ans)
    elif response["information_number"]=="9" or response["information_number"]==9: #涉及get_address_info
        if "天气" in question or "温度" in question or "气温" in question:
            response["information_number"]=11
            answ.append(start(response,question,prompt1))
        if "代码" in question:
            response["information_number"]=10
            answ.append(start(response,question,prompt1))
        key="地址信息"
        prompt=prompt1.format(question=question,k=key)
        key=prase_json_from_response(reply(prompt))["information"]
        for kkk in list(key):
            data={
                "query_conds": {"地址": f"{kkk}"},
                "need_fields":[]
            }
            t=api(data,"get_address_info")
            if t!=[]:
                answ.append(t)
    elif response["information_number"]=="10" or response["information_number"]==10: #涉及get_address_code
        key="省市区名称"
        prompt=prompt1.format(question=question,k=key)
        key=prase_json_from_response(reply(prompt))["information"]
        for kkk in list(key):
            sf=""
            s=""
            qx=""
            if "北京市" in kkk or "重庆市" in kkk or "上海市" in kkk or "天津市" in kkk:
                t1=kkk.split("市")
                sf=t1[0]+"市"
                s=sf
                if len(t1)<2:
                    return []
                qx=t1[1]
            else:
                t1=kkk.split("省")
                if len(t1)<2:
                    return []
                t2=t1[1].split("市")
                if len(t2)<2:
                    return []
                sf=t1[0]+"省"
                s=t2[0]+"市"
                qx=t2[1]
            data={
                "query_conds":{"省份": f"{sf}", "城市": f"{s}", "区县": f"{qx}"},
                "need_fields":[]
            }
            t=api(data,"get_address_code")
            if t!=[]:
                answ.append(t)
    elif response["information_number"]=="11" or response["information_number"]==11: #涉及get_temp_info
        key="省份名称"
        prompt=prompt1.format(question=question,k=key)
        key1=prase_json_from_response(reply(prompt))["information"]
        key="城市名称"
        prompt=prompt1.format(question=question,k=key)
        key2=prase_json_from_response(reply(prompt))["information"]
        key="日期"
        prompt=prompt1.format(question=question,k=key)
        key3=prase_json_from_response(reply(prompt))["information"]
        print(key1)
        print(key2)
        print(key3)
        for kkk in list(key1):
            
            data={
                "query_conds":{"省份": f"{list(key1)[0]}", "城市": f"{list(key2)[0]}", "日期": f"{list(key3)[0]}"},
                "need_fields":[]
            }
            t=api(data,"get_temp_info")
            if t!=[]:
                answ.append(t)
    return answ
with open('submission140.json', 'r', encoding='utf-8') as f:
    lines = f.readlines()
data1 = [json.loads(line.strip()) for line in lines]

ff=0
for q in data1:
   
    try:
        ans = q['answer']
        continue
    except:
        question = q['question']
        print(q['id'],question)
        while True:
            ttk=0

            try:

                if "整合报告" in question:
                    answer=report(question)
                elif "民事起诉状" in question:
                    prompt=LAWSUIT_CLASS.format(question=question)
                    t1=prase_json_from_response(reply(prompt))
                    ans={}
                    an=0
                    if "法人" in t1["原告信息"]:
                        t2=t1["原告信息"].replace("法人","")
                        data={
                            "query_conds": {"公司名称": f"{t2}"},
                            "need_fields": []
                        }
                        info1=api(data,"get_company_info")
                        ans["原告"]=info1["法人代表"]
                        ans["原告性别"]=""
                        ans["原告生日"]=""
                        ans["原告民族"]=""
                        ans["原告工作单位"]=t2
                        ans["原告地址"]=info1["办公地址"]
                        ans["原告联系方式"]=info1["联系电话"]
                        an=an+1
                    else:
                        ans["原告"]=t1["原告信息"]
                        t2=t1["原告信息"]
                        data={
                            "query_conds": {"公司名称": f"{t2}"},
                            "need_fields": []
                        }
                        info1=api(data,"get_company_info")
                        ans["原告地址"]=info1["办公地址"]
                        ans["原告法定代表人"]=info1["法人代表"]
                        ans["原告联系方式"]=info1["联系电话"]
                    t2=t1["原告律师事务所信息"]
                    data={
                            "query_conds": {"律师事务所名称": f"{t2}"},
                            "need_fields": []
                        }
                    info1=api(data,"get_lawfirm_info")
                    ans["原告委托诉讼代理人"]=info1["律师事务所负责人"]
                    ans["原告委托诉讼代理人联系方式"]=info1["通讯电话"]
                    if "法人" in t1["被告信息"]:
                        t2=t1["被告信息"].replace("法人","")
                        data={
                            "query_conds": {"公司名称": f"{t2}"},
                            "need_fields": []
                        }
                        info1=api(data,"get_company_info")
                        ans["被告"]=info1["法人代表"]
                        ans["被告性别"]=""
                        ans["被告生日"]=""
                        ans["被告民族"]=""
                        ans["被告工作单位"]=t2
                        ans["被告地址"]=info1["办公地址"]
                        ans["被告联系方式"]=info1["联系电话"]
                        an=an+2
                    else:
                        ans["被告"]=t1["被告信息"]
                        t2=t1["被告信息"]
                        data={
                            "query_conds": {"公司名称": f"{t2}"},
                            "need_fields": []
                        }
                        info1=api(data,"get_company_info")
                        ans["被告地址"]=info1["办公地址"]
                        ans["被告法定代表人"]=info1["法人代表"]
                        ans["被告联系方式"]=info1["联系电话"]
                    t2=t1["被告律师事务所信息"]
                    data={
                            "query_conds": {"律师事务所名称": f"{t2}"},
                            "need_fields": []
                        }
                    info1=api(data,"get_lawfirm_info")
                    ans["被告委托诉讼代理人"]=info1["律师事务所负责人"]
                    ans["被告委托诉讼代理人联系方式"]=info1["通讯电话"]
                    ans["诉讼请求"]=t1["纠纷信息"]
                    ans["事实和理由"]="上诉"
                    ans["证据"]=""
                    ans["法院名称"]=t1["法院信息"]
                    ans["起诉日期"]=t1["时间"]
                    t3=["get_company_sue_company","get_citizens_sue_company","get_company_sue_citizens","get_citizens_sue_citizens"]
                    answer=api(ans,t3[an]) 


                else:
                                       
                    prompt=QUESTION_NAME_CLASS.format(question=question)
                    question_list=prase_json_from_response(reply(prompt))
                    print(question_list["question"])
                    ans=""
                    ap=len(list(question_list["question"]))
                    apii=f"api调用次数为{ap}次。"
                    info_total=[apii]
                    for question in list(question_list["question"]): 
                        if question != list(question_list["question"])[0]  :   
                            prompt=ANSWER1_CLASS.format(question=question,fact1=ans)
                            question=prase_json_from_response(reply(prompt))["question"]
                        print("question:"+question)
                        prompt=GET_INFORMERTION_CLASS.format(question=question)
                        response = prase_json_from_response(reply(prompt))
                        f1=0
                        info=[]
                        while f1<2 and info==[]:
                            info=start(response,question,GET_KEY_CLASS)    #api返回的信息
                            f1=f1+1
                            print(info)
                        while f1<4 and info==[]:
                            info=start(response,question,GET_KEY3_CLASS)
                            f1=f1+1
                            print(info)
                        if info!=[]:
                            info_total.append(info)
                        else:
                            info=info_total
                        prompt=ANSWER_CLASS.format(question=question,fact1=info)
                        t=prase_json_from_response(reply(prompt))["answer"]
                        ans=ans+t+"。"
                        
                        print("ans:"+ans)
                    answer=ans
                break
            except:
                ttk=ttk+1
                if ttk==4:
                    q['answer']=question
                    break
            q['answer'] = answer
            print(q['answer'])
            ff=ff+1
            if ff%10==0:
                with open(f"submission{ff}.json", "w", encoding="utf-8") as f:
                    for item in data1:
                        f.write(json.dumps(item, ensure_ascii=False) + "\n")
with open("submission.json", "w", encoding="utf-8") as f:
    for item in data1:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")