"""Utilities for converting Persian/Arabic digits to English and back."""

# Persian (۰-۹) and Arabic-Indic (٠-٩) digit mappings
_FA_DIGITS = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789')

def fa_to_en(text):
    """Convert Persian/Arabic digits in a string to English digits."""
    if not text:
        return text
    return str(text).translate(_FA_DIGITS)

def to_number(value, default=0):
    """Convert a form value (possibly with Persian digits/commas) to float.

    Returns `default` for empty or non-numeric input.
    """
    if value is None:
        return default
    cleaned = fa_to_en(str(value)).replace(',', '').strip()
    if not cleaned:
        return default
    try:
        return float(cleaned)
    except ValueError:
        return default
