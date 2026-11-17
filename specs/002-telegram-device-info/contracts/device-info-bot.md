# Interface Contract: Telegram Device Info Bot Command

## Commands & Keyboard
- **Telegram Command**: `/deviceinfo`
- **Reply Keyboard Button**: `"Get Device Info"`
- **Authorization**: Requires `is_authorized(message)` (validates `ALLOWED_USER_ID`).

## Response Format (Markdown)
```markdown
📱 *Device Status & Info*

🔋 *Battery:*
• Level: *85%* (Charging)
• Temp: `32.5°C` | Voltage: `3.85V`
• Health: Good

💾 *Storage:*
• *Internal Storage*: 50.0 GB total / 30.0 GB used (60.0%)
• *System Data*: 10.0 GB total / 4.0 GB used (40.0%)

🧠 *RAM:*
• Total: `8.0 GB` | Used: `4.5 GB` (56.2%)
• Available: `3.5 GB`
```
