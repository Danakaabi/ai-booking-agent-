<p align="center">
  <img src="docs/assets/ai-booking-agent-banner.png"
       alt="AI Booking Agent"
       width="100%">
</p>

<h1 align="center">AI Booking Agent</h1>

<p align="center">
  <strong>Backend-first intelligent booking system evolving into a reusable AI-powered booking agent.</strong>
</p>

<p align="center">
  Built with FastAPI, MongoDB, deterministic AI logic, controlled LLM integration, and React.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/MongoDB-Database-47A248?logo=mongodb&logoColor=white" alt="MongoDB">
  <img src="https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black" alt="React">
  <img src="https://img.shields.io/badge/Vite-8-646CFF?logo=vite&logoColor=white" alt="Vite">
  <img src="https://img.shields.io/badge/Pydantic-Validation-E92063" alt="Pydantic">
  <img src="https://img.shields.io/badge/Pytest-234%20Passing-0A9EDC?logo=pytest&logoColor=white" alt="Tests">
  <img src="https://img.shields.io/badge/Phase%209-Completed-success" alt="Phase 9">
  <img src="https://img.shields.io/badge/Phase%2010-In%20Progress-orange" alt="Phase 10">
</p>

---

## Overview

**AI Booking Agent** is a reusable booking system designed around deterministic business rules, persistent conversation state, controlled AI execution, optional LLM-assisted language interpretation, and a React-based conversational interface.

The project is intentionally developed **backend-first** so that booking rules, scheduling, availability, staff assignment, conflict detection, validation, conversation state, context management, AI decisions, and controlled tool execution remain reliable regardless of which user interface or language model is connected to the system.

The architecture has evolved from a pure backend into a full conversational application:

```text
User
  ↓
React Chat Interface
  ↓
FastAPI
  ↓
Conversation System
  ↓
LLM / Deterministic Interpreter
  ↓
AI Core
  ↓
Decision Engine
  ↓
Controlled Business Tools
  ↓
Booking Engine
  ↓
Repository Layer
  ↓
MongoDB
```

The LLM is not the authority over booking operations.

It cannot directly access MongoDB, create bookings, bypass the Booking Engine, or independently choose arbitrary backend operations.

The deterministic application remains responsible for validation and execution.

---

## Current Status

| Phase | Status |
|---|---|
| Phase 1 — Foundation | ✅ Completed |
| Phase 2 — API & MongoDB Foundation | ✅ Completed |
| Phase 3 — Booking System | ✅ Completed |
| Phase 4 — Customers, Staff & Availability | ✅ Completed |
| Phase 5 — Booking Engine Expansion | ✅ Completed |
| Phase 6 — Conversation System | ✅ Completed |
| Phase 7 — AI Core & Controlled Execution | ✅ Completed |
| Phase 8 — AI Business Tools | ✅ Completed |
| Phase 9 — LLM Integration | ✅ Completed |
| Phase 10 — React Chat Interface & AI Booking Agent Simulation | 🚧 In Progress |
| Production Engineering | Planned |

Latest full backend regression before Phase 10:

```text
234 passed
0 failures
```

During Phase 10, the focused backend regression after introducing development CORS support also passed:

```text
17 passed
0 failures
```

The Phase 10 frontend currently passes ESLint validation.

---

## Implemented Features

### Booking

- [x] Create bookings
- [x] Retrieve all bookings
- [x] Retrieve booking by ID
- [x] Partial booking updates
- [x] Validated rescheduling
- [x] Booking cancellation
- [x] Booking status lifecycle
- [x] Confirmed-booking filtering
- [x] Cancelled-slot reuse
- [x] Conflict-aware creation and rescheduling
- [x] Self-conflict exclusion during updates

### Booking Engine

- [x] Centralized booking validation
- [x] Service validation
- [x] Business-hours validation
- [x] Staff validation
- [x] Service-to-staff validation
- [x] Staff availability validation
- [x] Booking conflict detection
- [x] Staff-aware conflict detection
- [x] Booking creation orchestration
- [x] Booking update and rescheduling orchestration
- [x] Booking cancellation orchestration
- [x] Repository-backed execution
- [x] Shared HTTP error mapping

### Availability & Scheduling

- [x] Business-hours validation
- [x] Full service-duration validation
- [x] Booking overlap detection
- [x] Double-booking prevention
- [x] Back-to-back booking support
- [x] Persistent availability configuration
- [x] Staff-specific working schedules
- [x] Staff availability validation
- [x] Staff-specific booking conflicts
- [x] Available time-slot generation
- [x] Occupied-slot exclusion
- [x] Available-slots API

### Customers

