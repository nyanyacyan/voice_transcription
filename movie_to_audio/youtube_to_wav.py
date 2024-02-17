# coding: utf-8
# --------------------------------------------------------------------------------
# 
# 2023/2/ 制作

#---バージョン---
# Python==3.8.10

# --------------------------------------------------------------------------------
import os
import sys
from dotenv import load_dotenv
import functools
from yt_dlp import YoutubeDL

load_dotenv()

project_paths = os.getenv('PYTHONPATH', '')
for path in project_paths.split(':'):
    if path not in sys.path:
        sys.path.append(path)

# 自作モジュール
from my_decorators.logging_decorators import debug_logger_decorator


class YoutubeToWav:
    def __init__(self):
        self.youtube_url = os.getenv('YOUTUBE_URL')
        
    @debug_logger_decorator
    def youtube_to_wav(self):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.youtube_url])


if __name__ == '__main__':
        # YouTube_To_Wavクラスのインスタンスを作成
    downloader = Youtube_To_Wav()
    
    # youtube_to_wavメソッドを実行
    downloader.youtube_to_wav()