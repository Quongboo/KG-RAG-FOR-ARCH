"""
节点之间的关系代理
"""


class Relationship:
    def __init__(self):
        self.source_entity: str = ""
        self.target_entity: str = ""
        self.relationship_desc: str = ""
        self.relationship_strength: int = 0

    def set_source_entity(self, source_entity: str):
        self.source_entity = source_entity

    def get_source_entity(self):
        return self.source_entity

    def set_target_entity(self, target_entity: str):
        self.target_entity = target_entity

    def get_target_entity(self):
        return self.target_entity

    def set_relationship_desc(self, relationship_desc: str):
        self.relationship_desc = relationship_desc

    def get_relationship_desc(self):
        return self.relationship_desc

    def set_relationship_strength(self, relationship_strength: int):
        self.relationship_strength = relationship_strength

    def get_relationship_strength(self):
        return self.relationship_strength
