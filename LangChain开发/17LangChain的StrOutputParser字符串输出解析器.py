"""
StrOutputParser是LangChain内置的简单字符串解析器
·可以将AIMessage解析为简单的字符串，符合了模型invoke方法要求（可传入字符串，不接收AIMessage类型）
·是Runnable接口的子类（可以加入链）
"""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi

model = ChatTongyi(model="qwen3-max")
prompt = PromptTemplate.from_template(
    "我邻居姓：{lastname}，刚生了{gender}，请起名，仅告知我名字无需其它内容。"
)

parser = StrOutputParser()
chain = prompt | model | parser | model

res = chain.invoke({"lastname": "王", "gender": "男"})
print(res.content)
