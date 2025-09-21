from datetime import date
from tarot.astro import card_from_date

def test_aries_decan1():
    # Around March 25 → Aries decan 1 → Two of Wands
    c = card_from_date(date(2024, 3, 25))
    assert c["name"] == "Two of Wands"

def test_taurus_decan2():
    # Around May 5 → Taurus decan 2 → Six of Pentacles
    c = card_from_date(date(2024, 5, 5))
    assert c["name"] == "Six of Pentacles"

def test_sagittarius_decan2():
    # Around Dec 5 → Sagittarius decan 2 → Nine of Wands
    c = card_from_date(date(2024, 12, 5))
    assert c["name"] == "Nine of Wands"
