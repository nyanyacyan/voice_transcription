# coding: utf-8
# ----------------------------------------------------------------------------------
# テキストを適正な大きさに分割するクラス
# 2023/2/18 制作

#! 非同期処理
# ----------------------------------------------------------------------------------
import os, asyncio
from transformers import GPT2Tokenizer

# 自作モジュール
from logger.debug_logger import Logger


# ----------------------------------------------------------------------------------


class ChatgptTextSplitSave:
    def __init__(self, debug_mode=False):
        # Loggerクラスを初期化
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode


# ----------------------------------------------------------------------------------
# トークンをカウントすることだけに作成された関数

    def token_count(self):
        '''
        命令部分のみ800トークン
        １つの翻訳指示で70トークン
        送信トークンの上限は16,384トークン（約12,500字）
        ChatGPTからのレスポンスの最大トークン数は4000（テキスト部分の最大値→日本語だと3000）
        リクエスト最大値（15000）- 命令文のみ（800）- 翻訳テキスト（2500）
        '''
        tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        before_file_path = "results_text_box/whisper_write_file.txt"
        sentence_file_path = "results_text_box/chatgpt_to_sentence.txt"

        self.logger.debug("総トークン数カウント")
        with open(before_file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        before_full_token = len(tokenizer.encode(text))

        print(f"full_token_count: {before_full_token}")

        self.logger.debug("命令文、総トークン数")
        with open(sentence_file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        sentence_full_token = len(tokenizer.encode(text))
        print(f"sentence_full_token: {sentence_full_token}")


# ----------------------------------------------------------------------------------
# 非同期処理で書き込み

    async def chatgpt_text_split_save(self):
        file_path = "results_text_box/whisper_write_file.txt"
        block_size = 2500  # このバーを超えたらテキストファイルを変える。少し余力を持ったものにする
        separat_part = '\n'
        output_dir = "chatgpt/data_division_box"

        tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

        self.logger.debug("分割処理スタート")

        loop = asyncio.get_running_loop()

        # 非同期処理で書き込み（書き込み部分は同期処理）
        text = await loop.run_in_executor(None, self.read_file, file_path)

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

                # 非同期処理で書き込み（書き込み部分は同期処理）
                await loop.run_in_executor(None, self.write_to_file, output_text, block)
                self.logger.debug(f"{output_text} 保存完了")


# ----------------------------------------------------------------------------------
# 同期処理のメリットを活かすため同期処理で記述
# 同期処理は非同期処理の下にまとめることによってわかりやすくなる
#! 非同期処理に同期処理をまとめるのは基本「I/O処理」に限る

    def read_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()


# ----------------------------------------------------------------------------------
# 同期処理のメリットを活かすため同期処理で記述
# 同期処理は非同期処理の下にまとめることによってわかりやすくなる
#! 非同期処理に同期処理をまとめるのは基本「I/O処理」に限る

    def write_to_file(self, filepath, content):
        with open(filepath, 'w', encoding='utf-8') as output_file:
            output_file.write(content)

# ----------------------------------------------------------------------------------
