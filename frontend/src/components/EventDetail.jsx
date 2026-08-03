function EventDetail({ event, onBack }) {
  return (
    <div>
      <button onClick={onBack}>Back to list</button>
      <h1>{event.name}</h1>
      <p>{event.location}</p>
      <p>{event.description}</p>
      <h3>Ticket Types</h3>
      {event.ticket_types.map(tt => (
        <p key={tt.id}>Price: {tt.price} — Capacity: {tt.capacity}</p>
      ))}
      <button onClick={() => alert("Booking coming in a later phase!")}>Book</button>
    </div>
  );
}

export default EventDetail;