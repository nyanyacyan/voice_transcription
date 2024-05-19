# coding: utf-8
# --------------------------------------------------------------------------------
# 2023/2/18 制作

#---バージョン---
# Python==3.8.10
# --------------------------------------------------------------------------------
import os,glob
from dotenv import load_dotenv
from yt_dlp import YoutubeDL

# 自作モジュール
from logger.debug_logger import Logger

load_dotenv()


###################################################################################


class YoutubeToMp3:
    def __init__(self,youtube_url, debug_mode=False):
        self.youtube_url = youtube_url
        # Loggerクラスを初期化
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode


###################################################################################


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

        # 実際にYoutubeDLクラスを使って上記で指定したオプションを使ってオブジェクトにしてるイメージ
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(self.youtube_url, download=True)
            movie_title = info_dict.get('title', 'downloaded_file')
            self.logger.debug(f"ダウンロードファイル名: {movie_title}")
            return movie_title




    def find_youtube_file_fullpath(self):
        download_dir = 'downloads'

        movie_title = self.youtube_to_mp3()
        self.logger.debug(movie_title)

        search_pattern = os.path.join(download_dir, f'*{movie_title}*.*')

        matching_files = glob.glob(search_pattern)

        if matching_files:
            return matching_files[0]
        raise Exception("ファイルが見つかりません。")

###################################################################################

class YoutubeToMp4:
    def __init__(self, debug_mode=False):

        # Loggerクラスを初期化
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode


###################################################################################
# --------------------------------------------------------------------------------


    # YouTube URLからmp4でダウンロード
    def youtube_to_mp4(self, youtube_url):
        # ダウンロードするディレクトリを指定
        download_directory = "downloads"

        # クラス定義みたいなもの
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            # 保存先の指定、ファイルのタイトルと拡張子を入れるためのテンプレ
            'outtmpl': os.path.join(download_directory,'%(title)s.%(ext)s'),
        }

        # ディレクトリがあるかを確認（無ければ作成）
        if not os.path.exists(download_directory):
            os.makedirs(download_directory)

        # 実際にYoutubeDLクラスを使って上記で指定したオプションを使ってオブジェクトにしてるイメージ
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            movie_title = info_dict.get('title', 'downloaded_file')
            self.logger.debug(f"ダウンロードファイル名: {movie_title}")
            return movie_title


# --------------------------------------------------------------------------------
