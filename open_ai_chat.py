from secret import key
from openai import OpenAI
# from make_sample_data import generate_glucose_levels
from token_count import num_tokens_from_string

def chat(cgm_data):
    """Generates a conversation with openai.

    Args:
        cgm_data (tuple): 24 hours of bgl's in 5 minute increments
        key (str): OpenAI API key

    Returns:
        list: conversation with openai
    """
    print("Here is the data we will analyze: ")
    print(cgm_data)
    print("Welcome! Here is the analysis for this data...(Type 'exit' to quit)")

    client = OpenAI(api_key=key)
    chatbot_conversation = []
    system_msg = "You are a helpful assistant."
    chatbot_conversation.append({"role": "system", "content": system_msg})

    initial_user_prompt = ('Analyze the following blood glucose data where the '
                            'first number is the time stamp and the second is '
                            'the blood glucose level. Give us the blood glucose'
                            ' range, the percentage of time in the 24 hour period'
                            ' that the time stamps are in range between'
                            ' 70 and 130, and general observations in one paragraph:'
                            f'\n{cgm_data}')
    chatbot_conversation.append({"role": "user", "content": initial_user_prompt})

    while True:
        if num_tokens_from_string(chatbot_conversation) < 128000:
            
            token_size = num_tokens_from_string(chatbot_conversation)
            print(f"Token Size: {token_size}")

            if token_size < 128000:
                response = client.chat.completions.create(
                    model = "gpt-4-1106-preview",
                    messages = chatbot_conversation
                    # max_tokens = 200  # Adjust based on your needs
                )
    
                chatbot_repsonse = response.choices[0].message.content
                print(f"{chatbot_repsonse}")
                chatbot_conversation.append({"role": "assistant", "content": chatbot_repsonse})
                print(f"Token size after response {num_tokens_from_string(chatbot_conversation)}")

            else:
                print("The conversation is too large to process.")
                break

            print ("To exit the conversation, type: 'exit'.")
            user_input = input("User: ")
            if user_input.lower() == "exit":
                break

            else:
                chatbot_conversation.append({"role": "user", "content": user_input})

        else:
            print("The conversation is too large to process.")
            break

    return chatbot_conversation

if __name__ == "__main__":
    # Create a data set to use
    sample_data = "2023-08-02 14:55:00:172.0, 2023-08-02 15:00:00:169.0, 2023-08-02 15:05:00:169.0"

    # Run the chat
    analysis_conv = chat(sample_data)