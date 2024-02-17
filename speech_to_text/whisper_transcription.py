# coding: utf-8
# ----------------------------------------------------------------------------------
# loggerクラス
# 2023/2/18 制作

#---バージョン---
# Python==3.8.10
# ----------------------------------------------------------------------------------
import os
from dotenv import load_dotenv
import openai

load_dotenv()

# 自作モジュール
from my_decorators.logging_decorators import debug_logger_decorator


class WhisperTranscription:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API')


    @debug_logger_decorator
    async def whisper_transcription(self):
        audio_file_path = os.getenv('AUDIO_FILE')  # 後にGUIから受け、変換したデータを入れる。
        audio_formats = ['mp3', 'wav']
        
        # mp3もwavともに処理できるように
        for audio_format in audio_formats:
            try:
                with open(f"{audio_file_path}.{audio_format}", "rb") as audio_file:
                    response = openai.Audio.transcribe(
                        model="whisper-large",
                        file=audio_file,
                        format=audio_format,
                        timestamps=True
                    )
                    break  # 正常に処理できたらループを抜ける

            except FileNotFoundError:
                continue  # 別の拡張子の処理へ

        # ファイル名を指定してテキストファイルに書き込む
        with open('whisper_write_file.txt', 'w', encoding='utf-8') as output_file:
            for word_info in response['data']['words']:
                word = word_info['word']
                start_time = word_info['start']
                end_time = word_info['end']

                # テキストファイルに書き込むフォーマット
                output_file.write(f"Start: {start_time}, End: {end_time} - {word}\n")