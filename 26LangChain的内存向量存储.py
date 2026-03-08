from langchain_core.vectorstores import InMemoryVectorStore
# 导入文本嵌入式模型
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path="./loader_data/info.csv",
    encoding="utf-8",
    source_column="source", # 指定本条数据的来源列
)

documents = loader.load()
# print(documents[0])

vector_store = InMemoryVectorStore (
    # 表明使用的文本嵌入式模型
    embedding = DashScopeEmbeddings()
)

# 向量存储的新增、删除、检索
vector_store.add_documents(
    documents= documents, # 被添加的文档，类型 list[Document]
    ids= ["id" + str(i) for i in range(1, len(documents) + 1)], # 文档的id，类型 list[str]
)

vector_store.delete(ids=["id1", "id2"])

# 检索，返回类型list[Document]
result = vector_store.similarity_search(
    query="Python",
    k=2, # 返回的文档数量
 )
print(result)