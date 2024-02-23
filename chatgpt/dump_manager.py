# coding: utf-8
# ----------------------------------------------------------------------------------
# dumpクラス
# 2023/2/18 制作

#---バージョン---
# Python==3.8.10
# ----------------------------------------------------------------------------------
import os
import pickle
import pandas as pd

# 自作モジュール
from logger.debug_logger import Logger
from my_decorators.logging_decorators import debug_logger_decorator

class DumpManager:
    '''  翻訳指示書を読込。全ての指示を１つに。

    translate_file-> 指示書をまとめたExcelファイル
    
    '''
    def __init__(self, pickle_file='excel_data.pickle', debug_mode=False):
        '''
        pickle_file-> pdにて保存して同じデータがないかを確認する場所
        '''
        self.pickle_file = pickle_file

        # Loggerクラスを初期化
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode


    def find_pickle_file(self):
        # pickle_fileがあるかを確認
        if os.path.exists(self.pickle_file):
            # 'rb'はバイナリ読込モード
            with open(self.pickle_file, 'rb') as handle:
                # 解析開始
                current_data = pickle.load(handle)
            return current_data

        else:
            # もしpickle_fileがなかったら新しいデータフレームを作成
            current_data = pd.DataFrame(columns=['from', 'to', 'instruction'])
            return current_data


    def dataframe_updated(self, translate_file):
        current_data = self.find_pickle_file(self.pickle_file)

        # Excelファイルにあるデータをデータフレームに入れ込む（まだpickle_fileには書き込まれてない）
        new_data = pd.read_excel(translate_file, usecols=['from', 'to'])

        # 　axisパラメーターは「.apply」メソッド時に使われる　axis=1は「列方向」に入れ込みたい-> fromとtoを入れている
        new_data['instruction'] = new_data.apply(lambda row: f'\n文章「{row["from"]}」は「{row["to"]}」と和訳\n', axis=1)

        # .set_index('from')部分をindexとする
        # .combine_firstは古い情報を確認して新しいものだけを選択（補完）してくれてる
        # .reset_index()これにより全てのデータをまとめる
        for _, new_row in new_data.iterrows():
            if new_row['from'] in current_data['from'].values:
                current_data.loc[current_data['from'] == new_row['from'], ['to', 'instruction']] = new_row[['to', 'instruction']]

            else:
                current_data = current_data.append(new_row, ignore_index=True)

        return current_data


    def write_pickle_file(self, translate_file):
        current_data = self.dataframe_updated(translate_file)
        # 'wb'はバイナリ書込モード
        # もしpickle_fileがなければ新規作成
        with open(self.pickle_file, 'wb') as handle:
            pickle.dump(current_data, handle, protocol=pickle.HIGHEST_PROTOCOL)


    def instructions_joint_text(self, translate_file):

        ここでpickle_fileに書き込まれたものを３列目のinstructionだけを抽出してテキストにする
        これをChatGPT側で読み込んで命令文にできるようにする。

        updated_data = self.dataframe_updated(translate_file)
        full_instructions = "".join(updated_data['instruction'].tolist())

        return full_instructions
    

    def dump_manager():
        '''  メインメソッド
        '''