import tiktoken

def num_tokens_from_string(text: str) -> int:
    """
    Returns the number of tokens in a text string.

    Args:
        text (str): The input text for which the number of tokens needs to be counted.

    Returns:
        int: The number of tokens in the input text.

    Raises:
        Exception: If there is an error during token counting, an exception is caught
                   and an error message is printed, and the function returns 0.
    """
    try:
        encoding_name = "cl100k_base"
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(str(text)))
        return num_tokens
    except Exception as e:
        print(f"Error counting tokens: {e}")
        return 0


if __name__ == "__main__":
    # Sample data with 20 data points
    sample_data = (
        "2023-08-02 14:55:00:172.0, 2023-08-02 15:00:00:169.0, "
        "2023-08-02 15:05:00:169.0, 2023-08-02 15:10:00:169.0, "
        "2023-08-02 15:15:00:169.0, 2023-08-02 15:20:00:169.0, "
        "2023-08-02 15:25:00:169.0, 2023-08-02 15:30:00:169.0, "
        "2023-08-02 15:35:00:169.0, 2023-08-02 15:40:00:169.0, "
        "2023-08-02 15:45:00:169.0, 2023-08-02 15:50:00:169.0, "
        "2023-08-02 15:55:00:169.0, 2023-08-02 16:00:00:169.0, "
        "2023-08-02 16:05:00:169.0, 2023-08-02 16:10:00:169.0, "
        "2023-08-02 16:15:00:169.0, 2023-08-02 16:20:00:169.0, "
        "2023-08-02 16:25:00:169.0, 2023-08-02 16:30:00:169.0"
    )
    
    num_of_tokens = num_tokens_from_string(sample_data)
    print(f"Number of tokens: {num_of_tokens}")

