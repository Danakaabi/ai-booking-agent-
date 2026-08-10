AI Booking Agent — Booking Domain Model

1. Core Entities

* Customer
* Staff
* Service
* Booking
* Conversation
* Message

2. Booking Lifecycle

* Pending
* Confirmed
* Cancelled
* Completed

3. Business Rules

* A booking must belong to one customer.
* A booking must reference one service.
* A booking may be assigned to one staff member.
* A booking cannot overlap with another confirmed booking for the same staff member.
* A cancelled booking cannot be cancelled again.
* A booking can only be rescheduled to an available time.

4. Availability Rules

* Staff must be working during the requested time.
* The selected service duration must fit inside the available slot.
* Existing bookings must not conflict with the requested time.

5. Relationships

* Customer → has many Bookings
* Staff → has many Bookings
* Service → has many Bookings
* Conversation → has many Messages
* Conversation → may relate to a Customer