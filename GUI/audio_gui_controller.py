# coding: utf-8
# ----------------------------------------------------------------------------------
# chatgpt翻訳リクエストクラス
# 2023/2/25 制作

#---バージョン---
# Python==3.8.10
# ----------------------------------------------------------------------------------
import os,sys

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

# 自作モジュール
from movie_to_audio.youtube_url_to_wav import YoutubeDL
from chatgpt.dump_manager import DumpManager

class AudioGuiController:
    def __init__(self):
        youtube_url_inst = YoutubeDL()
        dump_manager_inst = DumpManager()

    def youtube_url_click(self):
        '''
        音声データを抽出
        '''



    def mp4_dirlog_click(self):
        '''
        音声データを抽出
        '''
        mp4_data_dir = os.path.asbpath(os.path.dirname(__file__))
        mp4_data_path = filedialog.askdirectory(initialdir= mp4_data_dir)
        # entry1.set(mp4_data_path)  # 参照ボタン
        


    def mp3_dirlog_click(self):
        '''
        pathを取得するだけ
        '''
        mp3_data_dir = os.path.asbpath(os.path.dirname(__file__))
        mp3_data_path = filedialog.askdirectory(initialdir= mp3_data_dir)
        # entry2.set(mp3_data_path)  # 参照ボタン


    def instructions_update_click(self):
        '''
        '''



    def running_click(self):
        '''
        
        '''