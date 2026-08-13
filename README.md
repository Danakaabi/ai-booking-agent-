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
  <img src="https://img.shields.io/badge/PyMongo-Driver-47A248" alt="PyMongo">
  <img src="https://img.shields.io/badge/Pydantic-Validation-E92063" alt="Pydantic">
  <img src="https://img.shields.io/badge/Pytest-36%20Passing-0A9EDC?logo=pytest&logoColor=white" alt="Tests">
  <img src="https://img.shields.io/badge/Status-Active%20Development-orange" alt="Status">
</p>

---

## Overview

**AI Booking Agent** is an intelligent and reusable booking system being built to explore the intersection of:

- AI agent architecture
- Backend engineering
- REST API design
- MongoDB and NoSQL data modeling
- Booking workflows and business rules
- Availability and scheduling logic
- Booking conflict prevention
- Conversation memory
- Automated testing
- System design
- Safe LLM tool execution

The project is intentionally being developed **backend-first**.

Instead of connecting an LLM directly to a database, the system first establishes a reliable booking domain, API layer, repository layer, validation rules, scheduling rules, availability engine, booking engine, and automated tests.

The AI layer will later interact with these capabilities through controlled business tools.

---

## Why This Project?

A useful booking agent needs more than natural-language generation.

It must be able to reliably:

- understand what the user wants
- retrieve available services
- manage booking state
- validate booking information
- understand business hours
- check availability
- detect overlapping reservations
- prevent double-booking
- create and modify bookings
- cancel bookings safely
- preserve conversation context
- execute only approved business operations

The project therefore separates **AI reasoning** from **business execution**.

```text
User
  ↓
AI Agent
  ↓
Controlled Business Tools
  ↓
Booking Engine
  ↓
Availability & Business Rules
  ↓
Repository Layer
  ↓
MongoDB
```

The AI model will not manipulate the database directly.

---

# Current Status

> **Phase 3 — Booking System: Completed**
>
> **Phase 4 — Availability & Scheduling Foundation: In Progress**

The project currently has a functional FastAPI + MongoDB backend with:

- persistent booking lifecycle operations
- booking conflict detection
- double-booking prevention
- business-hours validation
- persistent availability configuration
- automated API and business-logic tests

Current automated test status:

```text
36 passed
```

A dependency deprecation warning is currently emitted by the FastAPI/Starlette TestClient stack and does not represent a failing test.

---

# Implemented Features

## Foundation

- [x] Git repository initialization
- [x] Structured project layout
- [x] `.gitignore`
- [x] Environment variable template
- [x] Project scope documentation
- [x] Booking domain documentation

## FastAPI

- [x] FastAPI application
- [x] Health-check endpoint
- [x] Services API
- [x] Bookings API
- [x] Pydantic request validation
- [x] Interactive Swagger documentation
- [x] HTTP error handling
- [x] Booking conflict HTTP responses
- [x] Business-hours validation during booking creation

## MongoDB

- [x] Local MongoDB environment
- [x] `ai_booking_agent` database
- [x] Services collection
- [x] Bookings collection
- [x] Availability collection
- [x] PyMongo integration
- [x] MongoDB connection layer
- [x] Repository pattern
- [x] ObjectId handling
- [x] Persistent booking operations
- [x] Persistent availability configuration

## Booking Management

- [x] Create booking
- [x] Retrieve all bookings
- [x] Retrieve booking by ID
- [x] Update booking
- [x] Cancel booking
- [x] Booking status management
- [x] `confirmed` booking state
- [x] `cancelled` booking state
- [x] Validation of booking input
- [x] 404 handling for missing bookings
- [x] Confirmed-booking filtering
- [x] Cancelled bookings excluded from conflict checks

## Availability & Scheduling

- [x] Availability schema
- [x] Day-of-week validation
- [x] Start/end time validation
- [x] Persistent availability repository
- [x] Active availability retrieval
- [x] Business-hours validation
- [x] Full booking-duration validation
- [x] Booking overlap detection
- [x] Booking conflict detection
- [x] Double-booking prevention
- [x] Back-to-back booking support
- [x] Cancelled slots become available again
- [x] Booking engine integration with availability rules
- [ ] Staff-specific schedules
- [ ] Service-to-staff availability
- [ ] Generated available time slots

