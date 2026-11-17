# Quickstart: Telegram Device Info Validation

## Prerequisites
- Python 3.x installed.
- Environment variables configured (`BOT_TOKEN`, `ALLOWED_USER_ID`, `DOWNLOAD_DIR`, `TRANSMISSION_REMOTE`).

## Running Validation
1. Start the Flask application:
   ```bash
   python app.py
   ```
2. Open Telegram and interact with the configured bot.
3. Send `/start` or `/deviceinfo`, or tap the "Get Device Info" button on the reply keyboard.
4. Verify that the bot responds with formatted Battery, Storage, and RAM details matching the contract schema.
