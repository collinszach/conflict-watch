import React, { useEffect, useState } from "react";
import MapView from "./MapView";
import FeedView from "./FeedView";

function App() {
  const [events, setEvents] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [source, setSource] = useState("All");
  const [search, setSearch] = useState("");

  useEffect(() => {
    fetch("http://localhost:8000/events")
      .then((res) => res.json())
      .then((data) => {
        setEvents(data);
        setFiltered(data);
      });
  }, []);

  useEffect(() => {
    let result = [...events];
    if (source !== "All") {
      result = result.filter(e => e.source.toLowerCase().includes(source.toLowerCase()));
    }
    if (search.trim()) {
      result = result.filter(e => e.summary.toLowerCase().includes(search.toLowerCase()));
    }
    setFiltered(result);
  }, [source, search, events]);

  return (
    <div style={{ padding: "1rem" }}>
      <h1>🛰️ Conflict Watch</h1>
      <div style={{ marginBottom: "1rem" }}>
        <input
          type="text"
          placeholder="Search events..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ marginRight: "1rem", padding: "0.5rem" }}
        />
        <select value={source} onChange={(e) => setSource(e.target.value)} style={{ padding: "0.5rem" }}>
          <option value="All">All Sources</option>
          <option value="twitter">Twitter</option>
          <option value="liveuamap">Liveuamap</option>
        </select>
      </div>
      <MapView events={filtered} />
      <FeedView events={filtered} />
    </div>
  );
}

export default App;