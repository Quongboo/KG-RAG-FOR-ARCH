"""
将数据写入到meo4j之中
"""
from pipeline.knowledge_extract_pipeline import KnowledgeExtract
from pipeline.write_node_rel_pipeline import WriteNodeRel
from utils.cached import write_to_json
import time


class ProcessWrite:
    def __init__(self):
        self.extract = KnowledgeExtract()
        self.write = WriteNodeRel()

    def write_node_rel_json(self, node_list, relation_list):
        json_node_list = []
        for node in node_list:
            node_name = node.get_node_name()
            node_class = node.get_node_class()
            node_desc = node.get_node_desc()
            node_info = node.get_node_info()
            node_data = {"node_name": node_name, "node_class": node_class, "node_desc": node_desc,
                         "node_info": node_info}
            json_node_list.append(node_data)

        json_rel_list = []
        for rel in relation_list:
            source_entity = rel.get_source_entity()
            target_entity = rel.get_target_entity()
            relationship_desc = rel.get_relationship_desc()
            relationship_strength = rel.get_relationship_strength()
            rel_data = {"source_entity": source_entity, "target_entity": target_entity,
                        "relationship_desc": relationship_desc, "relationship_strength": relationship_strength}
            json_rel_list.append(rel_data)

        # 提取的数据进行本地缓存
        current_time = time.time()
        node_cached_path = f"cached/{current_time}_node.json"
        rel_cached_path = f"cached/{current_time}_rel.json"
        write_to_json(node_cached_path, node_list)
        write_to_json(rel_cached_path, relation_list)

    def process(self, words_path: str):
        node_list, relation_list = self.extract.process(words_path)

        self.write_node_rel_json(node_list, relation_list)

        self.write.process(node_list, relation_list)
