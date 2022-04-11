from .tokenizer_factory import TokenizerFactory
from .test_gpt2_tokenizer import TEST_TOKENS, TEST_PROMPT, TEST_TOKEN_IDS


class TestGPTJTokenizer:
    def setup_method(self):
        self.tokenizer = TokenizerFactory.get_tokenizer("huggingface/gptj_6b")

    def test_encode(self):
        assert self.tokenizer.encode(TEST_PROMPT) == TEST_TOKEN_IDS

    def test_decode(self):
        assert self.tokenizer.decode(TEST_TOKEN_IDS) == TEST_PROMPT

    def test_tokenize(self):
        assert self.tokenizer.tokenize(TEST_PROMPT) == TEST_TOKENS

    def test_fits_within_context_window(self):
        # Should fit in the context window since we subtracted the number of tokens of the test prompt
        # from the max context window
        assert self.tokenizer.fits_within_context_window(TEST_PROMPT, 2048 - 51)
        # Should not fit in the context window because we're expecting one more extra token in the completion
        assert not self.tokenizer.fits_within_context_window(TEST_PROMPT, 2048 - 51 + 1)

    def test_truncate_from_right(self):
        # Create a prompt that exceed max context length: 51 * 41 = 2091 tokens
        long_prompt: str = TEST_PROMPT * 41
        assert not self.tokenizer.fits_within_context_window(long_prompt)

        # Truncate and ensure it fits within the context window
        truncated_long_prompt: str = self.tokenizer.truncate_from_right(long_prompt)
        assert self.tokenizer.tokenize_and_count(truncated_long_prompt) == 2048
        assert self.tokenizer.fits_within_context_window(truncated_long_prompt)

    def test_tokenize_and_count(self):
        assert self.tokenizer.tokenize_and_count(TEST_PROMPT) == 51