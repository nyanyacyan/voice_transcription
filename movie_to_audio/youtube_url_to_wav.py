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
        # ダウンロードするディレクトリを指定
        download_directory = "downloads"

        # クラス定義みたいなもの
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',  # mp4に入れ替えれば動画になる
                'preferredquality': '192',
            }],
            # 保存先の指定、ファイルのタイトルと拡張子を入れるためのテンプレ
            'outtmpl': os.path.join(download_directory,'%(title)s.%(ext)s'),
        }

        # ディレクトリがあるかを確認（無ければ作成）
        if not os.path.exists(download_directory):
            os.makedirs(download_directory)

        # 実際にクラスを使ってオブジェクトにしてるイメージ
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(self.youtube_url, download=True)
            movie_filename = ydl.prepare_filename(info_dict)
            print(f"ダウンロードファイル名: {movie_filename}")
            
            return os.path.join(download_directory, movie_filename)