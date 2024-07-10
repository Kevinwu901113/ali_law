from tools.tools import tools
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="33dcd2e786c4567b9f97a3ac9d38dad0.RMsTbtFmlmtq8zFa") # 请填写您自己的APIKey

def generate_ans(content,rsp):
    tools_list=tools()
    messages = [
        {
            "role": "user",
            "content":content 
        }
    ]
    # messages.append(response_choices[0].message.model_dump())
    messages.append({
        "role": "tool",
        "content": f"{rsp}",
        # "tool_call_id": response_choices[0].message.tool_calls[0].id
    })
    ans = (client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=messages,
        tools=tools_list,
    ).choices[0].message)
    return ans