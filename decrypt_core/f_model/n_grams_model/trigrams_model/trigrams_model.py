from ..ngram_model import Ngram_Model
from ...model_interface import Random_Mixin,Order_Mixin
from ...model_register import model_registry
import os
class Trigrams_Model(Ngram_Model):
    pass
Trigrams_Model.init_cls('./decrypt_core/f_model/word_tuple_model/trigrams_model/trigrams.json')

class Random_Trigrams_Model(Random_Mixin,Trigrams_Model):
    pass

model_registry.register('Random_Trigrams_Model',Random_Trigrams_Model)

class Order_Trigrams_Model(Order_Mixin,Trigrams_Model):
    pass

model_registry.register('Order_Trigrams_Model',Order_Trigrams_Model)