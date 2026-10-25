## Retries

The client retries a request when the server returns 503 or the connection drops.
Each retry waits twice as long as the previous one, starting at 100 ms and capped at 5 s.
The client gives up after 6 attempts and returns the last error to the caller.
Retries apply only to idempotent requests, such as GET and PUT.
For a POST, the client returns the error immediately, because sending it twice could create two records.
You can change the limits with the `retry.max_attempts` and `retry.max_backoff` settings.
Set `retry.max_attempts` to 1 to turn retries off.
The rate limiter knows when the server is overloaded and holds requests until the server recovers.
The retry budget exhaustion alert threshold controls when the on-call engineer is paged.
The metrics endpoint reports the number of retries per minute, so you can see whether the limits you chose fit your traffic.