## Testing

- [x] Pytest configured
- [x] Health endpoint test
- [x] Services endpoint tests
- [x] Booking creation tests
- [x] Booking retrieval tests
- [x] Booking update tests
- [x] Booking cancellation tests
- [x] Not-found behavior tests
- [x] Availability unit tests
- [x] Availability schema validation tests
- [x] Business-hours tests
- [x] Booking-duration boundary tests
- [x] Overlap detection tests
- [x] Conflict integration tests
- [x] Cancelled-booking conflict tests
- [x] Full test suite passing

Current result:

```text
36 passed
```

---

# Current Architecture

```text
AI Booking Agent
│
├── ai_core/
│   ├── availability.py
│   └── booking_engine.py
│
├── api/
│   ├── main.py
│   │
│   ├── routes/
│   │   ├── services.py
│   │   └── bookings.py
│   │
│   └── schemas/
│       ├── service.py
│       ├── booking.py
│       └── availability.py
│
├── database/
│   ├── connection.py
│   │
│   └── repositories/
│       ├── services.py
│       ├── bookings.py
│       └── availability.py
│
├── tests/
│   ├── test_health.py
│   ├── test_services.py
│   ├── test_bookings.py
│   └── test_availability.py
│
├── docs/
│   ├── assets/
│   ├── domain/
│   └── requirements/
│
├── .env.example
├── .gitignore
└── README.md
```

The backend now follows a layered flow:

```text
Client
   ↓
FastAPI
   ↓
API Routes
   ↓
Pydantic Validation
   ↓
Booking Engine
   ↓
Availability / Business Rules
   ↓
Repository Layer
   ↓
MongoDB
```

This separation prevents HTTP routing code from becoming tightly coupled to database operations or scheduling rules.

---

# Current API

## Health Check

```http
GET /health
```

Verifies that the application is running.

Example response:

```json
{
  "status": "ok",
  "service": "ai-booking-agent"
}
```

---

## Services

### Retrieve Active Services

```http
GET /services
```

Returns active services stored in MongoDB.

Example:

```json
[
  {
    "name": "Haircut",
    "duration_minutes": 60,
    "price": 85.0,
    "active": true
  }
]
```

Current service flow:

```text
GET /services
      ↓
FastAPI Route
      ↓
Repository Layer
      ↓
MongoDB
      ↓
Pydantic Schema
      ↓
JSON Response
```

---

# Booking API

## Create Booking

```http
POST /bookings
```

Creates and persists a new booking after validating the booking request against business rules.

Example request:

```json
{
  "service_id": "6a779ed59b6b145fcfe108ab",
  "customer_name": "Dana",
  "customer_phone": "0500000000",
  "booking_datetime": "2026-08-20T10:00:00"
}
```

New bookings default to:

```json
{
  "status": "confirmed"
}
```

Before persistence, the booking flow can verify:

```text
Booking Request
      ↓
Input Validation
      ↓
Service Resolution
      ↓
Business Hours
      ↓
Booking Duration
      ↓
Existing Confirmed Bookings
      ↓
Conflict Detection
      ↓
Create Booking
```

A booking outside configured business hours is rejected instead of being stored.

A booking that overlaps an existing confirmed reservation is also rejected.

---

## Retrieve All Bookings

```http
GET /bookings
```

Returns stored bookings.

---

## Retrieve Booking by ID

```http
GET /bookings/{booking_id}
```

Returns a single booking.

If the booking does not exist:

```json
{
  "detail": "Booking not found"
}
```

with:

```text
404 Not Found
```

---

## Update Booking

```http
PATCH /bookings/{booking_id}
```

Supports partial updates.

Example:

```json
{
  "customer_name": "Dana Updated"
}
```

Only supplied fields are updated.

---

