# credential-leak-demo

This package is intentionally designed for a safe local lab.

It reads only demo-prefixed environment variables and writes a redacted
"exfiltration attempt" record to a local sink file so defenders can
demonstrate the attack chain without stealing real credentials.
