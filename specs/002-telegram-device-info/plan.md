# Implementation Plan - Telegram Device Info Command

**Branch**: `specs/002-telegram-device-info` | **Date**: 2026-11-16 | **Status**: Approved

## Technical Context

- **Language / Version**: Python 3.x
- **Framework**: Flask (Web framework), `telebot` (Telegram Bot API)
- **Architecture**: Modular Flask Blueprint pattern (`modules/telegram_bot.py`, `modules/system_info.py`)
- **Data Access**: Subprocess execution (`getprop`, `transmission-remote`) and local file reads (`/proc/meminfo`, `/sys/class/power_supply`)
- **Dependencies**: Python standard library, Flask, telebot

## Constitution Check

- **Modular Blueprint Architecture**: Fully respected; extending `modules/telegram_bot.py` and reusing helpers from `modules/system_info.py`.
- **Zero-Bloot Lightweight Frontend / Minimalist Dependency Policy**: Maintained; no new external dependencies introduced.
- **Robust Error Resilience & Fallbacks**: Maintained; utilizing existing exception handling patterns in system info helpers.
- **Simplicity & Maintainability**: Maintained; YAGNI applied, no unrelated code modified.

## Phase 0: Research & Unknowns Resolution

- **Unknown 1**: How to import `get_battery`, `get_storage`, and `get_ram` from `modules.system_info` without circular imports or initialization issues?
  - *Resolution*: Import them locally inside the telegram bot formatting function or import cleanly at the module level since `system_info` does not import `telegram_bot`.

## Phase 1: Design & Contracts

- **Data Model (`data-model.md`)**: Documents the device info data structure aggregated for Telegram display.
- **Interface Contracts (`contracts/device-info-bot.md`)**: Specifies the Telegram bot command (`/deviceinfo`), keyboard button ("Get Device Info"), and formatted Markdown response structure.
- **Quickstart (`quickstart.md`)**: End-to-end verification steps for testing the new command.
