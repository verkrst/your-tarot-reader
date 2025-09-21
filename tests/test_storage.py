from tarot.storage import save_reading, load_history

def test_save_and_load_history(tmp_path):
    p = tmp_path / "hist.json"
    reading = {
        "timestamp": "2025-01-01 12:00:00",
        "spread": "1-card (astrology)",
        "intent": "",
        "seed": None,
        "cards": [{
            "name":"Two of Wands","suit":"Wands","arcana":"Minor",
            "is_reversed": False, "upright":"Meaning U", "reversed":"Meaning R", "keywords":""
        }],
        "interp": [{"position":"Insight","meaning":"Meaning U"}],
    }
    save_reading(str(p), reading)
    df = load_history(str(p))
    # columns, timestamp stays as string, and rich fields remain list[dict]
    assert list(df.columns) == ["timestamp","spread","intent","seed","cards","interp"]
    assert df.iloc[0]["timestamp"] == "2025-01-01 12:00:00"
    assert isinstance(df.iloc[0]["cards"], list)
    assert isinstance(df.iloc[0]["interp"], list)
