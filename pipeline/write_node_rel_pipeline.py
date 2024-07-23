"""
将数据写入Neo4j的pipeline
"""

from config.config_entity import get_config
from database.neo4j import write_node_to_neo4j, write_relation_to_neo4j, del_all_node_rel, neo4j, \
    write_new_node_to_neo4j
from typing import List
from entity.node_entity import Node
from entity.relationship_entity import Relationship


class WriteNodeRel():
    """
    将节点以及节点的关系写入数据库的类
    """

    def __init__(self):
        self.clean_all_data = get_config()['database']['clean_all_data']

    def process(self, node_list: List[Node] = [], relation_list: List[Relationship] = []):

        if self.clean_all_data == True:
            del_all_node_rel()

        if node_list is not None:
            write_new_node_to_neo4j(node_list)  # 实体写入知识图谱

        if relation_list is not None:
            write_relation_to_neo4j(relation_list)  # 关系写入知识图谱
