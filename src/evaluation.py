# evaluation.py
from logging_config import setup_logger

logger = setup_logger(__name__)

def normalize_text(text: str) -> str:
    """
    Normalizes text by converting various apostrophe types to standard straight apostrophe.
    This includes curly quotes and other common variants.
    """
    if not text:
        return text
        
    # Dict of apostrophe variants and their replacements
    apostrophe_variants = {
        '\u2019': "'",  # Right single quotation mark
        '\u2018': "'",  # Left single quotation mark
        '\u201B': "'",  # Single high-reversed-9 quotation mark
        '\u2032': "'",  # Prime
        '\u0060': "'",  # Grave accent
        '\u00B4': "'",  # Acute accent
    }
    
    normalized = text
    for variant, replacement in apostrophe_variants.items():
        normalized = normalized.replace(variant, replacement)
    
    return normalized

def evaluate_response(correct_answer: str, model_response: str) -> bool:
    """
    Returns True if the normalized correct_answer is a substring
    of the normalized model_response (case-insensitive).
    """
    if not model_response:
        logger.debug("Model response is empty or None.")
        return False

    # Normalize both strings and convert to lowercase for comparison
    normalized_answer = normalize_text(correct_answer).strip().lower()
    normalized_response = normalize_text(model_response).strip().lower()
    
    return normalized_answer in normalized_response