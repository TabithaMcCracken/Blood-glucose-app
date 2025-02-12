
import os
import sys
from openai import OpenAI
import PySimpleGUI as sg
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from modules.token_count import num_tokens_from_string

def chat(cgm_data, key):
    """Generates a conversation with OpenAI and displays the entire conversation in a PySimpleGUI window.

    Args:
        cgm_data (tuple): 24 hours of blood glucose data in 5-minute increments
        key (str): OpenAI API key

    Returns:
        None
    """

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

    # Create the layout for the window
    layout = [
        [sg.Text('ChatGPT Analysis')],
        [sg.Multiline(size=(60, 20), key='-CONVERSATION-', disabled=True)],
        [sg.InputText(size=(45, 1), key='-USER_INPUT-'), sg.Button('Send')]
    ]

    # Create the window with finalize=True
    window = sg.Window('ChatGPT Conversation', layout, return_keyboard_events=True, finalize=True)

    # Process the initial analysis and update the window
    token_size = num_tokens_from_string(chatbot_conversation)

    if token_size < 128000:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=chatbot_conversation
        )

        chatbot_response = response.choices[0].message.content
        chatbot_conversation.append({"role": "assistant", "content": chatbot_response})

        # Update the conversation in the window, skipping both system and initial user prompt
        conversation_text = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in chatbot_conversation[2:]])  # Skip the first two messages (system and initial user prompt)
        window['-CONVERSATION-'].update(conversation_text)

    else:
        sg.popup("Conversation too large to process.")
        window.close()
        return

    # Main event loop to handle user input and responses
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == 'Send':
            user_input = values['-USER_INPUT-']
            chatbot_conversation.append({"role": "user", "content": user_input})

            # Process the conversation with OpenAI
            token_size = num_tokens_from_string(chatbot_conversation)

            if token_size < 128000:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=chatbot_conversation
                )

                chatbot_response = response.choices[0].message.content
                chatbot_conversation.append({"role": "assistant", "content": chatbot_response})

                # Update the conversation in the window, starting from the assistant's response
                conversation_text = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in chatbot_conversation[2:]])  # Skip both the system and initial user prompt
                window['-CONVERSATION-'].update(conversation_text)
            else:
                sg.popup("Conversation too large to process.")
                break

            window['-USER_INPUT-'].update('')

    window.close()

if __name__ == "__main__":
    key = os.environ.get('OPENAI_KEY')
    sample_data = "2023-08-02 14:55:00:172.0, 2023-08-02 15:00:00:169.0, 2023-08-02 15:05:00:169.0"
    analysis_conv = chat(sample_data, key)