from .score import Score
from tokenizer.all_tokenizer import t5_tokenizer

class Token_Score(Score):
    def init_score(self) -> float:
        return -1.0

    def good_enough(self,score) -> bool:
        return score>2.7
        # return score>-0.1
        # return False
    
    def score_func(self,key:tuple[str,...])->float:
        substitution_dict={v: k for k, v in zip(self.vector, key)}
        substituted_text = "".join(substitution_dict.get(c, c) for c in self.chipher)
        tokens=t5_tokenizer.tokenize(substituted_text)
        return (
                sum([len(token) * (len(token) - 2) for token in tokens]) / len(substituted_text)
                + 1
            )
        # return -sum(1 for token in tokens if len(token)==1) / len(substituted_text)
        
        