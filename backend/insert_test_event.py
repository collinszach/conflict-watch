from db import SessionLocal, ConflictEvent

db = SessionLocal()

test_event = ConflictEvent(
    summary="⚠️ Artillery fire reported near Donetsk",
    lat=48.0159,
    lon=37.8029,
    event_type="artillery",
    source="TestManual"
)

db.add(test_event)
db.commit()
db.close()

print("✅ Test event inserted.")
