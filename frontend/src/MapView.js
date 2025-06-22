import React from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

function MapView({ events }) {
  return (
    <MapContainer center={[20, 0]} zoom={2} style={{ height: "400px", width: "100%", marginBottom: "2rem" }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {events.map((event, idx) => (
        <Marker key={idx} position={[event.lat, event.lon]}>
          <Popup>
            <strong>{event.event_type.toUpperCase()}</strong><br />
            {event.summary}<br />
            <em>{event.source}</em>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}

export default MapView;