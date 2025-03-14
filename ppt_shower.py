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


def open_ppt(file):
    os.startfile(file)


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
