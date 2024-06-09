from abc import ABC, abstractmethod
from logging import Logger
class Score(ABC):
    def __init__(self,chipher:str,vector:tuple[str,...],logger:Logger) -> None:
        self.chipher=chipher
        self.vector=vector
        self.max_score:float=self.init_score()
        self.key=vector
        self.logger=logger
        self.result_dict:dict[tuple[str,...],float]={}
    
    def __call__(self,key:tuple[str,...])->bool:
        score=self.score_func(key)
        if self.good_enough(score):
                self.result_dict.update({key:score})
        self.logger.info(f"密钥:{key}\n标准评分为:{score}\n")
        if score>self.max_score:
            self.max_score=score
            self.key=key
            return True
        else:
            return False
        
    @abstractmethod
    def score_func(self,key:tuple[str,...]):
        pass

    @abstractmethod
    def init_score(self)->float:
        pass

    def get_score(self)->float:
        return self.max_score
    
    def get_key(self)->tuple[str,...]:
        return self.key
    
    @abstractmethod
    def good_enough(self,score)->bool:
        pass

    def present_result(self) -> None:
        result = "最佳密钥:\n"
        result += f"Key: {self.key}, Score: {self.max_score}\n"
        result += "可能的好密钥:\n"
        sorted_results = sorted(self.result_dict.items(), key=lambda x: x[1], reverse=True)
        for key, score in sorted_results:
            result += f"Key: {key}, Score: {score}\n"
        self.logger.info(result)

    def have_result(self)->bool:
        return len(self.result_dict)>0