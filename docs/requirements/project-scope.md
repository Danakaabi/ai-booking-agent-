# AI Booking Agent — v0.1 Project Scope

## 1. Product Goal

Build an AI-powered booking system that allows customers to interact using natural language to manage appointments safely through controlled booking operations.

The first version focuses on the booking engine and its required business rules before introducing advanced AI behavior.

---

## 2. Target Users

### Customer
Can:
- View available services
- Check available booking times
- Create a booking
- Reschedule a booking
- Cancel a booking

### Staff
Can:
- View assigned bookings
- View working schedule
- Manage availability when supported

### Admin
Can:
- Manage services
- Manage staff
- Manage working hours
- View bookings
- Configure booking rules

---

## 3. Core Use Cases

The v0.1 system must support:

- View services
- View available times
- Create booking
- Reschedule booking
- Cancel booking
- Prevent conflicting bookings

---

## 4. Functional Requirements

The system must:

- Store customers
- Store staff
- Store services
- Store bookings
- Track booking status
- Validate required booking information
- Check availability before creating a booking
- Prevent double booking
- Allow valid booking cancellation
- Allow valid booking rescheduling

---

## 5. Non-Functional Requirements

The system should be:

- Secure
- Testable
- Maintainable
- Reliable
- Modular
- Easy to run locally
- Documented for other developers

Sensitive information and credentials must never be committed to the public repository.

---

## 6. In Scope — v0.1

Included:

- Customer model
- Staff model
- Service model
- Booking model
- Working hours
- Availability calculation
- Booking creation
- Booking cancellation
- Booking rescheduling
- Booking status management
- Conflict prevention
- Unit tests for booking rules

---

## 7. Out of Scope — v0.1

Not included yet:

- WhatsApp integration
- Payment processing
- Multi-business tenancy
- Advanced analytics
- RAG
- Vector databases
- Microservices
- Kubernetes
- Redis
- RabbitMQ
- Complex recommendation systems

These features may be introduced later only when a real requirement exists.

---

## 8. Edge and Failure Cases

The system must handle:

- Requested time is already booked
- Staff member is unavailable
- Service does not exist
- Customer does not exist
- Booking does not exist
- Invalid booking status
- Missing booking information
- Attempt to cancel an already cancelled booking
- Attempt to reschedule to an unavailable time

---

## 9. Acceptance Criteria

Phase 2 is complete when:

- The target users are clearly defined
- Core booking use cases are documented
- Functional requirements are documented
- Non-functional requirements are documented
- v0.1 scope is clearly limited
- Failure cases are documented
- Another developer can understand what v0.1 will build without reading the source code