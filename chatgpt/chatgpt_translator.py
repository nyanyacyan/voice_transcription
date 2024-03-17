# coding: utf-8
# ----------------------------------------------------------------------------------
# chatgpt翻訳リクエストクラス
# 2023/2/18 制作

#! 非同期処理
# ----------------------------------------------------------------------------------
from openai import OpenAI
import os
import pickle
import aiohttp
import aiofiles
from dotenv import load_dotenv

# 自作モジュール
from logger.debug_logger import Logger
from my_decorators.logging_decorators import debug_logger_decorator

load_dotenv()


# ----------------------------------------------------------------------------------


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


# ----------------------------------------------------------------------------------
# 文字起こしされたファイル読込
# before_text_file-> 分割された翻訳前のテキストファイル

    def text_read(self, before_text_file):
        with open(before_text_file, 'r', encoding='utf-8') as file:
            return file.read()


# ----------------------------------------------------------------------------------
# 同期処理のまま（バイナリデータのため読み書きが早いため）

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


# ----------------------------------------------------------------------------------


    async def chatgpt_request(self, before_text_file, full_instructions):
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

        # withは一連の流れをパッケージ化したもの（最後のファイルを閉じるの動作が重要）
        # 非同期処理では同期処理ができないため"aiofiles"を使うことで扱えるように定義することができる
        async with aiofiles.open('results_text_box/chatgpt_to_sentence.txt', 'w', encoding='utf-8') as f:
            # 実行部分は"await"
            await f.write(content_to_write)

        # APIを正規リクエスト方法
        # "エンドポイントの指定"
        # "認証情報"
        # "リクエスト内容"
        # この３つがあってリクエストになる

        # エンドポイント→集合場所
        url = "https://api.openai.com/v1/completions"

        # 認証情報
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # リクエスト情報
        data = {
            "model": "text-davinci-003",
            "prompt": messages,
            "max_tokens": 4096,
        }


        # リクエストを非同期処理する場合には簡素化されたもの（self.client.chat.completions.create()メソッド）では×
        # 正規のリクエスト方法により実行する必要がある
        # aiohttp.ClientSession() as session:はライブラリのインスタンスされたもの
        # 非同期でHTTPセッションを開始し、そのセッションを通じて様々なHTTPリクエスト（GET、POST、PUTなど）を非同期に実行

        # セッションはリクエストの送信準備と、コネクションの管理
        async with aiohttp.ClientSession() as session:

            # session.post()メソッドは、特にHTTP POSTリクエストを非同期に送信する際に利用
            async with session.post(url, json=data, headers=headers) as response:

                # 実行部分は"await"
                # .json()によってリクエストしたデータをjsonで返してくれる→レスポンスは基本バイナリデータ
                response_data = await response.json()
                translate_text = response_data.get("choices")[0].get("text","")

                self.logger.debug(translate_text)

                clean_text = translate_text.replace(')', '').replace('\n\n', '\n')

                self.logger.debug(clean_text)
                return clean_text


        # # OpenAI APIへのリクエスト送信
        # res = self.client.chat.completions.create(
        #     # モデルを選択
        #     model = "gpt-3.5-turbo-0125",

        #     # メッセージ
        #     messages  = messages,
        #     max_tokens  = 4096,             # 生成する文章の最大単語数
        #     n           = 1,                # いくつの返答を生成するか
        #     # stop        = None,             # 指定した単語が出現した場合、文章生成を打ち切る
        #     # temperature = 0,                # 出力する単語のランダム性（0から2の範囲） 0であれば毎回返答内容固定
        # )

        # # 応答
        # translate_text = res.choices[0].message.content

        # self.logger.debug(translate_text)

        # # ChatGPTからの文章をクリーン-> 必要があれば追加していく
        # clean_text = translate_text.replace(')', '').replace('\n\n', '\n')

        # self.logger.debug(clean_text)
        # return clean_text


# ----------------------------------------------------------------------------------
# メインメソッド カプセル化

    # @debug_logger_decorator
    async def chatgpt_translator(self, before_text_file, full_instructions):
        '''
        before_text_file-> 分割された翻訳前のテキストファイル
        translate_file-> 翻訳指示書ファイル（Excelファイル）
        '''
        self.logger.debug("翻訳処理開始")
        before_text_file = self.text_read(before_text_file)
        self.logger.debug("pickleファイルの読み込み開始")
        full_instructions = self.pickle_read()
        self.logger.debug(full_instructions)

        # 非同期処理した部分のみ非同期実行
        translated_text = await self.chatgpt_request(before_text_file, full_instructions)

        return translated_text


# ----------------------------------------------------------------------------------