# coding: utf-8
# --------------------------------------------------------------------------------
# mp４ から wavに変換するモジュール
# 2023/2/18 制作

#---バージョン---
# Python==3.8.10

# --------------------------------------------------------------------------------
import os
from dotenv import load_dotenv
from moviepy.editor import AudioFileClip

# 自作モジュール
from my_decorators.logging_decorators import debug_logger_decorator

load_dotenv()

class Mp4ToMp3:
    def __init__(self, mp4_path):
        self.mp4_path = mp4_path

    @debug_logger_decorator
    def mp4_to_mp3(self):
        mp4_file = self.mp4_path
        # 音声データに置き換え
        wav_file = AudioFileClip(mp4_file)

        new_mp3_filename = mp4_file.replace('.mp4', '.mp3')
        # 音声データを保存
        wav_file.write_audiofile(new_mp3_filename)
