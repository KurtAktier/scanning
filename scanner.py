import time
from datetime import datetime
from zoneinfo import ZoneInfo
from notifier import send_alert, format_timestamp

TRIGGER_KEYWORDS = [
    "positive phase 2",
    "meets primary endpoint",
    "fda approval",
    "strategic partnership",
    "acquisition at premium",
    "binding loi",
    "definitive agreement to be acquired",
    "multi-million purchase order",
    "ai partnership",
]

SEEN_HEADLINES = set()


def get_danish_time_str():
    dk = ZoneInfo("Europe/Copenhagen")
    return datetime.now(dk).strftime("%d-%m-%Y %H:%M dansk tid")


def fetch_latest_news():
    """Demo-data til test — udskiftes senere med rigtige nyhedskilder."""
    demo_news = [
        {
            "ticker": "TOVX",
            "headline": "Theriva Biologics announces positive Phase 2 data in pancreatic cancer",
            "market_cap_class": "microcap",
            "source": "press release",
        },
        {
            "ticker": "WGRX",
            "headline": "Wellgistics Health signs strategic AI partnership for prescription tracking",
            "market_cap_class": "microcap",
            "source": "newswire",
        },
        {
            "ticker": "SAP",
            "headline": "SAP to present at investor conference",
            "market_cap_class": "largecap",
            "source": "PR",
        },
    ]
    return demo_news


def score_news_item(item):
    hl = item["headline"].lower()
    score = 0
    reason_bits = []

    for kw in TRIGGER_KEYWORDS:
        if kw in hl:
            score += 1
            reason_bits.append(f"keyword:{kw}")

    if item["market_cap_class"].lower() in ["microcap", "smallcap"]:
        score += 1
        reason_bits.append("microcap_boost")

    if "acquisition" in hl or "definitive agreement" in hl:
        score += 1
        reason_bits.append("deal/ma")

    return score, ", ".join(reason_bits)


def process_news_cycle():
    news_items = fetch_latest_news()
    for n in news_items:
        headline_key = n["ticker"] + "::" + n["headline"]
        if headline_key in SEEN_HEADLINES:
            continue

        score, reason = score_news_item(n)

        if score >= 2:
            note = f"{reason} // kilde:{n['source']} // {get_danish_time_str()}"
            send_alert(
                ticker=n["ticker"],
                headline=n["headline"],
                risk="Høj (microcap / nyhedsdrevet)",
                extra_note=note,
            )
            SEEN_HEADLINES.add(headline_key)

    print(f"[{format_timestamp()}] cycle done ({len(news_items)} nyheder tjekket)")


def main_loop():
    while True:
        process_news_cycle()
        time.sleep(300)  # 5 minutter


if __name__ == "__main__":
    print(f"[{format_timestamp()}] START scanner-loop")
    main_loop()
