import pytest
from services.keyword_detector import KeywordDetector

# Test cases: (input_text, expected_keywords_list)
def keyword_test_cases():
    return [
        ("Check out the new ChatGPT features", ['chatgpt']),
        ("OpenAI releases GPT-4 model", ['openai', 'gpt-4']),
        ("Story about LLMs and machine learning advancements", ['llm', 'large language model', 'machine learning']),
        ("Building a simple neural network", ['neural network']),
        ("Analysis of Claude by Anthropic", ['claude', 'anthropic']),
        ("This title has no AI keywords.", []),
        ("Using midjourney for image generation", ['midjourney']),
        ("Training data for ML models", ['machine learning']), # ML is substring, should not match
        ("Deep learning is fascinating", ['deep learning']),
        ("Is Dall-E the best?", ['dalle', 'dall-e']),
        ("", []),
        (None, []),
        ("Llm", ['llm', 'large language model']), # Case-insensitivity, and llm implies large language model by our rule
        ("using chatgpt.", ['chatgpt']), # Punctuation
        ("The gpt-4 model is powerful", ['gpt-4']), # Word boundary
        ("An openai project", ['openai']), # Word boundary
        ("This title mentions llm and also LLM", ['llm', 'large language model']) # Should only appear once, and llm implies large language model
    ]

@pytest.mark.parametrize("text, expected_keywords", keyword_test_cases())
def test_find_ai_keywords(text, expected_keywords):
    found = KeywordDetector.find_ai_keywords(text)
    # Sort both lists to ensure order doesn't affect comparison
    assert sorted(found) == sorted(expected_keywords)

def test_is_ai_related():
    assert KeywordDetector.is_ai_related("New GPT-4 study released") is True
    assert KeywordDetector.is_ai_related("Updates on cloud computing") is False
    assert KeywordDetector.is_ai_related(None) is False
    assert KeywordDetector.is_ai_related("") is False 