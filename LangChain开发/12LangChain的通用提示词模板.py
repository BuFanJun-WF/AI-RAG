from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi
# 基于PromptTempLate类可以得到提示词模板，支持基于模板注入变量得到最终提示词。
# zero-shot思想下，可以基于PromptTemplate直接完成。
# few-shot思想下，需要更换为FewShotPromptTemplate


# 构建通用模板
prompt_template = PromptTemplate.from_template(
    "我的邻居姓{lastname}, 刚刚生了一个{gender}，你帮我起个名字，简单回答。"
)

# 调用.format方法，传入参数
# prompt = prompt_template.format(lastname="王", gender="男的")
#
# # print(prompt)
model = Tongyi(model="qwen-max")
# res = model.invoke(input=prompt)
# print(res)

# 构建执行链条
chain = prompt_template | model
res = chain.invoke(input = {"lastname": "王", "gender": "女的"})
print(res)