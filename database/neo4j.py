"""
neo4j的读写等操作类
"""
from typing import List
from py2neo import Graph, Node, Relationship, NodeMatcher
from py2neo.matching import RelationshipMatcher
from config.config_entity import get_config


class Neo4j:
    """
    Neo4j数据库相关操作
    """

    def __init__(self):
        config = get_config()
        self.graph = Graph(config['database']['neo4j_bolt'],
                           auth=(config['database']['neo4j_auth'], config['database']['neo4j_password']))

    def create_node(self, node_class=None, node_name=None, node_desc=None, node_info=None):
        """
        创建一个单一节点
        :param node_class: label
        :param node_name:
        :param node_desc:
        :param node_info:
        :return:
        """

        neo4j_node = Node(node_class, name=node_name, desc=node_desc, info=node_info)

        self.graph.create(neo4j_node)

    def create_node_list(self, node_list: List):
        """
        创建多个节点
        :param node_list: 节点列表
        :return:
        """
        self.graph.create(*node_list)

    def create_relation(self, start_node_name, end_node_name, relation_type: str, rel_info_dict):
        """
        创建节点之间的关系

        :param start_node_name: 起始节点的名称
        :param end_node_name: 终止节点的名称
        :param relation_type: 关系的类型//强度
        :param rel_info_dict: 关系的信息
        :return:
        """

        # 查找已有的起始节点和终止节点
        start_node = self.graph.nodes.match(name=start_node_name).first()
        end_node = self.graph.nodes.match(name=end_node_name).first()

        print(type(start_node), type(end_node))
        # 如果节点不存在,返回 None
        if not start_node or not end_node:
            return None

        # 构建关系的属性
        rel_properties = rel_info_dict
        print(rel_properties)

        relation_type = str(relation_type)

        # 创建关系
        relation = Relationship(start_node, relation_type, end_node, **rel_properties)
        self.graph.create(relation)

        return True

    def create_node_info(self, node_class, node_name, node_desc, node_info):
        """
        增加已有的节点的属性
        :param node_class: 节点类型
        :param node_name:  节点名称
        :param node_desc:  节点描述
        :param node_info:  节点信息
        :return:
        """

        exist_node = self.graph.nodes.match(node_class, name=node_name).first()
        exist_node["desc"] = node_desc
        exist_node["info"] = node_info
        self.graph.push(exist_node)

    def del_all_node_rel(self):
        """
        删除图谱中的所有的节点
        :return:
        """
        self.graph.delete_all()

    def del_single_node(self, label, node_name):
        """
        删除节点--单个
        :return:
        """
        node = self.graph.nodes.match(label, name=node_name).first()
        self.graph.delete(node)

    def del_label_node(self, label):
        """
        删除所有的同label节点
        :param label:
        :return:
        """
        # 创建节点查询器
        node_matcher = NodeMatcher(self.graph)
        nodes = node_matcher.match(label)
        for node in nodes:
            self.graph.delete(node)

    def del_relation(self, label, node1_name, node2_name, rel_type):
        """
        删除节点之间的关系
        :return:
        """
        node1 = self.graph.nodes.match(label, name=node1_name).first()
        node2 = self.graph.nodes.match(label, name=node2_name).first()
        relationship = Relationship(node1, rel_type, node2)
        self.graph.delete(relationship)

    def del_subject_info(self, label, node_name, del_info):
        """
        删除节点的属性
        :return:
        """
        node = self.graph.nodes.match(label, name=node_name).first()
        node.remove(del_info)
        # node.clear()              # 删除节点的所有属性
        self.graph.push(node)

    def search_node_info(self, label, node_name):
        """
        查找节点的属性
        (_5:房间 {area: 10, color: 'r', name: '\u4e66\u623f', 气味: '\u4e66\u9999'})
        :return:
        """
        node = self.graph.nodes.match(label, name=node_name).first()
        return node

    def search_node_rel(self, label, node_name):
        """
        查找单一节点的关系
        :param label:
        :param node_name:
        :return:
        """
        relationship_matcher = RelationshipMatcher(self.graph)
        node = self.graph.nodes.match(label, name=node_name).first()
        relationship = list(relationship_matcher.match([node], r_type=None))
        print(relationship)
        print(relationship[0])
        return relationship

    def search_nodes_rel(self, label, start_node_name, end_node_name):
        """
        查找指定的两个节点之间的关系
        :return:
        """
        relationship_matcher = RelationshipMatcher(self.graph)
        start_node = self.graph.nodes.match(label, name=start_node_name).first()
        end_node = self.graph.nodes.match(label, name=end_node_name).first()
        relationship = list(relationship_matcher.match((start_node, end_node), r_type=None))
        if relationship:
            rel_info = relationship[0]
        else:
            rel_info = "没有找到关系"
        return rel_info

    def check_node_exit(self, node_name: str):
        """
        检查节点是否以及存在
        :param node_name:
        :return:
        """
        node = self.graph.nodes.match(name=node_name).first()
        if node is None:
            return False
        else:
            return node

    def search_all_node_name(self):
        all_nodes = self.graph.run("MATCH (n) RETURN n")
        return all_nodes

    def search_node_and_relation(self, node_name: str):
        """
        根据节点名称，查询节点信息以及其相关的关系
        :return:node_rel_data:Dict
        """
        import re

        start_node = self.graph.nodes.match(name=node_name).first()

        node_desc = start_node['desc']
        node_info = start_node['info']

        relationship_matcher = RelationshipMatcher(self.graph)
        node = self.graph.nodes.match(name=node_name).first()
        relationship_list = list(relationship_matcher.match([node], r_type=None))

        # 获取和节点联系的相关关系
        node_rel_list = []
        for relationship in relationship_list:
            start_node_name = relationship.start_node['name']
            end_node_name = relationship.end_node['name']

            # TODO：如何获取这个值--目前才用正则解析，后期探索如果直接函数获取
            rel_type_str = str(relationship)
            regex = r'-\[:([^}])'
            match = re.search(regex, rel_type_str)
            rel_strength = match.group(1).strip()

            rel_desc = relationship['desc']

            rel_data = {"start_node_name": start_node_name, "end_node_name": end_node_name,
                        "rel_strength": rel_strength, "rel_desc": rel_desc}

            node_rel_list.append(rel_data)

        node_rel_data = {"node_name": node_name, "node_desc": node_desc,
                         "node_info": node_info, "node_rel_list": node_rel_list}

        print(f"节点查询及其关系的结果为：{node_rel_data}")
        return node_rel_data