- [x] Customer schema and validation
- [x] Customer repository
- [x] Customer API
- [x] Active customer filtering

### Staff

- [x] Staff schema and validation
- [x] Staff repository
- [x] Staff API
- [x] Service-to-staff relationships
- [x] Staff lookup by service
- [x] Staff-specific availability

### Conversation System

- [x] Conversation and message schemas
- [x] User, assistant, and system message roles
- [x] Conversation persistence
- [x] Message persistence
- [x] Ordered conversation history
- [x] Conversation isolation
- [x] Conversation state
- [x] Booking context
- [x] Partial context updates
- [x] Existing-context preservation
- [x] Conversation service
- [x] Conversation-to-booking conversion
- [x] Booking-engine integration
- [x] Conversation REST API
- [x] Active-intent persistence
- [x] Multi-turn booking continuation
- [x] Multi-turn availability continuation
- [x] LLM-aware message processing boundary

### AI Core

- [x] Intent detection
- [x] Entity extraction
- [x] Entity resolution
- [x] Context preparation
- [x] Existing-context merging
- [x] Missing-field detection
- [x] Structured AI decisions
- [x] Decision engine
- [x] Response generation
- [x] AI orchestration
- [x] Controlled business-action selection
- [x] Tool executor
- [x] Conversation-to-tool execution
- [x] No direct AI access to MongoDB
- [x] Deterministic fallback behavior

### AI Business Tools

The controlled execution layer currently exposes:

```text
GET_SERVICES         → get_services()
GET_STAFF            → get_staff()
GET_AVAILABLE_TIMES  → get_available_times()
CREATE_BOOKING       → execute_booking_from_conversation()
```

The decision layer maps supported intents to explicit business actions:

```text
BOOK               → CREATE_BOOKING
CHECK_AVAILABILITY → GET_AVAILABLE_TIMES
GET_SERVICES       → GET_SERVICES
GET_STAFF          → GET_STAFF
```

Availability requests require:

```text
service_id
staff_id
booking_datetime
```

Booking requests require:

```text
service_id
customer_name
customer_phone
booking_datetime
```

If required information is missing, the system returns:

```text
ASK_USER
```

When the required context is complete, the decision layer returns:

```text
CALL_TOOL
```

with an approved `BusinessAction`.

### LLM Integration

- [x] LLM provider abstraction
- [x] Structured LLM output model
- [x] LLM interpreter
- [x] Message interpreter boundary
- [x] OpenAI provider implementation
- [x] OpenAI Python SDK integration
- [x] Environment-based LLM configuration
- [x] LLM-specific error handling
- [x] Provider factory
- [x] Structured natural-language interpretation
- [x] Integration with existing orchestrator
- [x] Integration with conversation processing
- [x] FastAPI dependency boundary for the provider
- [x] Deterministic fallback when LLM is disabled
- [x] Tests around the LLM boundary
- [x] No direct LLM access to MongoDB
- [x] No direct LLM booking execution
- [x] No LLM bypass of Tool Executor
- [x] No LLM bypass of Booking Engine

The LLM is disabled by default:

```text
LLM_ENABLED=false
```

When disabled:

```text
User Message
      ↓
Deterministic AI Core
```

When enabled with valid configuration:

```text
User Message
      ↓
OpenAI Provider
      ↓
Structured Output
      ↓
Existing AI Core
      ↓
Decision Engine
      ↓
Controlled Execution
```

The real external OpenAI call remains configuration-dependent and requires a valid API key.

### React Chat Interface

Phase 10 currently includes:

- [x] React frontend foundation
- [x] Vite development environment
- [x] ESLint
- [x] Responsive chat shell
- [x] Message composer
- [x] Accessible message input
- [x] Loading-ready UI structure
- [x] Frontend environment configuration
- [x] API base URL configuration
- [x] Local environment files excluded from Git
- [x] Development CORS support
- [x] Dedicated conversation API client
- [x] Create-conversation API function
- [x] Send-message API function
- [x] Conversation-history API function
- [ ] Connect chat state to the conversation API
- [ ] Render user and assistant messages
- [ ] Loading state during message processing
- [ ] User-facing API error state
- [ ] New conversation interaction
- [ ] Conversation history UI
- [ ] Booking context panel
- [ ] Current intent display
- [ ] Booking status display

The React application does not contain booking business rules.

Its responsibility is limited to:

```text
UI
State
API Communication
User Interaction
Rendering
```

Backend responsibilities remain:

```text
AI Decisions
Entity Resolution
Context Management
Booking Rules
Validation
Tool Execution
Persistence
MongoDB
```

---

## Architecture

