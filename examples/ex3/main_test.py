import unittest
from unittest.mock import patch
from main import factorial, main

class TestFactorial(unittest.TestCase):

    # Purposefully incorrect test case.
    def test_factorial_zero(self):
        self.assertEqual(factorial(0), 0, "Factorial of 0 should be 1")

    def test_factorial_one(self):
        self.assertEqual(factorial(1), 1, "Factorial of 1 should be 1")

    def test_factorial_positive(self):
        self.assertEqual(factorial(4), 24, "Factorial of 4 should be 24")
        self.assertEqual(factorial(5), 120, "Factorial of 5 should be 120")

    def test_negative_input(self):
        with self.assertRaises(ValueError, msg="Should raise ValueError for negative input"):
            factorial(-1)

    @patch('builtins.input', return_value='5')
    def test_main(self, mock_input):
        main()

if __name__ == "__main__":
    unittest.main()