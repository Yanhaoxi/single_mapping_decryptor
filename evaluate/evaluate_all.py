from database import DB
from typing import Sequence
import random
import sys
sys.path.insert(0,'.')
from decrypt_core import *
import logging
import time
file_path = __file__
log_path=file_path.replace("evaluate_all.py", "evaluate.log")

logger = logging.getLogger("evaluate_logger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(log_path)
file_handler.setLevel(logging.WARNING)

formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
UNIT_VECTOR = (
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
)

def prepare_text(text: str) -> str:
    """
    Prepare the text for decryption, only letters are left and all letters will be transformed to lower case
    """
    return "".join(char for char in text.lower() if char.isalpha())


def single_table_substitution(text, substitution_dict):
    """Substitute the text according to the substitution_dict."""
    substituted_text = "".join(substitution_dict.get(c, c) for c in text)
    return substituted_text


def gen_random_key_dict(vector: Sequence) -> dict:
    """Generate a random substitution key according to vector which is passed in."""
    vector = list(vector)
    random_vector = random.sample(vector, len(vector))
    return {k: v for k, v in zip(vector, random_vector)}


def main_1():
    slist=[]
    time_list=[]
    while((text:=DB.get_data(min_words=50-20,max_words=50+20))!=None):
        for i in range(100):
            start_time = time.time()  # 开始计时
            pro_text = prepare_text(text)
            random_key=gen_random_key_dict(UNIT_VECTOR)
            chipher = single_table_substitution(pro_text, random_key)
            model_para_1 = Model_Para("Random_Token_Model",10, slice(0, None))
            model_para_2 = Model_Para("Random_Quadgrams_Model", 20, slice(0, None))
            model_para_3 = Model_Para("Shuffle_Model", 0, slice(0, None))
            key = decrypt(
                chipher,
                UNIT_VECTOR,
                20,
                [model_para_1,model_para_2],
                {model_para_2,model_para_3},               
                Token_Score,
                logger=logger
            )
            original_text = single_table_substitution(
                chipher, {k: v for k, v in zip(key, UNIT_VECTOR)}
            )
            end_time = time.time()  # 结束计时
            same_char_count = sum(c1 == c2 for c1, c2 in zip(pro_text, original_text))
            similarity = same_char_count / len(pro_text)
            logger.warning(f"min_words=50-20,max_words=50+20) Similarity: {similarity}")
            slist.append(similarity)
            elapsed_time = end_time - start_time  # 计算本次解密所需时间
            time_list.append(elapsed_time)  # 将时间添加到列表中
    DB.reset_cursor()
    recovery_rate = sum(1 for s in slist if s >= 0.99) / len(slist)
    logger.warning(f"Recovery rate: {recovery_rate}")
    average_time = sum(time_list) / len(time_list) if time_list else 0  # 计算平均时间
    logger.warning(f"Average decryption time: {average_time} seconds")  # 记录平均时间

def main_2():
    slist=[]
    time_list=[]
    while((text:=DB.get_data(min_words=50-20,max_words=50+20))!=None):
        for i in range(100):
            start_time = time.time()  # 开始计时
            pro_text = prepare_text(text)
            random_key=gen_random_key_dict(UNIT_VECTOR)
            chipher = single_table_substitution(pro_text, random_key)
            model_para_1 = Model_Para("Random_Token_Model",10, slice(0, None))
            model_para_2 = Model_Para("Random_Quadgrams_Model", 20, slice(0, None))
            model_para_3 = Model_Para("Shuffle_Model", 0, slice(0, None))
            key = decrypt(
                chipher,
                UNIT_VECTOR,
                20,
                [model_para_2],
                {model_para_2,model_para_3},               
                Token_Score,
                logger=logger
            )
            original_text = single_table_substitution(
                chipher, {k: v for k, v in zip(key, UNIT_VECTOR)}
            )
            end_time = time.time()  # 结束计时
            same_char_count = sum(c1 == c2 for c1, c2 in zip(pro_text, original_text))
            similarity = same_char_count / len(pro_text)
            logger.warning(f"min_words=50-20,max_words=50+20) Similarity: {similarity}")
            slist.append(similarity)
            elapsed_time = end_time - start_time  # 计算本次解密所需时间
            time_list.append(elapsed_time)  # 将时间添加到列表中
    DB.reset_cursor()
    recovery_rate = sum(1 for s in slist if s >= 0.99) / len(slist)
    logger.warning(f"Recovery rate: {recovery_rate}")
    average_time = sum(time_list) / len(time_list) if time_list else 0  # 计算平均时间
    logger.warning(f"Average decryption time: {average_time} seconds")  # 记录平均时间


if __name__ == "__main__":
    main_1()
    main_2()



