from tarot.deck import load_deck
from tarot.draw import shuffle_and_draw
from tarot.interpret import interpret_spread

def test_interpret_contains_intent_and_positions():
    deck = load_deck("data/deck.csv")
    cards = shuffle_and_draw(deck, n=3, seed=7, allow_reversed=False)
    interp = interpret_spread("3-card (Past/Present/Future)", cards, intent="career")
    assert [i["position"] for i in interp] == ["Past", "Present", "Future"]
    assert all("career" in i["meaning"] for i in interp)

