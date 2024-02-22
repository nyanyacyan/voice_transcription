# coding: utf-8
# ----------------------------------------------------------------------------------
# loggerクラス
# 2023/2/18 制作

#---バージョン---
# Python==3.8.10
# ----------------------------------------------------------------------------------
from openai import OpenAI
import os
import tiktoken
from dotenv import load_dotenv
import pandas as pd

# 自作モジュール
from logger.debug_logger import Logger
from my_decorators.logging_decorators import debug_logger_decorator

class ChatgptTranslator:
    def __init__(self, api_key, debug_mode=False):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)

        # Loggerクラスを初期化
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode

    @debug_logger_decorator
    def read_file(self, file_path):
        '''
        文字起こしされたファイル読込
        '''
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    @debug_logger_decorator
    def read_translation_instructions(self, translate_file):
        '''
        翻訳指示書を読込。全ての指示を１つに。
        '''
        df = pd.read_excel(translate_file, usecols=['from', 'to'])
        ja_translate = []

        for _, row in df.iterrows():

            translate_part = row['from']
            ja_part = row['to']

            instruction_part = f'\n文章「{translate_part}」は「{ja_part}」と和訳\n'

            ja_translate.append(instruction_part)

        return "".join(ja_translate)

    @debug_logger_decorator
    def chatgpt_request(self, before_text_file, ja_translate):
        '''
        ChatGPTへの指示書（余計な文字をクリーン）
        '''
        res = self.client.chat.completions.create(
            # モデルを選択
            model = "gpt-3.5-turbo",
            
            # メッセージ
            messages  = [
                {"role": "system", "content": f'You are a helpful assistant that translates to Japanese.'},
                {"role": "user",
                "content": f"添付したテキストファイルを全て文章を和訳して全てを表示ほしい。「{before_text_file}」\n「添付したテキストファイル」に下記の文章があった場合には必ず指定した和訳に置き換えてください。{ja_translate}\n上記で指定した和訳が、ちゃんと反映してるかを確認してるかな？。"},
            ] ,

            max_tokens  = 4096,             # 生成する文章の最大単語数
            n           = 1,                # いくつの返答を生成するか
            # stop        = None,             # 指定した単語が出現した場合、文章生成を打ち切る
            # temperature = 0,                # 出力する単語のランダム性（0から2の範囲） 0であれば毎回返答内容固定
        )

        # 応答
        translate_text = res.choices[0].message.content
        clean_text = translate_text.replace(')', '')

        return clean_text
    

    @debug_logger_decorator
    def chatgpt_translator(self, before_text_file_path, translate_file):
        '''
        メインメソッド
        クラスの全てを並べ当てはめる
        '''
        before_text_file = self.read_file(before_text_file_path)
        full_instructions = self.read_translation_instructions(translate_file)
        self.chatgpt_request(before_text_file, full_instructions)
