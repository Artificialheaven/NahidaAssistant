from openai import OpenAI
import os
import httpx
from openai import types

from pathlib import Path


class Moonshot:
    client = OpenAI(
        api_key="sk-*",
        base_url="https://api.moonshot.cn/v1",
    )
    messages = [
        {
            "role": "system",
            "content": "你是 Nahida Assistant，由 Eastcloud AI 提供的人工智能助手，"
                       "你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。"
                       "同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Nahida Assistant、Eastcloud AI 为专有名词"
                       "，不可翻译成其他语言。"
        }
    ]

    def create_file(self, file) -> types.FileObject:
        # return self.client.files.create(file=Path("files/痛点察觉.pdf"), purpose="file-extract")
        return self.client.files.create(file=file, purpose="file-extract")

    def add_file(self, file: [types.FileObject, None] = None, file_id=None):
        if file_id:
            self.messages.append({
                "role": "system",
                "content": self.client.files.content(file_id=file_id).text
            })
            return
        self.messages.append({
            "role": "system",
            "content": self.client.files.content(file_id=file.id).text
        })

    def estimate_token_count(self, input: str) -> int:
        """
        在这里实现你的 Tokens 计算逻辑，或是直接调用我们的 Tokens 计算接口计算 Tokens

        https://api.moonshot.cn/v1/tokenizers/estimate-token-count
        """
        header = {
            "Authorization": f"Bearer sk-*",
        }
        data = {
            "model": "moonshot-v1-128k",
            "messages": [
                {"role": "user", "content": input},
            ]
        }
        r = httpx.post("https://api.moonshot.cn/v1/tokenizers/estimate-token-count", headers=header, json=data)
        r.raise_for_status()
        return r.json()["data"]["total_tokens"]

    def add_system(self, content):
        self.messages.append({
            "role": "system",
            "content": content
        })

    def chat(self, content):
        self.messages.append({
            "role": "user",
            "content": content
        })

        stream = self.client.chat.completions.create(
            model="moonshot-v1-128k",
            messages=self.messages,
            temperature=0.3,
            stream=True,  # <-- 注意这里，我们通过设置 stream=True 开启流式输出模式
        )

        assistant = ""
        completion = []
        for chunk in stream:
            # 在这里，每个 chunk 的结构都与之前的 completion 相似，但 message 字段被替换成了 delta 字段
            delta = chunk.choices[0].delta  # message 字段被替换成 delta 字段
            if delta.content:
                # 我们在打印内容时，由于是流式输出，为了保证句子的连贯性，我们不人为地添加换行符
                # 因此通过设置 end="" 来取消 print 自带的换行符。
                assistant += delta.content
                print(f"\033[1;32m{delta.content}\033[0m", end="")
                completion.append(delta.content)

        self.messages.append({
            "role": "assistant",
            "content": assistant
        })
        print(f"\033[1;31;40m使用token数量： {self.estimate_token_count(''.join(completion))}\033[0m")
        return assistant


if __name__ == "__main__":
    moonshot = Moonshot()
    file = moonshot.create_file(Path("files/痛点察觉.pdf"))
    moonshot.add_file(file)
    moonshot.chat("总结一下这些文件的内容。")

