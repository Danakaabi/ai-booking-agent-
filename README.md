<p align="center">
  <img src="docs/assets/ai-booking-agent-banner.png"
       alt="AI Booking Agent"
       width="100%">
</p>

<h1 align="center">AI Booking Agent</h1>

<p align="center">
  <strong>Backend-first intelligent booking system evolving into a reusable AI agent.</strong>
</p>

<p align="center">
  Built with FastAPI, MongoDB, PyMongo, Pydantic and Pytest.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/MongoDB-Database-47A248?logo=mongodb&logoColor=white" alt="MongoDB">
  <img src="https://img.shields.io/badge/Pydantic-Validation-E92063" alt="Pydantic">
  <img src="https://img.shields.io/badge/Pytest-123%20Passing-0A9EDC?logo=pytest&logoColor=white" alt="Tests">
  <img src="https://img.shields.io/badge/Phase%206-Completed-success" alt="Phase 6">
  <img src="https://img.shields.io/badge/Status-Active%20Development-orange" alt="Status">
</p>

---

## Overview

**AI Booking Agent** is a reusable booking backend designed to evolve into an AI-powered booking agent.

The project is intentionally developed **backend-first** so that booking rules, scheduling, availability, staff assignment, conflict detection, validation, conversation state, context management, and persistence are reliable before introducing LLM reasoning.

```text
User / Client
      ↓
FastAPI
      ↓
Conversation API / Booking API
      ↓
Conversation Service / Booking Engine
      ↓
Validation & Business Rules
      ↓
Repository Layer
      ↓
MongoDB
```

The future AI layer will interact with the system through controlled business tools rather than direct database access.

This keeps probabilistic AI reasoning separate from deterministic booking rules, conversation infrastructure, and persistence.

---

# Current Status

> **Phase 1 — Foundation: Completed**
>
> **Phase 2 — API & MongoDB Foundation: Completed**
>
> **Phase 3 — Booking System: Completed**
>
> **Phase 4 — Customers, Staff & Availability: Completed**
>
> **Phase 5 — Booking Engine Expansion: Completed**
>
> **Phase 6 — Conversation System: Completed**
>
> **Phase 7 — AI Core: Next**

Current automated test status:

```text
123 passed
1 warning
0 failures
```

A FastAPI/Starlette TestClient dependency deprecation warning is currently emitted but does not represent a failing test.

---

# Implemented Features

## Booking

- [x] Create bookings
- [x] Retrieve all bookings
- [x] Retrieve booking by ID
- [x] Partial booking updates
- [x] Validated booking updates
- [x] Booking rescheduling
- [x] Booking cancellation
- [x] Booking status lifecycle
- [x] 404 handling
- [x] Confirmed-booking filtering
- [x] Cancelled-slot reuse
- [x] Conflict-aware booking creation
- [x] Conflict-aware booking rescheduling
- [x] Self-conflict exclusion during booking updates

## Booking Engine

- [x] Centralized booking validation
- [x] Booking creation orchestration
- [x] Booking update orchestration
- [x] Booking cancellation orchestration
- [x] Service validation
- [x] Business-hours validation
- [x] Staff validation
- [x] Service-to-staff validation
- [x] Staff availability validation
- [x] Booking conflict validation
- [x] Staff-aware conflict detection
- [x] Current-booking exclusion during rescheduling
- [x] Repository-backed booking execution
- [x] Shared HTTP error mapping for booking business errors

## Availability & Scheduling

- [x] Business-hours validation
- [x] Full service-duration validation
- [x] Booking overlap detection
- [x] Double-booking prevention
- [x] Back-to-back booking support
- [x] Persistent availability configuration
- [x] Staff-specific working schedules
- [x] Staff availability validation
- [x] Staff-specific booking conflicts
- [x] Available time slot generation
- [x] Occupied slot exclusion
- [x] Available slots API

## Customers

- [x] Customer schema
- [x] Customer validation
- [x] Customer repository
- [x] Customer API
- [x] Active customer filtering

## Staff

- [x] Staff schema
- [x] Staff validation
- [x] Staff repository
- [x] Staff API
- [x] Service-to-staff relationships
- [x] Staff lookup by service
- [x] Staff-specific availability

## Conversation System

