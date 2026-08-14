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
  <img src="https://img.shields.io/badge/Pytest-68%20Passing-0A9EDC?logo=pytest&logoColor=white" alt="Tests">
  <img src="https://img.shields.io/badge/Status-Active%20Development-orange" alt="Status">
</p>

---

## Overview

**AI Booking Agent** is a reusable booking backend designed to evolve into an AI-powered booking agent.

The project is intentionally developed **backend-first** so that scheduling, availability, conflict detection, validation, and persistence are reliable before adding LLM reasoning.

```text
User / Client
      ↓
FastAPI
      ↓
Business Logic
      ↓
Booking & Scheduling Engine
      ↓
Repository Layer
      ↓
MongoDB
```

The future AI layer will interact with the system through controlled business tools rather than direct database access.

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
> **Phase 5 — Booking Engine Expansion: Next**

Current automated test status:

```text
68 passed
```

A FastAPI/Starlette TestClient dependency warning is currently emitted but does not represent a failing test.

---

# Implemented Features

## Booking

- [x] Create bookings
- [x] Retrieve all bookings
- [x] Retrieve booking by ID
- [x] Partial booking updates
- [x] Booking cancellation
- [x] Booking status lifecycle
- [x] 404 handling
- [x] Confirmed-booking filtering
- [x] Cancelled-slot reuse

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
- [x] Full regression suite

```text
68 passed
```

---

# Architecture

```text
AI Booking Agent
│
├── ai_core/
│   ├── availability.py
│   ├── booking_engine.py
│   ├── staff_availability.py
│   └── available_slots.py
│
├── api/
│   ├── main.py
│   ├── routes/
│   │   ├── services.py
│   │   ├── bookings.py
│   │   ├── customers.py
│   │   └── staff.py
│   └── schemas/
│       ├── service.py
│       ├── booking.py
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
│   └── test_staff_availability.py
│
├── docs/
├── .env.example
├── .gitignore
└── README.md
```

Layered flow:

```text
Client
   ↓
FastAPI
   ↓
API Routes
   ↓
Pydantic Validation
   ↓
Business Logic
   ├── Booking Engine
   ├── Availability Rules
   ├── Conflict Detection
   ├── Staff Availability
   └── Slot Generation
   ↓
Repository Layer
   ↓
MongoDB
```

---

# API

## Health

```http
GET /health
```

---

## Services

```http
GET /services
```

---

## Bookings

```http
POST /bookings
GET /bookings
GET /bookings/{booking_id}
PATCH /bookings/{booking_id}
PATCH /bookings/{booking_id}/cancel
```

Bookings are validated against configured business hours and existing confirmed reservations.

Conflicting reservations return:

```text
409 Conflict
```

---

## Customers

Customer creation, retrieval, validation, and active-customer filtering are supported through the customer API and repository layer.

---

## Staff

```http
GET /staff
GET /staff/{staff_id}
```

Staff members can be linked to services and assigned individual working schedules.

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

Cancelled bookings are excluded from conflict detection and release their time slots.

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

Overlapping bookings are rejected.

```text
Existing:
10:00 → 11:00

Requested:
10:30 → 11:30

Result:
409 Conflict
```

Back-to-back bookings remain valid:

```text
10:00 → 11:00
11:00 → 12:00

No conflict
```

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
- AI business tools
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

FastAPI, MongoDB, PyMongo, repositories, schemas, and initial tests.

---

## Phase 3 — Booking System

**Completed**

Booking CRUD, lifecycle management, validation, cancellation, and automated API tests.

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

Result:

```text
68 passed
```

---

## Phase 5 — Booking Engine Expansion

**Next**

Planned:

- stronger booking orchestration
- centralized booking policies
- staff-aware booking decisions
- reusable booking operations
- lifecycle orchestration
- cleaner error boundaries
- preparation for AI business tools

```text
API / AI Tool
     ↓
Booking Engine
     ↓
Business Rules
     ↓
Repositories
     ↓
MongoDB
```

---

## Phase 6 — Conversation System

**Planned**

- conversations
- messages
- conversation history
- conversation context
- persistent memory

---

## Phase 7 — AI Core

**Planned**

- intent detection
- entity extraction
- booking state
- decision logic
- conversation memory

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
68 passed
```

---

# Current Development Focus

The scheduling foundation is now complete.

```text
Foundation               ✓
FastAPI + MongoDB        ✓
Booking System           ✓
Availability             ✓
Conflict Prevention      ✓
Customers                ✓
Staff                    ✓
Staff Scheduling         ✓
Available Slots          ✓

Booking Engine Expansion → NEXT
Conversation System
AI Core
Agent Tools
LLM Integration
Production Engineering
```

The next objective is:

> **Expand the booking engine into a reusable orchestration layer before introducing conversational AI.**

---

# Target AI Architecture

```text
Client
   ↓
FastAPI
   ↓
AI Agent
   ↓
Business Tools
   ↓
Booking Engine
   ↓
Scheduling Rules
   ↓
Repositories
   ↓
MongoDB
```

The AI model will decide **what operation is needed**.

Deterministic backend code will decide **whether the operation is valid and how it is executed**.

---

# Engineering Principles

- Separation of concerns
- Repository pattern
- Validation at application boundaries
- Deterministic scheduling
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
AI / API Layer
   ↓
Booking Engine
   ↓
Scheduling
   ↓
MongoDB
```

---

# Project Philosophy

> **AI should reason about the request.**
>
> **Business logic should decide what is allowed.**
>
> **The database should persist the result.**

---

<p align="center">
  <strong>AI Booking Agent</strong><br>
  Backend Engineering • Booking Systems • Scheduling • AI Agents • System Design
</p>