# chatgpt翻訳リクエストクラス
# 2023/2/26 制作

#---バージョン---
# Python==3.8.10
# ----------------------------------------------------------------------------------
import os,sys

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

# 自作モジュール
from movie_to_audio.youtube_url_to_wav import YoutubeToMp3
from movie_to_audio.movie_to_audio import Mp4ToMp3

from whisper.transcribe import WhisperTranscription
from chatgpt.data_division import ChatgptTextSplitSave
from chatgpt.translation_request import TranslationRequest
from chatgpt.dump_manager import DumpManager

# デコレーター
# from my_decorators.logging_decorators import debug_logger_decorator
# from my_decorators.error_handling_decorators import error_handling_decorator


api_key = os.getenv('OPENAI_API_KEY')

def error_message(message):
    error_message_label.conging(text=message)


def mp４_dirlog_click():
    '''
    音声データを抽出
    '''
    mp4_path = filedialog.askopenfilename(filetypes=[("MP4.files", "*.mp4")])
    if mp4_path:
        mp4_path_entry.set(mp4_path)  # StringVarオブジェクトにパスを設定
        os.environ['MP4_PATH'] = mp4_path
    else:
        messagebox.showerror("エラー", "選択されたファイルが mp4 形式ではありません。")


def mp3_dirlog_click():
    '''
    pathを取得するだけ
    '''
    mp3_path = filedialog.askopenfilename(filetypes=[("MP3.files", "*.mp3")])
    if mp3_path:
        mp3_path_entry.set(mp3_path)  # StringVarオブジェクトにパスを設定
        os.environ['MP3_PATH'] = mp3_path
    else:
        messagebox.showerror("エラー", "選択されたファイルが mp3 形式ではありません。")



def instructions_update_click():
    '''
    辞書更新
    '''
    translate_file = '翻訳指示ファイル.xlsx'
    dump_manager_inst = DumpManager()
    dump_manager_inst.write_pickle_file(translate_file)


def youtube_process():
    '''
    '''
    try:
        youtube_url = youtube_url_entry.get()
        youtube_to_mp3_inst = YoutubeToMp3(youtube_url)
        audio_file = youtube_to_mp3_inst.youtube_to_mp3()
        whisper_transcription_inst = WhisperTranscription(audio_file)
        whisper_transcription_inst.whisper_transcription()
        chatgpt_text_split_save_inst = ChatgptTextSplitSave()
        chatgpt_text_split_save_inst.chatgpt_text_split_save()

        input_dir = '/Users/nyanyacyan/Desktop/ProgramFile/project_file/voice_transcription/chatgpt/data_division_box'
        output_dir = '/Users/nyanyacyan/Desktop/ProgramFile/project_file/voice_transcription/chatgpt/translate_after_box'
        final_output_file = '/Users/nyanyacyan/Desktop/ProgramFile/project_file/voice_transcription/translated_completed.txt'
        tranlate_instruction = '/Users/nyanyacyan/Desktop/ProgramFile/project_file/voice_transcription/翻訳指示ファイル.xlsx'

        translation_req_class_inst = TranslationRequest(api_key=api_key)
        translation_req_class_inst.translate_all_files(input_dir, output_dir, tranlate_instruction)
        translation_req_class_inst.merge_translated_files(output_dir, final_output_file)

    except TypeError as e:
        error_message("テキストファイル生成ができてない可能性があります。{e}")

    except Exception as e:
        error_message("処理中にエラーが発生しました。{e}")

    

def mp4_process():
    '''
    '''
    mp4_path = mp4_path_entry.get()
    mp4_to_mp3_inst = Mp4ToMp3(mp4_path)
    audio_file = mp4_to_mp3_inst.mp4_to_mp3()
    whisper_transcription_inst = WhisperTranscription(audio_file)
    whisper_transcription_inst.whisper_transcription()
    chatgpt_text_split_save_inst = ChatgptTextSplitSave()
    chatgpt_text_split_save_inst.chatgpt_text_split_save()

    input_dir = '/Users/nyanyacyan/Desktop/ProgramFile/project_file/voice_transcription/chatgpt/data_division_box'
    output_dir = '/Users/nyanyacyan/Desktop/ProgramFile/project_file/voice_transcription/chatgpt/translate_after_box'
    final_output_file = '/Users/nyanyacyan/Desktop/ProgramFile/project_file/voice_transcription/translated_completed.txt'
    tranlate_instruction = '/Users/nyanyacyan/Desktop/ProgramFile/project_file/voice_transcription/翻訳指示ファイル.xlsx'

    translation_req_class_inst = TranslationRequest(api_key=api_key)
    translation_req_class_inst.translate_all_files(input_dir, output_dir, tranlate_instruction)
    translation_req_class_inst.merge_translated_files(output_dir, final_output_file)

