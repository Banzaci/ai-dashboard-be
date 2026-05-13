import re
from dateparser import parse


def extract_date(text: str):

    # 1. försök hitta explicita datum
    patterns = [
        r"\d{4}-\d{2}-\d{2}",
        r"\d{1,2}\s*(st|nd|rd|th)?\s*(of)?\s*(january|february|march|april|may|june|july|august|september|october|november|december)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            parsed = parse(match.group(0))
            if parsed:
                return parsed.date().isoformat()

    # fallback: full sentence parse
    parsed = parse(text)
    if parsed:
        return parsed.date().isoformat()

    return None