## Cancel Booking

```http
PATCH /bookings/{booking_id}/cancel
```

Cancellation is implemented as a booking lifecycle operation rather than immediately deleting the record.

The booking status changes from:

```text
confirmed
```

to:

```text
cancelled
```

This preserves the booking record for future history, auditing, analytics, and AI conversation context.

Cancelled bookings are excluded from active booking-conflict checks, allowing their time slots to become available again.

---

# Booking Lifecycle

The current booking lifecycle is intentionally simple:

```text
             ┌──────────────┐
             │   Booking    │
             │   Created    │
             └──────┬───────┘
                    │
                    ▼
             ┌──────────────┐
             │  confirmed   │
             └──────┬───────┘
                    │
             Cancel Booking
                    │
                    ▼
             ┌──────────────┐
             │  cancelled   │
             └──────────────┘
```

Only active confirmed bookings participate in booking conflict detection.

This means:

```text
confirmed booking
       ↓
occupies time slot

cancelled booking
       ↓
does not occupy time slot
```

Additional lifecycle rules can be introduced as the booking engine evolves.

---

# Availability System

The project now contains a persistent availability foundation.

Availability records define when bookings may occur.

Example:

```json
{
  "day_of_week": "sunday",
  "start_time": "09:00:00",
  "end_time": "17:00:00",
  "active": true
}
```

The current development database contains availability configuration for the days of the week.

Availability data is retrieved through the repository layer rather than accessed directly by the booking API.

```text
Booking Engine
      ↓
Availability Repository
      ↓
MongoDB
      ↓
Active Availability Records
```

---

# Availability Validation

Availability configuration is validated using Pydantic.

The system restricts `day_of_week` to supported weekday values.

Invalid arbitrary values such as:

```text
pizza
abc
holiday
```

are rejected.

Time ranges are also validated.

Valid:

```text
09:00 → 17:00
```

Invalid:

```text
17:00 → 09:00
09:00 → 09:00
```

The rule is:

```text
end_time > start_time
```

This prevents invalid scheduling configuration from entering the application.

---

# Business Hours

Bookings must fit inside configured business hours.

For example, given:

```text
Opening: 09:00
Closing: 17:00
```

a booking beginning at:

```text
10:00
```

may be valid.

A booking beginning before opening time is rejected.

A booking beginning at closing time is rejected.

The engine also considers the **full service duration**, not only the booking start time.

For a 60-minute service:

```text
16:00 → 17:00
```

is valid.

But:

```text
16:30 → 17:30
```

is rejected because the service would finish after closing time.

---

# Conflict Detection

The scheduling logic detects overlapping booking intervals.

Conceptually:

```text
Existing booking:
10:00 ───────── 11:00

Requested booking:
      10:30 ───────── 11:30

Result:
CONFLICT
```

The overlap rule is based on time intervals rather than comparing only exact start times.

The system detects cases including:

```text
Partial overlap
Contained booking
Containing booking
Identical booking times
```

---

# Back-to-Back Bookings

Adjacent bookings are allowed when they do not overlap.

Example:

```text
Booking A
10:00 ───────── 11:00

Booking B
                  11:00 ───────── 12:00
```

Result:

```text
No conflict
```

This allows available working time to be used efficiently without falsely treating adjacent reservations as overlapping.

---

# Double-Booking Prevention

Booking conflict detection is integrated into booking creation.

The system checks existing **confirmed** bookings before allowing a new reservation.

Example:

```text
Existing:
10:00 → 11:00

Requested:
10:30 → 11:30
```

The request is rejected with:

```text
409 Conflict
```

This prevents overlapping confirmed reservations from being persisted.

The high-level flow is:

```text
POST /bookings
      ↓
Booking Schema
      ↓
Business Hours Check
      ↓
Conflict Check
      ↓
┌───────────────┬─────────────────┐
│ No Conflict   │ Conflict        │
│               │                 │
▼               ▼
Create          409 Conflict
Booking
```

---

# Booking Engine

Business scheduling rules are being moved into `ai_core/booking_engine.py`.

