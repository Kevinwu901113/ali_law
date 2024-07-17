from zhipuai import ZhipuAI
from key import zhipu
import json
import re
import random
client = ZhipuAI(api_key=zhipu)
def reply(content):   
    messages = [          
        {
            "role": "user",
            "content":content 
        }
        
    ]
    extra_body=dict(
        conversation_id=str(random.randint(100000, 999999))
    )   
    response = client.chat.completions.create(
        model="glm-4", 
        messages=messages,
        extra_body=extra_body
       
    )
    return response.choices[0].message.content

def prase_json_from_response1(rsp: str):
    # 正则表达式，匹配```json ... ```
    pattern = r"```json(.*?)```"
    try:
        # 尝试匹配JSON数据
        match = re.search(pattern, rsp, re.DOTALL)
        if match:
            # 如果匹配成功，尝试解析JSON
            json_text = match.group(1).strip()
            if json_text:
                try:
                    return json.loads(json_text)
                except json.JSONDecodeError as e:
                    raise ValueError("JSON Decode Error: {}".format(e)) from None
            else:
                raise ValueError("Matched JSON text is empty.")
        else:
            # 如果没有匹配，尝试直接解析整个字符串
            return json.loads(rsp)
    except json.JSONDecodeError as e:
        # 如果解析整个字符串失败，抛出异常
        raise ValueError("JSON Decode Error: {}".format(e)) from None
    
def prase_json_from_response(rsp: str):
    pattern = r"```json(.*?)```"
    try:
        match = re.search(pattern, rsp, re.DOTALL)
        if match:
            json_text = match.group(1).strip()
            if json_text:
                try:
                    print("Trying to parse JSON:", json_text)  # 打印将要解析的 JSON
                    return json.loads(json_text)
                except json.JSONDecodeError as e:
                    # 提供失败时尝试解析的 JSON 文本
                    raise ValueError(f"JSON Decode Error: {e}\nFailed JSON: {json_text}") from None
            else:
                # 更明确的错误消息
                raise ValueError("Matched JSON text is empty.")
        else:
            print("No match found, trying to parse full response:", rsp)  # 打印完整响应
            return json.loads(rsp)
    except json.JSONDecodeError as e:
        # 提供解析失败的完整响应
        raise ValueError(f"JSON Decode Error: {e}\nComplete Response: {rsp}") from None
