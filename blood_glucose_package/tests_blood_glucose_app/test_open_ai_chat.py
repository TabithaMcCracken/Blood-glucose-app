import os
import unittest
from unittest.mock import patch
from io import StringIO
from blood_glucose_package.scripts.blood_glucose_app import chat

ModuleNotFoundError: 
/Users/tabithamccracken/Documents/codingnomads/blood_glucose_app/blood_glucose_package/open_ai_chat.py

class TestChatFunction(unittest.TestCase):

    def setUp(self):
        self.key = "test_key"
        self.sample_data = (
            "2023-08-02 14:55:00:172.0, 2023-08-02 15:00:00:169.0, "
            "2023-08-02 15:05:00:169.0"
        )

    @patch('builtins.input', side_effect=['exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_chat_exit(self, mock_stdout, mock_input):
        chat(self.sample_data, self.key)
        expected_output = "To exit the conversation, type: 'exit'.\nUser: "
        self.assertIn(expected_output, mock_stdout.getvalue())

    @patch('openai.OpenAI')
    @patch('builtins.input', side_effect=['Hello', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_chat_with_input(self, mock_stdout, mock_input, mock_openai):
        chat(self.sample_data, self.key)
        expected_output = "To exit the conversation, type: 'exit'.\nUser: "
        self.assertIn(expected_output, mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
