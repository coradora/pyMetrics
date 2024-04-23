import unittest
from unittest.mock import patch
from main import generate_random_number, is_even, main


class TestMain(unittest.TestCase):
    def test_generate_random_number(self):
        # Test if the generated number is within the expected range
        number = generate_random_number()
        self.assertTrue(1 <= number <= 20, "The number should be between 1 and 20")

    def test_is_even(self):
        # Test known even number
        self.assertTrue(is_even(2), "2 should be even")
        # Test known odd number
        self.assertFalse(is_even(1), "1 should be odd")

    @patch('builtins.input', return_value='n')  
    def test_main(self, mock_input):
        main()
if __name__ == '__main__':
    unittest.main()