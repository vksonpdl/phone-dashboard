# Feature Specification: Baseline Architectural Specification

**Feature Branch**: `specs/001-baseline-architecture-spec`

**Created**: 2026-11-16

**Status**: Approved (Frozen Contract)

**Input**: User description: "Analyze this existing repository to generate a baseline architectural specification. Create a spec.md that documents the current system state, specifically covering: 1. Core frameworks and primary dependencies. 2. Data access, state management, and persistence patterns. 3. API, routing, or entry-point structures. 4. Security, authentication, and authorization mechanisms. 5. Standard error handling and logging patterns. Treat this output as a "frozen contract" of the current architecture. Do not invent, refactor, or propose new features. Document exactly how the system operates today to establish a baseline context for future AI code generation."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - System Architectural Documentation & Baseline Verification (Priority: P1)

As a developer or AI assistant, I want a comprehensive and frozen baseline specification of the existing system architecture so that future modifications, feature additions, and maintenance strictly adhere to established patterns without regressions or architectural drift.

**Why this priority**: Establishes the authoritative contract for the codebase, ensuring compliance with existing frameworks, dependency models, and security boundaries.

**Independent Test**: Can be fully verified by reviewing `spec.md` against the repository source code (`app.py`, `modules/`, `static/`) to confirm 100% fidelity with core frameworks, routing structures, and error handling patterns.

**Acceptance Scenarios**:

1. **Given** the repository contains Flask backend modules and static frontend assets, **When** the architecture specification is inspected, **Then** core frameworks (Python 3, Flask, Telebot) and dependencies are accurately documented.
2. **Given** system operations interact with local OS files and CLI binaries (`transmission-remote`, `getprop`), **When** data access patterns are examined, **Then** direct process execution and file read patterns are explicitly detailed.

---

### Edge Cases

- What happens when external binaries (`transmission-remote`, `getprop`) or system paths (`/proc/meminfo`, `/sys/class/power_supply`) are missing or inaccessible? The system catches exceptions and returns graceful fallback JSON responses or default values.
- What happens when unauthorized Telegram users send messages or commands to the bot? The bot verifies `ALLOWED_USER_ID` and silently ignores or rejects unauthorized requests.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST use Python 3.x and Flask as the primary web application framework and WSGI server.
- **FR-002**: The application MUST automatically discover and register all non-private Python modules in the `modules/` directory as Flask Blueprints on startup.
- **FR-003**: The system MUST expose RESTful JSON API endpoints grouped by domain prefixes (`/api/system`, `/api/telegram`, `/api/torrents`) and serve static frontend files (`index.html`, `style.css`) from the root route (`/`).
- **FR-004**: Data access and state management MUST be stateless or rely on direct interrogation of OS system files (`/proc/*`, `/sys/*`) and CLI utilities (`getprop`, `transmission-remote`) via synchronous subprocess execution.
- **FR-005**: Security and authorization for the Telegram bot interface MUST enforce strict user validation against a configured numeric `ALLOWED_USER_ID` environment variable.
- **FR-006**: Error handling across backend modules MUST catch subprocess errors (`FileNotFoundError`, `TimeoutExpired`, non-zero return codes) and standard I/O exceptions, returning structured JSON error responses or graceful text messages.
- **FR-007**: Primary dependencies MUST be strictly restricted to Python standard library modules, Flask, and `pyTelegramBotAPI` (`telebot`).

### Key Entities *(include if feature involves data)*

- **Flask Application (`app.py`)**: Central entry point and blueprint router.
- **Module Blueprints (`modules/*.py`)**: Domain-specific API controllers and business logic handlers (System Info, Telegram Bot, Torrents).
- **Static Assets (`static/`)**: Single-page frontend dashboard interface (`index.html`, `style.css`).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of existing core frameworks, dependencies, routing structures, and security patterns are documented without introducing new features or architectural modifications.
- **SC-002**: All 5 requested architectural domains (Frameworks/Dependencies, Data Access/Persistence, API Routing, Security/Authorization, and Error Handling/Logging) are exhaustively defined.
- **SC-003**: The specification serves as a reliable, frozen baseline contract for subsequent AI code generation and automated Spec Kit workflows.

## Assumptions

- Target deployment environment includes Termux / Android OS or Linux-based environments where `getprop`, `/proc`, and `transmission-remote` paths are standard.
- Environment variables (`BOT_TOKEN`, `ALLOWED_USER_ID`, `DOWNLOAD_DIR`, `TRANSMISSION_REMOTE`) are supplied at runtime for the Telegram bot module.
- Frontend communicates exclusively via HTTP REST endpoints against Flask blueprints.
