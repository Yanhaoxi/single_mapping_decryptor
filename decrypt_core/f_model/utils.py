from typing import Sequence
import random
from .statics_fact import (
    UNIT_VECTOR,
    SINGLE_CHAR_FREQUENCY_TUPLE,
    SINGLE_CHAR_FREQUENCY_DICT,
)


def prepare_text(text: str) -> str:
    """
    Prepare the text for decryption, only letters are left and all letters will be transformed to lower case

    Args:
        text (str): The text to be prepared for decryption.

    Returns:
        str: The prepared text with only lowercase letters.
    """
    return "".join(char for char in text.lower() if char.isalpha())


def single_table_substitution(text, substitution_dict):
    """
    Substitute characters in the text according to the substitution_dict.

    Args:
        text (str): The input text to be substituted.
        substitution_dict (dict): A dictionary containing the substitution mappings.

    Returns:
        str: The substituted text.

    """
    substituted_text = "".join(substitution_dict.get(c, c) for c in text)
    return substituted_text


def gen_random_key_dict(vector: Sequence) -> dict:
    """
    Generate a random substitution key according to the given vector.

    Args:
        vector (Sequence): The vector used to generate the substitution key.

    Returns:
        dict: A dictionary representing the a single substitution mapping(identity mapping),
              where the keys are the elements of the vector the values are randomly shuffled keys.
    """
    vector = list(vector)
    random_vector = random.sample(vector, len(vector))
    return {k: v for k, v in zip(vector, random_vector)}


def char_frequency(text: str, standard_seq) -> dict:
    """
    Calculate the frequency of characters in a given text.

    Args:
        text (str): The input text.
        standard_seq: The sequence of characters to calculate the frequency for.

    Returns:
        dict: A dictionary containing the frequency of each character in the standard sequence.
    """
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

    Args:
        chipher (str): The input cipher text.
        standard_seq (Sequence[str]): The sequence of standard characters to consider.

    Returns:
        tuple[str, ...]: The estimated key generated from the cipher text.

    Procedure:
        standard_seq = "abcdefghijklmnopqrstuvwxyz"
        sorted_standard_seq = "etaoinshrdlcumwfgypbvkjxqz"
        sorted_chars = "eirtnsaolcdupmghybfvkjxqzw"
        char_index_map = {'e': 0, 't': 1, 'a': 2, 'o': 3, 'i': 4, 'n': 5, 's': 6, 'h': 7, 'r': 8, 'd': 9, 'l': 10, 'c': 11, 'u': 12, 'm': 13, 'w': 14, 'f': 15, 'g': 16, 'y': 17, 'p': 18, 'b': 19, 'v': 20, 'k': 21, 'j': 22, 'x': 23, 'q': 24, 'z': 25}
        a -> 2 -> r
        b -> 19 -> v
        ...
        z -> 25 -> z
        return ('r','v',...,'z')
    """
    frequency_dict = char_frequency(chipher, standard_seq)
    sorted_chars = sorted(frequency_dict, key=lambda x: frequency_dict[x], reverse=True)

    sorted_standard_seq = sorted(
        standard_seq, key=lambda x: SINGLE_CHAR_FREQUENCY_DICT[x], reverse=True
    )

    char_index_map = {char: index for index, char in enumerate(sorted_standard_seq)}
    return tuple(sorted_chars[char_index_map[char]] for char in standard_seq)


def step_change(key: tuple[str, ...], position: dict[int, int]) -> tuple[str, ...]:
    """
    Take a step to change the key according to position dict.

    Args:
        key (tuple[str, ...]): The current key.
        position (dict[int, int]): The positions to swap in the key.

    Returns:
        tuple[str, ...]: The updated key after swapping the positions.
    """
    for a, b in position.items():
        next_key = list(key)
        next_key[a], next_key[b] = next_key[b], next_key[a]
    return tuple(next_key)



