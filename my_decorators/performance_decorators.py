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
from tqdm import tqdm
from dotenv import load_dotenv
import functools


# 自作モジュール
from logger.debug_logger import Logger

load_dotenv()

# logger初期化
debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
logger_instance = Logger(__name__, debug_mode=debug_mode)
logger = logger_instance.get_logger()


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

