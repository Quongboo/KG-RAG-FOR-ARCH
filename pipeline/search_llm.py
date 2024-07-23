"""
结合查询到的资料请求大模型的pipeline
"""
import re
from typing import List
from copy import deepcopy
from llm.llm_client import llm_client
from config.config_entity import get_config
from prompt.prompt import answer_prompt


class SearchLLMPadder():

    def padding(self, parse_tuple_list):

        if parse_tuple_list[0] == '"answer"' and len(parse_tuple_list) >= 2:
            llm_answer = parse_tuple_list[1].upper()
            llm_answer = llm_answer.replace("<", "").replace(">", "")
            return llm_answer
        else:
            llm_answer = parse_tuple_list[1].upper()
            print(llm_answer)
            return '请求失败，请重试'


class SearchLLMParser():
    def __init__(self):
        self.tuple_delimiter = '{tuple_delimiter}'
        self.record_delimiter = "{record_delimiter}"
        self.completion_delimiter = "{completion_delimiter}"

    def parser_llm_output(self, llm_output):
        """
        解析大模型的输出
        :param llm_output:
        :return:
        """
        parse_ = re.sub(r"^\(|\)$", "", llm_output.strip())
        parse_tuple_list = parse_.split(self.tuple_delimiter)

        return parse_tuple_list


class SearchLLM():
    def __init__(self):
        self.padder = SearchLLMPadder()
        self.parser = SearchLLMParser()
        self.llm_request_func = llm_client.request_deepseek
        self.llm_token_check_func = llm_client.deepseek_check_token
        self.token_limit = int(get_config()['token_limit'])

    def get_node_message(self, nodes_rel_list: List):
        """
        构造所查询到的节点的关系prompt
        :param nodes_rel_list:
        :return:
        """
        node_message_list = []
        rel_message_list = []
        node_name_list = []
        for node_rel_data in nodes_rel_list:
            node_name = node_rel_data["node_name"]
            node_desc = node_rel_data["node_desc"]
            node_info = node_rel_data["node_info"]

            node_rel_list = node_rel_data["node_rel_list"]
            for rel in node_rel_list:
                start_node_name = rel["start_node_name"]
                end_node_name = rel["end_node_name"]
                rel_strength = rel["rel_strength"]
                rel_desc = rel["rel_desc"]

                rel_message = f'{start_node_name}与{end_node_name}的联系强度为{rel_strength}；关系为：{rel_desc}，'
                rel_message_list.append(rel_message)

            node_name_list.append(node_name)
            node_info_message = f"{node_name}的描述为{node_desc}，{node_name}的信息为：{node_info}；与其有密切联系的关系有{rel_message_list}"
            node_message_list.append(node_info_message)
        return node_message_list, node_name_list

    def get_message(self, user_question, nodes_rel_list):
        node_message_list, node_name_list = self.get_node_message(nodes_rel_list)
        message = deepcopy(answer_prompt)
        message[-1]["content"] = message[-1]["content"].format(user_question, node_name_list,
                                                               node_message_list)
        token = self.llm_token_check_func(message)
        if token < self.token_limit:
            return message
        else:
            # TODO：构建容错
            print(f'构造的消息超出了token数量限制，message：{message}')

    def process(self, user_question, nodes_rel_list):

        message = self.get_message(user_question, nodes_rel_list)
        llm_output = self.llm_request_func(message)
        parse_tuple_list = self.parser.parser_llm_output(llm_output)
        llm_answer = self.padder.padding(parse_tuple_list)
        print(llm_answer)
        return llm_answer
