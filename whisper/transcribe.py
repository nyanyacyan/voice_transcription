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

load_dotenv()

# 自作モジュール
from my_decorators.logging_decorators import debug_logger_decorator
from my_decorators.error_handling_decorators import error_handling_decorator


class WhisperTranscription:
    @debug_logger_decorator
    @error_handling_decorator
    def whisper_transcription(self):
        youtube_audio_file = os.getenv("AUDIO_FILE")
        mp4_audio_file = os.getenv("MP4_FILE")
        # youtube_audio_file = os.getenv("YOUTUBE_MOVIE_FILENAME")
        # mp4_audio_file = os.getenv("MP4_MOVIE_FILENAME")
        
        # ここでモデルを調整する
        # tiny, base, small, medium, large-v2, large-v3
        model = WhisperModel("base", device="cpu", compute_type="int8")

        # データをsegmentsとinfoに分けて保管
        if youtube_audio_file:
            segments, info = model.transcribe(
            youtube_audio_file,
            beam_size=5,  # 精度のクオリティを調節するもの数値を大きくする精度アップ時間ダウン
            vad_filter=True
        )
        else:
            segments, info = model.transcribe(
            mp4_audio_file,
            beam_size=5,  # 精度のクオリティを調節するもの数値を大きくする精度アップ時間ダウン
            vad_filter=True
        )


        print("表示する言語 '%s' 精度 %f\n" % (info.language, info.language_probability))

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
        with open('whisper_write_file.txt', 'w', encoding='utf-8') as output_file:
            for segment in results:
                output_file.write(f"{segment['start']} -> {segment['end']} {segment['text']})\n")

if __name__ == '__main__':
    whisper_inst = WhisperTranscription()
    whisper_inst.whisper_transcription()