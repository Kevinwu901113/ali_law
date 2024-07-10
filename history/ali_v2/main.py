from tools import tools
import json
from get_tool import tool_get_response
from use_tool import tool_use_response
from generate_ans import generate_ans
#获取工具函数
content = "请问凯盛新材这家上市公司旗下拥有哪些子公司，能否提供这些子公司的具体名称？"
response_messge = tool_get_response(content)   #response.choices[0].message
print(response_messge)
response_type = response_messge.content
if response_type==None:
    #调用函数

    answer = tool_use_response(response_messge)     #rsp.json()
    print(answer)
    f=0
    while answer==[] and f<=10:
        response_messge = tool_get_response(content)   #response.choices[0].message
        print(response_messge)
        answer = tool_use_response(response_messge)
        f=f+1        
    #生成答案
    ans=generate_ans(content,response_messge,answer)
    print(ans)

   

