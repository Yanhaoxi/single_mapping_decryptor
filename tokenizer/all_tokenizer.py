from transformers import T5Tokenizer  # type: ignore

tokenizer_path = "./tokenizer/t5_base_tokenizer"
t5_tokenizer = T5Tokenizer.from_pretrained(tokenizer_path, legacy=False)
