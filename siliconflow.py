from openai import OpenAI
import requests


class Siliconflow:
    client = OpenAI(
        base_url='https://api.siliconflow.cn/v1/',
        api_key="sk-*"
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

    def add_user(self, content):
        self.messages.append({
            "role": "user",
            "content": content
        })

    def chat(self, text):
        self.messages.append({
            "role": "user",
            "content": text
        })

        content = ""
        reasoning_content = ""
        response = self.client.chat.completions.create(
            model="Pro/deepseek-ai/DeepSeek-R1",
            messages=self.messages,
            stream=True,  # 启用流式输出
            max_tokens=16 * 1000
        )
        # 逐步接收并处理响应
        for chunk in response:
            if chunk.choices[0].delta.content:
                # 实际输出内容
                content += chunk.choices[0].delta.content
                print(f"\033[1;32m{chunk.choices[0].delta.content}\033[0m", end="")
            if chunk.choices[0].delta.reasoning_content:
                # 思考链
                reasoning_content += chunk.choices[0].delta.reasoning_content
                print(f"\033[1;37m{chunk.choices[0].delta.reasoning_content}\033[0m", end="")

        return content, reasoning_content


class SiliconflowV3:
    client = OpenAI(
        base_url='https://api.siliconflow.cn/v1/',
        api_key="sk-*"
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

    def add_user(self, content):
        self.messages.append({
            "role": "user",
            "content": content
        })

    def chat(self, text):
        self.messages.append({
            "role": "user",
            "content": text
        })

        content = ""
        reasoning_content = ""
        response = self.client.chat.completions.create(
            model="Pro/deepseek-ai/DeepSeek-V3",
            messages=self.messages,
            stream=True,  # 启用流式输出
        )
        # 逐步接收并处理响应
        for chunk in response:
            if chunk.choices[0].delta.content:
                # 实际输出内容
                content += chunk.choices[0].delta.content
                print(f"\033[1;32m{chunk.choices[0].delta.content}\033[0m", end="")
            if chunk.choices[0].delta.reasoning_content:
                # 思考链
                reasoning_content += chunk.choices[0].delta.reasoning_content
                print(f"\033[1;37m{chunk.choices[0].delta.reasoning_content}\033[0m", end="")

        return content, reasoning_content
