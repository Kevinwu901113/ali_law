#coding=utf-8
from tools import tools
import json
from get_tool import tool_get_response,strat,confirm
from use_tool import tool_use_response
from generate_ans import generate_ans
#获取工具函数
content = "请问Beijing Tricolor Technology Co., Ltd.拥有哪些子公司？这些子公司的参股比例分别是多少？"
strat()
response_messge = tool_get_response(content)   #response.choices[0].message
print(response_messge)
if response_messge.tool_calls==None:
    response_messge=confirm(content)   #response.choices[0].message
    print(response_messge)
if response_messge.tool_calls!=None:
    #调用函数

    answer = tool_use_response(response_messge)     #rsp.json()
    print(answer)
    

       
          
    #生成答案
    ans=generate_ans(content,response_messge,answer)
    print(ans)

   

