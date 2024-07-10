from sort_question import sort_question as sq
from question_normal import name_normal as nn, law_normal as ln
from get_info import get_company_info, search_sub_info, get_sub_info, search_register_info, get_register_info,law_info
from generate_ans import generate_ans
# content = "我想了解英文名称为Tianyang New Materials (Shanghai) Technology Co., Ltd.的上市公司旗下拥有哪些子公司？这些子公司的参股比例分别是多少？"
content = "我想要查询浙江时立态合科技有限公司的组织机构代码是多少？"
#目前无法解决的问题包含：
#   多轮查询问题
#   查询子公司数量（当子公司数量过多，会导致生成答案时文本太长）->会将所有子公司信息查询出来一起给到ans_generate

#1.问题分类
question_type = sq(content)
print(question_type)


#2.问题标准化
if(question_type.tool_calls[0].function.name=="company_question" or question_type.tool_calls[0].function.name=="sub_company_question"):
    normal_question = nn(question_type)
    print(normal_question)
elif(question_type.tool_calls[0].function.name=="law_question"):
    normal_question = ln(question_type)
    print(normal_question)

#3.处理问题
ans_info = {}
if(question_type.tool_calls[0].function.name=="company_question"):
    company_info = get_company_info(normal_question)
    ans_info = company_info
elif(question_type.tool_calls[0].function.name=="sub_company_question"):
    sub_info = search_sub_info(normal_question)
    print(sub_info)
    for sub in range(0,len(sub_info)):
        ans_info[sub] = get_sub_info(sub_info[sub])
        print(ans_info)
elif(question_type.tool_calls[0].function.name=="register_question"):
    register_info = get_register_info(question_type)
    print(register_info)
    ans_info = register_info
elif(question_type.tool_calls[0].function.name=="law_question"):
    law_info = law_info(normal_question)
    ans_info[0] = law_info
    print(ans_info)
elif(question_type.tool_calls[0].function.name=="open_question"):
    pass
else:
    pass

#4.答案生成
ans=generate_ans(content,ans_info)
print(ans)