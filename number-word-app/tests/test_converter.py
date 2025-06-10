class TestConverter(unittest.TestCase):
    def test_converter(self):
        result = convert_number_to_word(5)
        self.assertIn("five", result.lower())
        self.assertIn("mare", result.lower())  # Fixed indentation here

if __name__ == '__main__':
    unittest.main()