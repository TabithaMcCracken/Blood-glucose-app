import tiktoken
from make_sample_data import generate_glucose_levels

def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding_name = "cl100k_base"
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(str(string)))
    return num_tokens


if __name__ == "__main__":
    sample_data = "I love pizza."
    num_of_tokens = num_tokens_from_string(f"{sample_data}")
    print(num_of_tokens)