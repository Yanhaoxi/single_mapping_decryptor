from ..model_register import model_registry
from ..model_interface import Model,De_Result
from abc import abstractmethod
from ..utils import single_table_substitution
from logging import Logger


from tokenizer.all_tokenizer import t5_tokenizer

class Token_Model(Model):
    """This is a collection of methods used in decryption to approximate keys."""

    def __init__(self, chipher: str, vector: tuple[str, ...], logger: Logger) -> None:
        """init chipher and vector"""
        super().__init__(chipher, vector, logger)

    def __call__(
        self, max_iter: int, key_now: tuple[str, ...] | None
    ) -> tuple[tuple[str, ...], int, De_Result]:
        """A interface for outer to call"""
        return super().__call__(max_iter, key_now)

    def init_key(self) -> tuple[str, ...]:
        """Generate an initial estimation of the key on vector which is a character set to decrypt."""
        return super().init_key()

    @abstractmethod
    def core_func(self, key:tuple[str,...]):
        """The core function of the model to evaluate the proximity between the current decrypted ciphertext and the plaintext."""
        text=single_table_substitution(self.chipher, {v: k for k, v in zip(self.vector, key)})
        return t5_tokenizer.tokenize(text)

