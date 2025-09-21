from typing import List, Dict

def interpret_spread(spread: str, cards: List[Dict], intent: str = "") -> List[Dict]:
    out = []
    positions = []
    if spread.startswith("1"):
        positions = ["Insight"]
    else:
        positions = ["Past", "Present", "Future"][:len(cards)]
    for pos, card in zip(positions, cards):
        meaning = card['reversed'] if card.get('is_reversed') else card['upright']
        if intent:
            meaning = f"{meaning} (in context of '{intent}')"
        out.append({"position": pos, "meaning": meaning})
    return out
