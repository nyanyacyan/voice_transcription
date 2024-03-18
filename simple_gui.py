# GUI動かしてmainで動かすクラス
# 2023/2/26 制作

#! 非同期処理
# ----------------------------------------------------------------------------------
import os
import asyncio
import threading
from tkinter import *
from tkinter import filedialog, messagebox, ttk

from dotenv import load_dotenv

# 自作モジュール
from chatgpt.data_division import ChatgptTextSplitSave
from chatgpt.dump_manager import DumpManager
from chatgpt.translation_request import TranslationRequest
from logger.debug_logger import Logger
from movie_to_audio.movie_to_audio import Mp4ToMp3
from movie_to_audio.youtube_url import YoutubeToMp3
from whisper.transcribe import WhisperTranscription

# Loggerクラスを初期化
debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
logger_instance = Logger(__name__, debug_mode=debug_mode)
logger = logger_instance.get_logger()
debug_mode = debug_mode


load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

def error_message(message):
    error_message_label.config(text=message)


def instructions_update_click():
    '''
    辞書更新
    '''
    translate_file = '翻訳指示ファイル.xlsx'
    dump_manager_inst = DumpManager()
    dump_manager_inst.find_pickle_file()
    dump_manager_inst.dataframe_updated(translate_file)
    dump_manager_inst.write_pickle_file(translate_file)
    messagebox.showinfo("更新完了", "更新が完了しました。")


async def youtube_process():
    '''
    '''
    input_dir = 'chatgpt/data_division_box'
    output_dir = 'chatgpt/translate_after_box'
    final_output_file = 'results_text_box/translated_completed.txt'
    translate_instruction = '翻訳指示ファイル.xlsx'
    data_division_box = 'chatgpt/data_division_box'
    translate_after_box = 'chatgpt/translate_after_box'

    try:
        youtube_url = youtube_url_entry.get()
        youtube_to_mp3_inst = YoutubeToMp3(youtube_url)
        audio_file = await youtube_to_mp3_inst.find_youtube_file_fullpath()
        logger.debug("文字起こし開始")
        whisper_transcription_inst = WhisperTranscription(audio_file)
        await whisper_transcription_inst.whisper_transcription()
        chatgpt_text_split_save_inst = ChatgptTextSplitSave()
        await chatgpt_text_split_save_inst.chatgpt_text_split_save()
        translation_req_class_inst = TranslationRequest(api_key=api_key)
        await translation_req_class_inst.translate_all_files(input_dir, output_dir, translate_instruction)
        await translation_req_class_inst.merge_translated_files(output_dir, final_output_file)
        translation_req_class_inst.delete_text_files(data_division_box, translate_after_box)
        messagebox.showinfo("完了通知", "翻訳が完了しました。\ntranslated_completed.txtをご覧ください。")

    except TypeError as e:
        logger.error(f"TypeError: {e}")
        error_message(f"テキストファイル生成ができてない可能性があります。{e}")

    except Exception as e:
        logger.error(f"error: {e}")
        error_message(f"処理中にエラーが発生しました。{e}")



async def mp4_process():
    input_dir = 'chatgpt/data_division_box'
    output_dir = 'chatgpt/translate_after_box'
    final_output_file = 'translated_completed.txt'
    translate_instruction = '翻訳指示ファイル.xlsx'
    data_division_box = 'chatgpt/data_division_box'
    translate_after_box = 'chatgpt/translate_after_box'
    try:
        mp4_path = mp4_path_entry.get()
        mp4_to_mp3_inst = Mp4ToMp3(mp4_path)
        audio_file = await mp4_to_mp3_inst.mp4_to_mp3()
        logger.debug(audio_file)
        logger.debug("文字起こし開始")
        whisper_transcription_inst = WhisperTranscription(audio_file)
        await whisper_transcription_inst.whisper_transcription()
        chatgpt_text_split_save_inst = ChatgptTextSplitSave()
        await chatgpt_text_split_save_inst.chatgpt_text_split_save()
        translation_req_class_inst = TranslationRequest(api_key=api_key)
        await translation_req_class_inst.translate_all_files(input_dir, output_dir, translate_instruction)
        await translation_req_class_inst.merge_translated_files(output_dir, final_output_file)
        translation_req_class_inst.delete_text_files(data_division_box, translate_after_box)
        messagebox.showinfo("完了通知", "翻訳が完了しました。\ntranslated_completed.txtをご覧ください。")

    except TypeError as e:
        logger.error(f"TypeError: {e}")
        error_message(f"テキストファイル生成ができてない可能性があります。{e}")

    except Exception as e:
        logger.error(f"error: {e}")
        error_message(f"処理中にエラーが発生しました。{e}")


