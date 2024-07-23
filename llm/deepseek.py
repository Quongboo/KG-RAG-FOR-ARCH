"""
Deepseek接口
"""
from openai import OpenAI
from typing import List
from config.config_entity import get_config


class Deepseek:
    """
    for backward compatibility, you can still use `https://api.deepseek.com/v1` as `base_url`.
    """

    def __init__(self,
                 base_url: str = "https://api.deepseek.com",
                 model_name: str = "deepseek-chat",
                 time_out=5 * 60):
        self.base_url = base_url
        self.model_name = model_name
        self.api_key = get_config()['llm_api_key']['deepseek_api_key']
        self.time_out = time_out

    def request_deepseek(self, message: List, temperature: float = 0.7, max_tokens: int = 1024):
        """
        messages = [
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": "Hello"},
                    ]
        :param message:
        :param temperature:
        :param max_tokens:
        :return:
        """
        client = OpenAI(api_key=self.api_key,
                        base_url=self.base_url)

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=message,
            max_tokens=4096,
            temperature=0.7,
            stream=False
        )

        resp_text = response.choices[0].message.content
        return resp_text

    def get_token_deepseek(self, message: str):
        """
        deepseek官方文档token的估算方式：
        一般情况下模型中 token 和字数的换算比例大致如下：
            1 个英文字符 ≈ 0.3 个 token。
            1 个中文字符 ≈ 0.6 个 token。
        :return:
        """
        chinese_count = 0
        else_count = 0
        for char in message:
            if '\u4e00' <= char <= '\u9fff':
                chinese_count += 1
            else:
                else_count += 1
        token_nums = chinese_count * 0.6 + else_count * 0.3
        print({'token_nums': token_nums, 'chinese': chinese_count * 0.6, 'else': else_count * 0.3})
        return int(token_nums)