```text
AI Booking Agent
│
├── ai_core/
│   ├── __init__.py
│   ├── availability.py
│   ├── available_slots.py
│   ├── booking_engine.py
│   ├── business_action.py
│   ├── business_tools.py
│   ├── context_preparation.py
│   ├── conversation_service.py
│   ├── decision.py
│   ├── decision_engine.py
│   ├── entities.py
│   ├── entity_extractor.py
│   ├── entity_resolver.py
│   ├── intent.py
│   ├── intent_detector.py
│   ├── llm_config.py
│   ├── llm_errors.py
│   ├── llm_factory.py
│   ├── llm_interpreter.py
│   ├── llm_output.py
│   ├── llm_provider.py
│   ├── message_interpreter.py
│   ├── missing_fields.py
│   ├── missing_information.py
│   ├── openai_provider.py
│   ├── orchestrator.py
│   ├── resolved_entities.py
│   ├── response_generator.py
│   ├── staff_availability.py
│   └── tool_executor.py
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
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   │   └── conversations.js
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── .env.example
│   ├── .gitignore
│   ├── eslint.config.js
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── tests/
├── docs/
├── .env.example
├── .gitignore
└── README.md
```

### Layered Flow

```text
React Client
      ↓
FastAPI
      ↓
API Routes
      ↓
Pydantic Validation
      ↓
Conversation Service
      ↓
LLM / Deterministic Interpreter
      ↓
AI Core / Booking Engine
      ↓
Business Rules & Controlled Execution
      ↓
Repository Layer
      ↓
MongoDB
```

### AI Conversation Flow

```text
User Message
      ↓
Message Interpreter
      ↓
LLM or Deterministic Interpreter
      ↓
Intent + Extracted Entities
      ↓
Entity Resolution
      ↓
Context Preparation
      ↓
Merge With Existing Context
      ↓
Decision Engine
      ↓
ASK_USER / CALL_TOOL / UNKNOWN
      ↓
Response Generator / Tool Executor
      ↓
Business Tools / Booking Engine
      ↓
Repositories
      ↓
MongoDB
```

### LLM Boundary

```text
Natural Language
      ↓
LLM Provider
      ↓
Structured Interpretation
      ↓
Existing AI Core
```

The LLM does **not** execute business operations.

The controlled execution path remains:

```text
Decision Engine
      ↓
BusinessAction
      ↓
Tool Executor
      ↓
Business Tool / Booking Engine
      ↓
Validation
      ↓
Repository
      ↓
MongoDB
```

### Frontend Boundary

```text
React
  ↓
HTTP
  ↓
FastAPI
```

React never connects directly to:

```text
MongoDB
OpenAI
Repositories
Booking Engine
```

This preserves a single source of truth for booking and AI behavior.

---

## API

### Health

```http
GET /health
```

Provides a basic application health check.

### Services

```http
GET /services
```

Returns active services used by booking and AI workflows.

### Bookings

```http
POST  /bookings
GET   /bookings
GET   /bookings/{booking_id}
PATCH /bookings/{booking_id}
PATCH /bookings/{booking_id}/cancel
```

Booking operations pass through application-level business rules before persistence.

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
Create / Update Booking
```

Conflicting reservations return:

```text
409 Conflict
```

### Booking Rescheduling

`PATCH /bookings/{booking_id}` supports partial updates through `BookingUpdate`.

```text
Retrieve Existing Booking
      ↓
Merge Existing + Updated Fields
      ↓
Build Candidate Booking
      ↓
Validate Candidate
      ↓
Exclude Current Booking
      ↓
Apply Update
```

The existing booking is excluded from its own conflict check, preventing false self-conflicts while still protecting against collisions with other reservations.

### Conversations

```http
POST  /conversations
GET   /conversations/{conversation_id}
POST  /conversations/{conversation_id}/messages
GET   /conversations/{conversation_id}/messages
PATCH /conversations/{conversation_id}/booking-context
POST  /conversations/{conversation_id}/bookings
```

A conversation maintains an independent booking context:

```text
BookingContext
├── service_id
├── customer_name
├── customer_phone
├── booking_datetime
└── staff_id
```

All fields are optional while information is being collected.

Partial updates preserve previously collected values.

Messages are stored independently from the conversation document so conversation history can grow without continuously expanding one MongoDB document.

When a user message is submitted through the conversation API, the conversation service can process it through the configured message interpretation boundary.

```text
POST User Message
      ↓
Store Message
      ↓
Process Conversation Message
      ↓
LLM / Deterministic Interpreter
      ↓
AI Core
      ↓
