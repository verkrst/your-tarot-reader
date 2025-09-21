import pandas as pd

REQUIRED_COLS = ["name","arcana","suit","keywords","upright","reversed"]

def load_deck(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Deck is missing columns: {missing}")
    return df
