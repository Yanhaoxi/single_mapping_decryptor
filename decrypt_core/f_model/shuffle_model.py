from .model_interface import De_Result
from .model_register import model_registry
import random

class Shuffle_Model():    
    def __init__(self, chipher: str, vector: tuple[str, ...], logger) -> None:
        self.vector = vector

    def __call__(self, max_iter: int, key_now: tuple[str, ...] | None) -> tuple[tuple[str, ...], int, De_Result]:
        key_now=self.shuffle(key_now)
        if key_now is None:
            key_now = self.vector
        return key_now,0,De_Result.Shuffle

    def shuffle(self,tup):
        lst = list(tup)
        n_shuffle = len(lst) // 5
        if n_shuffle == 0:
            return tup
        indices_to_shuffle = random.sample(range(len(lst)), n_shuffle)
        elements_to_shuffle = [lst[i] for i in indices_to_shuffle]
        random.shuffle(elements_to_shuffle)
        for i, index in enumerate(indices_to_shuffle):
            lst[index] = elements_to_shuffle[i]
        return tuple(lst)
    
model_registry.register("Shuffle_Model", Shuffle_Model)
