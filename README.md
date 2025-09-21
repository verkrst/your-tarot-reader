# 🔮 Tarotly — Simple Tarot Readings (Streamlit)

Small Streamlit app for tarot spreads (1-card, 3-card). Deterministic daily seed, optional random seed, reversed cards, and a simple reading history.

## Quickstart
```bash
pip install -r requirements.txt
streamlit run app.py
# open the URL (usually http://localhost:8501)
```

## Tests & CI
```bash
pytest -q
```
GitHub Actions runs the same tests on every push/PR (see `.github/workflows/ci.yml`).

## Docker
```bash
docker build -t tarotly .
docker run -p 8501:8501 tarotly
```

## Data
Card data lives in `data/deck.csv`. Add/extend rows to include the full deck. Columns:
- `name` — card name (e.g., The Fool)
- `arcana` — Major/Minor
- `suit` — Cups/Wands/Swords/Pentacles or blank for Major
- `keywords` — comma-separated keywords
- `upright` — upright meaning
- `reversed` — reversed meaning
