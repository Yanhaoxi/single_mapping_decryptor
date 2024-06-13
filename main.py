from decrypt_core import *
import logging
logger = logging.getLogger("main")
logger.setLevel(logging.WARNING)
UNIT_VECTOR = ("a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",)
chipher="rfwvfxzgiuvowvkijgqdvqebfidrfwvqxfifxbfididvsmnuxqzeufiwqrrxdgbvhvofifxjfhvygmosvxiigvhvoyngnvziegzixuvzeygmoifnvbqfifzjwgoidvuvowvkixfimqifgzxgnvidfzjbdfkdfxzgihvoyrfcvryigkgnvrfwvfxzgiuvowvkiidvbqyygmrfhvkqznqcvfiuvowvkirybgzevowmr"

def main():
    model_para_2 = Model_Para("Random_Quadgrams_Model", 20, slice(0, None))
    model_para_3 = Model_Para("Shuffle_Model", 0, slice(0, None))
    key = decrypt(
        chipher,
        UNIT_VECTOR,
        20,
        [model_para_2],
        {model_para_2,model_para_3},               
        Token_Score,
        logger,
    )
    original_text = "".join({k: v for k, v in zip(key, UNIT_VECTOR)}.get(char, char) for char in chipher)
    print(original_text)
if __name__ == "__main__":
    main()