- [x] Conversation schema
- [x] Message schema
- [x] Message roles: user, assistant, system
- [x] Conversations MongoDB collection
- [x] Messages MongoDB collection
- [x] Conversation repository
- [x] Message repository
- [x] Conversation creation
- [x] Conversation retrieval
- [x] Message persistence
- [x] Conversation history
- [x] Ordered message history
- [x] Conversation isolation
- [x] Conversation state
- [x] Active and completed states
- [x] Booking context
- [x] Partial booking-context updates
- [x] Preservation of previously collected context
- [x] Conversation service
- [x] Conversation-to-booking conversion
- [x] Conversation-to-booking-engine integration
- [x] Conversation REST API
- [x] Shared booking business error mapping

## Testing

- [x] Schema tests
- [x] Repository tests
- [x] API tests
- [x] Booking lifecycle tests
- [x] Availability tests
- [x] Conflict detection tests
- [x] Customer tests
- [x] Staff tests
- [x] Staff availability tests
- [x] Available slot tests
- [x] Booking engine validation tests
- [x] Booking orchestration tests
- [x] Booking rescheduling tests
- [x] Rescheduling conflict tests
- [x] Self-conflict exclusion tests
- [x] Conversation schema tests
- [x] Conversation repository tests
- [x] Message repository tests
- [x] Conversation service tests
- [x] Booking context tests
- [x] Conversation API tests
- [x] Conversation-to-booking integration tests
- [x] Shared HTTP error mapping tests
- [x] Full regression suite

Current result:

```text
123 passed
1 warning
0 failures
```

---

# Architecture

```text
AI Booking Agent
│
├── ai_core/
│   ├── availability.py
│   ├── booking_engine.py
│   ├── conversation_service.py
│   ├── staff_availability.py
│   └── available_slots.py
│
├── api/
│   ├── main.py
│   ├── http_errors.py
│   ├── routes/
│   │   ├── services.py
│   │   ├── bookings.py
│   │   ├── conversations.py
│   │   ├── customers.py
│   │   └── staff.py
│   └── schemas/
│       ├── service.py
│       ├── booking.py
│       ├── conversation.py
│       ├── availability.py
│       ├── customer.py
│       ├── staff.py
│       └── staff_availability.py
│
├── database/
│   ├── connection.py
│   └── repositories/
│       ├── services.py
│       ├── bookings.py
│       ├── conversations.py
│       ├── messages.py
│       ├── availability.py
│       ├── customers.py
│       ├── staff.py
│       └── staff_availability.py
│
├── tests/
│   ├── test_health.py
│   ├── test_services.py
│   ├── test_bookings.py
│   ├── test_availability.py
│   ├── test_customers.py
│   ├── test_staff.py
│   ├── test_staff_availability.py
│   ├── test_conversation_schemas.py
│   ├── test_conversation_repository.py
│   ├── test_message_repository.py
│   ├── test_conversation_service.py
│   └── test_conversations_api.py
│
├── docs/
├── .env.example
├── .gitignore
└── README.md
```

Current layered flow:

```text
Client
   ↓
FastAPI
   ↓
API Routes
   ↓
Pydantic Validation
   ↓
Conversation Service / Booking Engine
   ↓
Business Rules & Orchestration
   ↓
Repository Layer
   ↓
MongoDB
```

Conversation-to-booking flow:

```text
User
   ↓
Conversation
   ↓
Messages + State
   ↓
Booking Context
   ↓
BookingCreate
   ↓
Booking Engine
   ↓
Validation & Scheduling Rules
   ↓
Repositories
   ↓
MongoDB
```

This separation prevents HTTP routing code from becoming tightly coupled to database operations, conversation state, or scheduling rules.

---

# API

## Health

```http
GET /health
```

Provides a basic application health check.

---

## Services

```http
GET /services
```

Returns available services.

Services provide scheduling information such as service duration, which is used by the booking engine during availability and conflict calculations.

---

## Bookings

```http
POST /bookings
GET /bookings
GET /bookings/{booking_id}
PATCH /bookings/{booking_id}
PATCH /bookings/{booking_id}/cancel
```

Booking operations are protected by application-level business rules.

Before a booking is created, the booking engine can validate:

```text
Booking Request
      ↓
Service Validation
      ↓
Business Hours
      ↓
Staff Validation
      ↓
Service-to-Staff Relationship
      ↓
Staff Availability
      ↓
Conflict Detection
      ↓
Create Booking
```

