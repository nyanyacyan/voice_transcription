# coding: utf-8
# ----------------------------------------------------------------------------------
# dumpクラス
# 2023/2/24 制作

#---バージョン---
# Python==3.8.10

# ---流れ---
# GUIで「辞書の更新」をクリック-> 始動-> 更新
# ----------------------------------------------------------------------------------
import os
from dotenv import load_dotenv
import pickle
import pandas as pd

from logger.debug_logger import Logger
from my_decorators.logging_decorators import debug_logger_decorator

load_dotenv()

class DumpManager:
    '''  翻訳指示書を読込。全ての指示を１つに。

    translate_file-> 指示書をまとめたExcelファイル
    
    '''
    def __init__(self, pickle_file='/Users/nyanyacyan/Desktop/ProgramFile/project_file/voice_transcription/data/excel_data.pickle'):
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
        try:
            with open(self.pickle_file, 'rb') as handle:
                self.logger.debug("pickleファイル発見。解析開始")
                # 解析開始
                existing_data = pickle.load(handle)
            return existing_data

        except EOFError:
            # もしファイルが空の場合に処理する
            # もしpickle_fileがなかったら新しいデータフレームを作成
            self.logger.debug("ファイルが空。新しいデータフレーム作成開始")
            existing_data = pd.DataFrame(columns=['from', 'to', 'instruction'])
            return existing_data


    def dataframe_updated(self, translate_file):
        existing_data = self.find_pickle_file()  # 既存データ

        # Excelファイルにあるデータをデータフレームに入れ込む（まだpickle_fileには書き込まれてない）
        new_data = pd.read_excel(translate_file, usecols=['from', 'to'])  # 新しいデータ

        # 　axisパラメーターは「.apply」メソッド時に使われる　axis=1は上から順番に行のデータを取得してる-> from列とto列の値を取得
        # .applyは各列（axis=0）各行（axis=1）のデータを取得する
        self.logger.debug("和訳を指定する文章を作成開始（３列目）")
        new_data['instruction'] = new_data.apply(lambda row: f'上記の文章の中に「{row["from"]}」という文章があった場合には「{row["to"]}」と和訳を指定してください。', axis=1)
        self.logger.debug("和訳を指定する文章を作成完了")

        updated_data = existing_data.copy()

        # .iterrows()は１行ずつにアクセス
        self.logger.debug("和訳を指定する文章を作成完了")
        for _, new_row in new_data.iterrows():
            # もし既存データの中に新しいデータの中に同じ値があったら
            if new_row['from'] in existing_data['from'].values:
                # 既存データと新しいデータが同じデータがあった場合、既存データに新しいデータの'to'と'instruction'に入れ替える
                existing_data.loc[existing_data['from'] == new_row['from'], ['to', 'instruction']] = new_row[['to', 'instruction']]

            else:
                # 同じではないものはそのまま既存データに追加する
                # new_rowは新しい行を選択
                # ignore_index=Trueは既存のindexルールがあっても無視して新しいindexを自動で割り当てる
                updated_data = pd.concat([updated_data, pd.DataFrame([new_row])], ignore_index=True)


        return updated_data


    def write_pickle_file(self, translate_file):
        updated_data = self.dataframe_updated(translate_file)

        updated_data.reset_index(drop=True, inplace=True)

        pd.set_option('display.max_columns', None)


        
        print(updated_data['instruction'])

        # 'wb'はバイナリ書込モード
        # もしpickle_fileがなければ新規作成
        with open(self.pickle_file, 'wb') as handle:
            pickle.dump(updated_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
