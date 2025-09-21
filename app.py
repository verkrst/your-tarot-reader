import streamlit as st
import pandas as pd
from datetime import datetime, date, timezone
from tarot.deck import load_deck
from tarot.draw import shuffle_and_draw
from tarot.interpret import interpret_spread
from tarot.storage import save_reading, load_history

st.set_page_config(page_title="Your Tarot Reader", page_icon="🔮", layout="wide")
st.title("🔮 Your Tarot Reader")


with st.sidebar:
    st.header("Reading options")
    spread = st.selectbox("Spread", ["1-card", "3-card (Past/Present/Future)"])
    allow_reversed = st.checkbox("Allow reversed cards", value=True)
    intent = st.text_input("Intent / question (optional)", placeholder="e.g., career, love, guidance...")

    st.divider()
    st.caption("Astrology mode (Sun → decan → card)")
    astro_date = st.date_input("Choose a date", help="Maps the Sun's sign/decan to a pip card")
    astro_btn = st.button("✨ Draw by Sun decan", use_container_width=True)

    with st.expander("Advanced", expanded=False):
        mode = st.radio("Randomness", ["Daily card (fixed per day)", "Random (seeded)", "Random (no seed)"], index=2)
        seed = None
        if mode == "Daily card (fixed per day)":
            from datetime import date
            seed = int(date.today().strftime("%Y%m%d"))
            st.caption(f"Using daily seed: {seed}")
        elif mode == "Random (seeded)":
            seed = st.number_input("Seed (integer)", value=42, step=1)

    draw_btn = st.button("🔀 Shuffle & Draw", use_container_width=True)

deck = load_deck("data/deck.csv")

# Astrology trigger
from tarot.astro import card_from_date
if astro_btn:
    card_info = card_from_date(astro_date)
    # Look up full meanings from deck; if missing, inform user
    row = deck.loc[deck["name"] == card_info["name"]]
    if row.empty:
        st.warning(f"Card **{card_info['name']}** not found in deck.csv. Add it to see meanings.")
        selected = [{
            "name": card_info["name"],
            "arcana": card_info["arcana"],
            "suit": card_info["suit"],
            "keywords": "",
            "upright": "",
            "reversed": "",
            "is_reversed": False,
        }]
        interp = [{"position": "Insight", "meaning": "(no meaning — add this card to data/deck.csv)"}]
    else:
        r = row.iloc[0].to_dict()
        r["is_reversed"] = False
        selected = [r]
        interp = [{"position": "Insight", "meaning": r["upright"]}]
    st.session_state["last_reading"] = {
        "spread": "1-card (astrology)",
        "intent": intent or "",
        "cards": selected,
        "interp": interp,
        "seed": None,
        "timestamp": __import__("datetime").datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    }

# Random draw trigger
if draw_btn:
    n = 1 if spread.startswith("1") else 3
    cards = shuffle_and_draw(deck, n=n, seed=seed, allow_reversed=allow_reversed)
    interp = interpret_spread(spread, cards, intent=intent or "")
    st.session_state["last_reading"] = {
        "spread": spread,
        "intent": intent,
        "cards": cards,
        "interp": interp,
        "seed": seed,
        "timestamp": __import__("datetime").datetime.utcnow().isoformat()
    }


if draw_btn:
    n = 1 if spread.startswith("1") else 3
    cards = shuffle_and_draw(deck, n=n, seed=seed, allow_reversed=allow_reversed)
    interp = interpret_spread(spread, cards, intent=intent or "")
    st.session_state["last_reading"] = {"spread": spread, "intent": intent, "cards": cards, "interp": interp, "seed": seed, "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}

if "last_reading" in st.session_state:
    reading = st.session_state["last_reading"]
    st.subheader("Your reading")

    cols = st.columns(len(reading["cards"]))
    for i, (card, col) in enumerate(zip(reading["cards"], cols), start=1):
        with col:
            # support both the new flag (is_reversed) and any older saves (reversed)
            is_rev = bool(card.get("is_reversed", card.get("reversed", False)))
            title = f"{card['name']}" + (" (reversed)" if is_rev else "")
            st.markdown(f"### {i}. {title}")

            suit = card.get("suit")
            arcana = str(card.get("arcana", "")).strip()
            st.caption(f"{arcana} — {suit}" if isinstance(suit, str) and suit.strip() else arcana)

            st.write(f"**Keywords:** {card.get('keywords', '')}")

            meaning = reading["interp"][i - 1]["meaning"]
            st.write(meaning)

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💾 Save to history"):
            save_reading("readings.csv", reading)
            st.success("Saved to history (readings.csv).")
    with c2:
        st.download_button(
            "⬇️ Download this reading (JSON)",
            data=pd.Series(reading).to_json(),
            file_name="reading.json",
            mime="application/json",
        )

st.subheader("History")
hist = load_history("readings.csv")
if hist.empty:
    st.info("No saved readings yet. Draw and click 'Save to history'.")
else:
    # make a display-friendly copy so Arrow/Streamlit can render it
    hist_disp = hist.copy()
    hist_disp["cards"] = hist_disp["cards"].apply(
        lambda cs: ", ".join([f"{c['name']}{' (reversed)' if c.get('is_reversed', c.get('reversed', False)) else ''}" for c in cs])
    )
    hist_disp["interp"] = hist_disp["interp"].apply(
        lambda xs: " | ".join([f"{x['position']}: {x['meaning']}" for x in xs])
    )
    st.dataframe(hist_disp[["timestamp", "spread", "intent", "cards", "interp"]], use_container_width=True)

    # simple frequency chart by card name (use the raw column, not the stringified one)
    by_card = hist["cards"].explode().apply(lambda c: c["name"])
    st.bar_chart(by_card.value_counts())
