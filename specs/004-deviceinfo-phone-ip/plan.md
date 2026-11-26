# Implementation Plan: Enhance Device Info with Phone IP

**Branch**: `004-deviceinfo-phone-ip` | **Date**: 2026-11-26 | **Spec**: [specs/004-deviceinfo-phone-ip/spec.md](spec.md)

**Input**: Feature specification and clarifications from `/specs/004-deviceinfo-phone-ip/spec.md`

## Summary

Enhance the existing `/api/system` (deviceinfo) endpoint in `modules/system_info.py` to include local network **Phone IP** addresses (supporting both IPv4 and IPv6 simultaneously, with Wi-Fi preferred over Cellular/VPN, and graceful fallback to `N/A` or `Unavailable` when offline or restricted). Maintain 100% backward compatibility with all existing device info fields.

## Technical Context

**Language/Version**: Python 3.x

**Primary Dependencies**: Flask, Python Standard Library (`socket`, `subprocess`, `os`, `netifaces` or socket interface enumeration)

**Storage**: N/A (Runtime system inspection)

**Testing**: Python `unittest` / Flask test client

**Target Platform**: Android / Linux mobile device environment with cross-platform fallback handling

**Project Type**: Web application (Flask backend + Vanilla HTML/CSS frontend)

**Performance Goals**: API response time < 50ms for local IP resolution

**Constraints**: Modular Blueprint architecture, Lightweight Vanilla Frontend, Robust Error Resilience & Fallbacks, Minimalist Dependency Policy (no new third-party dependencies).

**Scale/Scope**: Local device interface inspection

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Modular Blueprint Architecture**: PASS. Implemented within existing `modules/system_info.py` Flask Blueprint.
- **Lightweight Vanilla Frontend**: PASS. Clean REST JSON API consumed by existing Vanilla frontend.
- **Robust Error Resilience & Fallbacks**: PASS. Comprehensive try/except blocks around network interface enumeration returning graceful fallback (`N/A`) when offline or lacking permissions.
- **Minimalist Dependency Policy**: PASS. Uses Python standard library (`socket`, `subprocess`, etc.) with zero new third-party packages.
- **Simplicity & Maintainability**: PASS. Clean, concise, and focused strictly on the feature requirements.

## Project Structure

### Documentation (this feature)

```text
specs/004-deviceinfo-phone-ip/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── device-info.md
└── tasks.md             # Phase 2 output (created later via /speckit.tasks)
```

### Source Code (repository root)

```text
modules/
└── system_info.py       # Updated to include local Phone IP resolution (IPv4 & IPv6, Wi-Fi priority)

tests/
└── test_system_info.py  # Unit tests for IP retrieval, dual-stack support, and fallback behavior
```

**Structure Decision**: Extends existing Flask blueprint `modules/system_info.py`.
