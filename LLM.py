from zhipuai import ZhipuAI
from key import zhipu
import json
import re
client = ZhipuAI(api_key=zhipu)
def reply(content):   
    messages = [          
        {
            "role": "user",
            "content":content 
        }
        
    ]   
    response = client.chat.completions.create(
        model="glm-4", 
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