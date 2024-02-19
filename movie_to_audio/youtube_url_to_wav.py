# coding: utf-8
# --------------------------------------------------------------------------------
# 
# 2023/2/18 制作

#---バージョン---
# Python==3.8.10

# --------------------------------------------------------------------------------
import os
from dotenv import load_dotenv
from yt_dlp import YoutubeDL

# 自作モジュール
from my_decorators.logging_decorators import debug_logger_decorator

load_dotenv()

class YoutubeToWav:
    def __init__(self):
        self.youtube_url = os.getenv('YOUTUBE_URL')
        
    @debug_logger_decorator
    def youtube_to_wav(self):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',  # mp4に入れ替えれば動画になる
                'preferredquality': '192',
            }],
        }

        # mp4が必要な時に使う
        # ydl_opts = {
        #     'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        # }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.youtube_url])
