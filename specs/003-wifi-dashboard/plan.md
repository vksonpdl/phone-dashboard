# Implementation Plan: Expose Wi-Fi Dashboard in Patoli MotoHub Dashboard

**Branch**: `003-wifi-dashboard` | **Date**: 2026-11-20 | **Spec**: [specs/003-wifi-dashboard/spec.md](spec.md)

**Input**: Feature specification from `/specs/003-wifi-dashboard/spec.md`

## Summary

Expose a new **Wi-Fi Dashboard** navigation tab within the Patoli MotoHub Dashboard. The backend will consist of a new Flask Blueprint (`modules/wifi.py`) that queries active Wi-Fi connection details (SSID, RSSI/signal strength, IP, gateway, frequency band, link speed) and discovers connected peer devices on the local network (via `/proc/net/arp`, `ip neigh`, or network tools with robust fallbacks). The frontend (`static/index.html`, `static/style.css`) will integrate the new tab button, metric cards, peer device table, and tie into the existing auto-refresh polling and manual "Refresh Now" mechanisms.

## Technical Context

**Language/Version**: Python 3.x

**Primary Dependencies**: Flask, Python Standard Library (`subprocess`, `os`, `socket`, `re`)

**Storage**: N/A (Runtime OS system files and command execution)

**Testing**: Python `unittest` / Flask test client

**Target Platform**: Android / Linux mobile device environment with cross-platform fallback handling

**Project Type**: Web application (Flask backend + Vanilla HTML/CSS frontend)

**Performance Goals**: API response time < 500ms; frontend render < 2s

**Constraints**: Strict adherence to Modular Blueprint architecture, Lightweight Vanilla Frontend, and Robust Error Resilience. Zero new external dependencies.

**Scale/Scope**: Local network device discovery (typically 1-50 connected devices on residential/local Wi-Fi)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Modular Blueprint Architecture**: PASS. Implemented as a standalone Flask Blueprint (`modules/wifi.py`) registered via auto-discovery in `app.py`.
- **Lightweight Vanilla Frontend**: PASS. Pure HTML (`static/index.html`) and Vanilla CSS (`static/style.css`) with native fetch API integration.
- **Robust Error Resilience & Fallbacks**: PASS. All OS command executions and file reads (`/proc/net/arp`) include try/except blocks returning graceful fallback values.
- **Minimalist Dependency Policy**: PASS. Zero new third-party dependencies introduced (uses Flask and Python standard library).
- **Simplicity & Maintainability**: PASS. Clean, concise, and tightly focused on core functionality.

## Project Structure

### Documentation (this feature)

```text
specs/003-wifi-dashboard/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── wifi-dashboard.md
└── tasks.md             # Phase 2 output (created later via /speckit.tasks)
```

### Source Code (repository root)

```text
app.py                   # Main Flask application with blueprint auto-discovery
modules/
├── __init__.py
├── system_info.py
├── telegram_bot.py
├── torrents.py
└── wifi.py              # New Wi-Fi module blueprint

static/
├── index.html           # Updated with Wi-Fi Dashboard tab & UI cards
└── style.css            # Updated with styles for Wi-Fi network & device table
```

**Structure Decision**: Web application structure extending existing Flask blueprints in `modules/` and frontend files in `static/`.
