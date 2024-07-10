from tools import tools
from zhipuai import ZhipuAI
import json
import re
from key import zhipu

client = ZhipuAI(api_key=zhipu) # 请填写您自己的APIKey

def tool_get_response(content:str):
    tools_list=tools()
    
    messages = [
        {
            "role": "system",
            "content":"你是一个公司信息和法律信息查询分析助手，你有设定好的多个数据表查询工具，你需要提取用户问题中的关键信息和其所属类别，根据关键信息所属类别和需要获取的信息调用相应的工具查询下列四个数据表做出回答。"
        }, 
        {
            "role":"system",
            "content":"公司基本信息数据表：公司名称、简称、英文名称、关联证券、公司代码、曾用简称、所属市场、所属行业、上市日期、法人代表、总经理、董秘 、邮政编码 、注册地址 、办公地址 、联系电话 、传真 、官方网址 、电子邮箱 、入选指数 、主营业务 、经营范围 、机构简介 、每股面值 、首发价格 、首发募资净额 、首发主承销商"
        },
        {
            "role":"system",
            "content":"公司注册信息数据表：公司名称（外键，关联公司基本信息数据表中的公司名称）、登记状态、统一社会信用代码、注册资本、成立日期、省份、城市、区县、注册号、组织机构代码、参保人数、企业类型、曾用名"

        },
        {
            "role":"system",
            "content":"关联子公司信息表：关联上市公司股票代码、关联上市公司股票简称、关联上市公司全称（外键，关联公司基本信息数据表中的公司名称）、上市公司关系、上市公司参股比例（母公司在子公司的参股比例）、上市公司投资金额、公司名称（外键，关联公司基本信息数据表中的公司名称）"
        },
        {
            "role":"system",
            "content":"法律文书信息表：标题、案号、文书类型、原告（外键，关联公司基本信息数据表中的公司名称）、被告（外键，关联公司基本信息数据表中的公司名称）、原告律师、被告律师、案由、审理法条依据、涉案金额、判决结果、胜诉方、文件名"
        },              
        {
            "role": "user",
            "content":content +"这可能是一个多次调用工具才能解决的问题，先将问题分解成多步" 
        },         
        {
            "role": "system",
            "content":"上市公司（母公司）的全称以股份有限公司为后缀，子公司名称以有限公司为后缀"
        },
        {
            "role": "system",
            "content":"当遇到英文的公司名称(如Shanghai Electric Power Co., Ltd.),调用search_company_name_by_info工具,获取公司的中文名称后再进行后续操作。"
        },
        {
            "role": "system",
            "content":"当一个工具没有返回或者没有解决问题的时候，考虑使用其他工具。"
        },
        {
            "role": "system",
            "content":"根据关联上市公司(母公司)具体字段信息查询关联子公司(子公司)信息时,应调用名称为search_company_name_by_sub_info的工具,可以获取所有子公司的列表"
        }
    ]
    response = client.chat.completions.create(
        model="glm-4", # 填写需要调用的模型名称
        messages=messages,
        tools=tools_list,
        tool_choice="auto"
        
    )
   

    return response.choices[0].message

def strat():   
    messages = [          
        {
            "role": "user",
            "content":"清空历史对话信息，开始新对话" 
        },
        
    ]
    extra_body=dict(
        conversation_id="123457"
    )
    response = client.chat.completions.create(
        model="glm-4", # 填写需要调用的模型名称
        messages=messages,
        extra_body=extra_body
    )
   

    return response.choices[0].message

def confirm(content):  
    tools_list=tools() 
    messages = [
        {
            "role": "user",
            "content":content
        },          
        {
            "role": "user",
            "content":"如果你需要调用工具，请直接发出相应的tool_calls请求消息" 
        }
    ]
   
    response = client.chat.completions.create(
        model="glm-4", # 填写需要调用的模型名称
        messages=messages,
        tools=tools_list,
        tool_choice="auto"
        
    )
   

    return response.choices[0].message

def seperate(content):   
    messages = [          
        {
            "role": "user",
            "content":content 
        }
        
    ]   
    response = client.chat.completions.create(
        model="glm-4", # 填写需要调用的模型名称
        messages=messages
       
    )
    return response.choices[0].message.content

def prase_json_from_response(rsp: str):
    pattern = r"```json(.*?)```"
    rsp_json = None
    try:
      match = re.search(pattern, rsp, re.DOTALL)
      if match is not None:
        try:
          rsp_json =  json.loads(match.group(1).strip())
        except:
          pass
      else:
        rsp_json  = json.loads(rsp)
      return rsp_json
    except json.JSONDecodeError as e:
      raise("Json Decode Error: {error}".format(error = e))
QUESTION_CLASS = """
问题：
"{question}"
判断问题的类型。
问题类型：
类型 1: {{
    名称: direct_answer,
    描述: 直接用大模型回答，不需要查询数据表
    例子: 我国法律监督体系的构成、上市公司因违反信息披露规定与因市场操纵受到的处罚有何区别？、上市公司因涉嫌金融诈骗面临的法律风险有哪些？
}}

类型 2: {{
    名称: need_retrieval,
    描述: 需要查询数据表进行回答
    例子: 找下注册号为320512400000458是哪个公司？、劲拓股份拥有哪些子公司？、我想要查询浙江时立态合科技有限公司的组织机构代码是多少？
}}

--------
请按照以下json格式进行输出，可以被Python json.loads函数解析。只给出问题类型，不作解释，不作答：
```json
{{
    "category_name": ""
}}
```
"""

# # print(tool_get_response(""))
# print(tool_get_response("请问批发业注册资本最高的前3家公司的名称以及他们的注册资本（单位为万元）？"))
# print(tool_get_response("找下注册号为320512400000458是哪个公司？"))
# print(tool_get_response("华仁药业股份有限公司控股的子公司，超过50%的有几家？"))
# print(tool_get_response("请核查注册编号为370503228012016的公司的具体名字。"))
# print(tool_get_response("(2021)沪0104民初17782号，您能否协助查询该案件的判决所依据的法律条文？"))

# # print(tool_get_response("找下注册号为320512400000458是哪个公司？"))
# # print(tool_get_response("上市公司因涉嫌金融诈骗面临的法律风险有哪些？"))


