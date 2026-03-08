"""
提示词：用户的提问 + 向量库中的检索到的参考资料
"""
from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore

model = ChatTongyi(model="qwen3-max")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个助手，请根据提供的参考资料回答用户的问题。参考资料：{context}。"),
        ("human", "{question}"),
    ]
)

def print_prompt(prompt):
    print(prompt.to_string())
    print("-"*20)
    return prompt

vector_store = InMemoryVectorStore(
    embedding=DashScopeEmbeddings(model="text-embedding-v4")
)

# 准备向量库的资料数据
# 传入一个列表list[str]
vector_store.add_texts(["减肥就是要少吃多练", "要减肥，要吃健康食物", "要减肥，要运动","游泳对减肥效果很好，很适合大体重人员"])

query = "如何减肥"

# langchain中向量存储对象，as_retriever()方法，将向量存储对象转换为检索对象,返回一个Runnable接口的子类实例对象
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# 错误的写法
# chain = retriever | prompt | model | StrOutputParser()

"""
retriever:
    - 输入：用户的提问       str
    - 输出：向量库的检索结果  list[document]
prompt：
    - 输入：用户的提问+向量库的检索结果  dict
    - 输出：完整的提示词              PromptValue
    
RunnablePassthrough() 类似占位符的作用，可以拿到invoke的中的输入,也就是输入的会有两个地方都能拿到，一个是RunnablePassthrough()，一个是retriever
"""

def format_func(documents: list[Document]):
    if not documents:
        return "无相关参考资料"

    reference_text = "["
    for item in documents:
        print(item.page_content)
        reference_text += item.page_content
    reference_text += "]"

    return reference_text

chain = (
    {"question": RunnablePassthrough(), "context": retriever | format_func } | prompt | print_prompt | model | StrOutputParser()
)

res = chain.invoke(query)
print(res)