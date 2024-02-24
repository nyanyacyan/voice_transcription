# coding: utf-8
# ----------------------------------------------------------------------------------
# chatgpt翻訳リクエストクラス
# 2023/2/18 制作

#---バージョン---
# Python==3.8.10
# ----------------------------------------------------------------------------------
from openai import OpenAI
import os
import pickle
from dotenv import load_dotenv
import pandas as pd

# 自作モジュール
from logger.debug_logger import Logger
from my_decorators.logging_decorators import debug_logger_decorator

load_dotenv()

class ChatgptTranslator:
    def __init__(self, api_key, pickle_path = '/Users/nyanyacyan/Desktop/ProgramFile/project_file/voice_transcription/data/excel_data.pickle', debug_mode=False):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        self.pickle_path = pickle_path

        # Loggerクラスを初期化
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode

    @debug_logger_decorator
    def text_read(self, before_text_file):
        '''  文字起こしされたファイル読込

        before_text_file-> 分割された翻訳前のテキストファイル
        '''
        with open(before_text_file, 'r', encoding='utf-8') as file:
            return file.read()
        

    def pickle_read(self):
        with open(self.pickle_path, 'rb') as handle:
            loaded_pickle_data = pickle.load(handle)

            full_instructions = loaded_pickle_data['instruction']

        return full_instructions


    # @debug_logger_decorator
    def chatgpt_request(self, before_text_file, full_instructions):
        '''  ChatGPTへの指示書（余計な文字をクリーン）

        before_text_file-> 分割された翻訳前のテキストファイル
        ja_translate-> read_translation_instructionsによって指示書から１つにまとめた依頼文
        '''
        res = self.client.chat.completions.create(
            # モデルを選択
            model = "gpt-3.5-turbo",
            
            # メッセージ
            messages  = [
                {"role": "system", "content": f'You are a helpful assistant that translates to Japanese.'},
                {"role": "user",
                "content": f"添付したテキストファイルを必ず全て文章を和訳して全てを表示ほしい。「{before_text_file}」\n「添付したテキストファイル」に下記の文章があった場合には必ず指定した和訳に置き換えてください。{full_instructions}\n上記で指定した和訳が、ちゃんと反映してるかを確認してるかな？中略、続くなどで省略はしないでください。翻訳のみを返信してください。"},
            ] ,

            max_tokens  = 4096,             # 生成する文章の最大単語数
            n           = 1,                # いくつの返答を生成するか
            # stop        = None,             # 指定した単語が出現した場合、文章生成を打ち切る
            # temperature = 0,                # 出力する単語のランダム性（0から2の範囲） 0であれば毎回返答内容固定
        )

        # 応答
        translate_text = res.choices[0].message.content

        # ChatGPTからの文章をクリーン-> 必要があれば追加していく
        clean_text = translate_text.replace(')', '').replace('\n\n', '\n')

        print(clean_text)
        return clean_text
    

    # @debug_logger_decorator
    def chatgpt_translator(self, before_text_file, full_instructions):
        '''  メインメソッド　クラスの全てを並べ当てはめる

        before_text_file-> 分割された翻訳前のテキストファイル
        translate_file-> 翻訳指示書ファイル（Excelファイル）
        '''
        before_text_file = self.text_read(before_text_file)
        translated_text = self.chatgpt_request(before_text_file, full_instructions)

        return translated_text
