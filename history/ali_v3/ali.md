
问题判断->1。公司	2。子公司	3。法律案件	4。注册相关问题	5。开放问题


1公司相关问题查询->检查问题内是否含有英文公司名称、公司简称->查询公司信息，调用get_company_info

2子公司相关问题查询->检查问题内是否含有英文公司名称、公司简称->查询子公司，调用search_company_name_by_sub_info->批量调取get_sub_company_info

3法律案件相关问题查询->调用get_legal_document->调用search_case_num_by_legal_document

4注册相关问题查询->调用search_company_name_by_register->调用get_company_register

5直接generate_ans（可以考虑联网）
