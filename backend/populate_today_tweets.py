import snscrape.modules.twitter as sntwitter
from db import SessionLocal, ConflictEvent
from datetime import datetime, timezone
from fetchers.twitter_osint import extract_coordinates  # geoparsing helper

WATCH_ACCOUNTS = [
    "osinttechnical", "war_mapper", "sentdefender", "NOELreports", "Tendar"
]

def seed_todays_tweets():
    db = SessionLocal()
    added = 0

    for account in WATCH_ACCOUNTS:
        for tweet in sntwitter.TwitterUserScraper(account).get_items():
            if tweet.date.date() != datetime.utcnow().date():
                break  # only pull today's tweets

            if any(k in tweet.content.lower() for k in ["strike", "missile", "artillery", "attack", "explosion"]):
                if db.query(ConflictEvent).filter(ConflictEvent.summary == tweet.content).first():
                    continue

                lat, lon = extract_coordinates(tweet.content)
                event = ConflictEvent(
                    summary=tweet.content[:300],
                    lat=lat,
                    lon=lon,
                    event_type="twitter",
                    source=f"@{account}",
                    timestamp=tweet.date.replace(tzinfo=timezone.utc)
                )
                db.add(event)
                added += 1
                break  # limit to 1 relevant tweet per account

    db.commit()
    db.close()
    print(f"✅ Inserted {added} Twitter events for today.")

if __name__ == "__main__":
    seed_todays_tweets()