Invalid booking requests are rejected before persistence.

Conflicting reservations return:

```text
409 Conflict
```

---

## Booking Rescheduling

```http
PATCH /bookings/{booking_id}
```

Partial updates are supported through `BookingUpdate`.

Booking updates pass through the booking engine rather than directly modifying the database.

```text
PATCH Booking
      ↓
Retrieve Existing Booking
      ↓
Merge Existing + Updated Fields
      ↓
Create Candidate Booking
      ↓
Validate Candidate
      ↓
Exclude Current Booking
from Conflict Detection
      ↓
Apply Update
```

This allows a booking to be rescheduled while still enforcing the same scheduling rules used during booking creation.

For example:

```text
Existing Booking A:
10:00 → 11:00

Booking B:
13:00 → 14:00

Attempt to reschedule Booking B:
10:30 → 11:30

Result:
409 Conflict
```

The booking being updated is excluded from its own conflict check.

This prevents a valid update from being incorrectly rejected because the candidate overlaps with the booking's existing stored version.

---

## Conversations

```http
POST /conversations
GET /conversations/{conversation_id}
POST /conversations/{conversation_id}/messages
GET /conversations/{conversation_id}/messages
PATCH /conversations/{conversation_id}/booking-context
POST /conversations/{conversation_id}/bookings
```

The conversation API provides persistent conversation infrastructure without introducing an LLM.

A new conversation starts with:

```text
state = active

booking_context:
  service_id = None
  customer_name = None
  customer_phone = None
  booking_datetime = None
  staff_id = None
```

Messages are stored independently from the conversation document so conversation history can grow without continuously expanding one MongoDB document.

Conceptually:

```text
Conversation
    ├── state
    ├── booking_context
    └── timestamps

Messages
    ├── conversation_id
    ├── role
    ├── content
    └── created_at
```

### Conversation Messages

```http
POST /conversations/{conversation_id}/messages
GET /conversations/{conversation_id}/messages
```

Supported message roles:

```text
user
assistant
system
```

History is returned from oldest to newest and is isolated by `conversation_id`.

### Booking Context

```http
PATCH /conversations/{conversation_id}/booking-context
```

Booking context stores incomplete booking information while it is gathered over multiple messages.

```text
BookingContext
├── service_id
├── customer_name
├── customer_phone
├── booking_datetime
└── staff_id
```

All fields are optional at the conversation stage because the user may provide them incrementally.

Partial updates preserve existing values:

```text
Update 1:
service_id = service-123

Update 2:
customer_name = Dana

Final Context:
service_id = service-123
customer_name = Dana
```

### Create Booking from Conversation

```http
POST /conversations/{conversation_id}/bookings
```

A booking is executed only after the required context is complete.

```text
Conversation
      ↓
Booking Context
      ↓
Complete?
 ┌────┴────┐
 │         │
No        Yes
 │         │
 ▼         ▼
422    BookingCreate
            ↓
      Booking Engine
            ↓
      Business Rules
            ↓
        MongoDB
```

Conversation-specific errors are handled by the conversation API, while booking business errors use the shared HTTP error mapper.

---

## Customers

Customer creation, retrieval, validation, and active-customer filtering are supported through the customer API and repository layer.

Customer data is kept separate from booking business logic so that customer management can evolve independently.

---

## Staff

```http
GET /staff
GET /staff/{staff_id}
```

Staff members can be linked to supported services and assigned individual working schedules.

Booking validation can verify:

```text
Staff Exists
      ↓
Staff Supports Service
      ↓
Staff Is Working
      ↓
Staff Has No Booking Conflict
```

---

## Available Time Slots

```http
GET /staff/{staff_id}/available-slots
```

Example:

```http
GET /staff/{staff_id}/available-slots?target_date=2026-08-16&start_hour=9&end_hour=17&duration_minutes=60&interval_minutes=30
```

Slot generation considers:

- staff working schedules
- requested duration
- confirmed staff bookings
- booking conflicts
- scheduling boundaries

Example flow:

```text
Target Date
     ↓
Staff Schedule
     ↓
Candidate Slots
     ↓
Existing Staff Bookings
     ↓
Conflict Detection
     ↓
Available Slots
```

