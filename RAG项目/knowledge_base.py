"""
搭建知识库入库流程，知识库服务，实现三个函数，检查md5，保存md5， 获取md5字符串
"""
from datetime import datetime
import hashlib
import os

from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config_data as config
# 检查传入的md5字符串是否已经被处理过了
# return False(md5未处理过)  True(已经处理过，已有记录）
def check_md5(md5_str: str):
    """
    检查传入的md5字符串是否已经被处理过了
    return False(md5未处理过)  True(已经处理过，已有记录）
    """
    if not os.path.exists(config.md5_path):
        # 文件路径不存在，肯定没有处理过这个md5
        open(config.md5_path, "w", encoding="utf-8").close()
        return False

    else:
        for line in open(config.md5_path, "r", encoding="utf-8").readlines():
            # 处理字符串前后的空格和回车如果等于传入的字符串，则表示处理过了
            if line.strip() == md5_str:
                return True

    return False

def save_md5(md5_str: str):
    """将传入的md5字符串，记录到文件内保存"""
    with open(config.md5_path, "a", encoding="utf-8") as f:
        f.write(md5_str + "\n")


def get_md5_str(input_str: str, encoding="utf-8"):
    """
    将传入的字符串转换成md5字符串
    """
    # 将字符串转化为bytes字节数组
    str_bytes = input_str.encode(encoding=encoding)

    # 创建md5对象
    md5_obj = hashlib.md5()
    # 更新md5内容
    md5_obj.update(str_bytes)
    # 得到md5的十六进制字符串
    return md5_obj.hexdigest()

class KnowledgeBaseService(object):
    def __init__(self):
        # 如果文件夹不存在则创建，如果存在则跳过
        os.makedirs(config.persist_directory, exist_ok=True)

        # 向量存储的实例 Chroma向量库对象
        self.chroma = Chroma(
            collection_name=config.collection_name, # 数据库表名
            persist_directory=config.persist_directory, # 数据库本地存储文件夹
            embedding_function=config.embedding_function, # 嵌入函数
        )

        # 文本分割器的对象
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,  # 分割后的文本段最大长度
            chunk_overlap=config.chunk_overlap,  # 连续文本段之间的字符重叠数量
            separators=config.separators,  # 自然段落划分的符号
            length_function=len,  # 使用Python自带的len函数做长度统计的依据
        )

    def upload_by_str(self, data: str, filename):
        """将传入的字符串，进行向量化，存入向量数据库中"""
        # 先得到传入字符串的md5值
        md5_str = get_md5_str(data)

        if check_md5(md5_str):
            print("该文件已经处理过了")
            return "[跳过]内容已经存在知识库中"

        if len(data) > config.max_split_char_number:
            # 如果传入的字符串长度超过阈值，则进行文本分割
            knowledge_chunks: list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]


        metadata = {
            "source": filename,
            # 2025-01-01 10:00:00
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "wangfan",
        }

        # 内容添加到向量数据库中
        self.chroma.add_texts(
            texts=knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks],
        )

        save_md5(md5_str)

        return "[成功]内容已经成功载入向量库"

if __name__ == "__main__":
    kb = KnowledgeBaseService()
    res = kb.upload_by_str("这是一个测试", "testfile")
    print(res)