Store Assistant Response
```

The frontend can then retrieve the updated history through:

```http
GET /conversations/{conversation_id}/messages
```

### Staff

```http
GET /staff
GET /staff/{staff_id}
```

Staff members can be linked to services and assigned individual working schedules.

### Available Time Slots

```http
GET /staff/{staff_id}/available-slots
```

Slot generation considers:

- Staff schedules
- Requested service duration
- Confirmed staff bookings
- Conflict rules
- Scheduling boundaries

---

## AI Core & Controlled Execution

The AI Core acts as the deterministic decision and orchestration layer between conversational interpretation and backend business logic.

```text
AI Core
│
├── Intent Detection
├── Entity Extraction
├── Entity Resolution
├── Context Preparation
├── Missing-Field Detection
├── Decision Engine
├── Response Generation
├── Orchestration
└── Controlled Tool Execution
```

Conversational next actions and backend business actions are represented separately.

### Next Actions

```text
ASK_USER
UPDATE_CONTEXT
CALL_TOOL
COMPLETE
UNKNOWN
```

### Business Actions

```text
CREATE_BOOKING
GET_SERVICES
GET_STAFF
GET_AVAILABLE_TIMES
```

### Availability Example

```text
Intent: CHECK_AVAILABILITY
      ↓
Required Context Complete?
      ↓
CALL_TOOL
      ↓
GET_AVAILABLE_TIMES
      ↓
Tool Executor
      ↓
Business Tool
      ↓
Existing Availability Logic
```

### Booking Example

```text
Intent: BOOK
      ↓
Required Context Complete?
      ↓
CALL_TOOL
      ↓
CREATE_BOOKING
      ↓
Conversation Context
      ↓
BookingCreate
      ↓
Booking Engine
      ↓
Validation
      ↓
Repositories
      ↓
MongoDB
```

The Tool Executor does not grant either the deterministic AI layer or the LLM direct database access.

Booking creation continues through the Booking Engine, and business tools reuse existing repository and scheduling logic.

---

## LLM Integration

Phase 9 introduced an optional language-model boundary without replacing the deterministic AI Core.

The design follows:

```text
User Message
      ↓
Message Interpreter
      ↓
LLM Provider or Deterministic Interpreter
      ↓
Intent + ExtractedEntities
      ↓
Existing AI Pipeline
```

The LLM provider is represented through an abstraction rather than being coupled directly to the rest of the application.

Key files include:

```text
ai_core/llm_output.py
ai_core/llm_provider.py
ai_core/llm_interpreter.py
ai_core/message_interpreter.py
ai_core/llm_errors.py
ai_core/llm_config.py
ai_core/llm_factory.py
ai_core/openai_provider.py
```

### Provider Boundary

```text
Application
     ↓
LLMProvider
     ↓
OpenAIProvider
```

This makes the AI Core independent from a specific external model provider.

### Structured Output

The model does not return arbitrary instructions that are directly executed.

Instead:

```text
LLM
 ↓
Structured Output
 ↓
Validated Interpretation
 ↓
Existing AI Core
```

The existing decision and execution layers remain authoritative.

### Deterministic Fallback

LLM usage is disabled by default:

```text
LLM_ENABLED=false
```

When disabled, the existing deterministic pipeline continues to operate normally.

This means Phase 9 did not make the application dependent on an external LLM.

### Security Boundary

The LLM cannot:

- Access MongoDB
- Call repositories directly
- Create bookings directly
- Select arbitrary backend functions
- Bypass the Decision Engine
- Bypass the Tool Executor
- Bypass the Booking Engine
- Persist unvalidated booking operations

The architecture therefore remains:

```text
LLM
 ↓
Interpretation
 ↓
Deterministic AI Core
 ↓
Controlled Execution
```

rather than:

```text
LLM
 ↓
Database
```

---

## Multi-Turn Conversation Processing

The conversation system can preserve an active workflow across multiple messages.

Example:

```text
User:
I want to book Haircut
      ↓
Intent:
BOOK
      ↓
Missing Information
      ↓
ASK_USER
```

A later message can provide missing information without repeating the original booking intent.

Example:

```text
Assistant:
What name should I use for the booking?

User:
Dana
```

The persisted conversation context allows the system to continue the original workflow.

When the required context becomes complete:

```text
Complete Context
      ↓
Decision Engine
      ↓
CALL_TOOL
      ↓
Business Action
      ↓
Tool Executor
      ↓
Booking Engine / Business Tool
```

The same continuation mechanism supports availability requests through persisted `active_intent`.

---

## React Chat Interface

Phase 10 introduces the first real presentation layer for the AI Booking Agent.

The objective is not to create a large administration dashboard.

The first target is a focused conversational experience:

```text
Open React App
      ↓
Start Conversation
      ↓
Send User Message
      ↓
FastAPI Receives Message
      ↓
