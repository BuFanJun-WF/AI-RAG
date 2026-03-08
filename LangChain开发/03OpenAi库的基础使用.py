from openai import OpenAI
import os
# 1.获取client对象，OpenAI类对象
client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
# 2.调用模型
response = client.chat.completions.create(
    model="qwen3-max",
    messages=[
        # 设定模型的行为和规则
        {"role": "system", "content": "你是一个python编程专家，并且不说废话简单回答。"},
        # 设定模型的回答，由用户设定
        {"role": "assistant", "content": "你好，我是编程专家，并且话不多，你要问什么？"},
        # 用户的提问
        {"role": "user", "content": "请写一个python程序，将一个列表中的所有数字乘以2。"},
    ]
)

# 3.处理结果
print(response.choices[0].message.content)