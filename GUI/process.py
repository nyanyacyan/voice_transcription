# coding: utf-8
# ----------------------------------------------------------------------------------
#* 実行ファイル
# 2023/2/25 制作

#---バージョン---
# Python==3.8.10
# ----------------------------------------------------------------------------------
import os

from dotenv import load_dotenv

# 自作モジュール
from chatgpt.data_division import ChatgptTextSplitSave
from chatgpt.dump_manager import DumpManager
from chatgpt.translation_request import TranslationRequest
from logger.debug_logger import Logger
from movie_to_audio.movie_to_audio import Mp4ToMp3
from movie_to_audio.youtube_url import YoutubeToMp3
from whisper.transcribe import WhisperTranscription
from GUI.ui_components import YouTubeURLInput, FilePicker
from GUI.popup_messagebox import PopupMessageBox


class YouTubeProcess:
    def __init__(self, api_key, parent):
        self.logger = self.setup_logger()
        self.api_key = api_key
        self.input_dir = 'chatgpt/data_division_box'
        self.output_dir = 'chatgpt/translate_after_box'
        self.final_output_file = 'results_text_box/translated_completed.txt'
        self.translate_instruction = '翻訳指示ファイル.xlsx'
        self.data_division_box = 'chatgpt/data_division_box'
        self.translate_after_box = 'chatgpt/translate_after_box'

        self.youtube_url = YouTubeURLInput(parent)


    def setup_logger(self):
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        logger_instance = Logger(__name__, debug_mode=debug_mode)
        return logger_instance.get_logger()


    def process(self):
        try:
            youtube_url = self.youtube_url_input.get_url()
            youtube_to_mp3_inst = YoutubeToMp3(youtube_url)
            audio_file = youtube_to_mp3_inst.find_youtube_file_fullpath()
            self.logger.debug("文字起こし開始")
            whisper_transcription_inst = WhisperTranscription(audio_file)
            whisper_transcription_inst.whisper_transcription()
            chatgpt_text_split_save_inst = ChatgptTextSplitSave()
            chatgpt_text_split_save_inst.chatgpt_text_split_save()
            translation_req_class_inst = TranslationRequest(api_key=self.api_key)
            translation_req_class_inst.translate_all_files(self.input_dir, self.output_dir, self.translate_instruction)
            translation_req_class_inst.merge_translated_files(self.output_dir, self.final_output_file)
            translation_req_class_inst.delete_text_files(self.data_division_box, self.translate_after_box)
            self.message_box.show_info("完了通知", "翻訳が完了しました。\ntranslated_completed.txtをご覧ください。")

        except TypeError as e:
            self.logger.error(f"TypeError: {e}")
            self.message_box.show_error(f"テキストファイル生成ができてない可能性があります。{e}")

        except Exception as e:
            self.logger.error(f"error: {e}")
            self.message_box.show_error(f"処理中にエラーが発生しました。{e}")



class MP4Process:
    def __init__(self, api_key, parent):
        self.api_key = api_key
        self.input_dir = 'chatgpt/data_division_box'
        self.output_dir = 'chatgpt/translate_after_box'
        self.final_output_file = 'translated_completed.txt'
        self.translate_instruction = '翻訳指示ファイル.xlsx'
        self.data_division_box = 'chatgpt/data_division_box'
        self.translate_after_box = 'chatgpt/translate_after_box'
        # ロガーの初期化
        self.logger = self.setup_logger()
        self.mp4_path_picker = FilePicker(parent, "mp4")


    def setup_logger(self):
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        logger_instance = Logger(__name__, debug_mode=debug_mode)
        return logger_instance.get_logger()

    def process(self):
        try:
            mp4_path = self.mp4_path_picker.get_file_path()
            mp4_to_mp3_inst = Mp4ToMp3(mp4_path)
            audio_file = mp4_to_mp3_inst.mp4_to_mp3()
            self.logger.debug("文字起こし開始")
            whisper_transcription_inst = WhisperTranscription(audio_file)
            whisper_transcription_inst.whisper_transcription()
            chatgpt_text_split_save_inst = ChatgptTextSplitSave()
            chatgpt_text_split_save_inst.chatgpt_text_split_save()
            translation_req_class_inst = TranslationRequest(api_key=self.api_key)
            translation_req_class_inst.translate_all_files(self.input_dir, self.output_dir, self.translate_instruction)
            translation_req_class_inst.merge_translated_files(self.output_dir, self.final_output_file)
            translation_req_class_inst.delete_text_files(self.data_division_box, self.translate_after_box)
            self.message_box.show_info("完了通知", "翻訳が完了しました。\ntranslated_completed.txtをご覧ください。")

        except TypeError as e:
            self.logger.error(f"TypeError: {e}")
            self.message_box.show_error(f"テキストファイル生成ができてない可能性があります。{e}")

        except Exception as e:
            self.logger.error(f"error: {e}")
            self.message_box.show_error(f"処理中にエラーが発生しました。{e}")


class MP3Process:
    def __init__(self, api_key, parent):
        self.api_key = api_key
        self.input_dir = 'chatgpt/data_division_box'
        self.output_dir = 'chatgpt/translate_after_box'
        self.final_output_file = 'translated_completed.txt'
        self.translate_instruction = '翻訳指示ファイル.xlsx'
        # ロガーの初期化
        self.logger = self.setup_logger()
        self.mp3_path_picker = FilePicker(parent, "mp3")



    def setup_logger(self):
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        logger_instance = Logger(__name__, debug_mode=debug_mode)
        return logger_instance.get_logger()

    def process(self):
        try:
            audio_file = self.mp3_path_picker.get_file_path()
            whisper_transcription_inst = WhisperTranscription(audio_file)
            whisper_transcription_inst.whisper_transcription()
            chatgpt_text_split_save_inst = ChatgptTextSplitSave()
            chatgpt_text_split_save_inst.chatgpt_text_split_save()
            translation_req_class_inst = TranslationRequest(api_key=self.api_key)
            translation_req_class_inst.translate_all_files(self.input_dir, self.output_dir, self.translate_instruction)
            translation_req_class_inst.merge_translated_files(self.output_dir, self.final_output_file)
            self.message_box.show_info("完了通知", "翻訳が完了しました。\ntranslated_completed.txtをご覧ください。")

        except TypeError as e:
            self.logger.error(f"TypeError: {e}")
            self.message_box.show_error(f"警告", "テキストファイル生成ができてない可能性があります。{e}")

        except Exception as e:
            self.logger.error(f"error: {e}")
            self.message_box.show_error(f"処理中にエラーが発生しました。{e}")


class TranslationUpdater:
    def __init__(self, translate_file):
        self.translate_file = translate_file
        self.dump_manager = DumpManager()  # DumpManagerクラスのインスタンスを作成

    def update_instructions(self):
        """
        辞書データを更新する。
        使用する際には必ず
        translate_file = '翻訳指示ファイル.xlsx'を入れる
        """
        self.dump_manager.find_pickle_file()
        self.dump_manager.dataframe_updated(self.translate_file)
        self.dump_manager.write_pickle_file(self.translate_file)
        self.message_box.show_info("更新完了", "更新が完了しました。")
