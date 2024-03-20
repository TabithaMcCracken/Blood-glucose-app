import unittest
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch  # For Python versions < 3.3
from blood_glucose_package.token_count import num_tokens_from_string

class TestNumTokensFromString(unittest.TestCase):
    def test_valid_input(self):
        sample_data = "2023-08-02 14:55:00:172.0, 2023-08-02 15:00:00:169.0, 2023-08-02 15:05:00:169.0"
        result = num_tokens_from_string(sample_data)
        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)

    def test_empty_input(self):
        sample_data = ""
        result = num_tokens_from_string(sample_data)
        self.assertEqual(result, 0)

    def test_invalid_input(self):
        sample_data = ["2023-08-02 14:55:00:172.0", "2023-08-02 15:00:00:169.0"]
        with self.assertRaises(ValueError):
            num_tokens_from_string(sample_data)

    def test_exception_handling(self):
            sample_data = ["2023-08-02 14:55:00:172.0", "2023-08-02 15:00:00:169.0"]
            with self.assertRaises(ValueError, msg="Invalid input type. Only strings or integers are allowed."):
                num_tokens_from_string(sample_data)

if __name__ == "__main__":
    unittest.main()