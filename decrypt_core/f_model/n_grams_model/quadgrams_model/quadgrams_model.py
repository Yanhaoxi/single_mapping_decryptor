from ..ngram_model import Ngram_Model
from ...model_interface import Random_Mixin,Order_Mixin
from ...model_register import model_registry
class Quadgrams_Model(Ngram_Model):
    pass
Quadgrams_Model.init_cls('./decrypt_core/f_model/word_tuple_model/quadgrams_model/quadgrams.json')

class Random_Quadgrams_Model(Random_Mixin,Quadgrams_Model):
    pass

model_registry.register('Random_Quadgrams_Model',Random_Quadgrams_Model)

class Order_Quadgrams_Model(Order_Mixin,Quadgrams_Model):
    pass

model_registry.register('Order_Quadgrams_Model',Random_Quadgrams_Model)