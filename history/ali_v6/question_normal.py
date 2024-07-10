from tools.normal_tool import tools
from zhipuai import ZhipuAI
import json
import requests

client = ZhipuAI(api_key="33dcd2e786c4567b9f97a3ac9d38dad0.RMsTbtFmlmtq8zFa") # 请填写您自己的APIKey
domain = "comm.chatglm.cn"

def name_reverse(content):
    tools_list=tools()
    messages = [        
        {
            "role": "user",
            "content":content 
        },
        {
            "role": "system",
            "content":"你是一个人工助手，你需要判断这是一个公司名称、英文名称或者是公司简称"
        },
    ]
    response = client.chat.completions.create(
        model="glm-4", # 填写需要调用的模型名称
        messages=messages,
        tools=tools_list,
        tool_choice="auto",
    )
    return response.choices[0].message

def name_normal(response_message):
    response_json = response_message.tool_calls[0].function.arguments    # 解析response中返回的JSON字符串
    response_dict = json.loads(response_json)
    table = {ord(f):ord(t) for f,t in zip(
     u'，。！？【】（）％＃＠＆１２３４５６７８９０',
     u',.!?[]()%#@&1234567890')}

    key = response_dict["key"]
    value = response_dict["value"]
    value=value.translate(table)
    response_message = name_reverse(value)

    print(response_message)

    if(response_message.tool_calls[0].function.name=="公司简称" or response_message.tool_calls[0].function.name=="英文名称"):
        response_json = response_message.tool_calls[0].function.arguments    # 解析新response中返回的JSON字符串
        response_dict = json.loads(response_json)

        key = response_dict["key"]
        value = response_dict["value"]
        # value=value.translate(table)
        data = {
            "key": key,
            "value": value
        }

        url = f"https://{domain}/law_api/search_company_name_by_info"
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer DD588018ADCC373065941C2E935D04595E3C9CA65F8873A3'
        }
        
        rsp = requests.post(url, json=data, headers=headers)
        
        return rsp.json()

    return {"公司名称":value}

def law_normal(response_message):
    response_json = response_message.tool_calls[0].function.arguments    # 解析response中返回的JSON字符串
    response_dict = json.loads(response_json)
    table = {ord(f):ord(t) for f,t in zip(
     u'，。！？【】（）％＃＠＆１２３４５６７８９０',
     u',.!?[]()%#@&1234567890')}
    key = response_dict["key"]
    value = response_dict["value"]
    value=value.translate(table)
    data = {
        "key": key,
        "value": value
    }
    url = f"https://{domain}/law_api/search_case_num_by_legal_document"
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer DD588018ADCC373065941C2E935D04595E3C9CA65F8873A3'
    }
    rsp = requests.post(url, json=data, headers=headers)
    return rsp.json()