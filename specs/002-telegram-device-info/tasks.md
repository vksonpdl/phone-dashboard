---
description: "Task list for Telegram Device Info feature implementation"
---

# Tasks: Telegram Device Info Command

**Input**: Design documents from `/specs/002-telegram-device-info/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/device-info-bot.md, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1)
- Exact file paths included in descriptions.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project environment and codebase verification

- [x] T001 Verify existing repository structure and python environment readiness

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure prerequisites

- [x] T002 Verify Flask application (`app.py`) and Telegram blueprint (`modules/telegram_bot.py`) import successfully

---

## Phase 3: User Story 1 - Get Device Info via Telegram Bot (Priority: P1) 🎯 MVP

**Goal**: Extend the Telegram bot interface with a "Get Device Info" command and button that aggregates battery, storage, and RAM info.

**Independent Test**: Send `/deviceinfo` or tap "Get Device Info" in Telegram and verify formatted system metrics are received.

### Implementation for User Story 1

- [x] T003 [US1] Import `get_battery`, `get_storage`, and `get_ram` from `modules.system_info` in `modules/telegram_bot.py`
- [x] T004 [US1] Implement device info formatting helper function in `modules/telegram_bot.py` to construct structured Markdown output for battery, storage, and RAM data
- [x] T005 [US1] Add "Get Device Info" button to `main_menu_keyboard()` in `modules/telegram_bot.py`
- [x] T006 [US1] Implement `@bot.message_handler(commands=["deviceinfo"])` and text handler for `"Get Device Info"` with `is_authorized` check in `modules/telegram_bot.py`
- [x] T007 [US1] Register `deviceinfo` command in `set_my_commands` within `handle_start` in `modules/telegram_bot.py`

**Checkpoint**: User Story 1 is fully functional and testable independently.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Validation and cross-cutting checks

- [x] T008 Run quickstart.md validation steps and verify all existing Telegram commands and REST endpoints remain fully operational without regression

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup
- **User Story 1 (Phase 3)**: Depends on Foundational phase
- **Polish (Phase 4)**: Depends on User Story 1 completion

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 & 2 Setup/Foundational
2. Complete Phase 3: User Story 1 tasks
3. Validate via quickstart.md
