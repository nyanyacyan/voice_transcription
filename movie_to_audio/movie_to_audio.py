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

class Mp4ToWav:
    @debug_logger_decorator
    def mp4_to_wav(self):
        movie_file = os.getenv('MP4_FILE')
        # 音声データに置き換え
        wav_file = AudioFileClip(movie_file)
        # 音声データを保存
        wav_file.write_audiofile(movie_file.replace('.mp4', '.mp3'))
