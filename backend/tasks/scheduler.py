from apscheduler.schedulers.background import BackgroundScheduler
from fetchers.liveuamap import fetch_liveuamap_events
from fetchers.twitter_osint import fetch_twitter_events

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_liveuamap_events, 'interval', minutes=5)
    scheduler.add_job(fetch_twitter_events, 'interval', minutes=5)
    scheduler.start()
