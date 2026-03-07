"""
JsonOutputParser
主要功能
结构化输出解析
    将大模型的输出从 JSON 格式字符串解析为 Python 字典对象
    确保模型返回符合预期格式的 JSON 数据
数据类型转换
    自动将 JSON 字符串转换为 Python 原生数据结构（dict、list 等）
    方便后续代码直接使用和处理
可链式调用
    实现了 Runnable 接口，可以加入 Chain 中
    支持与其他组件组合使用
"""
from langchain_core.output_parsers import StrOutputParser,JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi

model = ChatTongyi(model="qwen3-max")
# first_prompt = PromptTemplate.from_template(
#     "我邻居姓：{lastname}，刚生了{gender}，请起名，仅告知我名字无需其它内容。"
# )
first_prompt = PromptTemplate.from_template(
    "我邻居姓：{lastname}，刚生了{gender}，请起名，并封装成JSON格式返回给我。要求key是name，value是你起的名字，"
    "请严格遵守格式要求"
)

second_prompt = PromptTemplate.from_template(
    "姓名：{name}，请帮我解析含义。"
)

str_parser = StrOutputParser()
json_parser = JsonOutputParser()
# chain = first_prompt | model | str_parser | second_prompt | model
chain = first_prompt | model | json_parser | second_prompt | model |str_parser
res = chain.stream({"lastname": "王", "gender": "男"})
for chunk in res:
    print(chunk, end="", flush=True)
