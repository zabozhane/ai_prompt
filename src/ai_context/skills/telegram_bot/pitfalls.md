# Telegram Bot Pitfalls

- Mixing long-running work directly in update handlers blocks responsiveness.
- Ignoring rate limits can get bot requests throttled.
- Relying on mutable in-memory session state breaks after restarts.
