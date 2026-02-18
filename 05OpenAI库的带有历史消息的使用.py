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
        {"role": "system", "content": "你是一个AI助理，使用最简洁的话语进行回答"},
        # 用户的提问
        {"role": "user", "content": "小明有两条宠物狗。"},
        # 设定模型的回答，由用户设定
        {"role": "assistant", "content": "好的"},
        # 用户的提问
        {"role": "user", "content": "小红有两条宠物狗。"},
        # 设定模型的回答，由用户设定
        {"role": "assistant", "content": "好的"},
        {"role": "user", "content": "现在总共有多少条宠物？"},
    ],
    # 开启流式输出的功能
    stream=True,
)

# 3.处理结果
# 使用循环进行遍历循环输出
# response.choices[0].message.content
for chunk in response:
    print(
        chunk.choices[0].delta.content,
        end=" ", # 表示用空格做结束
        flush=True # 表示立刻刷新
    )