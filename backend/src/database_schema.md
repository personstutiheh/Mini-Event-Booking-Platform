## Entity
### user
- id (primary key)
- email
- password 
- name
- role (admin/customer)

### events
- id (primary key)
- name
- date
- location
- description
- created_at

### ticket_types
- id (primary key)
- event_id (foreign key)
- type
- price
- capacity

### bookings
- id
- user_id
- ticket_type_id
- quantity
- status
- created_at

### Relationships :
- users to booking -> one to many
- events to ticket_types -> one to many
- ticket_types to bookings -> one to many
