import { useState } from "react";
import EventList from "./components/EventList";
import EventDetail from "./components/EventDetail";
import CreateEventCard from "./components/CreateEventCard";
import Login from "./components/Login";

function App() {
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);
  const [token, setToken] = useState(null);
  const [userEmail, setUserEmail] = useState(null);

  function handleEventCreated(){
    setRefreshKey(refreshKey + 1);
  }

  function handleLoginSuccess(newToken, email) {
    setToken(newToken);
    setUserEmail(email);
  }

  function handleLogout() {
    setToken(null);
    setUserEmail(null);
  }


  return (
    <div>
      {userEmail ? (
        <p>Logged in as {userEmail} <button onClick={handleLogout}>Logout</button></p>
      ) : (
        <Login onLoginSuccess={handleLoginSuccess} />
      )}

      {selectedEvent ? (
        <EventDetail event={selectedEvent} onBack={() => setSelectedEvent(null)} token={token} />
      ) : (
        <>
          {token && <CreateEventCard onEventCreated={handleEventCreated} token={token} />}
          <EventList key={refreshKey} onSelectEvent={setSelectedEvent} />
        </>
      )}
    </div>
  );
}

export default App;