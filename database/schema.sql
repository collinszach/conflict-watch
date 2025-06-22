CREATE TABLE conflict_events (
  id SERIAL PRIMARY KEY,
  lat FLOAT,
  lon FLOAT,
  event_type TEXT,
  summary TEXT,
  timestamp TIMESTAMPTZ,
  source TEXT
);
