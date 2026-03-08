import os, json
from collections.abc import Sequence

from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage
from  langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory


# message_to_dict 单个消息对象（BaseMessage类实例）-> 字典
# message_from_dict [字典、字典] —> [BaseMessage类实例、BaseMessage类实例]
# AIMessage、HumanMessage、SystemMessage都是BaseMessage的子类

class FileChatMessageHistory(BaseChatMessageHistory):
    """Chat message history stored in a file."""
    def __init__(self, session_id, storage_path):
        self.session_id = session_id # 会话id
        self.storage_path = storage_path # 不同会话id的存储路径

        # 完整存储路径
        self.file_path = os.path.join(self.storage_path, self.session_id + ".json")

        # 确保文件夹是存在的
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_message(self, messages: Sequence[BaseMessage]) -> None:
        # Sequence序列 类似list、tuple
        all_messages = list(self.messages) # 已有的消息列表
        all_messages.append(messages) # 新的和已有的融合成一个list

        # 将数据同步写入到本地文件中
        # 将类对象写入文件，可以将BaseMessage消息转化成字典，以json字符串的形式写入文件
        new_message= []
        for message in all_messages:
            new_message.append(message_to_dict(message))
        # 将数据写入文件
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_message, f, ensure_ascii=False)

    @property # @property装饰器将messages方法变成成员属性
    def messages(self) -> list[BaseMessage]:
        # 当前文件内：list[字典]
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages = json.load(f) # 返回值就是list[字典]
                return messages_from_dict(messages)
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        # 删除文件
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)


model = ChatTongyi(model="qwen3-max")
# prompt = PromptTemplate.from_template(
#     "你需要根据会话历史回应用户问题，对话历史：{chat_history}，用户提问：{input}，请回答"
# )

prompt = ChatPromptTemplate.from_messages([
    ("system", "你需要根据会话历史回应用户问题，对话历史"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "请回答如下问题：{input}"),

])

str_parser = StrOutputParser()

def print_history(history):
    print("="*20, history.to_string(), "="*20)
    return history

base_chain = prompt | print_history | model | str_parser


def get_history(session_id):
    return FileChatMessageHistory(session_id, "chat_history")


# 创建一个新的链，对原来链增强功能：自动附加历史消息
history_chain = RunnableWithMessageHistory(
    base_chain, # 被增强的原有chain
    get_history, # 通过会话id获取InMemoryChatMessageHistory类对象
    input_messages_key="input", # 表示用户输入在模板中的占位符
    history_messages_key="chat_history", # 表示历史消息在模板中的占位符
)

if __name__ == "__main__":
    # 固定格式，添加LangChain的配置，为当前程序配置所属的session_id
    session_config = {
        "configurable": {
            "session_id": "USER_001"
        }
    }
    # res = history_chain.invoke(
    #     {"input":"小明有2只猫"},
    #     session_config
    # )
    # print("第一次执行：", res)
    #
    # res = history_chain.invoke(
    #     {"input": "小刚有1只狗"},
    #     session_config
    # )
    # print("第二次执行：", res)

    # 从文件中读取内容
    res = history_chain.invoke(
        {"input": "总共有几只动物？"},
        session_config
    )
    print("第三次执行：", res)