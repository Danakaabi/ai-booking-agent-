<p align="center">
  <img src="docs/assets/ai-booking-agent-banner.png"
       alt="AI Booking Agent"
       width="100%">
</p>

# AI Booking Agent

An intelligent and reusable booking agent built to explore **AI agent architecture, backend engineering, MongoDB, REST APIs, conversation memory, automated booking workflows, testing, and system design**.

The project is designed as a general-purpose booking system that can later support different industries and communication channels while keeping the core booking and AI logic independent.

---

## Overview

AI Booking Agent aims to build an intelligent system capable of understanding booking requests, managing conversation context, checking services and availability, executing booking operations, and eventually interacting with users through an AI agent.

The architecture is being developed incrementally, starting with a reliable backend and database layer before introducing the AI decision-making components.

```text
Client
  ↓
FastAPI
  ↓
API Routes
  ↓
Repository Layer
  ↓
MongoDB
```

The planned AI architecture will extend this flow:

```text
User Message
     ↓
Intent Detection
     ↓
Conversation Memory
     ↓
Booking State
     ↓
Decision Engine
     ↓
Business Tools
     ↓
Booking Engine
     ↓
MongoDB
     ↓
Response
```

---

## Project Goals

- Build an intelligent booking workflow
- Design clean and maintainable REST APIs
- Learn and apply MongoDB and NoSQL data modeling
- Separate API, database, and business responsibilities
- Build framework-independent AI logic
- Implement intent detection
- Implement conversation memory
- Add booking state management
- Build reusable business tools for the AI agent
- Integrate LLM APIs safely
- Add automated testing
- Apply security and input-validation practices
- Containerize the project with Docker
- Add CI workflows with GitHub Actions
- Document architecture and engineering decisions

---

## Current Progress

### Foundation

- [x] Initialize Git repository
- [x] Create project structure
- [x] Configure `.gitignore`
- [x] Configure environment variable template
- [x] Document project scope
- [x] Document booking domain model

### FastAPI

- [x] Create FastAPI application
- [x] Add health-check endpoint
- [x] Add Services API
- [x] Add Pydantic service schema
- [x] Verify API responses locally
- [x] Generate interactive API documentation through FastAPI

### MongoDB

- [x] Install and configure MongoDB locally
- [x] Create `ai_booking_agent` database
- [x] Create services data
- [x] Install and configure PyMongo
- [x] Create MongoDB connection layer
- [x] Verify database connectivity using `ping`
- [x] Create repository layer
- [x] Read active services from MongoDB
- [x] Connect Services API to real MongoDB data

### Testing

- [x] Configure Pytest
- [x] Test health endpoint
- [x] Test services endpoint
- [x] Verify current test suite passes

Current test status:

```text
2 passed
```

---

## Current Architecture

```text
AI Booking Agent
│
├── api/
│   ├── main.py
│   ├── routes/
│   │   └── services.py
│   └── schemas/
│       └── service.py
│
├── database/
│   ├── connection.py
│   └── repositories/
│       └── services.py
│
├── ai_core/
│
├── tests/
│   ├── test_health.py
│   └── test_services.py
│
└── docs/
    ├── assets/
    ├── domain/
    └── requirements/
```

The project separates responsibilities between layers:

```text
API Route
    ↓
Repository
    ↓
Database
```

This keeps database access separate from HTTP routing and prepares the project for additional business and AI layers.

---

## Current API

### Health Check

```http
GET /health
```

Used to verify that the API is running correctly.

Example response:

```json
{
  "status": "ok",
  "server": "ai-booking-agent"
}
```

### Services

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

Current data flow:

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
Service Schema
      ↓
