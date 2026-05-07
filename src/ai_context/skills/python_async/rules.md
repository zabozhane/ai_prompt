# Python Async Rules

- Never block the event loop with sync I/O in coroutine paths.
- Bound concurrency with semaphores or worker pools.
- Propagate cancellation and timeouts intentionally.
- Use structured retries with jitter for flaky network calls.
