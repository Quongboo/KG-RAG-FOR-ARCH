"""
请求调用大语言模型的客户端
"""
from llm.deepseek import Deepseek
from typing import List


class LlmClient:
    """
        大语言模型调用客户端
    """

    def __init__(self):
        """
            大语言模型调用客户端、现在支持 deepseek
        """
        self.deepseek = Deepseek()

    def request_deepseek_list(self, message_list: List[List]):
        # TODO:并发请求,请求容错及重试
        answer_list = []
        for message in message_list:
            llm_output = self.deepseek.request_deepseek(message)
            answer_list.append(llm_output)
        return answer_list

    def request_deepseek(self, message: List):
        return self.deepseek.request_deepseek(message)

    def deepseek_check_token(self, message: List):
        message_str = str(message)
        return self.deepseek.get_token_deepseek(message_str)


llm_client = LlmClient()