Only slots that satisfy the scheduling rules are returned.

---

# Booking Engine

The booking engine is the central application layer for booking decisions.

Instead of allowing API routes to independently implement booking rules, reusable orchestration functions coordinate validation and persistence.

Current responsibilities include:

```text
Booking Engine
│
├── Service Resolution
├── Business-Hours Validation
├── Staff Validation
├── Service-to-Staff Validation
├── Staff Availability
├── Conflict Detection
├── Booking Creation Orchestration
├── Booking Update / Rescheduling Orchestration
└── Booking Cancellation Orchestration
```

The current architecture follows:

```text
API Route / Conversation Service
             ↓
        Booking Engine
             ↓
        Business Rules
             ↓
        Repositories
             ↓
           MongoDB
```

This is important for the future AI architecture because FastAPI routes, conversation workflows, and AI business tools can reuse the same deterministic booking engine.

---

# Centralized Booking Validation

Booking rules are coordinated through the booking engine before persistence.

Conceptually:

```text
validate_booking_request()
        ↓
Service Exists?
        ↓
Inside Business Hours?
        ↓
Staff Selected?
   ┌────┴────┐
   │         │
  Yes        No
   │         │
   ↓         │
Staff Exists │
   ↓         │
Supports     │
Service?     │
   ↓         │
Available?   │
   └────┬────┘
        ↓
Conflict Check
        ↓
Valid / Invalid
```

Conflict validation applies whether or not a booking contains a `staff_id`.

When a staff member is selected, conflict detection can operate against that staff member's confirmed bookings.

---

# Booking Creation Orchestration

Booking creation is coordinated through the booking engine.

```text
execute_booking_request()
        ↓
validate_booking_request()
        ↓
┌──────────────────┐
│ Valid?           │
├────────┬─────────┤
│ Yes    │ No      │
▼        ▼
Create   Return
Booking  Error
```

This keeps validation and execution together at the application layer instead of duplicating booking rules inside API routes or conversation logic.

---

# Booking Update Orchestration

Booking updates use the same business rules as booking creation.

```text
execute_booking_update()
        ↓
Retrieve Existing Booking
        ↓
Merge Update
        ↓
Build Candidate Booking
        ↓
validate_booking_request()
        ↓
Exclude Current Booking ID
        ↓
Conflict Detection
        ↓
Update Repository
```

This provides the foundation for safe rescheduling.

The current booking is excluded during conflict detection:

```text
All Confirmed Bookings
        ↓
Remove Current Booking
        ↓
Check Candidate Time
Against Remaining Bookings
```

This avoids false self-conflicts while still preventing collisions with other reservations.

---

# Booking Lifecycle

```text
Created
   ↓
confirmed
   ↓
Cancel
   ↓
cancelled
```

Confirmed bookings occupy scheduling slots.

Cancelled bookings are excluded from active conflict detection and release their time slots.

Cancellation preserves the booking record rather than immediately deleting it.

This supports future:

- booking history
- auditing
- analytics
- conversation context
- AI reasoning

---

# Conversation State

Conversation state is intentionally separate from booking status.

```text
Conversation State
active
completed
```

```text
Booking Status
confirmed
cancelled
```

The distinction prevents conversation lifecycle concerns from being mixed with booking lifecycle rules.

A conversation begins as:

```text
active
```

and can later transition to:

```text
completed
```

State changes update the conversation's `updated_at` timestamp.

---

# Booking Context

`BookingContext` is temporary conversation memory for booking data that has not yet become a real booking.

It mirrors the relevant fields from `BookingCreate`, but allows them to be optional while information is being collected.

```text
BookingContext             BookingCreate
--------------             -------------
service_id       Optional  Required
customer_name    Optional  Required
customer_phone   Optional  Required
booking_datetime Optional  Required
staff_id         Optional  Optional
```

`status` is intentionally excluded from `BookingContext` because `confirmed` and `cancelled` belong to an actual booking, not to pre-booking conversation memory.

When all required context fields are available:

```text
BookingContext
      ↓
build_booking_from_context()
      ↓
BookingCreate
      ↓
execute_booking_request()
```

The Booking Engine remains responsible for deciding whether the completed request is valid.

---

# Scheduling Rules

The system enforces deterministic scheduling rules.

