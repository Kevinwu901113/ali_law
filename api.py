# coding=utf-8
import requests
import re
from fuzzywuzzy import process
from dateutil.parser import parse as parse_date
import datetime

headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer DD588018ADCC373065941C2E935D04595E3C9CA65F8873A3'
        }
domain = "comm.chatglm.cn"
def api(data,type):
    url=f"https://{domain}/law_api/s1_b/{type}"
    rsp = requests.post(url, json=data, headers=headers)
    
    return rsp.json()

def match1(key,key_list):
        ans=[]
        for k in key:
              ans.append(process.extractOne(k, key_list)[0])
        
        return ans

def report(question):
        
        pattern = r'(.*?)(?=股份有限公司)'  
        # 执行匹配  
        match = re.search(pattern,question)  
        company=match.group(1).strip()+"股份有限公司"
        ans={'company_name':f"{company}"}
        dict_list={}
        if "工商信息" in question:
                data={
                "query_conds":  {"公司名称": f"{company}"},
                "need_fields": ["公司名称","登记状态","法定代表人","注册资本","成立日期","企业地址","联系电话","联系邮箱","注册号","组织机构代码","参保人数","行业一级","行业二级","行业三级","曾用名","经营范围"]
                }
                company_info=api(data,"get_company_register")
                dict_list["工商信息"]=[company_info]
        else:
                data={
                "query_conds":  {"公司名称": f"{company}"},
                "need_fields": ["公司名称","登记状态","法定代表人","注册资本","成立日期","企业地址","联系电话","联系邮箱","注册号","组织机构代码","参保人数","行业一级","行业二级","行业三级","曾用名","经营范围"]
                }
                company_info=api(data,"get_company_register")
                dict_list["工商信息"]=[company_info]
        data={
        "query_conds":  {"关联上市公司全称": f"{company}"},
        "need_fields": []
        }
        
        company_sub=api(data,"get_sub_company_info_list")
        if "过亿" in question:
               company_sub=[sub for sub in company_sub if sub["上市公司投资金额"]!=None and "亿" in str(sub["上市公司投资金额"]) ]
        if "全资" in question:
               company_sub=[sub for sub in company_sub if sub["上市公司参股比例"]!=None and str(sub["上市公司参股比例"])=="100.0" ]
        dict_list["子公司信息"]=company_sub
        company_list=[company]
        for sub in company_sub:
               company_list.append(sub["公司名称"])
        
        law=[]
        for c in company_list:
               data={
                "query_conds":  {"关联公司": f"{c}"},
                "need_fields": ["关联公司","标题","案号","文书类型","原告","被告","原告律师事务所","被告律师事务所","案由","涉案金额","日期","文件名"]
                }
               t= api(data,"get_legal_document_list")
               if isinstance(t, dict):
                      law.append(t)
               elif t!=[]:
                        law=law+t
        
        if "立案时间" in question:       
                pattern = r'\d{2}年'  
                matches = re.findall(pattern, question)           
                years = [match.replace('年', '') for match in matches][0]  
                years="20"+str(years)
                
                law=[l for l in law if years in l["案号"]] 
        
        if "审理时间" in question:       
                pattern = r'\d{2}年'  
                matches = re.findall(pattern, question)           
                years = [match.replace('年', '') for match in matches][0]  
                years="20"+str(years)
                law=[l for l in law if years in l["日期"]] 
        if "涉案金额" in question:
                if "10万" in question:
                      law=[l for l in law if float(l["涉案金额"])>100000]
                else: 
                        law=[l for l in law if float(l["涉案金额"])>0]
                
        dict_list["裁判文书"]=law
        xz=[]
        if "限制高消费" in question:
                
                for c in company_list:
                        data={
                                "query_conds":  {"限制高消费企业名称": f"{c}"},
                                "need_fields": []
                                }
                        t= api(data,"get_xzgxf_info_list")
                        if isinstance(t, dict):
                                xz.append(t)
                        elif t!=[]:
                                xz=xz+t
                xz=[x for x in xz if "2019" in x["案号"] and (x["涉案金额"]!='-' and float(x["涉案金额"])>0)]             
        dict_list["限制高消费"]=xz        
        ans["dict_list"]=str(dict_list)
        print(ans)
        return api(ans,"save_dict_list_to_word")



def generate_lawsuit_info(question):
    
        question=question.replace("法人","")


   

      