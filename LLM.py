from zhipuai import ZhipuAI
import json
import re
import logging
import os
from key import zhipu

# 配置日志记录
logging.basicConfig(level=logging.INFO)

# 从环境变量中获取API密钥
API_KEY = zhipu
client = ZhipuAI(api_key=API_KEY)

def reply(content):   
    messages = [          
        {
            "role": "user",
            "content": content 
        }
    ]   
    try:
        response = client.chat.completions.create(
            model="glm-4", 
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error during API call: {e}")
        return None

def parse_json_from_response(rsp: str):
    pattern = r"```json(.*?)```"
    try:
        match = re.search(pattern, rsp, re.DOTALL)
        if match:
            try:
                rsp_json = json.loads(match.group(1).strip())
                return rsp_json
            except json.JSONDecodeError as e:
                logging.error(f"JSON decode error from matched content: {e}")
                logging.debug(f"Matched content: {match.group(1).strip()}")
                return None
        else:
            try:
                rsp_json = json.loads(rsp)
                return rsp_json
            except json.JSONDecodeError as e:
                logging.error(f"JSON decode error from full response: {e}")
                logging.debug(f"Full response: {rsp}")
                return None
    except Exception as e:
        logging.error(f"Error parsing response: {e}")
        return None
