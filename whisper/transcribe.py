# coding: utf-8
# ----------------------------------------------------------------------------------
# loggerクラス
# 2023/2/18 制作

#---バージョン---
# Python==3.8.10
# ----------------------------------------------------------------------------------
import os
from dotenv import load_dotenv
from faster_whisper import WhisperModel

load_dotenv()

# 自作モジュール
from my_decorators.logging_decorators import debug_logger_decorator
from my_decorators.error_handling_decorators import error_handling_decorator
from my_decorators.performance_decorators import progress_bar_decorator


class WhisperTranscription:
    @debug_logger_decorator
    @error_handling_decorator
    # @progress_bar_decorator
    def whisper_transcription(self):
        audio_file = os.getenv("AUDIO_FILE")
        # tiny, base, small, medium, large-v2, large-v3
        model = WhisperModel("base", device="cpu", compute_type="int8")

        segments, info = model.transcribe(
            audio_file,
            beam_size=5,  # 精度のクオリティを調節するもの数値を大きくする精度アップ時間ダウン
            vad_filter=True
        )

        # # ファイル名を指定してテキストファイルに書き込む
        with open('whisper_write_file.txt', 'w', encoding='utf-8') as output_file:
            output_file.write("表示する言語 '%s' 精度 %f\n" % (info.language, info.language_probability))

            # セクションごとに時間を表示
            for segment in segments:
                output_file.write("[%.2fs -> %.2fs] %s\n" % (segment.start, segment.end, segment.text))