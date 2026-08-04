function EventDetail({ event, onBack, token }) {
  async function handleBook(ticketTypeId) {
    if (!token) {
      alert("Please log in to book");
      return;
    }

    const response = await fetch("http://localhost:8000/bookings", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
      body: JSON.stringify({ ticket_type_id: ticketTypeId, quantity: 1 }),
    });

    if (!response.ok) {
      alert("Booking failed");
      return;
    }

    alert("Booking successful!");
  }

  return (
    <div>
      <button onClick={onBack}>Back to list</button>
      <h1>{event.name}</h1>
      <p>{event.location}</p>
      <p>{event.description}</p>
      <h3>Ticket Types</h3>
      {event.ticket_types.map(tt => (
        <div key={tt.id}>
          <p>Price: {tt.price} — Capacity: {tt.capacity}</p>
          <button onClick={() => handleBook(tt.id)}>Book</button>
        </div>
      ))}
    </div>
  );
}

export default EventDetail;