neo4j = Neo4j()

"""
neo4j 批量读写操作
"""
from entity.node_entity import Node as Node_entity
from entity.relationship_entity import Relationship as Relationship_entity


def write_node_to_neo4j(node_list: List[Node_entity]):
    """
    将node_list中的节点批量写入到neo4j之中
    :param node_list:
    :return:
    """
    neo4j_node_list = []
    for node in node_list:
        node_name = str(node.get_node_name())
        node_class = str(node.get_node_class())
        node_desc = str(node.get_node_desc())
        node_info = str(node.get_node_info())
        print(node_name)
        neo4j.create_node(node_class=node_class, node_name=node_name, node_desc=node_desc, node_info=node_info)


def write_relation_to_neo4j(relation_list: List[Relationship_entity]):
    """
    将抽取的relation_list写入到neo4j之中
    TODO：批量写入
    :param relation_list:
    :return:
    """
    for relation in relation_list:
        source_entity_name = relation.get_source_entity()
        target_entity_name = relation.get_target_entity()

        relationship_desc = relation.get_relationship_desc()
        relation_dict = {'desc': relationship_desc}

        relationship_strength = str(relation.get_relationship_strength())

        relation = neo4j.create_relation(start_node_name=source_entity_name, end_node_name=target_entity_name,
                                         relation_type=relationship_strength, rel_info_dict=relation_dict)

        if relation is None:
            print(f'{source_entity_name}和{target_entity_name}在创建关系不存在，失败')


def del_all_node_rel():
    """
    删除所有的节点
    :return:
    """
    neo4j.del_all_node_rel()


def write_new_node_to_neo4j(node_list: List[Node_entity]):
    """
    上传新的节点到neo4j之中，如果是同名节点，则将属性添加到其中
    :param node_list:
    :return:
    """
    import ast

    for node in node_list:
        node_name = str(node.get_node_name())
        node_class = str(node.get_node_class())
        node_desc = str(node.get_node_desc())
        node_info_dict = node.get_node_info()

        # 检查是否已存在
        node_exit = neo4j.check_node_exit(node_name)
        if node_exit is not False:
            # 已存在，则在其基础上增加属性
            exit_desc = node_exit["desc"]
            exit_info = node_exit["info"]

            exit_info_dict = ast.literal_eval(exit_info)

            exit_node_class = list(node_exit.labels)[0]

            if exit_desc == node_desc:
                new_desc = exit_desc
            else:
                new_desc = exit_desc + ';' + node_desc

            exit_info_dict.update(node_info_dict)
            new_info = str(exit_info_dict)

            neo4j.create_node_info(node_class=exit_node_class, node_name=node_name, node_desc=new_desc,
                                   node_info=new_info)
        else:
            # 上传
            node_info = str(node_info_dict)
            neo4j.create_node(node_class=node_class, node_name=node_name, node_desc=node_desc, node_info=node_info)


def get_all_node_name():
    """
    获取neo4j的所有的节点名称
    :return:
    """
    node_name_list = []
    nodes = neo4j.search_all_node_name()
    for node in nodes:
        print(node)
        name = node[0]['name']
        node_name_list.append(name)
    return node_name_list
