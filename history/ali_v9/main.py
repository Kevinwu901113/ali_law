from classification import *
from sort_question import *
content = "我想要查询浙江时立态合科技有限公司的组织机构代码是多少？"

tool_class = classification_question(content)
print(tool_class)
sort = sort_question(content)
print(sort)