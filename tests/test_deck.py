import pandas as pd
from tarot.deck import load_deck

def test_load_deck_columns():
    df = load_deck("data/deck.csv")
    assert {"name","arcana","suit","keywords","upright","reversed"} <= set(df.columns)
    assert len(df) > 5
