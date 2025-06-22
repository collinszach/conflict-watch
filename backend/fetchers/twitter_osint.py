import snscrape.modules.twitter as sntwitter
from db import SessionLocal, ConflictEvent
from datetime import datetime, timezone
import spacy
from geopy.geocoders import Nominatim

nlp = spacy.load("en_core_web_sm")
geolocator = Nominatim(user_agent="conflict-watch")

def extract_coordinates(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "GPE":
            try:
                location = geolocator.geocode(ent.text)
                if location:
                    return location.latitude, location.longitude
            except:
                pass
    return 30.0, 0.0  # fallback


WATCH_ACCOUNTS = [
    "osinttechnical",
    "war_mapper",
    "sentdefender",
    "NOELreports",
    "Tendar"
]

def fetch_twitter_events():
    db = SessionLocal()
    added = 0

    for account in WATCH_ACCOUNTS:
        for tweet in sntwitter.TwitterUserScraper(account).get_items():
            if any(k in tweet.content.lower() for k in ["strike", "explosion", "airstrike", "mobilized", "missile", "shelling"]):
                if db.query(ConflictEvent).filter(ConflictEvent.summary == tweet.content).first():
                    break  # already stored

                lat, lon = extract_coordinates(tweet.content)
                event = ConflictEvent(
                    summary=tweet.content[:300],
                    lat=lat,
                    lon=lon,
                    event_type="osint",
                    source=f"@{account}",
                    timestamp=tweet.date.replace(tzinfo=timezone.utc)
                )
                db.add(event)
                added += 1

                break  # just grab 1 per user for now

    db.commit()
    db.close()
    print(f"✅ Added {added} Twitter OSINT events")
