import requests
headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer DD588018ADCC373065941C2E935D04595E3C9CA65F8873A3'
        }
domain = "comm.chatglm.cn"
def api(data,type):
    url=f"https://{domain}/law_api/{type}"
    rsp = requests.post(url, json=data, headers=headers)
    return rsp.json()