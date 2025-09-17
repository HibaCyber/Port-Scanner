Python Port Scanner (Educational)

A simple Python Port Scanner that uses the built-in socket library to probe TCP ports on a target host and list open ports. This tool is ideal for learning networking fundamentals — how sockets connect, how timeouts and errors are handled, and how to interpret results. It is intentionally lightweight and suitable for use on local test environments.

Important — For educational use only.
Use this scanner only on systems you own or on targets for which you have explicit, written permission to test. Unauthorized scanning may be illegal and may trigger defensive measures.

*Features*

Scans a specified range of TCP ports (default: 1–1024; can be extended up to 1–65535).
Uses Python's built-in socket library — no external dependencies required.
Configurable timeout and rate (delay) between connection attempts to avoid overloading targets.
Option to scan a single port, a range, or a list of common ports.
Prints open ports to the console and can optionally export results to CSV/JSON.
Educational logging: shows attempts, connection times, and basic error handling.

*Design Principles*

Non-destructive: only attempts to open TCP connections (no payloads, no exploitation).
Safe-by-default: conservative timeouts and optional rate-limiting.
Transparent: logs each attempt and result so learners can follow what's happening.
Responsible: explicit reminder to get permission and to test in controlled environments.
