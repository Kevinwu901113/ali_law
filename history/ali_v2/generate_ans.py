from tools import tools
from get_tool import tool_get_response
from zhipuai import ZhipuAI
from use_tool import tool_use_response

client = ZhipuAI(api_key="33dcd2e786c4567b9f97a3ac9d38dad0.RMsTbtFmlmtq8zFa") # 请填写您自己的APIKey

def generate_ans(content,response_message,rsp):
    tools_list=tools()
    messages = [
        {
            "role": "user",
            "content":content+"你可以继续调用相应工具获取更多信息，你认为信息足够做出推理时请给出回答，你或许需要利用数学知识以及逻辑推理在回答过程中"
        }
    ]
    messages.append(response_message.model_dump())
    messages.append({
        "role": "tool",
        "content": f"{rsp}",
        "tool_call_id": response_message.tool_calls[0].id
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