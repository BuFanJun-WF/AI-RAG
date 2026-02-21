from langchain_ollama import OllamaLLM

# 获取模型变量
model = OllamaLLM(model="my-glm")

# 设置问题
res = model.invoke(input="你是谁？你能做什么？")

# 打印响应
print(res)
