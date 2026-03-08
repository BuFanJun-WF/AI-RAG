# from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
#
# model = ChatTongyi(model="qwen3-max")

from langchain_ollama.chat_models import ChatOllama

model = ChatOllama(model="qwen3:4b")
# 准备消息列表
messages = [
    # 表示角色内容
    SystemMessage(content="你是一个边塞诗人"),
    # AIMessage表示给大模型一个实例
    # AIMessage(content="你好，我是编程专家，并且话很多，你要问什么？"),
    # 表示问题
    HumanMessage(content="写一首唐诗"),
]

res = model.stream(input = messages)

# 聊天模型需要通过content获取聊天的内容
for chunk in res:
    print(chunk.content, end="", flush=True)