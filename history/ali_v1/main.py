from tools import tools
from get_tool import tool_get_response
from use_tool import tool_use_response
from generate_ans import generate_ans
#获取工具函数
content = "我想了解化学原料和化学制品制造业这个行业的公司有哪些，请列出注册资本最大的3家头部公司，并给出他们的具体注册资本数额"
print("正在获取工具函数")
response_choices = tool_get_response(content)   #response.choices[0].message
print(tool_get_response(content))
print("获取工具函数成功")
#调用函数
print("正在调用函数")
answer = tool_use_response(response_choices)     #rsp.json()
print(tool_use_response(response_choices))
print("调用函数成功")
# #生成答案
# print("正在生成答案")
# print(generate_ans(content,response_choices,answer))
# print("生成答案成功")