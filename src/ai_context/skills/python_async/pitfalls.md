# Python Async Pitfalls

- Fire-and-forget tasks can hide exceptions and leak resources.
- Shared mutable state across coroutines causes race conditions.
- Unbounded gather() calls can overload external services.
