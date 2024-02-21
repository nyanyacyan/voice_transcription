# coding: utf-8
# ----------------------------------------------------------------------------------
# loggerクラス
# 2023/2/18 制作

#---バージョン---
# Python==3.8.10
# ----------------------------------------------------------------------------------
from openai import OpenAI
import os
from dotenv import load_dotenv
import pandas as pd

# 自作モジュール
# from logger.debug_logger import Logger

load_dotenv()

API_Key = os.getenv("OPENAI_API_KEY")

class ChatgptTranslator:
    # def __init__(self, debug_mode=False):
    #     # Loggerクラスを初期化
    #     debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
    #     self.logger_instance = Logger(__name__, debug_mode=debug_mode)
    #     self.logger = self.logger_instance.get_logger()
    #     self.debug_mode = debug_mode


    def chatgpt_translator(self):
        client = OpenAI(api_key=API_Key)



        # ここのファイルを複数読み込めるようにする
        # 読み込むテキストを定義
        with open('whisper_write_file.txt', 'r', encoding='utf-8') as file:
            text = file.read()

        # 翻訳指示ファイルを読み込む
        translate_file = '翻訳指示ファイル.xlsx'
        ja_translate_instruction = []

        df = pd.read_excel(translate_file, usecols=['from', 'to'])

        for index, row in df.iterrows():

            translate_part = row['from']
            ja_part = row['to']

            instruction_part = f'\n文章「{translate_part}」は「{ja_part}」と和訳\n'

            ja_translate_instruction.append(instruction_part)

        # 翻訳指示の内容を確認
        # self.logger.info(ja_translate_instruction)
        print(ja_translate_instruction)



        res = client.chat.completions.create(
            # モデルを選択
            model    = "gpt-3.5-turbo",
            
            # メッセージ
            messages  = [
                {"role": "system", "content": f'You are a helpful assistant that translates to Japanese.'},
                {"role": "user",
                "content": f"添付したテキストファイルを全て文章を和訳して全てを表示ほしい。「{text}」\n「添付したテキストファイル」に下記の文章があった場合には必ず指定した和訳に置き換えてください。{ja_translate_instruction}\n上記で指定した和訳が、ちゃんと反映してるかを確認してるかな？。"},
            ] ,

            
            max_tokens  = 4096,             # 生成する文章の最大単語数
            n           = 1,                # いくつの返答を生成するか
            # stop        = None,             # 指定した単語が出現した場合、文章生成を打ち切る
            # temperature = 0,                # 出力する単語のランダム性（0から2の範囲） 0であれば毎回返答内容固定
        )

        # 応答
        translate_text = res.choices[0].message.content
        clean_text = translate_text.replace(')', '')

        print(clean_text)


        with open('chatgpt_write_file.txt', 'w', encoding='utf-8') as output_file:
            output_file.write(clean_text)

if __name__ == '__main__':
    chatgpt_instance = ChatgptTranslator()
    chatgpt_instance.chatgpt_translator()