# coding: utf-8
# ----------------------------------------------------------------------------------
# loggerクラス
# 2023/2/18 制作

#! 非同期処理
# ----------------------------------------------------------------------------------
import os
import asyncio
from dotenv import load_dotenv
from faster_whisper import WhisperModel

load_dotenv()

# 自作モジュール
from logger.debug_logger import Logger


# ----------------------------------------------------------------------------------


class WhisperTranscription:
    def __init__(self, audio_file_path, debug_mode=False):
        # Loggerクラスを初期化
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode

        # ここにYouTubeとmp４それぞれが音声データに変換した入るのpath出す関数の返したものを入れる
        self.audio_file_path = audio_file_path


# ----------------------------------------------------------------------------------


    async def whisper_transcription(self):
        self.logger.debug(self.audio_file_path)

        loop = asyncio.get_running_loop()
        # ここでモデルを調整する
        # tiny, base, small, medium, large-v2, large-v3
        model = WhisperModel("large-v3", device="cpu", compute_type="int8")

        # データをsegmentsとinfoに分けて保管
        #* 非同期にする場合に引数がある場合にはlambdaが必要 → 関数を返してしまうため
        # lambdaを使わない場合は関数自体にfunctools.partialを使って定義することで関数として扱ってくれる
        self.audio_file_path
        segments, info = await loop.run_in_executor(None, lambda: model.transcribe(
            self.audio_file_path,
            beam_size=5,  # 精度のクオリティを調節するもの数値を大きくする精度アップ時間ダウン
            vad_filter=True
        ))

        self.logger.debug(f"表示する言語 '{info.language}' 精度 {info.language_probability}")

        results = [f"{s.start} -> {s.end} {s.text}" for s in segments]

        # ファイルに書き込む文字列を事前に準備
        output_content = "\n".join(results)

        # 非同期でファイルに書き込み
        # 非同期処理の流れの中で同期処理を実施 → 非ブロッキングI/O操作、パフォーマンス向上
        await loop.run_in_executor(None, self.write_to_file, 'results_text_box/whisper_write_file.txt', output_content)


# ----------------------------------------------------------------------------------
# 同期処理のメリットを活かすため同期処理で記述
# 同期処理は非同期処理の下にまとめることによってわかりやすくなる
#! 非同期処理に同期処理をまとめるのは基本「I/O処理」に限る

    def write_to_file(self, filepath, content):
        with open(filepath, 'w', encoding='utf-8') as output_file:
            output_file.write(content)


# ----------------------------------------------------------------------------------