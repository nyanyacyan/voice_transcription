# coding: utf-8
# ----------------------------------------------------------------------------------
# loggerクラス
# 2023/2/18 制作

#---バージョン---
# Python==3.8.10
# ----------------------------------------------------------------------------------
from openai import OpenAI

API_Key = "OPENAI_API_KEY"

class ChatgptTranslator:
    def chatgpt_translator(self):
        with open('whisper_write_file.txt', 'r', encoding='utf-8') as file:
            text = file.read()
        client = OpenAI(api_key=API_Key)

        completion = client.chat.completions.create(
            # モデルを選択
            model    = "gpt-3.5-turbo",
            
            # メッセージ
            messages  = [
                    {"role": "system", "content": f'You are a helpful assistant that translates to Japanese.'},
                    {"role": "user", "content": f'Translate the following text to Japanese :「{text}」. And Output only translated text'}
                    ] , 

            
            max_tokens  = 1024,             # 生成する文章の最大単語数
            n           = 1,                # いくつの返答を生成するか
            stop        = None,             # 指定した単語が出現した場合、文章生成を打ち切る
            temperature = 0,                # 出力する単語のランダム性（0から2の範囲） 0であれば毎回返答内容固定
        )

        # 応答
        response = completion.choices[0].message.content

        with open('chatgpt_write_file.txt', 'w', encoding='utf-8') as output_file:
            output_file.write(response)