def mp3_process():
    '''
    '''
    audio_file = mp3_path_entry.get()
    whisper_transcription_inst = WhisperTranscription(audio_file)
    whisper_transcription_inst.whisper_transcription()
    chatgpt_text_split_save_inst = ChatgptTextSplitSave()
    chatgpt_text_split_save_inst.chatgpt_text_split_save()

    input_dir = '/Users/nyanyacyan/Desktop/ProgramFile/project_file/voice_transcription/chatgpt/data_division_box'
    output_dir = '/Users/nyanyacyan/Desktop/ProgramFile/project_file/voice_transcription/chatgpt/translate_after_box'
    final_output_file = '/Users/nyanyacyan/Desktop/ProgramFile/project_file/voice_transcription/translated_completed.txt'
    tranlate_instruction = '/Users/nyanyacyan/Desktop/ProgramFile/project_file/voice_transcription/翻訳指示ファイル.xlsx'

    translation_req_class_inst = TranslationRequest(api_key=api_key)
    translation_req_class_inst.translate_all_files(input_dir, output_dir, tranlate_instruction)
    translation_req_class_inst.merge_translated_files(output_dir, final_output_file)



def submit_click():
    youtube_url = youtube_url_entry.get()
    mp4_path = mp4_path_entry.get()
    mp3_path = mp3_path_entry.get()

    print(f"youtube_url: {youtube_url}, mp4_path: {mp4_path}, mp3_path: {mp3_path}")

    if not youtube_url and not mp4_path and not mp3_path:
        messagebox.showerror("エラー", "YouTubeのURL、mp4、mp3のいずれかの入力（選択）がされてません。")
    
    
    if youtube_url:
        youtube_process()
    if mp4_path:
        mp4_process()
    if mp3_path:
        mp3_process()




if __name__ == '__main__':
    '''
    window作成→フレーム作成→ラベル作成→エントリー作成→ボタン作成
    '''


    # Window作成
    window = Tk()
    window.title("翻訳アプリ")
    window.geometry('500x320')


    # YouTubeフレーム作成
    youtube_frame = ttk.Frame(window, padding=(10, 20, 0, 10))
    youtube_frame.grid(row=0, column=0, sticky=W)

    # youtubeのURLを貼り付け箇所のラベル
    # padding=(10, 10)この部分がラベルの余白を設定。　左側「左右」、右側「上下」の余白
    youtube_url_label = ttk.Label(youtube_frame, text="YouTube URL", width=10, padding=(10, 10))
    youtube_url_label.grid(row=0, column=0)

    # youtubeのURL貼り付けエントリー
    youtube_url_entry = ttk.Entry(youtube_frame, width=25)
    youtube_url_entry.grid(row=0, column=1, padx=(10, 0))



    # mp４フレーム作成
    mp4_frame = ttk.Frame(window, padding=(10, 3, 0, 10))
    mp4_frame.grid(row=1, column=0, sticky=W)

    # mp４のpathを貼り付け箇所のラベル
    mp4_path_label = ttk.Label(mp4_frame, text="       mp4", width=10, padding=(10, 10))
    mp4_path_label.grid(row=1, column=0)

    # mp４のpath貼り付けエントリー
    mp4_entry_var = StringVar()
    mp4_path_entry = ttk.Entry(mp4_frame, textvariable=mp4_entry_var , width=25)
    mp4_path_entry.grid(row=1, column=1, padx=(10, 0))

    # mp4ボタン作成
    mp4_button = ttk.Button(mp4_frame, text="選択", width=2.5, command=mp4_dirlog_click)
    mp4_button.grid(row=1, column=2, padx=(8, 0))




    # mp3フレーム作成
    mp3_frame = ttk.Frame(window, padding=(10, 3, 0, 10))
    mp3_frame.grid(row=2, column=0, sticky="W")

    # mp４のpathを貼り付け箇所のラベル
    mp3_path_label = ttk.Label(mp3_frame, text="       mp3", width=10, padding=(10, 10))
    mp3_path_label.grid(row=2, column=0)

    # mp４のpath貼り付けエントリー
    mp3_entry_var = StringVar()
    mp3_path_entry = ttk.Entry(mp3_frame, textvariable=mp3_entry_var, width=25)
    mp3_path_entry.grid(row=2, column=1, padx=(10, 0))

    # mp3ボタン作成
    mp3_button = ttk.Button(mp3_frame, text="選択", width=2.5, command=mp3_dirlog_click)
    mp3_button.grid(row=2, column=2, padx=(8, 0))

    # error_messageフレーム作成
    error_frame = ttk.Frame(window, padding=10)
    error_frame.grid(row=3, column=0)

    # error_messageラベル作成
    error_message_label = ttk.Label(error_frame, text="", foreground="red")
    error_message_label.grid(row=3, column=0)


    # dumpフレーム作成
    dump_frame = ttk.Frame(window, padding=(60, 0, 10, 0))
    dump_frame.grid(row=4, column=0)
    
    # dumpボタン作成
    update_button = ttk.Button(dump_frame, text="辞書更新", command=instructions_update_click)
    update_button.grid(row=4, column=0, padx=5)



    # Runningフレーム作成
    running_frame = ttk.Frame(window, padding=(60, 15, 10, 0))
    running_frame.grid(row=5, column=0, )


    # runningボタン作成
    submit_button = ttk.Button(running_frame, text="翻訳開始", command=submit_click)
    submit_button.grid(row=5, column=0, padx=20)


    # cancelボタン作成
    cancel_button = ttk.Button(running_frame, text="閉じる", command=quit)
    cancel_button.grid(row=5, column=1, padx=20)

    window.mainloop()