Example business hours:

```text
09:00 → 17:00
```

For a 60-minute service:

```text
16:00 → 17:00   ✓
16:30 → 17:30   ✗
```

The full service duration must fit inside the configured availability window.

---

# Conflict Detection

Conflict detection operates on booking time intervals rather than only comparing exact start times.

Example:

```text
Existing:
10:00 → 11:00

Requested:
10:30 → 11:30

Result:
CONFLICT
```

The engine detects:

- partial overlap
- booking contained inside another booking
- booking containing another booking
- identical booking times

Conflicting booking requests are rejected before persistence.

---

# Back-to-Back Bookings

Adjacent reservations are allowed when their time intervals do not overlap.

```text
Booking A:
10:00 → 11:00

Booking B:
11:00 → 12:00

Result:
No Conflict
```

This allows working time to be used efficiently without incorrectly treating adjacent reservations as overlapping.

---

# Staff-Aware Scheduling

Bookings may optionally reference a staff member.

When a staff member is selected, the engine can validate:

```text
Requested Service
      ↓
Staff Member
      ↓
Supports Service?
      ↓
Working at Requested Time?
      ↓
Existing Staff Bookings
      ↓
Conflict Detection
      ↓
Booking Decision
```

This prevents assigning a booking to a staff member who:

- does not exist
- does not provide the requested service
- is outside their working schedule
- already has a conflicting confirmed booking

---

# Validation & Error Handling

Input validation is handled using **Pydantic**.

Current schema-level validation includes:

- required service ID
- customer name length
- customer phone length
- datetime parsing
- controlled booking status values
- controlled day-of-week values
- valid availability time ranges
- controlled conversation message roles
- message content length
- partial BookingContext validation

Application-level validation additionally protects against:

- missing services
- booking outside business hours
- booking beyond closing time
- missing staff
- unsupported staff-service combinations
- unavailable staff
- overlapping confirmed reservations
- conflicting rescheduling requests
- missing conversations
- incomplete booking context

Booking business HTTP errors are centralized in:

```text
api/http_errors.py
```

This keeps HTTP semantics consistent across both booking and conversation APIs.

Examples:

```text
Service not found
→ 404 Not Found

Booking time conflicts with an existing booking
→ 409 Conflict

Booking is outside business hours
→ 422 Unprocessable Entity

Booking context is incomplete
→ 422 Unprocessable Entity

Conversation not found
→ 404 Not Found
```

---

# Testing

The project uses **Pytest** and FastAPI testing utilities.

Run the complete test suite:

```bash
python -m pytest -v
```

Current result:

```text
123 passed
1 warning
0 failures
```

Current automated testing covers:

```text
Health
   └── Application health

Services
   ├── Retrieve services
   ├── Retrieve service by ID
   └── Active service mapping

Bookings
   ├── Create
   ├── Retrieve all
   ├── Retrieve by ID
   ├── Update
   ├── Cancel
   ├── Not-found behavior
   ├── Confirmed booking filtering
   ├── Conflict rejection
   ├── Cancelled slot reuse
   ├── Business-hours validation
   ├── Staff-specific conflict lookup
   ├── Centralized request validation
   ├── Booking execution
   ├── Valid rescheduling
   ├── Conflicting rescheduling rejection
   └── Self-conflict exclusion

Customers
   ├── Schema validation
   ├── Repository operations
   ├── API operations
   └── Active customer filtering

Staff
   ├── Schema validation
   ├── Repository operations
   ├── API operations
   ├── Service relationships
   └── Service-based lookup

Staff Availability
   ├── Working schedules
   ├── Unscheduled days
   ├── Availability validation
   ├── Slot generation
   ├── Occupied slot exclusion
   └── Available slots API

Availability
   ├── Opening-time rules
   ├── Closing-time rules
   ├── Full-duration validation
   ├── Overlap detection
   ├── Back-to-back bookings
   ├── Contained intervals
   ├── Identical intervals
   └── Schema validation

Conversation
   ├── Conversation schema
   ├── Message schema
   ├── Message-role validation
   ├── Conversation creation
   ├── Conversation retrieval
   ├── Conversation state
   ├── BookingContext validation
   ├── Partial context updates
   ├── Context preservation
   ├── Message persistence
   ├── Ordered history
   ├── Conversation isolation
   ├── Conversation service
   ├── Conversation API
   ├── Missing-conversation behavior
   ├── Incomplete-context behavior
   ├── Conversation-to-booking conversion
   ├── Conversation-to-booking-engine execution
   └── Shared business error mapping
```

