#coding=utf-8
from tools import tools
import json
from get_tool import tool_get_response,strat,confirm,seperate,prase_json_from_response,QUESTION_CLASS
from use_tool import tool_use_response
from generate_ans import generate_ans
#获取工具函数
#content = "请问批发业注册资本最高的前3家公司的名称以及他们的注册资本（单位为万元）？"
with open('question(1).json', 'r', encoding='utf-8') as f:
    lines = f.readlines()
data = [json.loads(line.strip()) for line in lines]
ff=0
for q in data:
    try:
        ans = q['answer']
        continue
    except:
        question = q['question']
        print(q['id'],question)
        try:
            strat()
            prompt=QUESTION_CLASS.format(question=question)
            
            response = prase_json_from_response(seperate(prompt))
            
            if response["category_name"] == "direct_answer":
                answer = seperate(question)
            else:
                response_messge = tool_get_response(question)   #response.choices[0].message
                print(response_messge)
                if response_messge.tool_calls==None:
                    response_messge=confirm(question)   #response.choices[0].message
                    print(response_messge)
                if response_messge.tool_calls!=None:
                    #调用函数
                    answer = tool_use_response(response_messge)     #rsp.json()               
                #生成答案
                answer=generate_ans(question,response_messge,answer).content
                
        except:
            answer = q['question']
        q['answer'] = answer
        print(q['answer'])
        ff=ff+1
        if ff%10==0:
            with open(f"submission{ff}.json", "w", encoding="utf-8") as f:
                for item in data:
                    f.write(json.dumps(item, ensure_ascii=False) + "\n")


with open("submission.json", "w", encoding="utf-8") as f:
    for item in data:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")


       
          
    

   

