import { useState, useEffect } from "react";
import { getEvents } from "../api";

function EventList({ onSelectEvent }) {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    getEvents().then(data => setEvents(data));
  }, []);

  return (
    <div>
      <h1>Events</h1>
      {events.map(event => (
        <div key={event.id} onClick={() => onSelectEvent(event)}>
          <h2>{event.name}</h2>
          <p>{event.location}</p>
        </div>
      ))}
    </div>
  );
}

export default EventList;