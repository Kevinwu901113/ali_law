#coding=utf-8
from tools import tools
import json
from get_tool import tool_get_response
from use_tool import tool_use_response
from generate_ans import generate_ans
#获取工具函数
content = "我想了解化学原料和化学制品制造业这个行业的企业名录，能否提供注册资本最高的3家公司的名称以及它们的注册资本数额？"
response_messge = tool_get_response(content)   #response.choices[0].message
print(response_messge)
if response_messge.content!=None:
    response_messge = tool_get_response(content)   #response.choices[0].message
print(response_messge)
response_type = response_messge.content
if response_type==None:
    #调用函数

    answer = tool_use_response(response_messge)     #rsp.json()
    print(answer)
    

       
          
    #生成答案
    ans=generate_ans(content,response_messge,answer)
    print(ans)

   

