"""
根据用户的问题匹配已有的节点名称
"""
import re
from database.neo4j import get_all_node_name
from copy import deepcopy
from prompt.prompt import nodes_match_prompt
from llm.llm_client import llm_client
from config.config_entity import get_config
from utils.string_utils import split_text, read_docx_to_sentence, split_chunk_list, clean_str, convert_json_to_dict, \
    convert_int


class MatchNodePadder():

    def padding(self, parse_tuple_list):
        user_entity_list = []
        match_data = {}
        for parse_tuple in parse_tuple_list:
            if parse_tuple[0] == '"user"' and len(parse_tuple) >= 2:
                user_entity = clean_str(parse_tuple[1])
                user_entity_list.append(user_entity)

            if parse_tuple[0] == '"match"' and len(parse_tuple) >= 3:
                match_entity = clean_str(parse_tuple[1].upper())
                match_strength = clean_str(parse_tuple[2].upper())
                data = {match_entity: match_strength}
                match_data.update(data)

        return user_entity_list, match_data





class MatchNodeParser():

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

        parse_tuple_list = []
        for parse_ in llm_output.split(self.record_delimiter):
            parse_ = re.sub(r"^\(|\)$", "", parse_.strip())
            parse_tuple_ = parse_.split(self.tuple_delimiter)
            parse_tuple_list.append(parse_tuple_)
        return parse_tuple_list


class MatchNode():
    def __init__(self):
        self.padder = MatchNodePadder()
        self.parser = MatchNodeParser()
        self.llm_request_func = llm_client.request_deepseek
        self.llm_token_check_func = llm_client.deepseek_check_token
        self.token_limit = int(get_config()['token_limit'])


    def get_message(self, node_name_list, user_question: str):
        """
        构建用户问题与实体匹配的message
        :param node_name_list:
        :param user_question:
        :return:
        """
        prompt = deepcopy(nodes_match_prompt)
        prompt[-1]["content"] = prompt[-1]["content"].format(node_name_list, user_question)
        token = self.llm_token_check_func(prompt)
        if token <  self.token_limit:
            return prompt
        else:
            # TODO：构建容错
            print(f'构造的消息超出了token数量限制，message：{prompt}')


    def process(self,user_question:str):
        """
        :param user_question:
        :return:
        user_entity_list:用户问题中所匹配到的实体
        match_data:用户问题的实体与已有实体之间的匹配关系
        """
        node_name_list = get_all_node_name()
        message = self.get_message(node_name_list, user_question)
        llm_output = self.llm_request_func(message)
        parse_tuple_list = self.parser.parser_llm_output(llm_output)
        user_entity_list, match_data = self.padder.padding(parse_tuple_list)
        return user_entity_list, match_data





