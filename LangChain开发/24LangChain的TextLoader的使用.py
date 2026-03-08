from langchain_community.document_loaders import TextLoader
# 递归字符文本分割器，主要用于按自然段落分割大文档
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader(
    file_path="loader_data/测试文本.txt", # 文件路径
    encoding="utf-8",
)
# 批量加载 .load()-> Document
document = loader.load()
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, # 分割的块大小
    chunk_overlap=50, # 块之间的重叠长度
    separators=["\n\n", "\n", "。", "！"], # 分割的分隔符,文本分段的依据
    length_function=len, # 测量文本长度的函数
)

split_docs = splitter.split_documents(document)
print(len(split_docs))
for doc in split_docs:
    print("-"*20)
    print(doc.page_content)
    print("-"*20)
# for doc in documents:
#     print(type(doc),doc)

# 懒加载, .lazy_load() 返回一个迭代器[Document]
# for doc in loader.lazy_load():
#     print(type(doc),doc)

