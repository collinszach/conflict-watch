import requests
from bs4 import BeautifulSoup
from db import SessionLocal, ConflictEvent
from datetime import datetime

def fetch_liveuamap_events():
    url = "https://liveuamap.com/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    db = SessionLocal()
    added = 0

    for item in soup.find_all("div", class_="feed_item"):
        title = item.get_text(strip=True)

        if any(k in title.lower() for k in ["missile", "airstrike", "attack", "explosion", "artillery", "mobilized"]):
            if db.query(ConflictEvent).filter(ConflictEvent.summary == title).first():
                continue  # avoid duplicates

            # In real version, parse coordinates from map or enrich later
            event = ConflictEvent(
                summary=title,
                lat=30.0,   # temporary placeholder
                lon=0.0,    # temporary placeholder
                event_type="alert",
                source="Liveuamap",
                timestamp=datetime.utcnow()
            )
            db.add(event)
            added += 1

    db.commit()
    db.close()
    print(f"✅ Fetched and stored {added} new events")
