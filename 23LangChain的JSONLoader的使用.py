# 安装jq包，pip install jq
from langchain_community.document_loaders import JSONLoader

# loader = JSONLoader(
#     file_path="./loader_data/stu.json", # 文件路径
#     # jq_schema='.name', # jq schema语法(表示抽取文件中name的内容)
#     jq_schema='.', # jq schema语法(表示抽取文件全部内容)
#     text_content=False, # 抽取的是否为字符串，默认为True
# )

# loader = JSONLoader(
#     file_path="./loader_data/stus.json", # 文件路径
#     # jq_schema='.[].name', # jq schema语法(表示抽取的文件是一个数组，然后我要抽取文件中所有的.name的内容)
#     jq_schema='.[0].name', # jq schema语法(表示抽取的文件是一个数组，然后我要抽取数组中第一个的.name的内容)
#     text_content=False, # 抽取的是否为字符串，默认为True
# )
loader = JSONLoader(
    file_path="./loader_data/stu_json_lines.json", # 文件路径
    jq_schema='.name', # jq schema语法(表示抽取的文件是一个数组，然后我要抽取数组中第一个的.name的内容)
    text_content=False, # 抽取的是否为字符串，默认为True
    json_lines=True, # 是否为json_lines格式（每一行都是一个独立的JSON对象）
)
# 批量加载 .load()-> [Document, Document, ...]
documents = loader.load()
print(documents)
# for doc in documents:
#     print(type(doc),doc)

# 懒加载, .lazy_load() 返回一个迭代器[Document]
# for doc in loader.lazy_load():
#     print(type(doc),doc)

