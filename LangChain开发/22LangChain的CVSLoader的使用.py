from langchain_community.document_loaders import CSVLoader
loader = CSVLoader(
    file_path="loader_data/stu.csv",
    csv_args={
        "delimiter": ",", # 指定分隔符
        "quotechar": '"', # 指定带有分隔符文本的引号包围是单引号还是双引号
        "fieldnames": ["id", "name", "age", "sex", "score"], # 如果数据原本有表头，就没有必要使用这个字段，没有表头则可以自行自定表头
    },
    encoding="utf-8",
)

# 批量加载 .load()-> [Document, Document, ...]
# documents = loader.load()
# print(documents)
# for doc in documents:
#     print(type(doc),doc)

# 懒加载, .lazy_load() 返回一个迭代器[Document]
for doc in loader.lazy_load():
    print(type(doc),doc)

