import tiktoken

def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding_name = "cl100k_base"
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(str(string)))
    return num_tokens


if __name__ == "__main__":
    sample_data = "2023-08-02 14:55:00:172.0, 2023-08-02 15:00:00:169.0, 2023-08-02 15:05:00:169.0"
    num_of_tokens = num_tokens_from_string(f"{sample_data}")
    print(num_of_tokens)