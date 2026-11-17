# Research: Telegram Device Info Command

## Decision 1: Reusing System Info Logic
- **Decision**: Import `get_battery`, `get_storage`, and `get_ram` directly from `modules.system_info`.
- **Rationale**: Avoids duplication of hardware and OS interrogation logic (`/proc/meminfo`, `/sys/class/power_supply`, `getprop`, `shutil.disk_usage`), ensuring 100% code reuse and consistency with REST API endpoints.
- **Alternatives Considered**: Duplicating inspection functions inside `telegram_bot.py` (Rejected due to maintenance overhead and DRY principle violation).

## Decision 2: Telegram Bot Interface Integration
- **Decision**: Add "Get Device Info" button to `main_menu_keyboard()`, register `/deviceinfo` command handler, and update `set_my_commands()` in `handle_start`.
- **Rationale**: Aligns seamlessly with existing bot interaction patterns and user menu expectations.
