"""
KG-RAG for ARCH
读取建筑规范资料，转化为图数据，并存储在Neo4j之中；并结合用户问题使用大模型进行查询
目前大语言模型使用deepseek
阶段划分：
1、知识提取      √
2、知识写入      √
3、知识搜索      √
4、搜索后处理    √
4、知识查询      √
"""
from pipeline.process_write_to_neo4j import ProcessWrite
from pipeline.process_search import ProcessSearch

if __name__ == '__main__':
    write_data = True
    if write_data:
        # 写入数据部分
        words_path = "asset/规范_word/综合医院建筑设计规范-2014.docx"
        write = ProcessWrite()
        write.process(words_path)

    # 获取数据部分
    user_question = "综合医院如何设计？"
    search = ProcessSearch()
    answer = search.process(user_question)



