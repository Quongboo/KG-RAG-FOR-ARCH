"""
从neo4j数据库进行查询
"""
from pipeline.match_node_pipeline import MatchNode
from pipeline.search_node_rel import SearchNodeRel
from pipeline.search_llm import SearchLLM


class ProcessSearch:
    def __init__(self):
        self.match = MatchNode()
        self.search_node = SearchNodeRel()
        self.search_llm = SearchLLM()

    def process(self, question: str):
        user_entity_list, match_data = self.match.process(question)
        nodes_rel_list = self.search_node.process(user_entity_list, match_data)
        llm_answer = self.search_llm.process(question, nodes_rel_list)
        return llm_answer
