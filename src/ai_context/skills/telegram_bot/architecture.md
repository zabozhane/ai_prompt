# Telegram Bot Architecture

- Use a thin Telegram adapter layer for polling/webhook updates.
- Route parsed updates into explicit application use-cases.
- Keep command handlers small and side-effect aware.
