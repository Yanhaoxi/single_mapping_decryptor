from database import DB
from typing import Sequence
import random
import sys
sys.path.insert(0,'.')
from decrypt_core import *
import logging
import time
file_path = __file__
log_path=file_path.replace("evaluate_some.py", "evaluate_some.log")

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

def gen_random_key_tuple(unit_vector, num_entries=26):
    if num_entries==0:
        ret=unit_vector
        a,b=random.choice(ret),random.choice(ret)
        while a==b:
            b=random.choice(ret)
        ret_gai=list(ret)
        c=ret_gai.index(a)
        d=ret_gai.index(b)
        ret_gai[c],ret_gai[d]=ret_gai[d],ret_gai[c]
        return tuple(ret),tuple(ret_gai)

    if num_entries==1:
        raise ValueError("num_entries must be greater than 1")
    if num_entries>len(unit_vector)-2:
        raise ValueError("num_entries must be less than or equal to the length of len(unit_vector)-2")
    slected_list=random.sample(unit_vector,num_entries)
    wait_list=slected_list.copy()
    wait_list.sort()
    for i in range(num_entries):
        if wait_list[i]==slected_list[i]:
            slected_list[i],slected_list[(i+1)%num_entries]=slected_list[(i+1)%num_entries],slected_list[i]
    ret=(dict(zip(wait_list,slected_list)).get(i,i) for i in unit_vector)
    error_set=set(slected_list)
    correct_set=set(unit_vector)-error_set
    if random.random()<0.5 and len(error_set)!=0:
        a,b=random.choice(tuple(error_set)),random.choice(tuple(correct_set))
    else:
        a=random.choice(tuple(correct_set))
        while (b:=random.choice(tuple(correct_set)))==a:
            pass

    ret=tuple(ret)
    ret_gai=list(ret)
    c=ret_gai.index(a)
    d=ret_gai.index(b)
    ret_gai[c],ret_gai[d]=ret_gai[d],ret_gai[c]
    # assert tuple(ret_gai)!=ret
    return ret,tuple(ret_gai)

def cal_similarity(key,uni):
    return sum(1 for i in range(len(uni)) if key[i]==uni[i])


# model_list=["Random_Token_Model","Order_Token_Model","Random_Quadgrams_Model","Single_Token_Model"]
model_list=["Random_Trigrams_Model"]
def main():
    for model_name in model_list:
        list_num=[0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
        for j in list_num:
            score=0
            num=0
            while((text:=DB.get_data(min_words=50-20,max_words=50+20))!=None):
                pro_text = prepare_text(text)
                for _ in range(500):
                    key=gen_random_key_dict(UNIT_VECTOR)
                    chipher = single_table_substitution(pro_text, key)

                    uni=tuple(key[i] for i in UNIT_VECTOR)
                    random_key,random_key_gai=gen_random_key_tuple(uni,j)
                    model = model_registry.get_model(model_name)(chipher, UNIT_VECTOR, logger)
                    c1=cal_similarity(random_key_gai,uni)
                    c2=cal_similarity(random_key,uni)
                    assert c1<c2
                    c1_text = single_table_substitution(chipher, {k: v for k, v in zip(random_key_gai, UNIT_VECTOR)})
                    same_char_count = sum(c1 == c2 for c1, c2 in zip(pro_text, c1_text))
                    c1_similarity = same_char_count / len(pro_text)
                    c2_text = single_table_substitution(chipher, {k: v for k, v in zip(random_key, UNIT_VECTOR)})
                    same_char_count = sum(c1 == c2 for c1, c2 in zip(pro_text, c2_text))
                    c2_similarity = same_char_count / len(pro_text)

                    e=c1_similarity<c2_similarity
                    d=bool((model.core_func(random_key_gai))<(model.core_func(random_key)))
                    if (d and e) or ((not d) and (not e)):
                        score += 1
                    num+=1
            DB.reset_cursor()
            logger.warning(f"{model_name}--{j}:rate:{score/num}")

if __name__ == "__main__":
    main()