Conversation System
      ↓
AI Core / LLM Boundary
      ↓
Assistant Response Stored
      ↓
React Loads Conversation History
      ↓
Chat Displays Response
```

### Current Frontend Architecture

```text
frontend/
│
├── src/
│   ├── api/
│   │   └── conversations.js
│   ├── App.jsx
│   ├── App.css
│   ├── index.css
│   └── main.jsx
│
├── .env.example
├── .gitignore
├── eslint.config.js
├── index.html
├── package.json
└── vite.config.js
```

The frontend currently uses:

```text
React 19
Vite 8
ESLint
Native React State
Fetch API
```

No external state-management library has been introduced because the current MVP does not yet require shared application state.

### Conversation API Client

The frontend API layer currently provides:

```text
createConversation()
sendMessage()
getConversationMessages()
```

This keeps HTTP communication outside the UI component and prevents API details from being scattered throughout React components.

### Frontend Environment

The frontend uses:

```text
VITE_API_BASE_URL
```

Example:

```text
VITE_API_BASE_URL=http://127.0.0.1:8000
```

This value is not a secret.

Local environment files are excluded from Git.

React must never contain:

```text
OPENAI_API_KEY
MongoDB credentials
Backend secrets
```

The browser communicates only with FastAPI.

### Development CORS

During local development:

```text
React
http://localhost:5173
```

communicates with:

```text
FastAPI
http://127.0.0.1:8000
```

FastAPI currently allows the React development origin through `CORSMiddleware`.

The configuration does not use unrestricted wildcard origins.

---

## Core Booking Rules

### Scheduling

The complete service duration must fit within the configured availability window.

Example:

```text
Business Hours:
09:00 → 17:00

60-minute service:
16:00 → 17:00   ✓
16:30 → 17:30   ✗
```

### Conflict Detection

Conflict detection uses time intervals rather than exact start-time equality.

```text
Existing:
10:00 → 11:00

Requested:
10:30 → 11:30

Result:
CONFLICT
```

The engine detects:

- Partial overlap
- Contained intervals
- Containing intervals
- Identical intervals

### Back-to-Back Bookings

Adjacent reservations are allowed.

```text
Booking A:
10:00 → 11:00

Booking B:
11:00 → 12:00

Result:
No Conflict
```

### Staff-Aware Scheduling

When a staff member is selected:

```text
Staff Exists
      ↓
Supports Service
      ↓
Is Working
      ↓
Has No Conflicting Booking
```

### Booking Lifecycle

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

Cancelled bookings release their slots while preserving booking history.

### Conversation State vs Booking Status

Conversation state:

```text
active
completed
```

Booking status:

```text
confirmed
cancelled
```

These lifecycles remain separate to avoid mixing conversation concerns with booking-domain rules.

---

## Validation & Error Handling

Input validation is handled with Pydantic.

Schema-level validation includes:

- Required and typed identifiers
- Customer name and phone constraints
- Datetime parsing
- Controlled booking status values
- Controlled day-of-week values
- Availability time ranges
- Controlled message roles
- Message content validation
- Partial `BookingContext` validation
- Structured LLM output validation

Application-level validation protects against:

- Missing services
- Bookings outside business hours
- Bookings extending beyond closing time
- Missing staff
- Unsupported staff-service combinations
- Unavailable staff
- Overlapping confirmed reservations
- Conflicting rescheduling
- Missing conversations
- Incomplete booking context
- Incomplete availability context
- Unsupported AI business actions
- Invalid LLM configuration
- Invalid or unsupported LLM output

Booking-related HTTP errors are centralized in:

```text
api/http_errors.py
```

Examples:

| Error | HTTP Result |
|---|---|
| Service not found | `404 Not Found` |
| Conversation not found | `404 Not Found` |
| Booking conflict | `409 Conflict` |
| Outside business hours | `422 Unprocessable Entity` |
| Incomplete booking context | `422 Unprocessable Entity` |

The React interface is being designed to translate API failures into user-facing error states rather than exposing internal exceptions directly.

---

## Testing

The backend uses Pytest and FastAPI testing utilities.

Run the full backend suite:

```bash
python -m pytest -v
```

Latest full regression before Phase 10:

```text
234 passed
0 failures
```

Testing covers:

```text
API & Schemas
├── Health
├── Services
├── Bookings
├── Customers
├── Staff
└── Conversations

Booking Domain
├── Validation
├── Conflict Detection
├── Creation
├── Rescheduling
├── Cancellation
├── Staff Availability
└── Available Slots

Conversation System
├── Persistence
├── History
├── State
├── Booking Context
├── Context Preservation
├── Booking Execution
├── Active Intent
└── Multi-Turn Continuation

