from .token_model import Token_Model
from ..model_interface import Random_Mixin,Order_Mixin
from ..model_register import model_registry
from ..utils import SINGLE_CHAR_FREQUENCY_TUPLE
class Random_Token_Model(Random_Mixin,Token_Model):
    def core_func(self, key: tuple[str, ...]):
        tokens_list = super().core_func(key)
        return (
            sum([len(token) * (len(token) - 2) for token in tokens_list]) / len(self.chipher)
            + 1
        )

model_registry.register("Random_Token_Model", Random_Token_Model)

class Order_Token_Model(Order_Mixin,Token_Model):
    def core_func(self, key: tuple[str, ...]):
        tokens_list = super().core_func(key)
        return (
            sum([len(token) * (len(token) - 2) for token in tokens_list]) / len(self.chipher)
            + 1
        )

model_registry.register("Order_Token_Model", Order_Token_Model)
   
class Single_Token_Model(Order_Mixin,Token_Model):
    def core_func(self, key: tuple[str, ...]):
        tokens_list = super().core_func(key)
        return (
            -sum([len(token) ==1 and token!='a' for token in tokens_list]) / len(self.chipher)
            + 1
        )

model_registry.register("Single_Token_Model", Single_Token_Model)