The booking engine acts as a reusable layer between interfaces such as FastAPI or future AI tools and the underlying repositories.

Current responsibilities include:

- service lookup
- service duration resolution
- availability lookup
- business-hours validation
- confirmed-booking lookup
- booking conflict detection

This architecture moves the project beyond CRUD-only behavior.

```text
API Route
    ↓
Booking Engine
    ↓
Business Rules
    ↓
Repositories
    ↓
MongoDB
```

The future AI agent will be able to reuse the same engine rather than implementing booking rules itself.

---

# Validation & Error Handling

Input validation is handled using **Pydantic**.

Current validation includes:

- required service ID
- customer name length
- customer phone length
- datetime parsing
- controlled booking status values
- controlled day-of-week values
- valid availability time ranges

Booking status is restricted to supported states rather than accepting arbitrary strings.

Availability records also reject unsupported weekday values and invalid time ranges.

Application-level business rules additionally protect against:

- booking outside business hours
- booking beyond closing time
- overlapping confirmed reservations

Missing booking resources return:

```http
404 Not Found
```

Conflicting booking requests return:

```http
409 Conflict
```

Business-rule validation can return:

```http
422 Unprocessable Entity
```

when the requested booking cannot be accepted under the configured scheduling rules.

---

# Testing

The project uses **Pytest** and FastAPI's testing utilities.

Run the complete test suite:

```bash
python -m pytest
```

For verbose output:

```bash
python -m pytest -v
```

Current result:

```text
36 passed
```

Current automated testing covers:

```text
Health API
   │
   └── Application health

Services
   │
   ├── Retrieve services
   ├── Retrieve service by ID
   └── Active service mapping

Bookings
   │
   ├── Create
   ├── Retrieve all
   ├── Retrieve by ID
   ├── Missing booking
   ├── Update
   ├── Missing booking during update
   ├── Cancel
   ├── Missing booking during cancellation
   ├── Confirmed booking filtering
   ├── Conflict rejection
   ├── Cancelled slot reuse
   └── Outside-business-hours rejection

Availability
   │
   ├── Opening-time rules
   ├── Closing-time rules
   ├── Full-duration validation
   ├── Overlap detection
   ├── Back-to-back bookings
   ├── Contained intervals
   ├── Identical intervals
   ├── Conflict detection
   ├── Availability schema validation
   ├── Day-of-week validation
   └── Active availability retrieval

Booking Engine
   │
   ├── Business-hours integration
   └── Conflict integration
```

The test suite is run after booking and scheduling changes to detect regressions across existing functionality.

---

# Technology Stack

## Implemented

| Technology | Purpose |
|---|---|
| Python 3.13 | Core programming language |
| FastAPI | REST API framework |
| MongoDB | NoSQL database |
| PyMongo | MongoDB Python driver |
| Pydantic | Data validation and schemas |
| Pytest | Automated testing |
| Uvicorn | ASGI development server |
| Git / GitHub | Version control and repository hosting |

## Planned

| Technology / Component | Purpose |
|---|---|
| LLM API | Natural-language reasoning |
| AI Agent Tools | Controlled business operations |
| Docker | Containerization |
| GitHub Actions | CI automation |

Additional technologies may later be explored for architectural comparison, including **ASP.NET Core** and relational databases.

---

# Development Roadmap

## Phase 1 — Foundation & Repository Setup

**Status: Completed**

Completed:

- repository initialization
- project structure
- Git configuration
- environment configuration
- project scope
- domain documentation

---

## Phase 2 — API & MongoDB Foundation

**Status: Completed**

Completed:

- FastAPI application
- health endpoint
- Services API
- MongoDB connection
- PyMongo integration
- repository layer
- Pydantic schemas
- initial automated testing

---

## Phase 3 — Booking System

**Status: Completed**

Completed:

- booking schema
- booking repository
- create booking
- retrieve bookings
- retrieve booking by ID
- partial booking updates
- booking cancellation
- booking status management
- validation
- 404 error handling
- automated booking API tests

