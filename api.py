# coding=utf-8
import requests
import re
from fuzzywuzzy import process
from key import team_key
from dateutil.parser import parse as parse_date
import datetime
headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {team_key}'
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
        return ans

# print(api(report("马应龙药业集团股份有限公司关于工商信息（不包括公司简介）及投资金额过亿的全资子公司，母公司及子公司的审理时间在2020年涉案金额大于10万的裁判文书（不需要判决结果）整合报告。"),"save_dict_list_to_word"))
      

def generate_lawsuit_info(question):
    pattern = r"(?P<plaintiff>.*?)的法人与(?P<defendant>.*?)的法人发生了(?P<dispute_type>.*?纠纷)，(?P<plaintiff_rep>.*?)委托给了(?P<plaintiff_law_firm>.*?)，(?P<defendant_rep>.*?)委托给了(?P<defendant_law_firm>.*?)，请写一份民事起诉状给(?P<court>.*?法院)时间是(?P<date>\d{4}(?:年(?:\d{1,2}(?:月(?:\d{1,2}(?:日)?)?)?)?|[-/]\d{1,2}(?:[-/]\d{1,2})?)?)"
    match = re.search(pattern, question)

    if not match:
        return "问题描述不符合预期格式。"

    date_str = match.group('date')
    try:
        lawsuit_date = parse_date(date_str, fuzzy=True)
        formatted_date = lawsuit_date.strftime('%Y-%m-%d')
    except ValueError:
        # Handle simple year or year-month formats
        year_match = re.match(r"(\d{4})年?$", date_str)
        year_month_match = re.match(r"(\d{4})年(\d{1,2})月?$", date_str)  # Matches "2024年2月"
        year_month_dash_match = re.match(r"(\d{4})-(\d{1,2})$", date_str)  # Matches "2024-2" or "2024-02"
        year_month_slash_match = re.match(r"(\d{4})/(\d{1,2})$", date_str)  # Matches "2024/2" or "2024/02"
        if year_match:
                formatted_date = f"{year_match.group(1)}年"  # Keep just the year
        elif year_month_match:
                formatted_date = f"{year_month_match.group(1)}年{int(year_month_match.group(2))}月"  # Formats to "2024年2月"
        elif year_month_dash_match:
                formatted_date = f"{year_month_dash_match.group(1)}-{year_month_dash_match.group(2).zfill(2)}"  # Formats to "2024-02"
        elif year_month_slash_match:
                formatted_date = f"{year_month_slash_match.group(1)}-{year_month_slash_match.group(2).zfill(2)}"  # Formats to "2024-02"
        else:
                formatted_date = "无法解析日期"

    # 提取信息
    plaintiff = match.group('plaintiff')
    defendant = match.group('defendant')
    plaintiff_law_firm = match.group('plaintiff_law_firm')
    defendant_law_firm = match.group('defendant_law_firm')
    dispute_type = match.group('dispute_type')

    # 获取原告公司信息
    plaintiff_data = {
        "query_conds": {"公司名称": plaintiff},
        "need_fields": ["公司名称", "法定代表人","企业地址", "联系电话", "联系邮箱"]
    }
    plaintiff_company_info = api(plaintiff_data, "get_company_register")

    # 获取被告公司信息
    defendant_data = {
        "query_conds": {"公司名称": defendant},
        "need_fields": ["公司名称", "法定代表人","企业地址", "联系电话", "联系邮箱"]
    }
    defendant_company_info = api(defendant_data, "get_company_register")

    # 组织所有数据
    result = {
        '原告': plaintiff,
        '原告地址': plaintiff_company_info['企业地址'] if plaintiff_company_info else 'API请求失败',
        '原告法定代表人': plaintiff_company_info['法定代表人'] if plaintiff_company_info else 'API请求失败',
        '原告联系方式': plaintiff_company_info['联系电话'] if plaintiff_company_info else 'API请求失败',
        '原告委托诉讼代理人': plaintiff_law_firm,
        '原告委托诉讼代理人联系方式': plaintiff_company_info['联系电话'] if plaintiff_company_info else 'API请求失败',
        '被告': defendant,
        '被告地址': defendant_company_info['企业地址'] if defendant_company_info else 'API请求失败',
        '被告法定代表人': defendant_company_info['法定代表人'] if defendant_company_info else 'API请求失败',
        '被告联系方式': defendant_company_info['联系电话'] if defendant_company_info else 'API请求失败',
        '被告委托诉讼代理人': defendant_law_firm,
        '被告委托诉讼代理人联系方式': defendant_company_info['联系电话'] if defendant_company_info else 'API请求失败',
        '诉讼请求': dispute_type,
        '事实和理由': '上诉',
        '证据': '详细证据列表待补充',
        '法院名称': match.group('court'),
        '起诉日期': formatted_date
    }
    
    return result

# 示例问题
if __name__ == '__main__':
    question = "深圳市佳士科技股份有限公司的法人与天津凯发电气股份有限公司的法人发生了产品生产者责任纠纷，深圳市佳士科技股份有限公司委托给了山东崇义律师事务所，天津凯发电气股份有限公司委托给了山东海金州律师事务所，请写一份民事起诉状给辽宁省沈阳市中级人民法院时间是2024年。"
    result = generate_lawsuit_info(question)
    print(result)
    print(api(result,"get_company_sue_company"))