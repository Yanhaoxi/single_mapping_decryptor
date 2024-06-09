from typing import Sequence
import random
import sys
sys.path.insert(0,'.')
from decrypt_core import *
UNIT_VECTOR = (
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
)
SINGLE_CHAR_FREQUENCY_TUPLE = (
    "e",
    "t",
    "a",
    "o",
    "i",
    "n",
    "s",
    "h",
    "r",
    "d",
    "l",
    "c",
    "u",
    "m",
    "w",
    "f",
    "g",
    "y",
    "p",
    "b",
    "v",
    "k",
    "j",
    "x",
    "q",
    "z",
)
SINGLE_CHAR_FREQUENCY_DICT = {
    "e": 11.1607,
    "t": 9.056,
    "a": 8.4966,
    "o": 7.5075,
    "i": 7.5466,
    "n": 7.0731,
    "s": 6.327,
    "h": 6.0943,
    "r": 5.9781,
    "d": 4.253,
    "l": 4.025,
    "c": 2.782,
    "u": 2.758,
    "m": 2.406,
    "w": 2.36,
    "f": 2.228,
    "g": 2.015,
    "y": 1.974,
    "p": 1.929,
    "b": 1.492,
    "v": 0.978,
    "k": 0.772,
    "j": 0.153,
    "x": 0.15,
    "q": 0.095,
    "z": 0.074,
}


def prepare_text(text: str) -> str:
    """
    Prepare the text for decryption, only letters are left and all letters will be transformed to lower case
    """
    return "".join(char for char in text.lower() if char.isalpha())


def char_frequency(text: str, standard_seq) -> dict:
    frequency_dict = {char: 0 for char in standard_seq}
    for char in text:
        try:
            frequency_dict[char] += 1
        except KeyError:
            pass
    return frequency_dict


def create_estimated_key(chipher: str, standard_seq: Sequence[str]) -> tuple[str, ...]:
    """
    Create an estimated key from the chipher by single char frequency analysis
    only char in the standard_seq will be considered
    """

    frequency_dict = char_frequency(chipher, standard_seq)
    sorted_chars = sorted(frequency_dict, key=lambda x: frequency_dict[x], reverse=True)

    sorted_standard_seq = sorted(
        standard_seq, key=lambda x: SINGLE_CHAR_FREQUENCY_DICT[x], reverse=True
    )

    char_index_map = {char: index for index, char in enumerate(sorted_standard_seq)}
    return tuple(sorted_chars[char_index_map[char]] for char in standard_seq)


def single_table_substitution(text, substitution_dict):
    """Substitute the text according to the substitution_dict."""
    substituted_text = "".join(substitution_dict.get(c, c) for c in text)
    return substituted_text


def gen_random_key_dict(vector: Sequence) -> dict:
    """Generate a random substitution key according to vector which is passed in."""
    vector = list(vector)
    random_vector = random.sample(vector, len(vector))
    return {k: v for k, v in zip(vector, random_vector)}


def main():
    text = """Beauty
        There were a sensitivity and a beauty to her that have nothing to do with looks. She was one to be listened to, whose words were so easy to take to heart.
        It is said that the true nature of being is veiled. The labor of words, the expression of art, the seemingly ceaseless buzz that is human thought all have in common the need to get at what really is so. The hope to draw close to and possess the truth of being can be a feverish one. In some cases it can even be fatal, if pleasure is one's truth and its attainment more important than life itself. In other lives, though, the search for what is truthful gives life.
        I used to find notes left in the collection basket, beautiful notes about my homilies and about the writer's thoughts on the daily scriptural readings. The person who penned the notes would add reflections to my thoughts and would always include some quotes from poets and mystics he or she had read and remembered and loved. The notes fascinated me. Here was someone immersed in a search for truth and beauty. Words had been treasured, words that were beautiful. And I felt as if the words somehow delighted in being discovered, for they were obviously very generous to the as yet anonymous writer of the notes. And now this person was in turn learning the secret of sharing them. Beauty so shines when given away. The only truth that exists is, in that sense, free."""
    pro_text = prepare_text(text)
    # random_key = {
    #     "a": "n",
    #     "b": "p",
    #     "c": "x",
    #     "d": "e",
    #     "e": "o",
    #     "f": "u",
    #     "g": "y",
    #     "h": "s",
    #     "i": "a",
    #     "j": "q",
    #     "k": "v",
    #     "l": "b",
    #     "m": "c",
    #     "n": "w",
    #     "o": "z",
    #     "p": "f",
    #     "q": "t",
    #     "r": "i",
    #     "s": "j",
    #     "t": "m",
    #     "u": "h",
    #     "v": "k",
    #     "w": "g",
    #     "x": "l",
    #     "y": "d",
    #     "z": "r",
    # }
    random_key=gen_random_key_dict(UNIT_VECTOR)
    print(random_key.values())
    chipher = single_table_substitution(pro_text, random_key)
    model_para_1 = Model_Para("Order_Token_Model",10, slice(0, None))
    model_para_2 = Model_Para("Random_Quadgrams_Model", 2, slice(0, None))
    model_para_3 = Model_Para("Shuffle_Model", 0, slice(0, None))
    key = decrypt(
        chipher,
        UNIT_VECTOR,
        10,
        [model_para_2,model_para_1],
    {model_para_2,model_para_1, model_para_3},
        Token_Score
    )
    print(key)
    orihinal_text = single_table_substitution(
        chipher, {k: v for k, v in zip(key, UNIT_VECTOR)}
    )
    print(orihinal_text)


if __name__ == "__main__":
    main()