Result:

```text
A functional persistent booking lifecycle backed by MongoDB.
```

---

## Phase 4 — Customers, Staff & Availability

**Status: In Progress**

### Completed so far

- availability data model
- availability Pydantic schema
- weekday validation
- availability time-range validation
- MongoDB availability collection
- availability repository
- active availability retrieval
- business-hours rules
- service-duration-aware availability validation
- interval overlap detection
- booking conflict detection
- double-booking prevention
- cancelled booking exclusion from conflicts
- booking engine integration
- API-level scheduling validation
- automated availability tests

### Remaining

- customer management
- staff management
- service-to-staff relationships
- staff-specific working schedules
- staff availability
- generated available time slots

This phase is moving the project beyond basic booking CRUD toward real scheduling behavior.

---

## Phase 5 — Booking Engine Expansion

**Status: Partially Started**

The booking engine foundation now exists and already participates in scheduling decisions.

Current capabilities include:

- service resolution
- availability resolution
- business-hours validation
- booking conflict detection

Planned expansion includes:

- staff availability validation
- service-to-staff rules
- available-slot generation
- additional booking policies
- lifecycle orchestration
- reusable booking operations

Target flow:

```text
API / AI Tool
     ↓
Booking Engine
     ↓
Business Rules
     ↓
Repository
     ↓
MongoDB
```

---

## Phase 6 — Conversation System

**Status: Planned**

Planned components:

- conversations
- messages
- conversation history
- conversation context
- persistent memory

This layer will allow the future AI agent to maintain context across multiple user messages.

---

## Phase 7 — AI Core

**Status: Planned**

The AI layer will introduce:

- intent detection
- entity extraction
- conversation memory
- booking state management
- decision logic

Example:

```text
"I want a haircut tomorrow after 6 PM."

              ↓

Intent
CREATE_BOOKING

              ↓

Entities
service = Haircut
date = tomorrow
time = after 18:00
```

The goal is to keep this logic independent from the web framework whenever practical.

---

## Phase 8 — AI Business Tools

**Status: Planned**

The AI agent will interact with the application through explicit tools such as:

```text
get_services
get_staff
get_available_times
create_booking
update_booking
cancel_booking
```

Architecture:

```text
AI Agent
   ↓
Business Tools
   ↓
Booking Engine
   ↓
Repository Layer
   ↓
MongoDB
```

The model will not receive unrestricted database access.

---

## Phase 9 — LLM Integration

**Status: Planned**

Planned work:

- connect an LLM API
- tool calling
- structured outputs
- prompt design
- input validation
- controlled tool execution
- error handling
- guardrails

---

## Phase 10 — Production Engineering

**Status: Planned**

Planned improvements:

- expanded unit tests
- integration tests
- AI workflow tests
- security validation
- logging
- Docker
- GitHub Actions
- CI testing
- deployment preparation

---

# Target AI Architecture

The target system is designed so that AI reasoning and deterministic business operations remain separated.

```text
                    Client / Channel
                           │
                           ▼
                       FastAPI
                           │
                           ▼
                       AI Agent
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
       Intent           Memory        Booking State
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                    Decision Engine
                           │
                           ▼
                    Business Tools
                           │
                           ▼
                    Booking Engine
                           │
                           ▼
               Availability / Rules
                           │
                           ▼
                    Repository Layer
                           │
                           ▼
                        MongoDB
```

---

# Example Future AI Workflow

A user might eventually send:

```text
"I need a haircut tomorrow after 6 PM."
```

The system should process that request through:

```text
User Message
     ↓
Intent Detection
     ↓
Entity Extraction
     ↓
Conversation Context
     ↓
Service Resolution
     ↓
Availability Check
     ↓
Business Hours Check
     ↓
Conflict Detection
     ↓
Booking Decision
     ↓
Controlled Business Tool
     ↓
Booking Engine
     ↓
MongoDB
     ↓
Confirmation Response
```

The important architectural principle is that the language model **decides what operation is needed**, while deterministic application code **decides whether that operation is valid and performs it safely**.

