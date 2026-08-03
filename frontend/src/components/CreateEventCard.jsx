import { useState } from "react";

function CreateEventCard({ onEventCreated }) {
  const [name, setName] = useState("");
  const [eventDate, setEventDate] = useState("");
  const [location, setLocation] = useState("");
  const [description, setDescription] = useState("");
  const [price, setPrice] = useState("");
  const [capacity, setCapacity] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();

    const newEvent = {
      name,
      event_date: eventDate,
      location,
      description,
      ticket_types: [
        { price: Number(price), capacity: Number(capacity) }
      ]
    };

    const response = await fetch("http://localhost:8000/events", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newEvent),
    });

    const created = await response.json();
    onEventCreated(created);
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Create Event</h2>
      <input placeholder="Name" value={name} onChange={e => setName(e.target.value)} />
      <input type="datetime-local" value={eventDate} onChange={e => setEventDate(e.target.value)} />
      <input placeholder="Location" value={location} onChange={e => setLocation(e.target.value)} />
      <input placeholder="Description" value={description} onChange={e => setDescription(e.target.value)} />
      <input placeholder="Price" value={price} onChange={e => setPrice(e.target.value)} />
      <input placeholder="Capacity" value={capacity} onChange={e => setCapacity(e.target.value)} />
      <button type="submit">Create</button>
    </form>
  );
}

export default CreateEventCard;