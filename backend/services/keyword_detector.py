import re
from django.conf import settings
import logging 

logger = logging.getLogger(__name__) 

class KeywordDetector:
    """Service for detecting AI-related keywords in text"""
    
    # List of AI-related keywords to detect (canonical forms)
    AI_KEYWORDS = [
        'chatgpt', 'gpt-4', 'gpt-3', 'openai', 'claude', 'anthropic', 
        'gemini', 'bard', 'llm', 'large language model', 'artificial intelligence',
        'machine learning', 'deep learning', 'neural network', 'transformer',
        'diffusion', 'midjourney', 'stable diffusion', 'dalle', 'dall-e'
    ]

    # Map specific text patterns to the list of canonical keywords they imply.
    # Order can matter if patterns overlap; more specific should ideally be first,
    # but set logic for found_keywords_set handles multiple paths to same keyword.
    VARIANT_MAP = {
        # Pattern: list of canonical keywords from AI_KEYWORDS to add if pattern matches
        re.compile(r'\bllms?\b', re.IGNORECASE): ['llm', 'large language model'],
        re.compile(r'\bml\b', re.IGNORECASE): ['machine learning'],
        re.compile(r'\bdall-e\b', re.IGNORECASE): ['dall-e', 'dalle'],
        # If text is "dalle", it will be caught by direct match of 'dalle'.
        # If text is "dall-e", it's caught by direct match of 'dall-e' AND by this rule.
        # The set ensures 'dall-e' and 'dalle' are added once.
    }
    
    @classmethod
    def find_ai_keywords(cls, text):
        """
        Find AI-related keywords in the text.
        Uses direct matching for canonical keywords and a variant map for common alternatives.
        Returns a sorted list of found canonical keywords.
        """
        if not text:
            return []
            
        found_keywords_set = set()
        
        # 1. Try direct matches for keywords in AI_KEYWORDS (canonical forms)
        for keyword in cls.AI_KEYWORDS:
            try:
                # Use word boundaries (\b) to match whole words.
                # re.escape handles special characters in keywords.
                # re.IGNORECASE makes the search case-insensitive.
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, text, re.IGNORECASE):
                    found_keywords_set.add(keyword) 
            except re.error as e:
                # Log regex compilation errors if a keyword is problematic
                logger.error(f"Regex error compiling pattern for keyword '{keyword}': {e}")
        
        # 2. Process variants from the VARIANT_MAP
        # This allows specific patterns to map to one or more canonical keywords
        for pattern_regex, canonical_keywords_to_add in cls.VARIANT_MAP.items():
            # pattern_regex is already a compiled regex object
            if re.search(pattern_regex, text):
                for canonical_keyword in canonical_keywords_to_add:
                    # Ensure we only add keywords that are defined in our canonical list
                    if canonical_keyword in cls.AI_KEYWORDS:
                        found_keywords_set.add(canonical_keyword)
                        
        return sorted(list(found_keywords_set))
    
    @classmethod
    def is_ai_related(cls, text):
        """Check if text contains any AI-related keywords"""
        return len(cls.find_ai_keywords(text)) > 0
