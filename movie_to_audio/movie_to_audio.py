# coding: utf-8
# --------------------------------------------------------------------------------
# mp４ から wavに変換するモジュール
# 2023/2/18 制作

#! 非同期処理
# --------------------------------------------------------------------------------
import os
import asyncio

from dotenv import load_dotenv
from moviepy.editor import AudioFileClip

# 自作モジュール
from logger.debug_logger import Logger

load_dotenv()

class Mp4ToMp3:
    def __init__(self, mp4_path, debug_mode=False):
        self.mp4_path = mp4_path

        # Loggerクラスを初期化
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode


    async def mp4_to_mp3(self):
        mp4_file = self.mp4_path
        download_directory = "downloads"

        # ファイル名を取得
        base_filename = os.path.basename(mp4_file)

        # ファイル名の拡張子を変更
        new_mp3_filename = base_filename.replace('.mp4', '.mp3')

        # 指定したディレクトリとファイル名を繋ぎ合わせてフルパスに
        full_mp3_path = os.path.join(download_directory, new_mp3_filename)

        mp3_file = AudioFileClip(mp4_file)

        # 音声データを保存
        # コルーチン化（非同期処理）
        # run_in_executorの第一引数にNoneを指定するとデフォルトのThreadPoolExecutorを使用
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, mp3_file.write_audiofile, full_mp3_path)

        return full_mp3_path
