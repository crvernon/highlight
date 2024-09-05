import unittest

import tiktoken

import highlight as hlt


class TestGetTokenCount(unittest.TestCase):
    def test_get_token_count_default_model(self):
        text = "This is a test."
        expected_token_count = len(tiktoken.encoding_for_model("gpt-4o").encode(text))
        self.assertEqual(hlt.get_token_count(text), expected_token_count)

    def test_get_token_count_custom_model(self):
        text = "Another test."
        model = "gpt-3.5-turbo"
        expected_token_count = len(tiktoken.encoding_for_model(model).encode(text))
        self.assertEqual(hlt.get_token_count(text, model), expected_token_count)

    def test_get_token_count_empty_text(self):
        text = ""
        expected_token_count = len(tiktoken.encoding_for_model("gpt-4o").encode(text))
        self.assertEqual(hlt.get_token_count(text), expected_token_count)


if __name__ == "__main__":
    unittest.main()
