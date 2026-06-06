import re

def clean_text(text: str) -> str:
    """
    Standardizes input text by forcing lowercase and stripping 
    unwanted special symbols or structural line breaks.
    """
    if not text:
        return ""
    text = text.lower()
    # Replace newlines and tabs with spaces
    text = re.sub(r'[\r\n\t]+', ' ', text)
    # Strip non-alphanumeric marks, keeping standard sentence punctuation
    text = re.sub(r'[^a-z0-9\s\.\,\?\!]', '', text)
    # Collapse multiple consecutive spaces into a single space
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def split_into_sentences(text: str) -> list[str]:
    """
    Splits a body of text into individual sentences based on standard punctuation marks.
    Filters out empty or short fragments.
    """
    cleaned = clean_text(text)
    # Split using punctuation delimiters
    sentences = re.split(r'[\.\?\!]', cleaned)
    # Return trimmed, non-empty sentences containing actual words
    return [s.strip() for s in sentences if len(s.strip()) > 8]