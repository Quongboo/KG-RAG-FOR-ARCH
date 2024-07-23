"""
文本类处理
"""
import html
import re
from typing import Any
import json
from docx import Document


def split_text(text: str, chunk: int):
    """
    将文本按照chunk切分为一个块截断保存为一个列表
    :param text: 待处理的文本
    :param chunk: 分块的大小
    :return:
    """
    # 存储截断后的文本块的列表
    text_blocks = []
    # 计算需要截断的块数
    num_blocks = (len(text) + (chunk - 1)) // chunk
    # 逐个截断文本并添加到列表中
    for i in range(num_blocks):
        start = i * chunk
        end = (i + 1) * chunk
        block = text[start:end]
        text_blocks.append(block)
    return text_blocks


def read_docx_to_sentence(file_path):
    """
    读取word文件
    :param file_path:
    :return:
    """
    doc = Document(file_path)
    paragraphs = [p.text for p in doc.paragraphs]
    return [item.replace(" ", "") for item in paragraphs if item.strip() != ""]


def split_chunk_list(word_list, chunk_length):
    """
    将列表按照设定的字数进行切分
    :param word_list:
    :param chunk_length:
    :return:
    """
    chunk_list = []
    current_chunk = []
    current_length = 0

    for word in word_list:
        if current_length + len(word) <= chunk_length:
            current_chunk.append(word)
            current_length += len(word)
        else:
            chunk_list.append(current_chunk)
            current_chunk = [word]
            current_length = len(word)

    if current_chunk:
        chunk_list.append(current_chunk)

    return chunk_list


def clean_str(text: Any) -> str:
    """
    清理输入的字符串
    :param text:
    :return:
    """
    if not isinstance(text, str):
        return str(text)

    result = html.unescape(text.strip())  # 不转义HTML实体并删除前后空白

    result = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", result)  # 删除控制字符

    result = result.replace('"', '')  # 删除双引号

    return result


def convert_json_to_dict(json_string):
    """
    将 JSON 格式的字符串转换成 Python 字典。
    """
    try:
        json_string = json_string.strip('"')
        data_dict = json.loads(json_string)
    except:
        data_dict = {}
    return data_dict


def convert_int(text):
    """
    将输入的字符转化为整数
    :param text:
    :return:
    """
    try:
        data = int(text)
        return data
    except:
        return -1


