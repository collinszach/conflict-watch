import React from "react";

function FeedView({ events }) {
  return (
    <div>
      <h2>📜 Latest Events</h2>
      <ul>
        {events.map((event, idx) => (
          <li key={idx} style={{ marginBottom: "1rem" }}>
            <strong>{new Date(event.timestamp).toLocaleString()}</strong>: {event.summary} ({event.source})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default FeedView;