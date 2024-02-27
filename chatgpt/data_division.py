# coding: utf-8
# ----------------------------------------------------------------------------------
# テキストを適正な大きさに分割するクラス
# 2023/2/18 制作

#---バージョン---
# Python==3.8.10
# ----------------------------------------------------------------------------------
import os
from transformers import GPT2Tokenizer

class ChatgptTextSplitSave:
    def chatgpt_text_split_save(self):
        file_path = "whisper_write_file.txt"
        block_size = 1500  # このバーを超えたらテキストファイルを変える。少し余力を持ったものにする
        separat_part = '\n'
        output_dir = "/Users/nyanyacyan/Desktop/ProgramFile/project_file/voice_transcription/chatgpt/data_division_box"

        tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        # 一つ一つを区切ってるパーツによって分解
        lines = text.split(separat_part)

        # 各ボックスの初期化
        blocks = []
        block = ''
        token_count = 0

        for line in lines:
            # lineにあるトークンをカウント
            t = len(tokenizer.encode(line))

            # トークンカウントが０以上（初期ではない）＋block_sizeを超えてしまったら新しくリストに追加する
            if token_count > 0 and block_size < (token_count + t):
                blocks.append(block)
                token_count = 0
                block = ''
            
            # トークンカウントを追加
            token_count += t

            # ブロックに区切れた部分を追加する（区切られたもの自体も追加）
            block += line + separat_part

        # 最後のblock_sizeに達してないものも追加（ここまでのものは全てblocksに追加されてるためない）
        if block:
            blocks.append(block)


            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            for i, block in enumerate(blocks):
                output_text = os.path.join(output_dir, f'{i+1}_text_block.txt')
                with open(output_text, 'w', encoding='utf-8') as output_file:
                    output_file.write(block)

                print(f"{output_text} 保存完了")
