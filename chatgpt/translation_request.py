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
import re
from dotenv import load_dotenv
import concurrent.futures
from tqdm import tqdm

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


    def translate_and_save_file(self, before_file, translate_instruction, output_dir):
        ''' 処理のみ定義-> ファイルを読込-> 翻訳実行-> テキストファイルに書込

        file_path-> 分割された翻訳前のテキストファイル
        translate_instruction-> 翻訳指示書（Excelファイル）
        output_dir-> 翻訳が終わったテキストを格納するpath
        '''

        # ファイル名を取得
        self.logger.debug("単品、並行処理スタート")
        base_name = os.path.basename(before_file)
        self.logger.debug(f"読込する分割されたファイル名: {base_name}")

        # 翻訳クラスの実行（実行時、API KEYが必要）
        translated_text = self.chatgpt_translator_inst.handle_request(before_file, translate_instruction)
        self.logger.debug(f"受け取った翻訳内容: {translated_text}")

        # output_dir + base_name（元々のファイル名）することでパスにしてる
        output_path = os.path.join(output_dir, base_name)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(translated_text)

        self.logger.debug(output_path)
        self.logger.debug("並行処理完了")

        return output_path





    def translate_all_files(self, input_dir, output_dir, translate_instruction):
        '''  ディレクトリ全てのテキストファイルを読込→ 並列処理を定義→

        input_dir = translate_and_save_fileでの引数 file_path -> 翻訳前の元データ
        output_dir-> translate_and_save_fileでの引数（翻訳が終わったテキストを格納するpath）そのため位置引数はtranslatorより前になる。
        translator = translate_and_save_fileでの引数 translate_instruction -> 翻訳指示書（Excelファイル）
        '''

        # input_dir内の全てのテキストファイルのパスを検索してリストとして返す
        # os.path.joinによって特定のものを指定する
        # glob()によって一致した全てのファイルのフルパスをリストとして返す
        files = glob.glob(os.path.join(input_dir, '*.txt'))
        self.logger.debug(f"files: {files}")


        # with concurrent.futures.ThreadPoolExecutor() as executor:によって並列処理の準備をする（ThreadPoolExecutorのインスタンス化）
        with concurrent.futures.ThreadPoolExecutor() as executor:

            # 各ファイルに対してtranslate_and_save_file関数を処理する→存在するファイル全てをexecutorによって並列処理する
            futures = [executor.submit(self.translate_and_save_file, file, translate_instruction, output_dir) for file in files]

            processed_count = 0

            # concurrent.futures.as_completedにて完了通知をそれぞれの並列処理から受けることで、全ての処理が完了するのを待つ
            self.logger.debug("並行処理スタート")

            try:
                for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), ncols=100, desc="ChatGPTからの返答"):

                    self.logger.debug(future)

                try:
                    result = future.result()
                    if not result or result.isspace():
                        self.logger.error(f"ChatGPTのレスポンスが期待してるものを返してない可能性があります（明らかに文字数が少ない）")

                    else:
                        self.logger.debug("翻訳処理完了")
                        processed_count += 1

                except Exception as e:
                    self.logger.error(f"翻訳処理中にエラーが発生しました: {e}")

            except Exception as e:
                self.logger.error(f"並行処理の監視中にエラーが発生しました: {e}")




    def merge_translated_files(self, output_dir, final_output_file):
        '''  テキストファイルにまとめる処理
        ディレクトリにあるテキストファイルをリスト化してインデックスの順番に並び替え-> それを順番にテキストファイルにまとめていく
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


    def delete_text_files(self, data_division_box, translate_after_box):
        division_text_files = glob.glob(os.path.join(data_division_box, '*.txt'))
        after_text_files = glob.glob(os.path.join(translate_after_box, '*.txt'))

        if not division_text_files:
            self.logger.error(f"ファイルが見つかりません: {e}")
        else:
            for file_path in division_text_files:
                try:
                    os.remove(file_path)
                    self.logger.debug(f"{file_path} を全て削除")
                except Exception as e:
                    self.logger.error(f"{file_path} の削除中にエラーが発生しました: {e}")

        if not division_text_files:
            self.logger.error(f"ファイルが見つかりません: {e}")
        else:
            for file_path in after_text_files:
                try:
                    os.remove(file_path)
                    self.logger.debug(f"{file_path} を削除しました。")

                except Exception as e:
                    self.logger.error(f"{file_path} の削除中にエラーが発生しました: {e}")