AI Core
├── Intent Detection
├── Entity Extraction
├── Entity Resolution
├── Context Preparation
├── Missing Information
├── Decision Engine
├── Orchestration
├── Response Generation
├── Business Tools
└── Tool Execution

LLM Boundary
├── LLM Configuration
├── Provider Abstraction
├── Provider Factory
├── Structured Output
├── LLM Interpreter
├── Message Interpreter
├── OpenAI Provider
├── Fallback Behavior
└── Orchestrator Integration

Integration
├── Conversation → Booking Engine
├── AI Decision → Business Tool
├── Message Interpreter → AI Core
└── Full Regression Suite
```

During Phase 10, focused backend tests after adding development CORS support produced:

```text
17 passed
0 failures
```

Frontend linting:

```bash
cd frontend
npm run lint
```

Current result:

```text
PASS
0 ESLint errors
```

Frontend component and interaction testing will be introduced when the chat behavior becomes sufficiently stable to justify the additional testing setup.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.13 | Backend core language |
| FastAPI | REST API |
| MongoDB | NoSQL database |
| PyMongo | MongoDB driver |
| Pydantic | Data and structured-output validation |
| Pytest | Backend automated testing |
| Uvicorn | ASGI development server |
| OpenAI Python SDK | Optional LLM provider integration |
| React 19 | Chat interface |
| Vite 8 | Frontend development and build tooling |
| ESLint | Frontend static analysis |
| Git / GitHub | Version control |

### Planned

- React chat API integration completion
- Message rendering
- Loading and error states
- Conversation history UX
- Booking context presentation
- Frontend component testing
- API mocking / interaction testing
- Docker
- GitHub Actions
- Continuous Integration
- Logging
- Deployment preparation
- Security hardening

---

## Development Roadmap

### Phase 1 — Foundation

**Completed**

Repository structure, Git configuration, project scope, and domain documentation.

### Phase 2 — API & MongoDB Foundation

**Completed**

FastAPI, MongoDB, PyMongo, repositories, schemas, and initial automated tests.

### Phase 3 — Booking System

**Completed**

Booking CRUD, lifecycle management, validation, cancellation, persistence, and API testing.

### Phase 4 — Customers, Staff & Availability

**Completed**

Customer and staff management, service relationships, availability, staff schedules, conflicts, slot generation, APIs, and regression tests.

### Phase 5 — Booking Engine Expansion

**Completed**

Centralized booking validation and orchestration for creation, updates, rescheduling, cancellation, staff-aware scheduling, conflicts, and shared HTTP error mapping.

### Phase 6 — Conversation System

**Completed**

Persistent conversations, messages, history, state, `BookingContext`, partial updates, conversation services, REST APIs, and Booking Engine integration.

### Phase 7 — AI Core & Controlled Execution

**Completed**

Intent detection, entity extraction and resolution, context preparation, missing-information detection, structured decisions, orchestration, response generation, business-action selection, and controlled execution.

### Phase 8 — AI Business Tools

**Completed**

Implemented controlled reusable tools and decision routing for:

```text
get_services
get_staff
get_available_times
create_booking
```

Also completed:

- Intent-to-business-action routing
- Context requirements per supported workflow
- Controlled execution through existing backend logic
- Multi-turn availability continuation
- Business-tool regression tests
- Decision-engine regression tests
- Conversation-service regression tests
- Full regression validation

Final Phase 8 architecture:

```text
User Message
      ↓
AI Core
      ↓
Decision Engine
      ↓
Business Action
      ↓
Tool Executor
      ↓
Business Tool / Booking Engine
      ↓
Validation & Business Rules
      ↓
Repositories
      ↓
MongoDB
```

No AI component writes directly to MongoDB.

### Phase 9 — LLM Integration

**Completed**

Implemented:

- LLM provider abstraction
- Structured LLM output
- LLM interpreter
- Message interpreter boundary
- OpenAI provider
- OpenAI Python SDK integration
- Environment-based configuration
- Provider factory
- LLM-specific error handling
- Integration with the orchestrator
- Integration with conversation processing
- FastAPI provider dependency
- Deterministic fallback
- Tests around the LLM boundary

Phase 9 preserved the existing deterministic system.

Final architecture:

```text
User Message
      ↓
LLM / Deterministic Interpreter
      ↓
Intent + ExtractedEntities
      ↓
Entity Resolution
      ↓
BookingContext
      ↓
Decision Engine
      ↓
BusinessAction
      ↓
Tool Executor
      ↓
Business Tools / Booking Engine
      ↓
Repositories
      ↓
