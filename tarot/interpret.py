"""Generate concise interpretations for supported spreads."""

from typing import List, Dict


def interpret_spread(spread: str, cards: List[Dict], intent: str = "") -> List[Dict]:
    """Create an interpretation for the given spread and cards.

    For 1-card spreads, the position label is ``Insight``.
    For 3-card spreads, the labels are ``Past``, ``Present``, ``Future`` (truncated
    to the number of cards provided).

    :param spread: Spread name (e.g., "1-card", "3-card (Past/Present/Future)").
    :param cards: List of card dicts that include ``upright``, ``reversed``,
                  and optional ``is_reversed`` (bool).
    :param intent: Optional short context string (e.g., "career", "love").
    :return: List of dicts with keys: ``position`` and ``meaning``.
    """
    positions = ["Insight"] if spread.startswith("1") else ["Past", "Present", "Future"][: len(cards)]

    out: List[Dict] = []
    for pos, card in zip(positions, cards):
        # choose upright or reversed meaning; default to empty strings if missing
        meaning = card.get("reversed", "") if card.get("is_reversed") else card.get("upright", "")
        if intent:
            meaning = f"{meaning} (in context of '{intent}')"
        out.append({"position": pos, "meaning": meaning})
    return out
