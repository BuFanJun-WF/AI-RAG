"""
自定义解析器，使用RunnableLambda进行实现
"""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables import RunnableLambda

model = ChatTongyi(model="qwen3-max")
first_prompt = PromptTemplate.from_template(
    "我邻居姓：{lastname}，刚生了{gender}，请起名，仅告知我名字无需其它内容。"
)
second_prompt = PromptTemplate.from_template(
    "姓名：{name}，请帮我解析含义。"
)
# parser = StrOutputParser()
# chain = first_prompt | model | parser | second_prompt | model

# 函数的入参：AIMessage
my_func = RunnableLambda(lambda ai_message: ai_message.content)
chain = first_prompt | model | my_func | second_prompt | model | StrOutputParser()

res = chain.stream({"lastname": "王", "gender": "女"})
for chunk in res:
    print(chunk, end="", flush=True)
