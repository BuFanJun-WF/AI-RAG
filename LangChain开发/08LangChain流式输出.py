# from langchain_ollama import OllamaLLM
#
# # 获取模型变量
# model = OllamaLLM(model="my-glm")

from langchain_community.llms.tongyi import Tongyi

# 获取模型变量
model = Tongyi(model="qwen-max")

# 设置问题，进行流式输出，替换invoke方法
res = model.stream(input="你是谁？你能做什么？")

# 打印响应
for chunk in res:
    print(chunk, end="", flush=True)
