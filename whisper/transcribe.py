# coding: utf-8
# ----------------------------------------------------------------------------------
# loggerクラス
# 2023/2/18 制作

#---バージョン---
# Python==3.8.10
# ----------------------------------------------------------------------------------
import os
from dotenv import load_dotenv
from tqdm import tqdm
from faster_whisper import WhisperModel
import time

load_dotenv()

# 自作モジュール
from logger.debug_logger import Logger



class WhisperTranscription:
    def __init__(self, audio_file_path, debug_mode=False):
        # Loggerクラスを初期化
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode

        # ここにYouTubeとmp４それぞれが音声データに変換した入るのpath出す関数の返したものを入れる
        self.audio_file_path = audio_file_path


# --------------------------------------------------------------------------------


    def whisper_transcription(self):
        self.logger.debug(f"self.audio_file_path: {self.audio_file_path}")

        start_time = time.time()

        # ここでモデルを調整する
        # tiny, base, small, medium, large-v2, large-v3
        model = WhisperModel("large-v3", device="cpu", compute_type="int8")

        self.logger.info(f"model: {model}")

        # データをsegmentsとinfoに分けて保管
        self.audio_file_path
        segments, info = model.transcribe(
            self.audio_file_path,
            beam_size=5,  # 精度のクオリティを調節するもの数値を大きくする精度アップ時間ダウン
            vad_filter=True
        )

        self.logger.debug("表示する言語 '%s' 精度 %f\n" % (info.language, info.language_probability))

        results = []

        # 初期値
        timestamps = 0.0

        with tqdm(total=info.duration, unit=" audio seconds") as pbar:
            for s in segments:
                # start、endはプロパティ　開始時間、終了時間をもってる
                segment_dict = {'start':s.start, 'end':s.end, 'text':s.text}
                results.append(segment_dict)
                pbar.update(s.end - timestamps)
                # ここでタイムスタンプを終了時間に更新して次のセグメントへ。
                timestamps = s.end
            if timestamps < info.duration:
                pbar.update(info.duration - timestamps)

        # # ファイル名を指定してテキストファイルに書き込む
        with open('results_text_box/whisper_write_file.txt', 'w', encoding='utf-8') as output_file:
            for segment in results:
                output_file.write(f"{segment['start']} -> {segment['end']} {segment['text']})\n")


        end_time = time.time()

        diff_time = start_time - end_time

        self.logger.info(f"diff_time: {diff_time}")
