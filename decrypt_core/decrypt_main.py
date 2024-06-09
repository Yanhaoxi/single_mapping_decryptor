from typing import Type
import random
# 日志部分
import logging
import os

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
log_dir = os.path.join(current_dir, "logs")
log_file = "decrypt_runner.log"

os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger("decrypt_runner_logger")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(os.path.join(log_dir, log_file))
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
# 日志部分结束


from .f_model.model_register import model_registry
from .f_model.model_interface import Model,De_Result,Model_Para
from .score.score import Score

# 解密主函数
# 模型参数 model_name,chipher_slice与初始化有关 max_iter与初始化无关
# 以及是否达极大值也仅与前两者有关
    
# len(vector)>=2
# max_iter>=1
# model_random_set 仅(model_name,chipher_slice)不同的模型有效
def decrypt(
    chipher: str,
    vector: tuple[str,...],
    iter_num: int,
    model_order_list: list[Model_Para],
    model_random_set: Model_Para,
    score_cls:Type[Score],
    logger:logging.Logger=logger,
) -> tuple[str, ...]|None:

    # 构建模型字典
    inited_model: dict['Model_Para', 'Model'] = {}
    # 初始化key
    key = None
    # 初始化评分器
    score_self=score_cls(chipher,vector,logger)
    # 对模型是否迭代进行缓存
    cache:set['Model_Para'] = set()
    shuffled:set['Model_Para'] = set()
    # 顺序
    for model_para in model_order_list:
        # 如果模型已经解密过并且无迭代发生，则跳过
        if model_para in cache:
            continue
        # 如果模型未初始化，则初始化
        if inited_model.get(model_para) is None:
            inited_model[model_para] = model_registry.get_model(
                model_para.model_name
            )(chipher[model_para.chipher_slice], vector,logger)

        # 模型解密
        min_iter_num = min(model_para.max_iter, iter_num)
        logger.info(
            f"{model_para.model_name}开始解密\n最大迭代次数为{min_iter_num}\n当前密钥为{key}\n\n"
        )
        key, do_iter_num, result = inited_model[model_para](
            min_iter_num, key
        )
        logger.info(
            f"{model_para.model_name}解密结束\n迭代次数为{do_iter_num}\n当前密钥为:{key}\n\n"
        )
        iter_num -= do_iter_num
        match result:
            case De_Result.Noleft_changed:
                cache.clear()
                shuffled.clear()
            case De_Result.Unchanged:
                cache.add(model_para)
                shuffled.clear()
            case De_Result.left_changed:
                cache.clear()
                cache.add(model_para)
                shuffled.clear()
            case De_Result.Shuffle:
                cache.clear()
                shuffled.add(model_para)
        
        score_self(key)
        if iter_num <= 0:
            break

    while(True):
        # 仅取出未在cache中的模型
        left=model_random_set-cache-shuffled
        if left == set():
            break
        model_para=random.choice(list(left))
        # 如果模型未初始化，则初始化
        if inited_model.get(model_para) is None:
            inited_model[model_para] = model_registry.get_model(
                model_para.model_name
            )(chipher[model_para.chipher_slice], vector,logger)


        # 模型解密
        min_iter_num = min(model_para.max_iter, iter_num)
        logger.info(
            f"{model_para.model_name}开始解密\n最大迭代次数为{min_iter_num}\n当前密钥为{key}\n\n"
        )
        key, do_iter_num, result = inited_model[model_para](
            min_iter_num, key
        )
        logger.info(
            f"{model_para.model_name}解密结束\n迭代次数为{do_iter_num}\n当前密钥为:{key}\n\n"
        )
        iter_num -= do_iter_num
        match result:
            case De_Result.Noleft_changed:
                cache.clear()
                shuffled.clear()
            case De_Result.Unchanged:
                cache.add(model_para)
                shuffled.clear()
            case De_Result.left_changed:
                cache.clear()
                cache.add(model_para)
                shuffled.clear()
            case De_Result.Shuffle:
                cache.clear()
                shuffled.add(model_para)
        score_self(key)
        if iter_num <= 0  or score_self.have_result()==True:
            break

    score_self.present_result()
    logger.info(f"解密结束\n剩余迭代次数:{iter_num}\n")
    return score_self.get_key()