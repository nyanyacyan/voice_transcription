# coding: utf-8
# ----------------------------------------------------------------------------------
# chatgpt翻訳リクエストクラス
# 2023/2/25 制作

#---バージョン---
# Python==3.8.10
# ----------------------------------------------------------------------------------
import os,sys

import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox

# 自作モジュール
from chatgpt.data_division import ChatgptTextSplitSave
from chatgpt.dump_manager import DumpManager
from chatgpt.translation_request import TranslationRequest
from logger.debug_logger import Logger
from movie_to_audio.movie_to_audio import Mp4ToMp3
from movie_to_audio.youtube_url import YoutubeToMp3
from whisper.transcribe import WhisperTranscription


# ----------------------------------------------------------------------------------
#* 親クラスとして定義。これによって様々なComponentを入れられるようにする

class BaseFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.init_ui()


    def init_ui(self):
        '''
        「init_ui」は、GUIを作成するときの「空のキャンパス」を作成してるイメージ。
        これからここにどんどんGUIの機能を追加していく。
        raise NotImplementedErrorは初期化してるイメージ。
        '''
        raise NotImplementedError


# ----------------------------------------------------------------------------------


class YouTubeURLInput(BaseFrame):
    def init_ui(self):
        youtube_url_label = ttk.Label(self, text="YouTube URL")
        youtube_url_label.pack(side=tk.LEFT, padx=5)

        self.youtube_url_entry = ttk.Entry(self)
        self.youtube_url_entry.pack(fill=tk.X, expand=True)

    def get_url(self):
        return self.youtube_url_entry.get()


# ----------------------------------------------------------------------------------


class FilePicker(BaseFrame):
    # parentはコンポーネントの親要素に当たる部分をもらわないと行けない
    # parentの親要素はTkWindow、その他のフレームなど→基本はmainにて（tk.Tk）が入る
    # これによって配置や継承されるスタイルが決まる
    def __init__(self, parent, file_type, *args, **kwargs):
        # parentはメイン部分で定義（tk.Tk）されるためそのまま引き継ぐ
        super().__init__(parent, *args, **kwargs)

        # parentとfile_typeはわかりやすく受け取るために書く
        # 拡張子を選択
        self.file_type = file_type
        self.init_ui()

#* 

    def init_ui(self):
        '''ファイルタイプに基づいたラベルとエントリー、選択ボタンのセットアップ'''
        file_label = ttk.Label(self, text=f"{self.file_type} file")
        file_label.pack(side=tk.LEFT, padx=5)

        self.file_path_entry = ttk.Entry(self)
        self.file_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        select_button = ttk.Button(self, text="Select", command=self.select_file)
        select_button.pack(side=tk.LEFT, padx=5)


# ----------------------------------------------------------------------------------
#* file_typeに応じたファイル選択ダイアログの開き方を決定


    def select_file(self):
        filetypes = [(f"{self.file_type.upper()} files", f"*.{self.file/type}")]
        file_path = filedialog.askopenfilename(filetypes=filetypes)
        if file_path:
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, file_path)


# ----------------------------------------------------------------------------------


    def get_file_path(self):
        return self.file_path_entry.get()


# ----------------------------------------------------------------------------------