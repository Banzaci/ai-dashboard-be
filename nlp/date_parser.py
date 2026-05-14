from datetime import datetime, timedelta
import re
import dateparser
from typing import Any, Dict
import re

def parse_date(text: str):
    if not text:
        return None

    text = text.lower().strip()

    # ----------------------------
    # 1. CLEAN COMMON NORMALIZATION
    # ----------------------------
    text = text.replace("st", "").replace("nd", "").replace("rd", "").replace("th", "")

    # normalize "1 of june" → "1 june"
    text = re.sub(r"(\d)\s+of\s+", r"\1 ", text)

    # ----------------------------
    # 2. DATEPARSER CORE (MAIN ENGINE)
    # ----------------------------
    settings: Dict[str, Any] = {
        "PREFER_DATES_FROM": "future",
        "RELATIVE_BASE": datetime.now(),
        "STRICT_PARSING": False
    }

    parsed = dateparser.parse(text, settings=settings)  # type: ignore

    if parsed:
        return parsed.date()

    # ----------------------------
    # 3. FALLBACK: STRICT PATTERN MATCH (LAST RESORT)
    # ----------------------------
    match = re.search(r"(\d{1,2})\s*([a-zA-Z]+)", text)

    if match:
        day = int(match.group(1))
        month_text = match.group(2)

        months = {
            "january": 1, "jan": 1,
            "february": 2, "feb": 2,
            "march": 3, "mar": 3,
            "april": 4, "apr": 4,
            "may": 5,
            "june": 6, "jun": 6,
            "july": 7, "jul": 7,
            "august": 8, "aug": 8,
            "september": 9, "sep": 9,
            "october": 10, "oct": 10,
            "november": 11, "nov": 11,
            "december": 12, "dec": 12,
        }

        month = months.get(month_text)

        if month:
            year = datetime.now().year
            return datetime(year, month, day).date()

    return None


def add_nights(start_date, nights: int):
    return start_date + timedelta(days=nights)