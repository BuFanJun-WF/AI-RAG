"""
基于Streamlit完成WEB网页上传服务

pip install streamlit

运行命令：streamlit run .\app_file_uploader.py
Streamlit：当WEB页面元素发生变化，则代码重新执行一遍
"""

import streamlit as st

# 添加网页标题
st.title("知识库更新服务")

# 上传文件上传方法
uploader_file = st.file_uploader(
    "请上传txt文件",
    type=["txt"],
    accept_multiple_files=False, # False表示仅接受一个文件的上传
)

if uploader_file is not None:
    # 提取文件的信息
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024 # KB

    st.subheader(f"文件信息 文件名：{file_name}")
    st.write(f"格式：{file_type} | 大小：{file_size:.2f} KB")

    # 获取文件中的内容
    text = uploader_file.getvalue().decode("utf-8")

    # 开发的时候写一下数据看看
    # st.write(text)

