from tarot.deck import load_deck
from tarot.draw import shuffle_and_draw
import pytest

def test_deterministic_seed():
    deck = load_deck("data/deck.csv")
    a = shuffle_and_draw(deck, n=3, seed=123, allow_reversed=True)
    b = shuffle_and_draw(deck, n=3, seed=123, allow_reversed=True)
    assert [x["name"] for x in a] == [x["name"] for x in b]
    assert [x.get("is_reversed", False) for x in a] == [x.get("is_reversed", False) for x in b]

def test_unique_cards():
    deck = load_deck("data/deck.csv")
    cards = shuffle_and_draw(deck, n=5, seed=1)
    names = [c["name"] for c in cards]
    assert len(names) == len(set(names))

def test_invalid_n_raises():
    deck = load_deck("data/deck.csv")
    with pytest.raises(ValueError):
        shuffle_and_draw(deck, n=0)
    with pytest.raises(ValueError):
        shuffle_and_draw(deck, n=len(deck)+1)