---

# Engineering Principles

## Separation of Concerns

HTTP routing, validation, persistence, scheduling, business rules, and AI reasoning are separated into distinct responsibilities.

## Repository Pattern

Database access is encapsulated behind repository functions rather than being scattered throughout API routes or business logic.

## Validation at Boundaries

Incoming API data and availability configuration are validated before reaching persistence or business logic.

## Deterministic Scheduling

Availability, duration, overlap, and conflict rules are implemented as deterministic application logic rather than delegated to an AI model.

## Testability

Important behavior is covered by automated tests, including lower-level scheduling functions and API integration behavior.

## Maintainability

The architecture is being expanded incrementally rather than placing booking, database, scheduling, and AI logic into a single module.

## Security

Secrets and environment-specific configuration must not be committed to Git.

Future LLM integration will use controlled operations instead of unrestricted model access to internal systems.

## AI Safety

The future agent will invoke explicit tools with validated arguments.

```text
LLM
 ↓
Validated Tool Call
 ↓
Booking Engine
 ↓
Business Rules
 ↓
Repository
 ↓
Database
```

## Framework Independence

Core booking, availability, and future AI logic should remain as independent as practical from FastAPI so they can later be reused through other interfaces and communication channels.

---

# Local Development

## 1. Clone the Repository

```bash
git clone https://github.com/Danakaabi/ai-booking-agent-.git
cd ai-booking-agent
```

## 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

## 3. Configure Environment Variables

Use:

```text
.env.example
```

as the reference for local configuration.

Do not commit secrets or private credentials.

## 4. Start MongoDB

MongoDB must be available before using database-dependent endpoints or running database-dependent tests.

Verify the local MongoDB server:

```bash
mongosh --eval 'db.runCommand({ ping: 1 })'
```

A successful result should include:

```text
{ ok: 1 }
```

## 5. Run the API

```bash
uvicorn api.main:app --reload
```

Application:

```text
http://127.0.0.1:8000
```

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

OpenAPI specification:

```text
http://127.0.0.1:8000/openapi.json
```

## 6. Run Tests

```bash
python -m pytest
```

For verbose output:

```bash
python -m pytest -v
```

Current expected result:

```text
36 passed
```

---

# Current Development Focus

The project has progressed beyond basic booking CRUD.

The current engineering focus is:

> **Complete the scheduling and availability layer before introducing conversation and AI reasoning.**

The progression now looks like:

```text
Booking CRUD
     │
     │ Completed
     ▼
Availability Foundation
     │
     │ Implemented
     ▼
Business Hours
     │
     │ Implemented
     ▼
Conflict Prevention
     │
     │ Implemented
     ▼
Booking Engine
     │
     │ Foundation Implemented
     ▼
Staff Scheduling
     ↓
Available Slot Generation
     ↓
Conversation System
     ↓
AI Core
     ↓
Agent Tools
     ↓
LLM Integration
```

This sequencing is intentional.

The future AI agent should consume a reliable scheduling engine rather than inventing scheduling decisions itself.

---

# Long-Term Vision

The goal is not to build only another booking REST API.

The project is intended to evolve into a reusable booking agent capable of understanding natural-language requests while relying on deterministic backend rules for execution.

Potential future domains include:

- salons
- clinics
- healthcare scheduling
- events
- professional services
- other appointment-based systems

Different channels should eventually be able to reuse the same booking engine without rebuilding the core logic.

```text
Web
   ┐
Mobile
   ├────→ AI / API Layer
Chat
   ┘            ↓
          Booking Engine
                ↓
        Availability Rules
                ↓
             MongoDB
```

---

# Project Philosophy

> **AI should reason about the request.  
> Business logic should decide what is allowed.  
> The database should persist the result.**

This separation is the foundation of the project as it evolves from a tested booking backend into an AI-driven booking system.

---

<p align="center">
  <strong>AI Booking Agent</strong><br>
  Backend Engineering • Booking Systems • Availability • AI Agents • System Design
</p>