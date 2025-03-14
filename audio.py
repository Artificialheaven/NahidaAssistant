from pathlib import Path
from openai import OpenAI


def create_audio(text, file_name):
    speech_file_path = Path(__file__).parent / f"audios/{file_name}"

    client = OpenAI(
        api_key="sk-*",
        base_url="https://api.siliconflow.cn/v1"
    )

    with client.audio.speech.with_streaming_response.create(
        model="FunAudioLLM/CosyVoice2-0.5B",
        voice="speech:3399b843:5b1kp0nmhd:ukkpancrdiqrbmylatgf",
        input=text,
        response_format="mp3"
    ) as response:
        response.stream_to_file(speech_file_path)


if __name__ == "__main__":
    create_audio("你好，我的朋友。很高兴认识你。", "test.mp3")