The full regression suite is run after booking, scheduling, conversation, and integration changes to detect regressions across existing functionality.

---

# Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.13 | Core language |
| FastAPI | REST API |
| MongoDB | NoSQL database |
| PyMongo | MongoDB driver |
| Pydantic | Validation |
| Pytest | Automated testing |
| Uvicorn | ASGI development server |
| Git / GitHub | Version control |

Planned:

- LLM API
- intent detection
- AI business tools
- tool calling
- Docker
- GitHub Actions

---

# Development Roadmap

## Phase 1 — Foundation

**Completed**

Repository structure, Git configuration, project scope, and domain documentation.

---

## Phase 2 — API & MongoDB Foundation

**Completed**

FastAPI, MongoDB, PyMongo, repositories, schemas, and initial automated tests.

---

## Phase 3 — Booking System

**Completed**

Booking CRUD, lifecycle management, validation, cancellation, persistence, and automated API testing.

---

## Phase 4 — Customers, Staff & Availability

**Completed**

Delivered:

- customer management
- staff management
- service-to-staff relationships
- business availability
- staff working schedules
- staff availability
- conflict prevention
- staff-specific booking lookup
- available slot generation
- available slots API
- regression testing

---

## Phase 5 — Booking Engine Expansion

**Completed**

Implemented:

- [x] Centralized booking validation
- [x] Service validation
- [x] Business-hours validation
- [x] Staff-aware booking decisions
- [x] Service-to-staff validation
- [x] Staff availability validation
- [x] Centralized conflict validation
- [x] Booking creation orchestration
- [x] Booking update orchestration
- [x] Booking cancellation orchestration
- [x] Validated rescheduling
- [x] Current-booking exclusion during rescheduling
- [x] Conflict-aware booking updates
- [x] Reusable booking operations
- [x] Centralized HTTP error mapping
- [x] Regression testing

Final Phase 5 direction:

```text
API
 ↓
Booking Engine
 ↓
Validation & Orchestration
 ↓
Business Rules
 ↓
Repositories
 ↓
MongoDB
```

The booking engine is now reusable by both REST routes and conversation workflows.

---

## Phase 6 — Conversation System

**Completed**

Implemented:

- [x] Conversation model/schema
- [x] Message model/schema
- [x] Conversations collection
- [x] Messages collection
- [x] Conversation repository
- [x] Message repository
- [x] Create conversation
- [x] Get conversation
- [x] Store user messages
- [x] Store assistant/system messages
- [x] Retrieve conversation history
- [x] Conversation state
- [x] Booking context
- [x] Partial context updates
- [x] Conversation service
- [x] Conversation-to-booking conversion
- [x] Booking Engine integration
- [x] Conversation REST API
- [x] Shared booking HTTP error mapping
- [x] Validation and error handling
- [x] Unit and integration testing
- [x] Full regression testing

Final Phase 6 flow:

```text
User
 ↓
Conversation API
 ↓
Conversation Service
 ↓
Messages + State + Booking Context
 ↓
BookingCreate
 ↓
Booking Engine
 ↓
Repositories
 ↓
MongoDB
```

Final Phase 6 regression:

```text
123 passed
1 warning
0 failures
```

No LLM was introduced during this phase.

---

## Phase 7 — AI Core

**Next**

Planned direction:

- intent detection
- entity extraction
- conversation decision logic
- booking-intent state handling
- deterministic orchestration around existing conversation context
- preparation for controlled tool selection

The AI core will build on the completed Conversation System rather than replacing it.

---

## Phase 8 — AI Business Tools

**Planned**

```text
get_services
get_staff
get_available_times
create_booking
update_booking
cancel_booking
```

These tools will expose controlled booking operations to the future AI agent.

The AI layer will not access MongoDB directly.

---

## Phase 9 — LLM Integration

**Planned**

- LLM API
- tool calling
- structured outputs
- prompt design
- guardrails
- controlled execution

---

## Phase 10 — Production Engineering

**Planned**

