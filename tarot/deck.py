"""Deck loading utilities for the Tarot app."""

import pandas as pd

REQUIRED_COLS = ["name", "arcana", "suit", "keywords", "upright", "reversed"]


def load_deck(path: str) -> pd.DataFrame:
    """Load the Tarot deck CSV and validate required columns.

    The file must contain columns: ``name``, ``arcana``, ``suit``,
    ``keywords``, ``upright``, ``reversed``.

    :param path: Path to the deck file (e.g., ``data/deck.csv``).
    :return: DataFrame of card rows.
    :raises ValueError: If any required column is missing.
    """
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Deck is missing columns: {missing}")
    return df
