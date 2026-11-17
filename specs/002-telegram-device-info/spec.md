# Feature Specification: Telegram Device Info Command

**Feature Branch**: `specs/002-telegram-device-info`

**Created**: 2026-11-16

**Status**: Draft

**Input**: User description: "enhance the phone-dashboard telegram tool by adding a new command Get Device Info. this should return Battery info, storage Info and Ram info. reuse the existing code as much as possible . do not change any existing logic"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Get Device Info via Telegram Bot (Priority: P1)

As an authorized user interacting with the Telegram bot interface, I want to request device information ("Get Device Info") so that I can conveniently review the current battery status, storage volumes, and RAM usage directly in Telegram.

**Why this priority**: Directly fulfills the user requirement to extend the Telegram tool with comprehensive device metrics while reusing existing system inspection routines.

**Independent Test**: Can be fully tested by sending the "Get Device Info" command/keyboard action to the authorized Telegram bot and verifying that formatted battery, storage, and RAM details are returned correctly.

**Acceptance Scenarios**:

1. **Given** an authorized user taps or sends "Get Device Info", **When** the command is processed, **Then** the bot retrieves and formats current battery metrics (level, status, temperature, voltage, health), storage volumes (internal storage, system data, SD card if available), and RAM usage (total, used, available, percentage).
2. **Given** an unauthorized user attempts to request device info, **When** the message is received, **Then** the bot rejects or ignores the request based on existing security authorization logic (`ALLOWED_USER_ID`).

---

### Edge Cases

- What happens when system hardware data files (`/proc/meminfo`, `/sys/class/power_supply`) or disk usage queries encounter errors or missing paths? The underlying functions fall back gracefully, returning default or safe values without crashing the bot handler.
- What happens if the Telegram request times out or encounters network issues? Exception handling catches the error and reports a clean failure message to the user chat.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The Telegram bot interface MUST include a new menu keyboard button and text command option for "Get Device Info".
- **FR-002**: Selecting "Get Device Info" MUST aggregate battery metrics, storage volume usage, and RAM consumption by reusing the existing helper functions from the system information domain (`modules/system_info.py`).
- **FR-003**: The returned device info response MUST be formatted clearly in Markdown for optimal readability within Telegram clients.
- **FR-004**: Authorization checks (`is_authorized`) MUST be strictly enforced for the new "Get Device Info" command.
- **FR-005**: The enhancement MUST NOT modify existing system logic or break existing Telegram commands ("Start Torrent Download", "Get Torrents Status", "Delete Torrent").

### Key Entities *(include if feature involves data)*

- **Telegram Bot Handler (`modules/telegram_bot.py`)**: Manages incoming messages, keyboard layouts, and bot responses.
- **System Info Providers (`modules/system_info.py`)**: Reusable data-gathering functions (`get_battery()`, `get_storage()`, `get_ram()`).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Authorized users receive complete and formatted battery, storage, and RAM details within 2 seconds of invoking "Get Device Info".
- **SC-002**: 100% of existing Telegram bot commands and torrent management flows remain fully operational without regression.
- **SC-003**: Code reuse exceeds 90% by directly leveraging existing logic from `modules/system_info.py`.

## Assumptions

- Reusing functions from `modules/system_info.py` inside `modules/telegram_bot.py` is structurally clean and avoids code duplication.
- Telegram message output formatting complies with Markdown parser requirements supported by `telebot`.
