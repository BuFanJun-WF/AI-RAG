"""
PromptTemplate：通用提示词模板，支持动态注入信息。
FewShotPromptTempLate：支持基于模板注入任意数量的示例信息。
ChatPromptTemplate：支持注入任意数量的历史会话信息。
"""
from langchain_core.prompts import ChatPromptTemplate
# MessagesPlaceholder作为占位，提供history作为占位的key
from langchain_core.prompts import MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi

# from_messages方法，从列表中获取多轮次会话作为聊天的基础模板
chat_prompt_template = ChatPromptTemplate.from_messages([
    ("system","你是一个风景诗人，可以作诗。"),
    MessagesPlaceholder(variable_name="history"),
    ("human","请再来一首诗"),
])

history_data = [
    ("human","你来写一首唐诗"),
    ("ai", "床前明月光，疑似地上霜。举头望明月，低头思故乡。")
]

prompt_text = chat_prompt_template.invoke({"history": history_data}).to_string()

# print(prompt_text)

model = ChatTongyi(model="qwen3-max")
res = model.invoke(input=prompt_text)
print(res.content)
