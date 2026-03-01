from langchain_community.embeddings import DashScopeEmbeddings
from langchain_ollama import OllamaEmbeddings

# 本地导入包
# from langchain_ollama import OllamaEmbeddings

# 初始化嵌入模型对象，其默认使用模型是：text-embedding-v1
embed = DashScopeEmbeddings()
# embed = OllamaEmbeddings(model="qwen3-embedding")

print(embed.embed_query("你好"))
print(embed.embed_documents(["你好", "世界"]))