MongoDB
```

The LLM cannot:

```text
Access MongoDB
Execute bookings directly
Choose arbitrary backend operations
Bypass Tool Executor
Bypass Booking Engine
Persist unvalidated operations
```

LLM support remains disabled by default:

```text
LLM_ENABLED=false
```

The deterministic AI Core therefore remains fully operational without an external model.

### Phase 10 — React Chat Interface & AI Booking Agent Simulation

**In Progress**

The objective is to create the first real user interface for interacting with the existing AI Booking Agent.

The phase deliberately begins with a focused chat experience rather than a large administrative dashboard.

Current progress:

- React 19 + Vite 8 project created
- ESLint configured
- Responsive chat shell implemented
- Message input and Send interaction shell implemented
- FastAPI and React development servers verified
- CORS configured for the local React origin
- Focused backend regression passed
- Frontend environment configuration added
- Local frontend `.env` excluded from Git
- Conversation API client created
- `createConversation()` implemented
- `sendMessage()` implemented
- `getConversationMessages()` implemented
- Frontend lint passes

Current integration target:

```text
User
  ↓
React Chat Interface
  ↓
Create Conversation
  ↓
Send Message
  ↓
FastAPI
  ↓
Conversation System
  ↓
AI Core / LLM Boundary
  ↓
Store Assistant Response
  ↓
Load Conversation History
  ↓
Render Chat Messages
```

Planned Phase 10 expansion:

- Connect `App.jsx` state to the conversation API
- Render user and assistant message bubbles
- Loading state
- Error state
- New Conversation
- Conversation history
- Booking context panel
- Current intent
- Selected service
- Selected staff
- Customer information
- Booking date and time
- Booking status
- Availability results
- Component and interaction testing

React remains a presentation layer.

No booking logic will be duplicated in the frontend.

### Production Engineering

**Planned**

After the conversational interface reaches a stable state:

- Docker
- GitHub Actions
- Continuous Integration
- Security validation
- Logging
- Deployment preparation
- Production configuration
- Frontend production build strategy

---

## Local Development

### Clone

```bash
git clone https://github.com/Danakaabi/ai-booking-agent-.git

cd ai-booking-agent
```

### Create Virtual Environment

```bash
python -m venv .venv

source .venv/bin/activate
```

### Backend Environment

Use the root `.env.example` as the configuration reference.

LLM integration is optional and disabled by default.

Example:

```text
LLM_ENABLED=false
```

A real OpenAI API key must never be committed to Git.

### MongoDB

Verify that MongoDB is available:

```bash
mongosh --eval 'db.runCommand({ ping: 1 })'
```

Expected:

```text
{ ok: 1 }
```

MongoDB must be running before repository and integration tests.

### Run Backend API

From the project root:

```bash
uvicorn api.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

### Run Backend Tests

```bash
python -m pytest -v
```

Latest full regression before Phase 10:

```text
234 passed
0 failures
```

### Frontend Setup

From the project root:

```bash
cd frontend
npm install
```

Create the local frontend environment from the example:

```bash
cp .env.example .env
```

The development configuration currently uses:

```text
VITE_API_BASE_URL=http://127.0.0.1:8000
```

The frontend environment must never contain an OpenAI API key or database credentials.

### Run React Frontend

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
```

During development, both applications run independently:

```text
React
localhost:5173

        ↓ HTTP

FastAPI
127.0.0.1:8000
```

### Frontend Lint

```bash
npm run lint
```

---

## Current Development Focus

```text
Foundation                         ✓
FastAPI + MongoDB                  ✓
Booking System                    ✓
Availability & Scheduling         ✓
Customers & Staff                 ✓
Booking Engine                    ✓
Conversation System               ✓
Intent Detection                  ✓
Entity Extraction & Resolution    ✓
Context Preparation               ✓
Missing Information               ✓
Decision Engine                   ✓
Response Generation               ✓
AI Orchestration                  ✓
Controlled Tool Execution         ✓
AI Business Tools                 ✓
Multi-Turn Availability           ✓
LLM Provider Abstraction          ✓
Structured LLM Output             ✓
OpenAI Provider                   ✓
Deterministic LLM Fallback        ✓
LLM Boundary Tests                ✓
Backend Full Regression           ✓
React Foundation                  ✓
Chat Shell                        ✓
Frontend API Layer                ✓
React → FastAPI Chat Integration  → CURRENT
Chat Message Rendering            → NEXT
Chat UX Expansion                 → LATER
Production Engineering            → LATER
```

The current objective is:

> **Connect the React chat interface to the existing conversation API and complete the first end-to-end AI Booking Agent simulation without duplicating backend business logic.**

---

## Target Application Architecture

```text
User
  ↓
