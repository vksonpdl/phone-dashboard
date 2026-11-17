<!--
Sync Impact Report:
- Version change: Initial Ratification (v1.0.0)
- Modified principles: N/A (Initial creation from template)
- Added sections: Core Principles (I. Modular Blueprint Architecture, II. Lightweight Vanilla Frontend, III. Robust Error Resilience, IV. Minimalist Dependencies, V. Simplicity & Maintainability), Technology & Architecture Constraints, Development Workflow, Governance.
- Removed sections: Template placeholder sections replaced with concrete project policies.
- Follow-up TODOs: None
-->

# Phone Dashboard Constitution

## Core Principles

### I. Modular Blueprint Architecture
Every backend feature or domain (e.g., system info, telegram bot, torrents) is encapsulated as a standalone Flask Blueprint within the `modules/` directory. The main application (`app.py`) automatically discovers and registers all valid non-private module blueprints on startup. Modules must be self-contained and independently maintainable.

### II. Lightweight Vanilla Frontend
The user interface resides in the `static/` directory (`index.html`, `style.css`), communicating via clean RESTful JSON endpoints provided by Flask blueprints. Avoid heavy frontend build tools, complex UI frameworks, or unnecessary asset pipelines unless explicitly required by feature specifications.

### III. Robust Error Resilience & Fallbacks
Because the application runs in various environments (including non-Android or resource-restricted execution contexts), all hardware, OS-specific calls (`getprop`, `/proc`, `/sys/class`), and external tool integrations must implement robust exception handling and fallback responses (e.g., returning default or safe values when system files or binaries are unavailable).

### IV. Minimalist Dependency Policy
Rely strictly on the Python standard library and Flask. Do not introduce alternative libraries, bloated third-party packages, or alternative frameworks without explicit project justification. Package hierarchy and language version must remain strictly aligned with existing project conventions.

### V. Simplicity & Maintainability
Adhere strictly to YAGNI ("You Aren't Gonna Need It"). Keep code concise, readable, and tightly focused on core functionality. Do not modify unrelated classes, introduce speculative abstractions, or rewrite working legacy code.

## Technology & Architecture Constraints

- **Language & Runtime**: Python 3.x.
- **Framework**: Flask (lightweight WSGI web framework).
- **Architecture**: Modular Blueprint pattern (`modules/*.py` auto-discovered by `app.py`).
- **Frontend**: Plain HTML (`static/index.html`) and Vanilla CSS (`static/style.css`).
- **External Interfaces**: REST JSON APIs over HTTP, supporting standard system/device interactions and helper utilities.

## Development Workflow & Conventions

- **Codebase Adoption**: Inspect existing codebase and adopt its current architecture, conventions, and style.
- **Alignment**: Keep language version, build tool, package hierarchy, and testing framework strictly aligned with what is already present in this repo.
- **Non-Regression**: Do not introduce alternative libraries, modify unrelated classes, or rewrite working legacy code.
- **Verification**: Ensure all additions integrate cleanly with the existing auto-discovery mechanism and follow established error-handling patterns.

## Governance

- **Supremacy**: This constitution supersedes all other informal practices and development habits within the project.
- **Amendments**: Amendments require documented rationale, semantic version increments, and impact analysis via Sync Impact Reports.
- **Compliance Review**: All code contributions, reviews, and architectural changes must verify compliance with these core principles and constraints.

**Version**: 1.0.0 | **Ratified**: 2026-11-16 | **Last Amended**: 2026-11-16
