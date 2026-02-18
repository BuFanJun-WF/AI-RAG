from langchain_community.llms.tongyi import Tongyi

# 获取模型变量
model = Tongyi(model="qwen-max")

# 设置问题
res = model.invoke(input="你是谁？你能做什么？")

# 打印响应
print(res)
