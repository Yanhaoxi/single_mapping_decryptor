from math import log10
import json
def data_json(ngramfile,targetfile ,sep=' '):
    '''加载包含ngrams和计数的文件,计算对数概率'''
    ngrams = {}  # 存储ngrams及其计数的字典
    with open(ngramfile, 'r') as file:
        for line in file:
            key, count = line.split(sep)  # 将行按分隔符分割为ngram和计数
            ngrams[key.lower()] = int(count)  # 将ngram及其计数存储到字典中
    L = len(key)  # ngram的长度
    N = sum(ngrams.values())  # 所有ngrams的总计数
    # 计算对数概率
    for key in ngrams.keys():
        ngrams[key] = log10(
            float(ngrams[key]) / N)  # 计算ngram的对数概率
        
    data = {'ngrams': ngrams, 'L': L, 'N': N}  # 存储ngrams、ngram长度和总计数的字典
    with open(targetfile, 'w') as f:
        json.dump(data, f, indent=4)

# import os
# path=os.path.dirname(__file__)
# data_json(os.path.join(path,'english_trigrams.txt'),os.path.join(path,'trigrams.json'))


