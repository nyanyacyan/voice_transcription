# coding: utf-8
# ----------------------------------------------------------------------------------
#* モジュールのみとして利用
# 2023/2/25 制作

#---バージョン---
# Python==3.8.10
# ----------------------------------------------------------------------------------
from tkinter import messagebox

class PopupMessageBox:
    @staticmethod
    def show_info(title, message):
        messagebox.showinfo(title, message)

    @staticmethod
    def show_warning(title, message):
        messagebox.showwarning(title, message)

    @staticmethod
    def show_error(title, message):
        messagebox.showerror(title, message)

    @staticmethod
    def ask_question(title, message):
        return messagebox.askquestion(title, message)  # 'yes' or 'no'
    # user_response = MessageBoxHelper.ask_question("確認", "このファイルを削除しますか？")

    # if user_response == 'yes':
    #     print("ユーザーは「はい」を選択しました。ファイルを削除します。")
    #     # ここにファイル削除の処理を追加
    # else:
    #     print("ユーザーは「いいえ」を選択しました。ファイル削除をキャンセルします。")


    @staticmethod
    def ask_ok_cancel(title, message):
        return messagebox.askokcancel(title, message)  # True or False
    # OK/Cancel ダイアログを表示し、ユーザーの応答に基づいて処理を行う
    # if MessageBoxHelper.ask_ok_cancel("確認", "この操作を実行しますか？"):
    #     print("操作が承認されました。")
    # else:
    #     print("操作がキャンセルされました。")

    @staticmethod
    def ask_yes_no(title, message):
        return messagebox.askyesno(title, message)  # True or False
    # Yes/No ダイアログを表示し、ユーザーの応答に基づいて処理を行う
    # if MessageBoxHelper.ask_yes_no("確認", "続行しますか？"):
    #     print("続行します。")
    # else:
    #     print("操作を中止します。")

    @staticmethod
    def ask_retry_cancel(title, message):
        return messagebox.askretrycancel(title, message)  # True or False
    # Retry/Cancel ダイアログを表示し、ユーザーの応答に基づいて処理を行う
    # while MessageBoxHelper.ask_retry_cancel("再試行", "操作に失敗しました。再試行しますか？"):
    #     # 何らかの処理を再試行
    #     print("再試行します。")
    #     # 成功したと仮定する
    #     break
    # else:
    #     print("操作をキャンセルしました。")