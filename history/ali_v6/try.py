import requests
domain = "comm.chatglm.cn"

data = {
"key": "英文名称",
"value": "Tianyang New Materials (Shanghai) Technology Co., Ltd."
}
url = f"https://comm.chatglm.cn/law_api/search_company_name_by_info"
headers = {
'Content-Type': 'application/json',
'Authorization': 'Bearer DD588018ADCC373065941C2E935D04595E3C9CA65F8873A3'
}
rsp = requests.post(url, json=data, headers=headers)
print(rsp.json())