from tools import tools
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="83f828eef2455a762a25724c4f8a6df2.3Ae0zjoiEO2KiYED") # 请填写您自己的APIKey

def tool_get_response(content:str):
    tools_list=tools()
    messages = [
        {"role": "assistant","content":"多次结果查询使用多个response返回"},
        {"role": "user","content":content}
    ]
    response = client.chat.completions.create(
        model="glm-4", # 填写需要调用的模型名称
        messages=messages,
        tools=tools_list,
        tool_choice="auto",
    )
    return response.choices

