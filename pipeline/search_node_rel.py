"""
查询节点及节点的关系相关信息
"""
from typing import List
from config.config_entity import get_config
from database.neo4j import neo4j

class SearchNodeRel():
    def __init__(self):
        self.node_threshold_value = int(get_config()['search']['node_threshold_value'])

    def filter_nodes(self, match_data):
        """
        筛选合格的实体
        :return:
        """
        filter_node_name_list = []
        for node_name, node_value in match_data.items():
            node_value = int(node_value)
            if node_value >= self.node_threshold_value:
                filter_node_name_list.append(node_name)
            else:
                print(f'实体和用户问题联系判定分数不足:{self.node_threshold_value}，舍去：{node_name}')
        return filter_node_name_list

    def search_node_rel_info(self, filter_node_name_list: List):
        """
        获取节点的信息以及节点的关系信息
        :param filter_node_name_list:
        :return:
        """
        nodes_rel_list = []
        for _name in filter_node_name_list:
            node_rel_data = neo4j.search_node_and_relation(_name)
            nodes_rel_list.append(node_rel_data)
        return nodes_rel_list


    def process(self, user_entity_list, match_data):

        filter_node_name_list = self.filter_nodes(match_data)
        nodes_rel_list = self.search_node_rel_info(filter_node_name_list)
        return nodes_rel_list





