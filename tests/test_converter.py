import unittest
from app.converter import convert_number

class TestNumberToWordConverter(unittest.TestCase):

    def test_predefined_fallback(self):
        # Test predefined fallback for a single number
        result = convert_number("99")['result']
        valid_results = {"pap", "pea pea"}
        self.assertIn(result, valid_results,
                      f"Expected one of {valid_results}, but got {result}")

    def test_no_word(self):
        # Test for numbers that cannot be converted
        result = convert_number("000")['result']
        self.assertEqual(result, "No word or phrase found for this number.")

    def test_full_match(self):
        # Test for a direct predefined match
        result = convert_number("10")['result']
        valid_results = {"tease"}
        self.assertIn(result, valid_results,
                      f"Expected one of {valid_results}, but got {result}")

    def test_decimal_number(self):
        # Test for decimal numbers
        result = convert_number("45.78")['result']
        valid_results = {"rail point cave"}
        self.assertIn(result, valid_results,
                      f"Expected one of {valid_results}, but got {result}")

    def test_chunking(self):
        # Test for chunking numbers into predefined words
        result = convert_number("543")['result']
        possible_results = set(result.split("\n"))
        valid_results = {"lea ram", "lair ma", "lea ear ma"}
        self.assertTrue(
            any(res.split(") ")[1] in valid_results for res in possible_results if ") " in res),
            f"Expected one of {valid_results}, but got {possible_results}"
        )

    def test_multiple_results(self):
        # Test for numbers that can have multiple valid chunking combinations
        result = convert_number("123")['result']
        possible_results = set(result.split("\n"))
        valid_results = {"tit ma", "tin ma", "tie name"}
        self.assertTrue(
            any(res.split(") ")[1] in valid_results for res in possible_results if ") " in res),
            f"Expected one of {valid_results}, but got {possible_results}"
        )

    def test_invalid_input(self):
        # Test for invalid input
        result = convert_number("abc")['result']
        self.assertEqual(result, "No word or phrase found for this number.")

    def test_large_number(self):
        # Test for a large number with multiple chunking possibilities
        result = convert_number("123456")['result']
        possible_results = set(result.split("\n"))
        valid_results = {"tin ma lash", "tie noah ma rail shea"}
        self.assertTrue(
            any(res.split(") ")[1] in valid_results for res in possible_results if ") " in res),
            f"Expected one of {valid_results}, but got {possible_results}"
        )

if __name__ == "__main__":
    unittest.main()