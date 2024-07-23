"""
Gradio 前端展示
1、将word数据上传，提取知识的关系，将其写入neo4j数据库之中
2、询问问题，进行回答
"""

"""
rag模块的web-ui
"""
import time
import gradio as gr
import argparse
import matplotlib
from pipeline.process_search import ProcessSearch
from pipeline.process_write_to_neo4j import ProcessWrite


write_neo4j = ProcessWrite


matplotlib.use('Agg')
APPTITLE = "KG-RAG-FOR-ARCH"



def search_llm_neo4j(question: str):
    """
    查询用户的问题
    :param question:
    :return:
    """
    search = ProcessSearch()
    llm_answer = search.process(question)
    return llm_answer

def write_words_to_noe4j(input_file):
    """
    将word文件写入neo4j之中
    :return:
    """
    print("input_file", input_file)
    import shutil
    import os

    # 上传文件
    file_name = os.path.basename(input_file)
    target_path = f"asset/user/{file_name}"
    shutil.copy(input_file, target_path)
    yield '上传成功'
    time.sleep(2)
    # 处理与识别
    yield '正在识别实体与关系'
    write_neo4j = ProcessWrite()
    write_neo4j.process(target_path)
    print(1111)
    # TODO:删除落盘文件
    yield '识别完成，可以基于新的资料进行搜索'


def get_args():
    parser = argparse.ArgumentParser(
        description='KG-RAG-FOR-ARCH')
    parser.add_argument('--host', default='127.0.0.1', help='IP Host')  # 本地命令
    # parser.add_argument('--host', default='0.0.0.0', help='IP Host')                  # 服务器命令
    parser.add_argument('--port', default=7863,
                        help='port')
    args = parser.parse_args()
    return args


def webui(args):
    # 页面设置
    while True:
        with gr.Blocks(title=f'{APPTITLE}', mode=f'{APPTITLE}') as barkgui:
            gr.Markdown("# <center>- KG-RAG-FOR-ARCH助手  - </center>")

            # 页面
            with gr.Tab("⭐ KG-RAG-FOR-ARCH知识助手"):
                # 输入问题
                gr.Markdown("## 🐶 输入你的问题")
                with gr.Row():
                    with gr.Column():
                        question_label = "你的问题输入在这里"
                        question = gr.Textbox(label="输入问题", lines=1, placeholder=question_label)

                # 查询RAG知识库按钮
                with gr.Row():
                    with gr.Column():
                        search_kg_rag_button = gr.Button("查询KG-RAG知识库", variant="primary")

                # 回答框
                answer_output = gr.Textbox(label="LLM回答内容", lines=10)

                search_kg_rag_button.click(search_llm_neo4j,
                                           inputs=[question],
                                           outputs=[answer_output]
                                           )


                # 上传word提取知识图谱
                new_words = gr.UploadButton("补充请上传新的需要解析关系的word,解析成功后，下方会显示：识别完成",
                                                  file_count="single",
                                                  file_types=[".docx"],
                                                  )

                room_config_button = gr.Button("开始解析", variant="primary")

                write_info = gr.Textbox(label="解析过程", lines=1)

                room_config_button.click(write_words_to_noe4j,
                                         inputs=[new_words],
                                         outputs=[write_info]
                                         )


            # 加入登录密码
            barkgui.queue().launch(show_error=True,
                                   server_name=args.host,
                                   server_port=args.port,
                                   share=True,
                                   # auth=("quyongbo", "quyongbo")
                                   )

webui(get_args())
