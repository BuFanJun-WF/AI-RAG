from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_community.llms.tongyi import Tongyi
# 基于PromptTempLate类可以得到提示词模板，支持基于模板注入变量得到最终提示词。
# zero-shot思想下，可以基于PromptTemplate直接完成。
# few-shot思想下，需要更换为FewShotPromptTemplate


# 构建通用模板
prompt_template = PromptTemplate.from_template(
    "单词：{word}，反义词：{antonym}"
)
example_data = [
    {"word": "中国", "antonym": "外国"},
    {"word": "男", "antonym": "女"},
]

few_shot_prompt = FewShotPromptTemplate(
    # 示例数据
    examples=example_data,
    # 提示模板
    example_prompt=prompt_template,
    # 提示词模板
    prefix="给出指定词的反义词，有如下实例",
    # 后面的问题
    suffix="基于实例告诉我，{input_word}的反义词是？",
    # 输入变量，问题的输入变量
    input_variables=["input_word"],
)

# 调用.format方法，传入参数
prompt_text = few_shot_prompt.invoke(input={"input_word":"左"}).to_string()
print(prompt_text)
model = Tongyi(model="qwen-max")
# res = model.invoke(input=prompt_text)
# print(res)

# 构建执行链条
chain = few_shot_prompt | model
res = chain.invoke(input = {"input_word":"左"})
print(res)