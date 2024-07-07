from zhipuai import ZhipuAI
import json
import re
client = ZhipuAI(api_key="33dcd2e786c4567b9f97a3ac9d38dad0.RMsTbtFmlmtq8zFa")
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