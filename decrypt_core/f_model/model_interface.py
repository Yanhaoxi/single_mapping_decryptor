from abc import ABC, abstractmethod
from logging import Logger
from .utils import create_estimated_key
import random
from .utils import step_change
from enum import Enum
from typing import NamedTuple, Tuple

class De_Result(Enum):
    Noleft_changed = 1 #cache清空，但是不会被加入到cache
    left_changed = 2 #cache清空，然后被加入到cache
    Unchanged= 3 #不会被加入到cache
    Shuffle=4 #Shuffle模型的结果

class Model_Para(NamedTuple):
    model_name: str
    max_iter: int 
    chipher_slice: slice
    def slice_to_tuple(self):
        s=self.chipher_slice
        return s.start, s.stop, s.step
    def __hash__(self):
        return hash((self.model_name,self.slice_to_tuple()))
    def __eq__(self,other):
        return hash(self)==hash(other)
    def __repr__(self) -> str:
        return f"({self.model_name},{self.chipher_slice}:{self.max_iter})"
    
class Model(ABC):
    @abstractmethod
    def __init__(self, chipher: str, vector: tuple[str, ...], logger: Logger) -> None:
        self.chipher = chipher
        self.vector = vector
        self.logger = logger

    @abstractmethod
    def __call__(
        self, max_iter: int, key_now: tuple[str, ...] | None
    ) -> tuple[tuple[str, ...], int, De_Result]:
        """A interface for outer to call"""
        if key_now is None:
            key_now = self.init_key()
        return self.decrypt(max_iter, key_now)

    @abstractmethod
    def init_key(self) -> tuple[str, ...]:
        """Generate an initial estimation of the key on vector which is a character set to decrypt."""
        return create_estimated_key(self.chipher, self.vector)

    @abstractmethod
    def decrypt(
        self, max_iter: int, key_now: tuple[str, ...]
    ) -> tuple[tuple[str, ...], int, De_Result]:
        """Decrypt the chipher text and approximate key step by step."""
        pass

    @abstractmethod
    def core_func(self, key: tuple[str, ...])->float:
        """The core function of the model to evaluate the proximity between the current decrypted ciphertext and the plaintext."""
        pass


# 仅用于Model的混入类模型方法
class Random_Mixin:
    def decrypt(self, max_iter: int, key_now: tuple[str, ...]) -> tuple[tuple[str, ...], int, De_Result]:
        vector = self.vector #type:ignore
        max_score = self.core_func(key_now) #type:ignore
        self.logger.info(f"初始分数:{max_score}\n初始key:{key_now}\n") #type:ignore
        count=650*max_iter
        cache: set[tuple[int, int]] = set()
        all_patterns = {(i, j) for i in range(len(vector)) for j in range(len(vector)) if i < j}
        changed=False
        i=0
        for i in range(count):
            left_pattern=all_patterns-cache
            if left_pattern==set():
                break
            a,b=random.choice(list(left_pattern))
            next_key=step_change(key_now, {a: b})
            score = self.core_func(next_key) #type:ignore
            if score > max_score:
                changed=True
                max_score = score
                key_now = next_key
                self.logger.info( #type:ignore
                    f"优化-> {{key:{key_now},score:{max_score}}}\n"
                )
                cache.clear()
                cache|={(a,b)}
            else:
                cache|={(a,b)}
        count -= i
        match (count,changed) :
            case (0,True):
                result= De_Result.Noleft_changed
            case (_,False):
                result= De_Result.Unchanged
            case (_,True):
                result= De_Result.left_changed
        return key_now, i//650+1, result
    
    
# 仅用于Model的混入类模型方法
class Order_Mixin:
    def decrypt(
        self, max_iter: int, key_now: tuple[str, ...]
    ) -> tuple[tuple[str, ...], int, De_Result]:
        """Decrypt the chipher text and approximate key step by step."""
        vector = self.vector #type:ignore
        max_score = self.core_func(key_now) #type:ignore
        self.logger.info(f"初始分数:{max_score}\n初始key:{key_now}\n") #type:ignore
        iter_count = 0
        Changed = True
        cache: set[tuple[int, int]] = set()
        while Changed:
            if iter_count >= max_iter:
                break
            self.logger.info(f"第{iter_count+1}次迭代开始:\n") #type:ignore
            iter_count += 1

            queue = list(vector)
            random.shuffle(queue)
            flag = True
            Changed = False
            while len(queue) > 0:
                if flag:
                    element = queue.pop()
                    element_index = key_now.index(element)
                for i in range(len(key_now)):
                    if i == element_index:
                        continue
                    if (element_index, i) in cache:
                        continue
                    next_key = step_change(key_now, {element_index: i})
                    score = self.core_func(next_key) #type:ignore
                    if score > max_score:
                        max_score = score
                        key_now = next_key
                        self.logger.info( #type:ignore
                            f"优化-> {{key:{key_now},score:{max_score}}}\n"
                        )
                        flag = False
                        Changed = True
                        cache.clear()
                        cache.add((i, element_index))
                        break
                    else:
                        cache.add((i, element_index))
                flag = True
        match (iter_count,Changed) :#Changed 是最后一轮有无更改
            case (_,True):
                result= De_Result.Noleft_changed
            case (1,False):
                result= De_Result.Unchanged
            case (_,False):
                result= De_Result.left_changed
        return key_now, iter_count, result
   