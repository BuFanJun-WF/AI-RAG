# 安装pypdf包，pip install pypdf
from langchain_community.document_loaders import PyPDFLoader


loader = PyPDFLoader(
    file_path="loader_data/", # 文件路径
    mode="page", # 读取模式，可选page（按页面划分不同的Document）或者single（所有页面直接生成单个Document）
    password="文件密码",
)
# 批量加载 .load()-> [Document, Document, ...]
# documents = loader.load()
# print(documents)
# for doc in documents:
#     print(type(doc),doc)

# 懒加载, .lazy_load() 返回一个迭代器[Document]
for doc in loader.lazy_load():
    print(type(doc),doc)