JSON Response
```

---

## Technology Stack

### Implemented

- **Python**
- **FastAPI**
- **MongoDB**
- **PyMongo**
- **Pydantic**
- **Pytest**
- **Uvicorn**

### Planned

- LLM APIs
- AI Agent Tools
- Docker
- GitHub Actions

Additional technologies may be introduced later for architectural comparison and expansion, including ASP.NET Core and relational databases.

---

## Roadmap

### Phase 1 — Foundation & Repository Setup

**Status: Completed**

Project structure, documentation, Git configuration, environment setup, and initial domain design.

### Phase 2 — API & MongoDB Foundation

**Status: Completed**

FastAPI application, health endpoint, Services API, MongoDB connection, repository layer, schemas, and initial automated tests.

### Phase 3 — Booking System

**Next**

Planned work includes:

- Booking schemas
- Booking repository
- Create booking endpoint
- Retrieve bookings
- Update booking
- Cancel booking
- Booking status management
- Validation and error handling

### Phase 4 — Customers, Staff & Availability

Planned components:

- Customer management
- Staff management
- Service-to-staff relationships
- Working schedules
- Available time calculation
- Booking conflict prevention

### Phase 5 — Booking Engine

The booking engine will contain the core business rules independently from the API layer.

Planned responsibilities:

- Validate booking requests
- Check service availability
- Check staff availability
- Prevent overlapping bookings
- Manage booking lifecycle
- Expose reusable booking operations

### Phase 6 — Conversation System

Planned components:

- Conversations
- Messages
- Conversation history
- Conversation context
- Persistent memory

### Phase 7 — AI Core

The AI layer will introduce:

- Intent detection
- Entity extraction
- Conversation memory
- Booking state management
- Decision engine

Example:

```text
"I want a haircut tomorrow after 6 PM"

              ↓

Intent
CREATE_BOOKING

              ↓

Entities
service = Haircut
date = tomorrow
time = after 18:00
```

### Phase 8 — AI Business Tools

The AI agent will interact with the booking system through controlled tools such as:

```text
get_services
get_staff
get_available_times
create_booking
update_booking
cancel_booking
```

The AI model will not access the database directly.

```text
AI Agent
   ↓
Business Tools
   ↓
Booking Engine
   ↓
Repository
   ↓
MongoDB
```

### Phase 9 — LLM Integration

Planned work:

- Connect an LLM API
- Tool calling
- Structured outputs
- Prompt design
- Input validation
- Safe tool execution
- Error handling
- Guardrails

### Phase 10 — Production Engineering

Planned improvements:

- Expanded unit tests
- Integration tests
- AI workflow tests
- Security validation
- Logging
- Docker
- GitHub Actions
- CI testing
- Deployment preparation

---

## Target Architecture

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

## Engineering Principles

This project follows several engineering principles:

**Separation of Concerns**

API routes, database access, business logic, and AI logic are kept in separate layers.

**Testability**

Core functionality is designed to be testable independently.

**Security**

Secrets and environment-specific configuration should not be committed to Git.

**Maintainability**

The project structure is designed to remain understandable as functionality grows.

**AI Safety**

The future AI agent will execute controlled business tools rather than directly manipulating the database.

**Framework Independence**

Core booking and AI logic should remain as independent as practical from the web framework.

---

## Local Development

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install project dependencies as defined by the project environment.

Start MongoDB before running database-dependent functionality.

Run the API:

```bash
uvicorn api.main:app --reload
```

The local API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

Run tests:

```bash
pytest -v
```

---

## Project Status

🚧 **Active Development**

The backend foundation and initial MongoDB integration are working.

Current focus:

> Building the booking system and business rules that will later become tools for the AI agent.

---

## Long-Term Vision

The goal is not only to create a booking REST API.

The final system should be capable of receiving a natural-language booking request such as:

```text
"I need a haircut tomorrow after 6 PM."
```

and processing it through:

```text
User Request
     ↓
Intent Detection
     ↓
Entity Extraction
     ↓
Conversation Memory
     ↓
Availability Check
     ↓
Booking Decision
     ↓
Business Tool
     ↓
Booking Creation
     ↓
Confirmation Response
```

The core system is intended to remain reusable so that different communication channels can be integrated later without rebuilding the booking engine.

---

## License

A license has not yet been selected for this project.