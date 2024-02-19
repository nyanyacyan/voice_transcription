# coding: utf-8
# ----------------------------------------------------------------------------------
# loggerクラス
# 2023/2/18 制作

#---バージョン---
# Python==3.8.10
# ----------------------------------------------------------------------------------
import os
import time
import sys
from dotenv import load_dotenv
import functools
from functools import wraps


# 自作モジュール
# from logger.debug_logger import Logger

load_dotenv()

# logger初期化
# debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
# logger_instance = Logger(__name__, debug_mode=debug_mode)
# logger = logger_instance.get_logger()


# 呼び出す際には「 @performance_decorator 」
def performance_decorator(func):
    @functools.wraps(func)

    # *args=> 関数の引数に何を入れてもいい状態にする(位置引数)
    # **kwargs=> 引数に特別な要素の指定することができる（キーワード引数=> 辞書含む）
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)  # 元の関数を呼び出してる
        end_time = time.time()
        logger.debug(f"{func.__name__}処理時間 : {end_time - start_time} seconds")
        return result
    return wrapper


# @progress_decorator
def progress_bar_decorator(width=50):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()

            result_generator = func(*args, **kwargs)
            if not hasattr(result_generator,'__iter__'):
                result_generator = [result_generator]

            for progress in func(*args, **kwargs):
                elapsed_time = time.time() - start_time

                if progress > 0:
                    estimated_total = elapsed_time / (progress / 100)
                    remaining_time = estimated_total - elapsed_time

                else:
                    remaining_time = 0  # 進捗が0の場合、残り時間を0とする

                filled_length = int(width * progress // 100)
                bar = '=' * filled_length + '>' + '-' * (width - filled_length - 1)
                sys.stdout.write(f'\rProgress: [{bar}] {progress:.2f}% Complete, 残り時間: {remaining_time:.2f} seconds')
                sys.stdout.flush()

            print()
        return wrapper
    return decorator


# テスト用の関数
@progress_bar_decorator(width=50)
def test_function():
    for i in range(101):
        time.sleep(0.1)  # 模擬的な処理時間
        yield i  # 現在の進捗をパーセンテージで返す

test_function()