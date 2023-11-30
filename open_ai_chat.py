# Things we're looking for from the API
# Blood sugar range
# General observations
# Trend Analysis: 
# Morning 6am -12noon
# Afternoon: 12noon - 6pm
# Evening: 6pm - 12midnight
# Overnight: 12midnight - 6am

from datetime import datetime, timedelta
from secret import key
import openai
from make_sample_data import generate_glucose_levels
from token_count import num_tokens_from_string

def chat(cgm_data):
    """Generates a conversation with openai.

    Args:
        cgm_data (tuple): 24 hours of bgl's in 5 minute increments

    Returns:
        list: conversation with openai
    """

    print("Welcome! Here is the analysis for this data...(Type 'exit' to quit)")


    openai.api_key = key
    chatbot_conversation = []
    system_msg = "You are a helpful assistant."
    chatbot_conversation.append({"role": "system", "content": system_msg})

    initial_user_prompt = f'Analyze the following blood glucose data where the first number is the time stamp and the second is the blood glucose level. Give us the blood glucose range, the percentage of time in range between 70 and 130, and general observations in one paragraph:\n{cgm_data}'
    chatbot_conversation.append({"role": "user", "content": initial_user_prompt})
    
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = chatbot_conversation,
        # max_tokens = 200  # Adjust based on your needs
    )
    
    
    chatbot_repsonse = response["choices"][0]["message"]["content"]
    print(f"{chatbot_repsonse}")
    chatbot_conversation.append({"role": "assistant", "content": chatbot_repsonse})
    print("What else would you like to know?")

    while True:
        if num_tokens_from_string(chatbot_conversation) < 4097:
            user_input = input ("User: ")
            if user_input.lower() == "exit":
                break

            chatbot_conversation.append({"role": "user", "content": user_input})

            token_size = num_tokens_from_string(chatbot_conversation)
            print(f"Token size: {token_size}")

            if token_size < 4097:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=chatbot_conversation
                )

                chatbot_repsonse = response["choices"][0]["message"]["content"]
                print(f"Chatbot: {chatbot_repsonse}")
                chatbot_conversation.append({"role": "assistant", "content": chatbot_repsonse})
                print(f"Token size after response: {num_tokens_from_string(chatbot_conversation)}")
                
            else:
                print("The conversation is too large to process.")
                break

        else:
            print("The conversation is too large to process.")
            break

    
    return chatbot_conversation

if __name__ == "__main__":
    # Create a data set to use
    cgm_data = generate_glucose_levels()
    token_count = num_tokens_from_string(cgm_data)
    print(token_count)
    # Run the chat
    
    # analysis_conv = chat(cgm_data)