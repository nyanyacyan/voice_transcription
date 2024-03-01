from simple_gui import mp3_entry_var


from tkinter import filedialog, messagebox


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