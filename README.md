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
  <img src="https://img.shields.io/badge/Pytest-10%20Passing-0A9EDC?logo=pytest&logoColor=white" alt="Tests">
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
- Conversation memory
- Automated testing
- System design
- Safe LLM tool execution

The project is intentionally being developed **backend-first**.

Instead of connecting an LLM directly to a database, the system first establishes a reliable booking domain, API layer, repository layer, validation rules, and automated tests.

The AI layer will later interact with these capabilities through controlled business tools.

---

## Why This Project?

A useful booking agent needs more than natural-language generation.

It must be able to reliably:

- understand what the user wants
- retrieve available services
- manage booking state
- validate booking information
- check availability
- prevent conflicting reservations
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
Repository Layer
  ↓
MongoDB
```

The AI model will not manipulate the database directly.

---

# Current Status

> **Phase 3 — Booking System: Completed**
>
> **Next: Phase 4 — Customers, Staff & Availability**

The project currently has a functional FastAPI + MongoDB backend with booking lifecycle operations and automated API tests.

Current automated test status:

```text
10 passed
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

## MongoDB

- [x] Local MongoDB environment
- [x] `ai_booking_agent` database
- [x] Services collection
- [x] Bookings collection
- [x] PyMongo integration
- [x] MongoDB connection layer
- [x] Repository pattern
- [x] ObjectId handling
- [x] Persistent booking operations

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

## Testing

- [x] Pytest configured
- [x] Health endpoint test
- [x] Services endpoint test
- [x] Booking creation test
- [x] Booking retrieval tests
- [x] Booking update tests
- [x] Booking cancellation tests
- [x] Not-found behavior tests
- [x] Full test suite passing

---

# Current Architecture

```text
AI Booking Agent
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
│       └── booking.py
│
├── database/
│   ├── connection.py
│   │
│   └── repositories/
│       ├── services.py
│       └── bookings.py
│
├── ai_core/
│
├── tests/
│   ├── test_health.py
│   ├── test_services.py
│   └── test_bookings.py
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

The current backend follows:

```text
Client
   ↓
FastAPI
   ↓
API Routes
   ↓
Pydantic Validation
   ↓
Repository Layer
   ↓
MongoDB
```

This separation prevents HTTP routing code from becoming tightly coupled to database operations.

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
get_all_services()
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

Creates and persists a new booking.

Example request:

```json
{
  "service_id": "6a779ed59b6b145fcfe108ab",
  "customer_name": "Dana",
  "customer_phone": "0500000000",
  "booking_datetime": "2026-08-20T19:00:00"
}
```

New bookings default to:

```json
{
  "status": "confirmed"
}
```

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

For example:

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

Example response:

```json
{
  "service_id": "6a779ed59b6b145fcfe108ab",
  "customer_name": "Dana",
  "customer_phone": "0500000000",
  "booking_datetime": "2026-08-20T19:00:00",
  "status": "cancelled",
  "id": "..."
}
```

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

Additional lifecycle rules can be introduced as the booking engine evolves.

---

# Validation & Error Handling

Input validation is handled using **Pydantic**.

Current validation includes:

- required service ID
- customer name length
- customer phone length
- datetime parsing
- controlled booking status values

Booking status is restricted to supported states rather than accepting arbitrary strings.

For example, a value such as:

```text
hello
```

is rejected by validation.

Missing booking resources return:

```http
404 Not Found
```

instead of silently returning an empty result.

---

# Testing

The project uses **Pytest** and FastAPI's testing utilities.

Run the complete test suite:

```bash
python -m pytest
```

Current result:

```text
10 passed
```

Current test coverage includes behavior for:

```text
Health API
   │
   └── Application health

Services API
   │
   └── Retrieve services

Bookings API
   │
   ├── Create
   ├── Retrieve all
   ├── Retrieve by ID
   ├── Missing booking
   ├── Update
   ├── Missing booking during update
   ├── Cancel
   └── Missing booking during cancellation
```

The test suite is run after booking changes to detect regressions across existing functionality.

---

# Technology Stack

## Implemented

| Technology | Purpose |
|---|---|
| Python | Core programming language |
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

**Status: Next**

Planned components:

- customer management
- staff management
- service-to-staff relationships
- working schedules
- availability calculation
- booking conflict detection
- double-booking prevention

This phase moves the project beyond basic booking CRUD toward actual scheduling logic.

---

## Phase 5 — Booking Engine

**Status: Planned**

The booking engine will isolate business rules from both FastAPI and the future AI layer.

Planned responsibilities:

- validate booking requests
- verify service availability
- verify staff availability
- prevent overlapping bookings
- enforce booking rules
- manage booking lifecycle
- expose reusable booking operations

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

HTTP routing, validation, persistence, business rules, and AI reasoning are separated into distinct responsibilities.

## Repository Pattern

Database access is encapsulated behind repository functions rather than being scattered throughout API routes.

## Validation at Boundaries

Incoming API data is validated before reaching persistence logic.

## Testability

Important behavior is covered by automated tests and designed so that individual layers can increasingly be tested independently.

## Maintainability

The architecture is being expanded incrementally rather than placing booking, database, and AI logic into a single module.

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
Business Rules
 ↓
Repository
 ↓
Database
```

## Framework Independence

Core booking and AI logic should remain as independent as practical from FastAPI so it can later be reused through other interfaces and communication channels.

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

Use the provided:

```text
.env.example
```

as the reference for local configuration.

Do not commit secrets or private credentials.

## 4. Start MongoDB

MongoDB must be available before using database-dependent endpoints or running database-dependent tests.

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

---

# Current Development Focus

The backend foundation and core booking lifecycle are now operational.

The next engineering milestone is:

> **Availability calculation and booking conflict prevention.**

This includes determining whether a requested time can actually be booked rather than simply storing a booking request.

The planned progression is:

```text
Booking CRUD
     │
     │ Completed
     ▼
Availability
     ↓
Conflict Prevention
     ↓
Booking Engine
     ↓
Conversation System
     ↓
AI Core
     ↓
Agent Tools
     ↓
LLM Integration
```

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
  Backend Engineering • Booking Systems • AI Agents • System Design
</p>