- Docker
- GitHub Actions
- CI
- security validation
- logging
- deployment preparation

---

# Local Development

## Clone

```bash
git clone https://github.com/Danakaabi/ai-booking-agent-.git
cd ai-booking-agent
```

## Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

## MongoDB

Verify MongoDB:

```bash
mongosh --eval 'db.runCommand({ ping: 1 })'
```

Expected:

```text
{ ok: 1 }
```

MongoDB must be running before executing tests that depend on repository persistence.

If MongoDB is not running as a Homebrew service, it can be started manually using the configured `mongod.conf` before running repository and integration tests.

## Run API

```bash
uvicorn api.main:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

## Run Tests

```bash
python -m pytest -v
```

Current expected result:

```text
123 passed
1 warning
0 failures
```

A dependency deprecation warning from the FastAPI/Starlette TestClient stack may appear and does not currently represent a failing test.

---

# Current Development Focus

The deterministic booking foundation and persistent Conversation System are complete.

```text
Foundation                         ✓
FastAPI + MongoDB                  ✓
Booking System                     ✓
Availability                       ✓
Conflict Prevention                ✓
Customers                          ✓
Staff                              ✓
Staff Scheduling                   ✓
Available Slots                    ✓
Centralized Booking Validation     ✓
Booking Creation Orchestration     ✓
Validated Rescheduling             ✓
Booking Update Orchestration       ✓
Booking Cancellation Orchestration ✓
Booking Engine Expansion           ✓
Conversation Schemas               ✓
Conversation Persistence           ✓
Message History                    ✓
Conversation State                 ✓
Booking Context                    ✓
Conversation ↔ Booking Engine      ✓
Conversation REST API              ✓
Shared Error Handling              ✓
AI Core                            → NEXT
Agent Tools
LLM Integration
Production Engineering
```

The current objective is:

> **Build the AI decision layer on top of the completed deterministic booking and conversation infrastructure without duplicating business logic.**

---

# Target AI Architecture

```text
Client
   ↓
FastAPI
   ↓
Conversation System
   ↓
AI Agent
   ↓
Business Tools
   ↓
Booking Engine
   ↓
Validation & Scheduling Rules
   ↓
Repositories
   ↓
MongoDB
```

The AI model will decide:

```text
What operation is needed?
What information is still missing?
Which controlled tool should be used?
```

The deterministic backend will decide:

```text
Is the operation allowed?
How should it be executed?
```

The database will persist the validated result.

---

# Why Backend-First?

The project deliberately does not begin with an LLM.

A booking agent must reliably understand and enforce rules such as:

```text
Does the service exist?
Does the staff member provide the service?
Is the business open?
Is the staff member working?
Does the full service duration fit?
Does another confirmed booking overlap?
Can this booking be safely rescheduled?
Is the conversation context complete enough to request a booking?
```

These decisions should not depend on probabilistic model output.

The future AI agent will therefore use deterministic backend operations and persistent conversation infrastructure rather than reproducing booking logic inside prompts.

---

# Engineering Principles

- Separation of concerns
- Repository pattern
- Centralized booking orchestration
- Dedicated conversation service
- Validation at application boundaries
- Deterministic scheduling
- Conflict-safe booking operations
- Persistent conversation state
- Partial booking-context collection
- Shared HTTP error mapping
- Automated regression testing
- Framework-independent business logic
- Controlled AI tool execution
- No direct AI access to MongoDB
- No secrets committed to Git

---

# Long-Term Vision

The project is intended to evolve into a reusable AI booking agent for domains such as:

- salons
- clinics
- healthcare scheduling
- events
- professional services
- appointment-based businesses

```text
Web
Mobile
Chat
   ↓
Conversation / AI Layer
   ↓
Business Tools
   ↓
Booking Engine
   ↓
Scheduling
   ↓
MongoDB
```

The same deterministic booking engine and conversation infrastructure can support multiple interfaces without duplicating business rules.

---

# Project Philosophy

> **AI should reason about the request.**
>
> **Conversation infrastructure should preserve context and state.**
>
> **Business logic should decide what is allowed.**
>
> **The database should persist the validated result.**

---

<p align="center">
  <strong>AI Booking Agent</strong><br>
  Backend Engineering • Booking Systems • Scheduling • Conversation Systems • AI Agents • System Design
</p>