#coding=utf-8
from tools import tools
import json
from analysis_question import tool_get_response
# from get_tool import tool_get_response
from use_tool import tool_use_response
from generate_ans import generate_ans
#获取工具函数
content = "如何防止财务造假？"
response_messge = tool_get_response(content)   #response.choices[0].message
print(response_messge)
# response_type = response_messge.content
# if response_type==None:
#     #调用函数

#     answer = tool_use_response(response_messge)     #rsp.json()
#     print(answer)
    

       
          
#     #生成答案
#     ans=generate_ans(content,response_messge,answer)
#     print(ans)

   

