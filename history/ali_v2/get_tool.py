from tools import tools
from zhipuai import ZhipuAI
import json

client = ZhipuAI(api_key="33dcd2e786c4567b9f97a3ac9d38dad0.RMsTbtFmlmtq8zFa") # 请填写您自己的APIKey

def tool_get_response(content:str):
    tools_list=tools()
    messages = [
        {
            "role": "system",
            "content":"你是一个公司信息和法律信息查询分析助手，你有设定好的多个数据表查询工具，你需要提取用户问题中的关键信息和其所属类别，根据关键信息所属类别和需要获取的信息调用相应的工具查询数据表做出回答。"
        },
        {
            "role": "system",
            "content":"你的查询流程应该如下，先判断公司名称是否已经转换为全称？你需要将公司简称以及英文名称转换成公司全称。"
        },
        {
            "role": "system",
            "content":"对于子公司的查询，先确认公司名称是否已经转换为中文全称后，再进行查询工作。"
        },
        {
            "role": "system",
            "content":"当一个工具没有返回或者没有解决问题的时候，考虑使用其他工具。"
        },
        {
            "role": "user",
            "content":content +"这可能是一个多次调用工具才能解决的问题，先将问题分解成多步" 
        }
    ]
    response = client.chat.completions.create(
        model="glm-4", # 填写需要调用的模型名称
        messages=messages,
        tools=tools_list,
        tool_choice="auto",
    )
    return response.choices[0].message



# # print(tool_get_response(""))
# print(tool_get_response("请问批发业注册资本最高的前3家公司的名称以及他们的注册资本（单位为万元）？"))
# print(tool_get_response("找下注册号为320512400000458是哪个公司？"))
# print(tool_get_response("华仁药业股份有限公司控股的子公司，超过50%的有几家？"))
# print(tool_get_response("请核查注册编号为370503228012016的公司的具体名字。"))
# print(tool_get_response("(2021)沪0104民初17782号，您能否协助查询该案件的判决所依据的法律条文？"))

# # print(tool_get_response("找下注册号为320512400000458是哪个公司？"))
# # print(tool_get_response("上市公司因涉嫌金融诈骗面临的法律风险有哪些？"))


