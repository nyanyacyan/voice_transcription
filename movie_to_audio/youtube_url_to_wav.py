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

class YoutubeToMp3:
    def __init__(self,youtube_url):
        self.youtube_url = youtube_url
        
    @debug_logger_decorator
    def youtube_to_mp3(self):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',  # mp4に入れ替えれば動画になる
                'preferredquality': '192',
            }],
            'outtmpl': '%(title)s.%(ext)s',
        }

        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(self.youtube_url, download=False)
            movie_filename = ydl.prepare_filename(info_dict)
            ydl.download([self.youtube_url])
            print(f"ダウンロードファイル名: {movie_filename}")