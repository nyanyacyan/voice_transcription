# coding: utf-8
# ----------------------------------------------------------------------------------
# loggerクラス
# 2023/2/23 制作

#---バージョン---
# Python==3.8.10
# chatgptクラスの並行処理の実施-> 翻訳した後のディレクトリにテキスト保存-> 一つにまとめる
# ----------------------------------------------------------------------------------
import os
import glob
from dotenv import load_dotenv
import concurrent.futures

# 自作モジュール
from logger.debug_logger import Logger
from my_decorators.logging_decorators import debug_logger_decorator

from chatgpt.chatgpt_translator import ChatgptTranslator

load_dotenv()


class TranslationRequest:
    def __init__(self, api_key, debug_mode=False):
        # Loggerクラスを初期化
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode

        self.chatgpt_translator_inst = ChatgptTranslator(api_key)


    # @debug_logger_decorator
    def translate_and_save_file(self, before_file, tranlate_instruction, output_dir):
        ''' 処理のみ定義-> ファイルを読込-> 翻訳実行-> テキストファイルに書込

        file_path-> 分割された翻訳前のテキストファイル
        tranlate_instruction-> 翻訳指示書（Excelファイル）
        output_dir-> 翻訳が終わったテキストを格納するpath
        '''

        # ファイル名を取得
        base_name = os.path.basename(before_file)
        self.logger.debug(f"読込する分割されたファイル名: {base_name}")

        # 翻訳クラスの実行（実行時、API KEYが必要）
        translated_text = self.chatgpt_translator_inst.chatgpt_translator(before_file, tranlate_instruction)
        self.logger.info(f"受け取った翻訳内容: {translated_text}")

        # output_dir + base_name（元々のファイル名）することでパスにしてる
        output_path = os.path.join(output_dir, base_name)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(translated_text)
        
        self.logger.debug(output_path)
        return output_path
    


    # @debug_logger_decorator
    def translate_all_files(self, input_dir, output_dir, tranlate_instruction):
        '''  ディレクトリ全てのテキストファイルを読込→ 並列処理を定義→ 

        input_dir = translate_and_save_fileでの引数 file_path -> 翻訳前の元データ
        output_dir-> translate_and_save_fileでの引数（翻訳が終わったテキストを格納するpath）そのため位置引数はtranslatorより前になる。
        translator = translate_and_save_fileでの引数 tranlate_instruction -> 翻訳指示書（Excelファイル）
        '''

        # input_dir内の全てのテキストファイルのパスを検索してリストとして返す
        # os.path.joinによって特定のものを指定する
        # glob()によって一致した全てのファイルのフルパスをリストとして返す
        files = glob.glob(os.path.join(input_dir, '*.txt'))


        # with concurrent.futures.ThreadPoolExecutor() as executor:によって並列処理の準備をする（ThreadPoolExecutorのインスタンス化）
        with concurrent.futures.ThreadPoolExecutor() as executor:

            # 各ファイルに対してtranslate_and_save_file関数を処理する→あるファイル全てをexecutorによって並列処理する
            futures = [executor.submit(self.translate_and_save_file, file, tranlate_instruction, output_dir) for file in files]

            # concurrent.futures.as_completedにて完了通知をそれぞれの並列処理から受けることで、全ての処理が完了するのを待つ
            for future in concurrent.futures.as_completed(futures):
                print(f"パーツの翻訳処理完了 {future.result()}")

    # @debug_logger_decorator
    def merge_translated_files(self, output_dir, final_output_file):
        '''  ディレクトリにあるテキストファイルをリスト化してインデックスの順番に並び替え-> それを順番にテキストファイルにまとめていく
        
        output_dir-> output_dir-> translate_and_save_fileでの引数（翻訳が終わったテキストを格納するpath）そのため位置引数はtranslatorより前になる。
        translated_completed_file-> 最終のファイルパス（ファイル名）
        '''

        # 全ての翻訳されたテキストを取得してリストにしたものを名前の冒頭にあるインデックスでソートする。
        # sorted関数の2つ目の引数keyはソート要素
        # os.path.basename(x)は各ファイル（x）の名前取得
        # .split('_')[0]にて'.'にて分割して頭部分のみ抽出
        # intにて数値部分を整数に変換（ソートできるように変換）
        files = sorted(glob.glob(os.path.join(output_dir, '*.txt')), key=lambda x: int(os.path.basename(x).split('_')[0]))

        # final_output_fileに最後、書き込む
        # final_output_fileは最後にファイル名を指定する
        with open(final_output_file, 'w', encoding='utf-8') as output_file:

            # ソートされたテキストファイルのリストを一つ一つ読み込んで順番に入れ込んでいく。
            for file in files:

                # 各テキストファイルを読み取る。
                with open(file, 'r', encoding='utf-8') as infile:

                    # 読み込んだ内容を書き込んで最後に改行を入れる
                    output_file.write(infile.read() + '\n')


# # 使用例
# if __name__ == '__main__':
#     api_key = os.getenv('OPENAI_API_KEY')

#     input_dir = ''
#     output_dir = ''
#     final_output_file = ''

#     translation_req_class_inst = TranslationRequest(api_key=api_key)
#     translation_req_class_inst.translate_all_files(input_dir, output_dir)
#     translation_req_class_inst.merge_translated_files(output_dir, final_output_file)