#coding=utf-8
from api import *

# content = "我想了解化学原料和化学制品制造业这个行业的企业名录，能否提供注册资本最高的3家公司的名称以及它们的注册资本数额？"

# print(get_company_info("昆山东威科技股份有限公司"))
# print(get_company_register("浙江时立态合科技有限公司"))
# print(get_legal_document("(2020)苏0412民初6970号"))
# print(get_sub_company_info("香料江苏怡达化学股份有限公司"))
# print(search_company_name_by_info("公司简称","劲拓股份"))
# print(search_company_name_by_sub_info("关联上市公司全称","上海锦江国际酒店股份有限公司"))
# print(search_company_name_by_info("所属行业","化学原料和化学制品制造业"))
# print(search_case_num_by_legal_document("被告","新城控股集团股份有限公司"))

# tmp = []
# sub = ["北京联合执信医疗科技有限公司","迪安诊断科技（深圳）有限公司","迪安至善诊断技术（上海）有限公司","广州迪会信医疗器械有限公司","杭州迪安基因工程有限公司","杭州迪安人力资源有限公司","杭州迪安生物技术有限公司","杭州迪安医学检验中心有限公司","杭州迪安智投咨询有限公司","杭州凯莱谱精准医疗检测技术有限公司","杭州万原点私募基金管理有限公司","杭州晓飞检健康科技有限公司","杭州一原创业投资合伙企业（有限合伙）","江苏迪众医疗器械有限公司","内蒙古迪安丰信医疗科技有限责任公司","青岛智颖医疗科技有限公司","陕西凯弘达医疗设备有限公司","上海迪智融资租赁有限公司","上海观合医药科技股份有限公司","新疆元鼎医疗器械有限公司","宣城迪安医疗器械有限公司","云南盛时迪安生物科技有限公司","浙江迪安基因健康创业中心有限公司","浙江迪安健检医疗管理有限公司","浙江迪安鉴定科学研究院","浙江迪安深海冷链物流有限公司","浙江迪安诊断生命科学研究院","浙江迪安证鉴检测技术有限公司"]
# for i in sub:
#     print(i)
#     tmp.append(get_sub_company_info(i))

# print(tmp)

body = {
    "email": "919231551@qq.com",
    "password": "Kevin218"
}
url = f"http://scutgbt.eu.org:40027/api/v1"
headers = {
'Accept': 'application/json',
'Authorization': 'Bearer 1|nO3KAQqGpWRe5hY171ZSxYhiYIwHSi3zOdA1oT5J'
}
rsp = requests.post(url, headers=headers)
print(rsp)
rsp = rsp.text
print(rsp)