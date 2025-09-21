from typing import List, Dict, Optional
import random
import pandas as pd

def shuffle_and_draw(deck: pd.DataFrame, n: int = 1, seed: Optional[int] = None, allow_reversed: bool = True) -> List[Dict]:
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
        row['is_reversed'] = bool(allow_reversed and (rnd.random() < 0.5))
        results.append(row)
    return results
