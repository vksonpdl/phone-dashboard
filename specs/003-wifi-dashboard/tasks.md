# Tasks: Expose Wi-Fi Dashboard in Patoli MotoHub Dashboard

**Input**: Design documents from `/specs/003-wifi-dashboard/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Optional (manual verification and quickstart validation guide).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Exact file paths are included in all task descriptions

## Path Conventions

- Flask backend blueprint: `modules/wifi.py`
- Application entry: `app.py`
- Frontend UI: `static/index.html`
- Frontend CSS: `static/style.css`
- Feature specifications: `specs/003-wifi-dashboard/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Initialize Wi-Fi blueprint module skeleton with route prefix `/api/wifi` in modules/wifi.py
- [ ] T002 Verify blueprint auto-registration via app.py by starting Flask server

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T003 Implement helper utility for running shell commands and reading system files with robust try/except exception handling and fallback values in modules/wifi.py
- [ ] T004 Define fallback and default Wi-Fi data structures per data-model.md in modules/wifi.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - View Active Wi-Fi Connection Details (Priority: P1) 🎯 MVP

**Goal**: Retrieve and display baseline details of the mobile device's currently connected Wi-Fi network (SSID, signal strength/RSSI, IP address, gateway, frequency band, link speed, and connection duration) with graceful disconnected fallback.

**Independent Test**: Navigate to `/api/wifi` and verify that active Wi-Fi connection parameters and duration are accurately returned as JSON.

### Implementation for User Story 1

- [ ] T005 [P] [US1] Implement active Wi-Fi connection details detection (SSID, RSSI, IP, gateway, frequency band, link speed, connection duration) using system commands and OS interface reads in modules/wifi.py
- [ ] T006 [US1] Expose GET /api/wifi endpoint returning active Wi-Fi network payload in modules/wifi.py
- [ ] T007 [P] [US1] Create active Wi-Fi network status card UI in static/index.html
- [ ] T008 [US1] Add active Wi-Fi data loader logic in static/index.html

**Checkpoint**: At this point, User Story 1 is fully functional and delivers an MVP for monitoring host Wi-Fi status.

---

## Phase 4: User Story 2 - Discover and View Connected Network Devices (Priority: P2)

**Goal**: Discover and list peer devices connected to the same Wi-Fi network, displaying their device identifiers (Hostname, IP Address, MAC Address) and connection durations.

**Independent Test**: Load the Wi-Fi Dashboard and verify that discovered peer devices on the local network are rendered with hostname, IP, MAC, and connection duration.

### Implementation for User Story 2

- [ ] T009 [P] [US2] Implement peer device discovery parser reading `/proc/net/arp` and `ip neigh` with hostname resolution in modules/wifi.py
- [ ] T010 [US2] Integrate discovered device list with connection duration tracking into GET /api/wifi endpoint in modules/wifi.py
- [ ] T011 [P] [US2] Add Connected Devices table markup in static/index.html
- [ ] T012 [US2] Implement peer devices rendering and empty-state handling in static/index.html
- [ ] T013 [P] [US2] Add CSS styling for Connected Devices table and status badges in static/style.css

**Checkpoint**: At this point, User Stories 1 and 2 are functional, providing both active Wi-Fi details and local network peer auditing.

---

## Phase 5: User Story 3 - Dashboard Navigation & Refresh Controls Integration (Priority: P3)

**Goal**: Seamlessly integrate the Wi-Fi Dashboard into the main navigation bar and connect to auto-refresh polling and manual reload controls without resetting active timers.

**Independent Test**: Click between dashboard navigation tabs, toggle auto-refresh intervals, and click "Refresh Now" (`↻`) to confirm data reloads smoothly.

### Implementation for User Story 3

- [ ] T014 [US3] Add "Wi-Fi Dashboard" navigation tab button to `<nav class="tabs">` in static/index.html
- [ ] T015 [US3] Register `wifi` tab loader into `TAB_LOADERS` dictionary in static/index.html
- [ ] T016 [US3] Connect Wi-Fi loader to auto-refresh interval select and manual Refresh Now button in static/index.html

**Checkpoint**: All three user stories are integrated and fully operational with the dashboard UI and controls.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Verification and final quality hardening

- [ ] T017 Verify error resilience and fallback states when Wi-Fi is disconnected in modules/wifi.py and static/index.html
- [ ] T018 Execute validation steps defined in specs/003-wifi-dashboard/quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - Sequential delivery in priority order: P1 → P2 → P3
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Extends backend endpoint from US1 with `devices` array - independently testable
- **User Story 3 (P3)**: Ties UI together with navigation tabs and refresh controls

---

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Complete Phase 1: Setup (`modules/wifi.py` skeleton)
2. Complete Phase 2: Foundational (helper utilities and fallback models)
3. Complete Phase 3: User Story 1 (Active Wi-Fi info retrieval + basic UI card)
4. Validate User Story 1 independently via `/api/wifi` and browser

### Incremental Delivery
1. Add User Story 2 (Peer device discovery via ARP/neighbor table)
2. Add User Story 3 (Navigation tab and refresh controls hookup)
3. Run end-to-end quickstart validation
