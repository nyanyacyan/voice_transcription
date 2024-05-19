# coding: utf-8
# --------------------------------------------------------------------------------
# 2023/2/18 制作

#---バージョン---
# Python==3.8.10
# --------------------------------------------------------------------------------
import os

from movie_to_audio.youtube_url import YoutubeToMp4

from logger.debug_logger import Logger

# --------------------------------------------------------------------------------


class Test:
    def __init__(self, debug_mode=False) -> None:
        self.youtube_to_mp4 = YoutubeToMp4(debug_mode=debug_mode)
        # Loggerクラスを初期化
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode

    def test_process(self):
        try:
            self.logger.info(f"******** youtube_to_mp4 開始 ********")

            # ここにアドレスを入力
            youtube_url = ''
            self.logger.info(f"youtube_url: {youtube_url}")

            self.youtube_to_mp4(youtube_url=youtube_url)


            self.logger.info(f"******** youtube_to_mp4 終了 ********")

        except Exception as e:
            self.logger.error(f" youtube_to_mp4 処理中にエラーが発生 {e}")

# --------------------------------------------------------------------------------


if __name__ == '__main__':

    main = Test()
    main.test_process()