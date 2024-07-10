from tools.question_tool import tools
from zhipuai import ZhipuAI
import json

client = ZhipuAI(api_key="33dcd2e786c4567b9f97a3ac9d38dad0.RMsTbtFmlmtq8zFa") # 请填写您自己的APIKey


def sort_question(content:str):
    tools_list=tools()
    messages = [        
        {
            "role": "user",
            "content":content 
        },
        {
            "role": "system",
            "content":"你是一个法律解答助手，你的任务是分析问题，判断问题是公司问题（询问公司相关信息）、公司注册问题、子公司问题（任何有关子公司的问题）、法律案件问题或是开放性常识问题。"
        },
    ]
    response = client.chat.completions.create(
        model="glm-4", # 填写需要调用的模型名称
        messages=messages,
        tools=tools_list,
        tool_choice="auto",
    )
   

    return response.choices[0].message