from ..ngram_model import Ngram_Model
from ...model_interface import Random_Mixin,Order_Mixin
from ...model_register import model_registry
import os
class Quintgrams_Model(Ngram_Model):
    pass
Quintgrams_Model.init_cls('./decrypt_core/f_model/word_tuple_model/quintgrams_model/quintgrams.json')

class Random_Quintgrams_Model(Random_Mixin,Quintgrams_Model):
    pass

model_registry.register('Random_Quintgrams_Model',Random_Quintgrams_Model)

class Order_Quintgrams_Model(Order_Mixin,Quintgrams_Model):
    pass

model_registry.register('Order_Quintgrams_Model',Order_Quintgrams_Model)