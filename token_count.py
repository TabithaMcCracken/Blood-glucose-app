import tiktoken
from make_sample_data import generate_glucose_levels

# encoding = tiktoken.get_encoding("cl100k_base")
# encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

sample_data = generate_glucose_levels()

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


if __name__ == "__main__":
    num_of_tokens = num_tokens_from_string(f"{sample_data}", "cl100k_base")
    print(num_of_tokens)