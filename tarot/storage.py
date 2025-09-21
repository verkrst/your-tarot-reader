"""Persist and reload reading history as JSON records.

The history file stores an array of JSON objects. Rich fields like
``cards`` and ``interp`` are kept as lists of dicts. Timestamps are
kept as plain strings to avoid auto date parsing issues.
"""

from pathlib import Path
import pandas as pd


def save_reading(path: str, reading: dict) -> None:
    """Append a reading to the history file.

    Creates the file if it does not exist, loads existing records,
    appends one row, and writes JSON records back to disk.

    :param path: Path to the history file (e.g., ``readings.json`` or ``readings.csv``).
    :param reading: Dict with keys: ``timestamp``, ``spread``, ``intent``,
                    ``seed``, ``cards`` (list[dict]), ``interp`` (list[dict]).
    :return: None
    """
    p = Path(path)
    p.touch(exist_ok=True)
    df = load_history(path)
    row = {
        "timestamp": reading["timestamp"],
        "spread": reading["spread"],
        "intent": reading["intent"],
        "seed": reading["seed"],
        "cards": reading["cards"],   # keep as list[dict]
        "interp": reading["interp"], # list[dict]
    }
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_json(p, orient="records", indent=2)


def load_history(path: str) -> pd.DataFrame:
    """Load the reading history without auto-parsing dates.

    If the file is missing or empty, returns an empty DataFrame with the
    expected columns. Date parsing is disabled so ``timestamp`` remains a
    plain string.

    :param path: Path to the history file.
    :return: DataFrame with columns: ``timestamp``, ``spread``, ``intent``,
             ``seed``, ``cards``, ``interp``.
    """
    p = Path(path)
    if not p.exists() or p.stat().st_size == 0:
        return pd.DataFrame(columns=["timestamp", "spread", "intent", "seed", "cards", "interp"])
    try:
        return pd.read_json(p, convert_dates=False)
    except ValueError:
        return pd.DataFrame(columns=["timestamp", "spread", "intent", "seed", "cards", "interp"])
