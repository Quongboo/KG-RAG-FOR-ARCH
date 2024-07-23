"""
知识提取pipeline
将文本知识识别为graph关系的知识数据
"""

from utils.string_utils import split_text, read_docx_to_sentence, split_chunk_list, clean_str, convert_json_to_dict, \
    convert_int
from config.config_entity import get_config
from prompt.prompt import graph_nodes_prompt
from llm.llm_client import llm_client
from copy import deepcopy
from typing import List
from entity.node_entity import Node
from entity.relationship_entity import Relationship
import re


class KnowledgeExtractPadder():

    def padding(self, parse_list):

        node_list = []
        relation_list = []

        for parser in parse_list:
            if parser[0] == '"entity"' and len(parser) >= 4:  # 解析实体，且保证解析的长度正确
                node = Node()
                try:
                    node_name = clean_str(parser[1].upper())
                    node_class = clean_str(parser[2].upper())
                    node_desc = clean_str(parser[3])
                    node_info = convert_json_to_dict(parser[4])

                    node.set_node_name(node_name)  # 存储实体
                    node.set_node_class(node_class)
                    node.set_node_desc(node_desc)
                    node.set_node_info(node_info)

                    node_list.append(node)
                except:
                    pass

            if parser[0] == '"relationship"' and len(parser) >= 4:  # 解析关系
                relation = Relationship()
                try:
                    source_entity = clean_str(parser[1].upper())
                    target_entity = clean_str(parser[2].upper())
                    relationship_desc = clean_str(parser[3])
                    relationship_strength = convert_int(clean_str(parser[4]))  # 保障为数字

                    relation.set_source_entity(source_entity)
                    relation.set_target_entity(target_entity)
                    relation.set_relationship_desc(relationship_desc)
                    relation.set_relationship_strength(relationship_strength)

                    relation_list.append(relation)
                except:
                    pass

        return node_list, relation_list


class KnowledgeExtractParser():
    def __init__(self):
        self.tuple_delimiter = '{tuple_delimiter}'
        self.record_delimiter = "{record_delimiter}"
        self.completion_delimiter = "{completion_delimiter}"

    def parse_tuple(self, llm_output):

        parse_tuple_list = []
        for parse_ in llm_output.split(self.record_delimiter):
            parse_ = re.sub(r"^\(|\)$", "", parse_.strip())
            parse_tuple_ = parse_.split(self.tuple_delimiter)
            parse_tuple_list.append(parse_tuple_)
        return parse_tuple_list

    def parser_llm_output_list(self, llm_output_list):
        """
        解析大模型的输出
        :param llm_output_list:
        :return:
        """
        parse_list = []
        for llm_output in llm_output_list:
            parse_tuple_list = self.parse_tuple(llm_output)
            parse_list.extend(parse_tuple_list)
        return parse_list


class KnowledgeExtract():
    def __init__(self):
        self.chunk_length = get_config()['knowledge_extract']['chunk_length']
        self.node_class = get_config()['knowledge_extract']['chunk_length']
        self.token_limit = int(get_config()['token_limit'])
        self.llm_request_func = llm_client.request_deepseek_list
        self.llm_token_check_func = llm_client.deepseek_check_token
        self.parser = KnowledgeExtractParser()
        self.padder = KnowledgeExtractPadder()

    def check_token(self, chunk_text):
        """
        检查请求体是否超过了chunk的数量，超过则拆分，目前拆分为固定的数量的chunk=2000
        :param chunk_text:
        :return:
        """
        prompt = deepcopy(graph_nodes_prompt)
        prompt[-1]["content"] = prompt[-1]["content"].format(self.node_class, chunk_text)
        request_token = self.llm_token_check_func(prompt)

        if request_token > self.token_limit:
            chunk_size = 2000
            chunks = [chunk_text[i:i + chunk_size] for i in range(0, len(chunk_text), chunk_size)]
            return chunks

        else:
            return False

    def get_message_list(self, chunk_list: List):
        """
        构建message_list
        :param chunk_list:
        :return:
        """
        message_list = []
        for i in range(len(chunk_list)):
            text = chunk_list[i]
            text_string = ''.join(text)
            check_token_chunks = self.check_token(text_string)
            if check_token_chunks:
                for chunk in check_token_chunks:
                    prompt = deepcopy(graph_nodes_prompt)
                    prompt[-1]["content"] = prompt[-1]["content"].format(self.node_class, chunk)
                    message_list.append(prompt)
            else:
                prompt = deepcopy(graph_nodes_prompt)
                prompt[-1]["content"] = prompt[-1]["content"].format(self.node_class, text)
                message_list.append(prompt)
        return message_list

    def process(self, words_path: str):
        """
        从文字中获取到节点自身以及节点之间的关系
        :param words_path:
        :return:
        """

        word_sentence_list = read_docx_to_sentence(words_path)
        chunk_list = split_chunk_list(word_list=word_sentence_list, chunk_length=self.chunk_length)

        message_list = self.get_message_list(chunk_list)
        llm_output_list = self.llm_request_func(message_list)
        parse_list = self.parser.parser_llm_output_list(llm_output_list)
        node_list, relation_list = self.padder.padding(parse_list)

        return node_list, relation_list
