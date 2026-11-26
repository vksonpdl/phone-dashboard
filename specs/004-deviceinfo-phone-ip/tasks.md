# Tasks: Enhance Device Info with Phone IP

**Input**: Design documents from `/specs/004-deviceinfo-phone-ip/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/device-info.md, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and structure verification

- [x] T001 Verify project structure per implementation plan in `app.py` and `modules/system_info.py`
- [x] T002 [P] Verify Python 3.x and Flask dependencies in development environment

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before user story implementation

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Verify existing blueprint registration and system overview endpoint in `modules/system_info.py`
- [x] T004 [P] Setup unit test suite base structure in `tests/test_system_info.py`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Retrieve Phone IP in Device Info (Priority: P1) 🎯 MVP

**Goal**: Enhance the `/api/system` (deviceinfo) endpoint so that its output includes active local network **Phone IP** addresses (supporting both IPv4 and IPv6 simultaneously, with Wi-Fi interface precedence over Cellular/VPN, and graceful fallback to `N/A` when offline) while maintaining 100% backward compatibility.

**Independent Test**: Invoke `GET /api/system` and verify that the `device` object contains all existing fields plus the `phone_ip` object with `ipv4` and `ipv6` attributes. Test offline fallback by simulating network disconnection.

### Tests for User Story 1 (Optional/TDD)

- [x] T005 [P] [US1] Add unit tests in `tests/test_system_info.py` verifying IPv4 and IPv6 retrieval, loopback exclusion, Wi-Fi interface precedence, and offline `N/A` fallback

### Implementation for User Story 1

- [x] T006 [P] [US1] Implement local network interface enumeration and IP filtering helper in `modules/system_info.py` to exclude loopback (`127.0.0.1`, `::1`) and link-local addresses
- [x] T007 [US1] Implement interface priority logic in `modules/system_info.py` preferring Wi-Fi interfaces over Cellular and VPN
- [x] T008 [US1] Implement dual-stack collection supporting both IPv4 and IPv6 simultaneously in `modules/system_info.py`
- [x] T009 [US1] Enhance `get_device()` function in `modules/system_info.py` to include `phone_ip` with `ipv4` and `ipv6` fields matching existing response structure
- [x] T010 [US1] Add robust try/except error handling in `modules/system_info.py` returning `N/A` when offline, in airplane mode, or lacking permissions

**Checkpoint**: At this point, User Story 1 is fully functional and testable independently

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Cross-cutting improvements and validation

- [x] T011 [P] Run quickstart.md validation steps (`curl http://127.0.0.1:5000/api/system`)
- [x] T012 Run unit test suite (`python -m unittest discover tests`) to confirm 100% test pass rate and zero regressions
- [x] T013 [P] Code cleanup and review against project constitution principles

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS user story work
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion
- **Polish (Phase 4)**: Depends on User Story 1 completion

### Parallel Opportunities

- T002 and T004 can run in parallel during setup/foundational phases
- T005 and T006 can run in parallel prior to service integration

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 & 2 (Setup & Foundational)
2. Complete Phase 3 (User Story 1)
3. **STOP and VALIDATE**: Verify via `quickstart.md` steps and unit tests
