# Telegram Bot Rules

- Keep bot handlers idempotent and safe for retries.
- Validate incoming update payloads before processing.
- Separate transport concerns (Telegram API) from domain logic.
- Log failed Telegram API calls with request context.
