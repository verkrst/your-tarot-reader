"""Card drawing logic with optional deterministic seeding."""

from typing import List, Dict, Optional
import random
import pandas as pd


def shuffle_and_draw(
    deck: pd.DataFrame,
    n: int = 1,
    seed: Optional[int] = None,
    allow_reversed: bool = True
) -> List[Dict]:
    """Draw unique cards from the deck.

    Shuffles indices (optionally with a fixed RNG seed) and returns the first
    ``n`` cards as dictionaries. When ``allow_reversed`` is True, each card is
    independently flagged as reversed with 50% probability via the same RNG.
    The original card fields are preserved and an ``is_reversed`` boolean is
    added to each result.

    :param deck: Deck DataFrame from ``load_deck``.
    :param n: Number of cards to draw (>= 1).
    :param seed: Optional RNG seed for reproducible draws.
    :param allow_reversed: Whether to randomly mark cards as reversed.
    :return: List of card dicts (each includes ``is_reversed``).
    :raises ValueError: If ``n`` < 1 or ``n`` exceeds the number of cards.
    """
    if n <= 0:
        raise ValueError("n must be >= 1")
    if len(deck) < n:
        raise ValueError("Deck too small for requested draw")

    rnd = random.Random(seed) if seed is not None else random.Random()
    indices = list(range(len(deck)))
    rnd.shuffle(indices)

    chosen = indices[:n]
    results = []
    for idx in chosen:
        row = deck.iloc[idx].to_dict()
        row["is_reversed"] = bool(allow_reversed and (rnd.random() < 0.5))
        results.append(row)
    return results
