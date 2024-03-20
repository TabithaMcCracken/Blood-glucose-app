import unittest
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch  # For Python versions < 3.3
from blood_glucose_package.blood_glucose_app import num_tokens_from_string