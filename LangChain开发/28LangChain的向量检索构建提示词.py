"""
提示词：用户的提问 + 向量库中的检索到的参考资料
"""
from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore

model = ChatTongyi(model="qwen3-max")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个助手，请根据提供的参考资料回答用户的问题。参考资料：{context}。"),
        ("human", "{question}"),
    ]
)

vector_store = InMemoryVectorStore(
    embedding=DashScopeEmbeddings(model="text-embedding-v4")
)

# 准备向量库的资料数据
# 传入一个列表list[str]
vector_store.add_texts(["减肥就是要少吃多练", "要减肥，要吃健康食物", "要减肥，要运动","游泳对减肥效果很好，很适合大体重人员"])

query = "如何减肥"
# 检索向量库,进行匹配
result = vector_store.similarity_search(query, k=2)

reference_text = "["
for item in result:
    print(item.page_content)
    reference_text += item.page_content
reference_text += "]"

print(reference_text)

def print_prompt(prompt):
    print(prompt.to_string())
    print("-"*20)
    return prompt

chain = prompt | print_prompt | model | StrOutputParser()

res = chain.invoke({"question": query, "context": reference_text})
print(res)