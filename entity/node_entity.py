"""
知识图谱实体节点的代理
"""
from typing import Dict


class Node:
    def __init__(self):
        self.node_name: str = ""
        self.node_class: str = ""
        self.node_desc: str = ""
        self.node_info: Dict = {}

    def set_node_name(self, node_name: str):
        self.node_name = node_name

    def get_node_name(self):
        return self.node_name

    def set_node_class(self, node_class: str):
        self.node_class = node_class

    def get_node_class(self):
        return self.node_class

    def set_node_desc(self, node_desc: str):
        self.node_desc = node_desc

    def get_node_desc(self):
        return self.node_desc

    def set_node_info(self, node_info: Dict):
        self.node_info = node_info

    def get_node_info(self):
        return self.node_info
