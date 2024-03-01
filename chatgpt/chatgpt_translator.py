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
    def __init__(self, api_key, pickle_path = 'data/excel_data.pickle', debug_mode=False):
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
        # バイナリモードでファイルを開く
        with open(self.pickle_path, 'rb') as handle:
            loaded_pickle_data = pickle.load(handle)
        self.logger.debug(loaded_pickle_data['instruction'])
        try:
            # pickleファイルにあるデータのinstructionに分けられたものを\nで繋ぎ合わせる
            # tolist()はデータをPythonの基本形式に戻す
            instructions = '\n'.join([''.join(x).strip() for x in loaded_pickle_data['instruction'].tolist()])
            self.logger.debug(f'instructions: {instructions}')

        except Exception as e:
            raise self.logger.error(f"Error: {e}")

        return instructions


    # @debug_logger_decorator
    def chatgpt_request(self, before_text_file, full_instructions):
        '''  ChatGPTへの指示書（余計な文字をクリーン）

        before_text_file-> 分割された翻訳前のテキストファイル
        ja_translate-> read_translation_instructionsによって指示書から１つにまとめた依頼文
        '''
        self.logger.debug(f"before_text_file: {before_text_file}")
        self.logger.debug(f"full_instructions: {full_instructions}")

        # メッセージ内容を構築
        messages  = [
            {"role": "system", "content": f'You are a helpful assistant that translates to Japanese.'},
            {"role": "user",
            "content": f"翻訳指示:\n\n1. 翻訳対象: このリクエストに含まれる英語および韓国語のテキストを全て日本語に翻訳してください。\n\n2. 特定用語の指定翻訳:\n{full_instructions}\n\n3. 翻訳のルール:\n・省略せずに全文を翻訳してください。\n・タイムスタンプは原文どおりに保持してください。\n・改行は各テキストブロックの終わりにのみ行ってください。\n・翻訳の際、コメントは加えないでください。\n改善された翻訳指示の例:\n翻訳テキストを提出する際には、以下のフォーマットルールに注意してください：\n\n\n**タイムスタンプと翻訳テキストは同じ行に記載してください。**タイムスタンプの直後に翻訳テキストを続けてください。改行は許可されていません。\n\n正しい例: 14.69 -> 17.39 こんにちは！今日の仕事はどうですか？\n\n誤った例: 14.69 -> 17.39\nこんにちは！今日の仕事はどうですか？\n\n**改行は各テキストブロックの終わり、つまり一連の対話や段落が完全に終了した後のみに行ってください。**これは、テキストが読みやすく、整理されていることを保証するためです。\n\nテキスト:\n{before_text_file}\n\n"},
        ]
        # メッセージ内容をコンソールに出力
        chatgpt_to_sentence = []

        for message in messages:
            self.logger.debug(f"内容: \n{message['content']}")
            chatgpt_to_sentence.append(message['content'])

        # リストはそのままでは書き込めないから分岐させる
        content_to_write = "\n".join(chatgpt_to_sentence)

        with open('chatgpt_to_sentence.txt', 'w', encoding='utf-8') as f:
            f.write(content_to_write)

        # OpenAI APIへのリクエスト送信
        res = self.client.chat.completions.create(
            # モデルを選択
            model = "gpt-3.5-turbo-0125",

            # メッセージ
            messages  = messages,
            max_tokens  = 4096,             # 生成する文章の最大単語数
            n           = 1,                # いくつの返答を生成するか
            # stop        = None,             # 指定した単語が出現した場合、文章生成を打ち切る
            # temperature = 0,                # 出力する単語のランダム性（0から2の範囲） 0であれば毎回返答内容固定
        )

        # 応答
        translate_text = res.choices[0].message.content

        self.logger.debug(translate_text)

        # ChatGPTからの文章をクリーン-> 必要があれば追加していく
        clean_text = translate_text.replace(')', '').replace('\n\n', '\n')

        self.logger.debug(clean_text)
        return clean_text


    # @debug_logger_decorator
    def chatgpt_translator(self, before_text_file, full_instructions):
        '''  メインメソッド クラスの全てを並べ当てはめる

        before_text_file-> 分割された翻訳前のテキストファイル
        translate_file-> 翻訳指示書ファイル（Excelファイル）
        '''
        self.logger.debug("翻訳処理開始")
        before_text_file = self.text_read(before_text_file)
        self.logger.debug("pickleファイルの読み込み開始")
        full_instructions = self.pickle_read()
        self.logger.debug(full_instructions)
        translated_text = self.chatgpt_request(before_text_file, full_instructions)

        return translated_text
