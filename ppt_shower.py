import wave

import pyautogui
import keyboard
import os
import subprocess
import time
from playsound import playsound
import re

from pydub import AudioSegment
from pydub.playback import play
import pyaudio


CHUNK = 1024  # 每个缓冲区的帧数
FORMAT = pyaudio.paInt16  # 采样位数
CHANNELS = 1  # 单声道
RATE = 44100  # 采样频率


def open_ppt(file):
    os.startfile(file)


def record_audio(wave_out_path, record_second):
    """ 录音功能 """
    p = pyaudio.PyAudio()  # 实例化对象
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)  # 打开流，传入响应参数
    wf = wave.open(wave_out_path, 'wb')  # 打开 wav 文件。
    wf.setnchannels(CHANNELS)  # 声道设置
    wf.setsampwidth(p.get_sample_size(FORMAT))  # 采样位数设置
    wf.setframerate(RATE)  # 采样频率设置

    for _ in range(0, int(RATE * record_second / CHUNK)):
        data = stream.read(CHUNK)
        wf.writeframes(data)  # 写入数据
    stream.stop_stream()  # 关闭流
    stream.close()
    p.terminate()
    wf.close()


def play_ppt(segments):
    time.sleep(5)
    keyboard.press_and_release("f5")
    time.sleep(2)

    for i in range(len(segments)):
        for j in range(len(segments[i])):
            if "停顿" in segments[i][j]:
                pattern = r'\[停顿-(\d+)\]'
                time.sleep(int(re.match(pattern, segments[i][j]).group(1)))
                print(segments[i][j])
            else:
                song = AudioSegment.from_mp3(f'audios/{i}-{j}.mp3')
                play(song)
                print(f"[{i+1}] 播放音频 audios/{i}-{j}.mp3 {segments[i][j]}")
        keyboard.press_and_release('right')
        print(f"翻页到 {i+1}")


if __name__ == "__main__":
    song = AudioSegment.from_mp3(f'audios/{1}-{0}.mp3')
    play(song)
    time.sleep(5)
