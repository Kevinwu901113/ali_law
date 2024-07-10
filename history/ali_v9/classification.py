from tools import *
from zhipuai import ZhipuAI
import json

client = ZhipuAI(api_key="33dcd2e786c4567b9f97a3ac9d38dad0.RMsTbtFmlmtq8zFa") # 请填写您自己的APIKey


def classification_question(content:str):
    tools_list=classification_tools()
    messages = [        
        {
            "role": "user",
            "content":content 
        },
        {
            "role": "system",
            "content":"你是一个法律解答助手，你的任务是分析问题，判断问题是公司类型问题（包含公司信息问题、公司注册信息问题、子公司相关问题）、法律相关问题或者是开放性问题"
        },
    ]
    response = client.chat.completions.create(
        model="glm-4", # 填写需要调用的模型名称
        messages=messages,
        tools=tools_list,
        tool_choice="auto",
    )
   

    return response.choices[0].message