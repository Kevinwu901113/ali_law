import requests

from key import team_key
from fuzzywuzzy import process
headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {team_key}'
        }
domain = "comm.chatglm.cn"
def api(data,type):
    url=f"https://{domain}/law_api/s1_b/{type}"
    rsp = requests.post(url, json=data, headers=headers)
    
    return rsp.json()

def match1(key,key_list):
        ans=[]
        for k in key:
              ans.append(process.extractOne(k, key_list))
        
        return ans