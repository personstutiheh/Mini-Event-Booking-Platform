import { useState } from "react";
import EventList from "./components/EventList";
import EventDetail from "./components/EventDetail";
import CreateEventCard from "./components/CreateEventCard";

function App() {
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  function handleEventCreated(){
    setRefreshKey(refreshKey + 1);
  }

  return (
      <div>
        {selectedEvent ? (
          <EventDetail event={selectedEvent} onBack={() => setSelectedEvent(null)} />
        ) : (
          <>
            <CreateEventCard onEventCreated={handleEventCreated} />
            <EventList key={refreshKey} onSelectEvent={setSelectedEvent} />
          </>
        )}
      </div>
    );
  }

export default App;