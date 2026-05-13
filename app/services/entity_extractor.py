import re
from dateparser import parse

from app.utils.extract_date import extract_date, extract_date_range

def extract_entities(text: str):

    # --------------------
    # guests
    # --------------------
    guests_match = re.search(
        r"(\d+)\s*(person|people|guests|pax|room)?",
        text.lower()
    )
    guests = int(guests_match.group(1)) if guests_match else 1

    # --------------------
    # dates
    # --------------------
    start_date, end_date = extract_date_range(text)

    if not start_date:
        start_date = extract_date(text)

    return {
        "guests": guests,
        "start_date": start_date,
        "end_date": end_date
    }