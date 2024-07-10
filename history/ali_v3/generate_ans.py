from tools import tools
from get_tool import tool_get_response
from zhipuai import ZhipuAI
from use_tool import tool_use_response

client = ZhipuAI(api_key="33dcd2e786c4567b9f97a3ac9d38dad0.RMsTbtFmlmtq8zFa") # 请填写您自己的APIKey

def generate_ans(content,response_message,rsp):
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
            "role": "system",
            "content":"当遇到英文的公司名称(如Shanghai Electric Power Co., Ltd.),调用search_company_name_by_info工具,获取公司的中文名称后再进行后续操作。"
        },
        {
            "role": "system",
            "content":"当一个工具没有返回或者没有解决问题的时候，考虑使用其他工具。"
        },
        {
            "role": "system",
            "content":"根据关联上市公司(母公司)具体字段信息查询关联子公司(子公司)信息时,应调用名称为search_company_name_by_sub_info的工具"
        },
        # {
        #     "role": "system",
        #     "content":"想得到母公司（上市公司）对子公司具体的参股比例信息,应调用名称为search_company_name_by_sub_info的工具,将已知的所有子公司名称分别传入工具中得到上市公司参股比例"
        # },
        {
            "role": "user",
            "content":content+"这可能是一个多次调用工具才能解决的问题，你可以将问题分解成多步，可以继续调用相应工具获取更多信息，你认为信息足够做出推理时请给出回答，你或许需要利用数学知识以及逻辑推理在回答过程中"
        }
    ]
    messages.append(response_message.model_dump())
    messages.append({
        "role": "tool",
        "content": f"{rsp}",
        "tool_call_id": response_message.tool_calls[0].id
    })
    messages.append({
        "role": "system",
        "content": "想得到母公司（上市公司）对子公司具体的参股比例信息,应调用名称为get_all_connect_company的工具,将已知的所有子公司名称列表传入工具中得到上市公司参股比例"
    })
    ans = (client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=messages,
        tools=tools_list,
    ).choices[0].message)
    response_type = ans.content    # 解析response中返回的JSON字符串
    f=0
    while response_type ==None:
        answer = tool_use_response(ans)     #rsp.json()
        print(answer)        
        messages.append(ans.model_dump())
        messages.append({
            "role": "user",
            "content": content+"你可以继续调用相应工具获取更多信息，你认为信息足够做出推理时请给出回答，或许需要利用数学知识以及逻辑推理在回答过程中"
        })
        messages.append({
            "role": "tool",
            "content": f"{answer}",
            "tool_call_id": ans.tool_calls[0].id
        })
        messages.append({
        "role": "system",
        "content": "想得到母公司（上市公司）对子公司具体的参股比例信息,应调用名称为get_all_connect_company的工具,将已知的所有子公司名称列表传入工具中得到上市公司参股比例"
        })
        ans = (client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=messages,
        tools=tools_list,
        ).choices[0].message)
        print(ans)
        response_type = ans.content
        if response_type!= None and f<2:
            messages.append({
            "role": "user",
            "content": content+"在这个问题下，现在必须继续调用至少一次工具查询数据表获取新信息验证并完善你的回答"
            })
            
            ans = (client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=messages,
            tools=tools_list,
            ).choices[0].message)
            print(ans)
            response_type = ans.content   
            if response_type!=None:
                messages.append({
                "role": "user",
                "content": "请再进行一次工具调用"
                
                })
                ans = (client.chat.completions.create(
                model="glm-4",  # 填写需要调用的模型名称
                messages=messages,
                tools=tools_list,
                ).choices[0].message)
                response_type = ans.content
            f=f+1


    return ans