React Chat Interface
  ↓
FastAPI
  ↓
Conversation System
  ↓
Message Interpreter
  ↓
LLM / Deterministic Interpreter
  ↓
AI Core
  ↓
Decision Engine
  ↓
Controlled Business Tools
  ↓
Booking Engine
  ↓
Validation & Scheduling Rules
  ↓
Repositories
  ↓
MongoDB
```

The interpretation layer determines:

- What does the user mean?
- Which entities are present?
- What information is still missing?

The deterministic AI Core determines:

- What is the active workflow?
- Is the context complete?
- Which approved business action is required?
- Should the system ask the user for more information?

The deterministic backend determines:

- Is the operation allowed?
- Does it satisfy booking rules?
- Is the requested time available?
- Does the selected staff member support the service?
- Does the operation conflict with an existing booking?
- How should the operation be executed?

React determines:

- What should be displayed?
- What message did the user enter?
- Is an API request in progress?
- Should a loading or error state be rendered?
- Which conversation history should be shown?

The database persists only validated results.

---

## Why Backend-First?

The project deliberately did not begin with an LLM or frontend.

A booking agent must reliably answer questions such as:

- Does the service exist?
- Does the staff member provide it?
- Is the business open?
- Is the staff member working?
- Does the full service duration fit?
- Does another confirmed booking overlap?
- Can this booking be safely rescheduled?
- Is the conversation context complete?

These decisions should not depend on probabilistic model output or frontend state.

The LLM can therefore operate as an interpretation layer without becoming the authority for booking rules or persistence.

React can operate as a presentation layer without becoming the authority for business logic.

This gives the project a clear separation:

```text
React
      ↓
Presentation

LLM
      ↓
Interpretation

AI Core
      ↓
Decision & Orchestration

Booking Engine
      ↓
Business Rules

Repositories
      ↓
Persistence

MongoDB
      ↓
Stored State
```

---

## Engineering Principles

- Separation of concerns
- Repository pattern
- Centralized booking orchestration
- Dedicated conversation service
- Validation at application boundaries
- Deterministic scheduling
- Conflict-safe booking operations
- Persistent conversation state
- Partial booking-context collection
- Structured AI decisions
- Explicit business-action routing
- Controlled tool execution
- Shared HTTP error mapping
- LLM provider abstraction
- Structured LLM outputs
- Deterministic fallback behavior
- LLM isolation from persistence
- Frontend isolation from business logic
- Dedicated frontend API layer
- Minimal frontend dependencies
- Environment-based configuration
- Responsive design
- Accessibility-conscious UI
- Automated regression testing
- Framework-independent backend business logic
- No direct AI access to MongoDB
- No direct React access to MongoDB
- No direct React access to OpenAI
- No secrets committed to Git

---

## Security Boundaries

The system intentionally separates trust boundaries.

### React

React may:

```text
Send HTTP requests
Render API responses
Maintain UI state
Collect user input
```

React may not:

```text
Access MongoDB
Contain database credentials
Contain OpenAI API keys
Execute Booking Engine logic
Bypass FastAPI
```

### LLM

The LLM may:

```text
Interpret natural language
Produce structured interpretation
```

The LLM may not:

```text
Access MongoDB
Execute repositories
Create bookings directly
Choose arbitrary functions
Bypass deterministic validation
```

### Backend

FastAPI and the deterministic application layers remain responsible for:

```text
Validation
Decision routing
Controlled execution
Booking rules
Conflict detection
Persistence
```

---

## Long-Term Vision

The project is intended to evolve into a reusable AI booking agent for domains such as:

- Salons
- Clinics
- Healthcare scheduling
- Events
- Professional services
- Appointment-based businesses

```text
Web / Mobile / Chat
          ↓
Conversation Interface
          ↓
LLM / Deterministic Interpretation
          ↓
AI Core
          ↓
Business Tools
          ↓
Booking Engine
          ↓
Scheduling
          ↓
MongoDB
```

The same deterministic Booking Engine, conversation infrastructure, AI Core, LLM boundary, and controlled tools can support multiple interfaces without duplicating business rules.

A future administrative dashboard can be added independently from the conversational client.

---

## Project Philosophy

> **AI should interpret the request.**
>
> **Conversation infrastructure should preserve context and state.**
>
> **Deterministic logic should decide what is allowed.**
>
> **Controlled tools should execute approved operations.**
>
> **React should present and interact with the system, not duplicate it.**
>
> **The database should persist only validated results.**

---

<p align="center">
  <strong>AI Booking Agent</strong><br>
  Backend Engineering • Booking Systems • Scheduling • Conversation Systems • LLM Integration • AI Agents • React • System Design
</p>