async def mp3_process():
    '''
    '''
    input_dir = 'chatgpt/data_division_box'
    output_dir = 'chatgpt/translate_after_box'
    final_output_file = 'translated_completed.txt'
    translate_instruction = '翻訳指示ファイル.xlsx'

    try:
        audio_file = mp3_path_entry.get()
        whisper_transcription_inst = WhisperTranscription(audio_file)
        await whisper_transcription_inst.whisper_transcription()
        chatgpt_text_split_save_inst = ChatgptTextSplitSave()
        await chatgpt_text_split_save_inst.chatgpt_text_split_save()
        translation_req_class_inst = TranslationRequest(api_key=api_key)
        await translation_req_class_inst.translate_all_files(input_dir, output_dir, translate_instruction)
        await translation_req_class_inst.merge_translated_files(output_dir, final_output_file)
        messagebox.showinfo("完了通知", "翻訳が完了しました。\ntranslated_completed.txtをご覧ください。")

    except TypeError as e:
        logger.error(f"TypeError: {e}")
        error_message(f"テキストファイル生成ができてない可能性があります。{e}")

    except Exception as e:
        logger.error(f"error: {e}")
        error_message(f"処理中にエラーが発生しました。{e}")


async def submit_click():
    youtube_url = youtube_url_entry.get()
    mp3_path = mp3_path_entry.get()
    mp4_path = mp4_path_entry.get()

    logger.debug(f"youtube_url: {youtube_url}, mp4_path: {mp4_path}, mp3_path: {mp3_path}")

    if not youtube_url and not mp4_path and not mp3_path:
        messagebox.showerror("エラー", "YouTubeのURL、mp4、mp3のいずれかの入力（選択）がされてません。")

    if youtube_url:
        await youtube_process()
    if mp4_path:
        await mp4_process()
    if mp3_path:
        await mp3_process()


# Tkinter内で非同期処理を実行するための関数
def run_async_task():
    # 新しいイベントループ（司令塔）を作成→非同期タスクを実行する準備
    loop = asyncio.new_event_loop()

    # このイベントループを使って、非同期タスクを管理するように指示を出してる。
    asyncio.set_event_loop(loop)

    # submit_clickをeventループに追加それが完了するまで実行
    loop.run_until_complete(submit_click())

# 新しいスレッドを作成。
# スレッドとは、プログラムの中で別の作業を同時に行うことができる小さな作業員のこと
# target=run_async_task→新しい作業員（スレッド）に、run_async_task関数を実行してもらうという意味
# .start()は開始
def on_button_click():
    threading.Thread(target=run_async_task).start()



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


    def mp４_dirlog_click():
        '''
        音声データを抽出
        '''
        mp4_path = filedialog.askopenfilename(filetypes=[("MP4.files", "*.mp4")])

        # もしmp4_pathがなかったらリターン（何もせず抜ける）を返す
        if not mp4_path:
            return

        # .lower()-> 全てを小文字にする mp4の部分を大文字が混ざってしまう可能性があるため
        # .endswith('.mp4')-> 拡張子部分を取得して引数に指定されてるものになってるか確認
        # もし拡張子がmp4でなかったらエラーメッセージを出す。
        if not mp4_path.lower().endswith('.mp4'):
            messagebox.showerror("エラー", "選択されたファイルが mp4 形式ではありません。")

        else:
            # 上記以外のものだったらパスを取得して反映
            mp4_entry_var.set(mp4_path)  # StringVarオブジェクトにパスを設定


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

    def mp3_dirlog_click():
        '''
        pathを取得するだけ
        '''
        mp3_path = filedialog.askopenfilename(filetypes=[("MP3.files", "*.mp3")])

        # もしmp3_pathがなかったらリターン（何もせず抜ける）を返す
        if not mp3_path:
            return

        # .lower()-> 全てを小文字にする　mp3の部分を大文字が混ざってしまう可能性があるため
        # .endswith('.mp3')-> 拡張子部分を取得して引数に指定されてるものになってるか確認
        # もし拡張子がmp3でなかったらエラーメッセージを出す。
        if not mp3_path.lower().endswith('.mp3'):
            messagebox.showerror("エラー", "選択されたファイルが mp3 形式ではありません。")

        else:
            # 上記以外のものだったらパスを取得して反映
            mp3_entry_var.set(mp3_path)  # StringVarオブジェクトにパスを設定

    # mp3ボタン作成
    mp3_button = ttk.Button(mp3_frame, text="選択", width=2.5, command=mp3_dirlog_click)
    mp3_button.grid(row=2, column=2, padx=(8, 0))



    # error_messageフレーム作成
    error_frame = ttk.Frame(window, padding=10, width=480)
    error_frame.grid(row=3, column=0)

    # error_messageラベル作成
    error_message_label = ttk.Label(error_frame, text="", foreground="red", wraplength=480, font=("Helvetica", 10))
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
    submit_button = ttk.Button(running_frame, text="翻訳開始", command=on_button_click)
    submit_button.grid(row=5, column=0, padx=20)


    # cancelボタン作成
    cancel_button = ttk.Button(running_frame, text="閉じる", command=quit)
    cancel_button.grid(row=5, column=1, padx=20)

    window.mainloop()