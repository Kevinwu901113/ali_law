#coding=utf-8
from tools import tools
import json
from get_tool import tool_get_response,strat,confirm
from use_tool import tool_use_response
from generate_ans import generate_ans
#获取工具函数
content = "请查询景津装备股份有限公司所属的行业类别，并告知在该行业分类下共有多少家公司？"
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

   

