# tarot/astro.py
from datetime import date, datetime

NUM_TO_NAME = {2:"Two",3:"Three",4:"Four",5:"Five",6:"Six",7:"Seven",8:"Eight",9:"Nine",10:"Ten"}

# Sign start/end (approximate tropical zodiac date ranges)
SIGN_RANGES = [
    ("Capricorn", (12,22), (1,19)),
    ("Aquarius",  (1,20),  (2,18)),
    ("Pisces",    (2,19),  (3,20)),
    ("Aries",     (3,21),  (4,19)),
    ("Taurus",    (4,20),  (5,20)),
    ("Gemini",    (5,21),  (6,20)),
    ("Cancer",    (6,21),  (7,22)),
    ("Leo",       (7,23),  (8,22)),
    ("Virgo",     (8,23),  (9,22)),
    ("Libra",     (9,23),  (10,22)),
    ("Scorpio",   (10,23), (11,21)),
    ("Sagittarius",(11,22),(12,21)),
]

# Decan → card mapping (Golden Dawn style for the 36 pip cards)
SIGN_TO_DECAN = {
    "Aries":       [("Wands",2),("Wands",3),("Wands",4)],
    "Taurus":      [("Pentacles",5),("Pentacles",6),("Pentacles",7)],
    "Gemini":      [("Swords",8),("Swords",9),("Swords",10)],
    "Cancer":      [("Cups",2),("Cups",3),("Cups",4)],
    "Leo":         [("Wands",5),("Wands",6),("Wands",7)],
    "Virgo":       [("Pentacles",8),("Pentacles",9),("Pentacles",10)],
    "Libra":       [("Swords",2),("Swords",3),("Swords",4)],
    "Scorpio":     [("Cups",5),("Cups",6),("Cups",7)],
    "Sagittarius": [("Wands",8),("Wands",9),("Wands",10)],
    "Capricorn":   [("Pentacles",2),("Pentacles",3),("Pentacles",4)],
    "Aquarius":    [("Swords",5),("Swords",6),("Swords",7)],
    "Pisces":      [("Cups",8),("Cups",9),("Cups",10)],
}

def _date_in_range(d: date, start, end) -> bool:
    sm, sd = start; em, ed = end
    if sm <= em:  # normal (no year wrap)
        return (d.month, d.day) >= (sm, sd) and (d.month, d.day) <= (em, ed)
    # wraps year end (e.g., Capricorn)
    return (d.month, d.day) >= (sm, sd) or (d.month, d.day) <= (em, ed)

def _sign_for_date(d: date) -> str:
    for sign, start, end in SIGN_RANGES:
        if _date_in_range(d, start, end):
            return sign
    # Fallback (shouldn't happen)
    return "Aries"

def _sign_start_date(d: date, start) -> date:
    sm, sd = start
    # Handle year wrap: if start is in Dec and d is in Jan, use previous year
    year = d.year
    if sm == 12 and d.month == 1:
        year -= 1
    return date(year, sm, sd)

def _decan_index(d: date, sign: str) -> int:
    # days since sign start → 0..2 buckets of ~10 days
    for s, start, end in SIGN_RANGES:
        if s == sign:
            start_date = _sign_start_date(d, start)
            delta = (d - start_date).days
            return min(max(delta // 10, 0), 2)
    return 0

def card_from_date(d: date) -> dict:
    """Return a dict with at least name/suit/arcana for the Sun's decan on date d."""
    sign = _sign_for_date(d)
    decan = _decan_index(d, sign)
    suit, num = SIGN_TO_DECAN[sign][decan]
    name = f"{NUM_TO_NAME[num]} of {suit}"
    return {
        "name": name,
        "suit": suit,
        "arcana": "Minor",
        "is_reversed": False,  # astrology mode returns upright by default
    }
