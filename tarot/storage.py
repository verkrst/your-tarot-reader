import json
import pandas as pd
from pathlib import Path

def save_reading(path: str, reading: dict) -> None:
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
    p = Path(path)
    if not p.exists() or p.stat().st_size == 0:
        return pd.DataFrame(columns=["timestamp","spread","intent","seed","cards","interp"])
    try:
        # keep timestamps as plain strings
        return pd.read_json(p, convert_dates=False)
    except ValueError:
        return pd.DataFrame(columns=["timestamp","spread","intent","seed","cards","interp"])

