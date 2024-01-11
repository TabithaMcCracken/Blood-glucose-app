
import os
from openai import OpenAI
from token_count import num_tokens_from_string

def chat(cgm_data, key):
    """Generates a conversation with openai.

    Args:
        cgm_data (tuple): 24 hours of bgl's in 5 minute increments
        key (str): OpenAI API key

    Returns:
        list: conversation with openai
    """

    print("Welcome! Here is the analysis for this data...(Type 'exit' to quit)")

    client = OpenAI(api_key=key)
    chatbot_conversation = []
    system_msg = "You are a helpful assistant."
    chatbot_conversation.append({"role": "system", "content": system_msg})

    initial_user_prompt = (
        'Analyze the following blood glucose data where the '
        'first number is the time stamp and the second is '
        'the blood glucose level. Give us the blood glucose'
        ' range, at what times are the levels out of the'
        ' 70-130 range and general observations in one paragraph:'
        f'\n{cgm_data}'
    )
    chatbot_conversation.append({"role": "user", "content": initial_user_prompt})

    while True:
            
        token_size = num_tokens_from_string(chatbot_conversation)

        if token_size < 128000:
            response = client.chat.completions.create(
                model = "gpt-4-1106-preview",
                messages = chatbot_conversation
            )

            chatbot_repsonse = response.choices[0].message.content
            print(chatbot_repsonse)
            chatbot_conversation.append({"role": "assistant", "content": chatbot_repsonse})

        else:
            print("The conversation is too large to process.")
            break

        print ("To exit the conversation, type: 'exit'.")
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break

        else:
            chatbot_conversation.append({"role": "user", "content": user_input})

    return chatbot_conversation

if __name__ == "__main__":
    # Get OPENAI API key from environment variable
    key = os.environ.get('OPENAI_KEY')

    # Create a data set to use
    sample_data = "2023-08-02 14:55:00:172.0, 2023-08-02 15:00:00:169.0, 2023-08-02 15:05:00:169.0"

    # Run the chat
    analysis_conv = chat(sample_data, key)