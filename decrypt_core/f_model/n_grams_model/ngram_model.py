import json
from ..model_interface import Model, De_Result
from logging import Logger
from math import log10
import random

class Ngram_Model(Model):
    data: dict[str, float] = {}
    L: int = 0
    floor: float = 0
    N: int = 0

    def init_key(self) -> tuple[str, ...]:
        """Generate an initial estimation of the key on vector which is a character set to decrypt."""
        vector = list(self.vector)
        while True:
            random.shuffle(vector)
            score=self.core_func(tuple(vector))
            if score>-8.7:
                break
        return tuple(vector)
        
    
    @classmethod
    def init_cls(cls, filename):
        with open(filename, "r") as f:
            data_dict = json.load(f)
        cls.data = data_dict["ngrams"]
        cls.L = data_dict["L"]
        cls.N = data_dict["N"]
        cls.floor = log10(0.01 / cls.N)

    def __init__(self, chipher: str, vector: tuple[str, ...], logger: Logger) -> None:
        """init chipher and vector"""
        super().__init__(chipher,vector,logger)
        self.ngram: dict[str, int] = self.text2ngram(chipher)
        

    @classmethod
    def text2ngram(cls, text: str) -> dict[str, int]:
        """将文本转换为ngram"""
        ngram: dict[str, int] = {}
        for i in range(len(text) - cls.L + 1):
            ngram[text[i : i + cls.L]] = ngram.get(text[i : i + cls.L], 0) + 1
        return ngram

    def __call__(
        self, max_iter: int, key_now: tuple[str, ...] | None
    ) -> tuple[tuple[str, ...], int, De_Result]:
        """A interface for outer to call"""
        return super().__call__(max_iter, key_now)


    def core_func(self, key: tuple[str, ...]):
        """The core function of the model to evaluate the proximity between the current decrypted ciphertext and the plaintext."""
        score = 0.0
        sub_dict = {i: v for i, v in zip(key, self.vector)}
        for piece, freq in self.ngram.items():
            subpiece = "".join(sub_dict.get(i, i) for i in piece)
            score += freq * self.data.get(subpiece, self.floor)
        score /= len(self.ngram)
        return score




