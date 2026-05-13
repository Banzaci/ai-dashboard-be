import re
from dateparser import parse


def extract_date(text: str):

    text = text.lower()

    # ----------------------------
    # 1. STRICT PATTERN (HIGHEST PRIORITY)
    # ----------------------------
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

    # ----------------------------
    # 2. CLEANED PARTIAL PARSE (NOT FULL SENTENCE FIRST)
    # ----------------------------
    partial = re.search(
        r"(from|on)?\s*\d{1,2}\s*(st|nd|rd|th)?\s*(of)?\s*(january|february|march|april|may|june|july|august|september|october|november|december)",
        text,
        re.IGNORECASE
    )

    if partial:
        parsed = parse(partial.group(0))
        if parsed:
            return parsed.date().isoformat()

    # ----------------------------
    # 3. FALLBACK (LAST RESORT ONLY)
    # ----------------------------
    parsed = parse(text, settings={"PREFER_DATES_FROM": "future"})
    if parsed:
        return parsed.date().isoformat()

    return None

def extract_date_range(text: str):

    text = text.lower().replace(" of ", " ")

    match = re.search(r"from (.+?) to (.+)", text)

    if not match:
        return None, None

    start = parse(match.group(1))
    end = parse(match.group(2))

    if not start or not end:
        return None, None

    return start.date().isoformat(), end.date().isoformat()