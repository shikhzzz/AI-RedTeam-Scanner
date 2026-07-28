# AI Red Team Scanner 

An automated prompt injection vulnerability scanner for LLM-powered applications.
Built to demonstrate how AI systems can be systematically tested for security weaknesses
— the same way a penetration tester would approach a web application.

---

## What is prompt injection?

Prompt injection is the #1 vulnerability in LLM applications (OWASP Top 10 for LLMs).
It happens when an attacker crafts inputs that cause an AI model to ignore its 
instructions and behave in unintended ways — revealing secrets, abandoning its 
role, or bypassing restrictions.

This tool automates that attack process.

---

## What this scanner does

- Fires a library of adversarial payloads at a target LLM
- Detects signs of successful prompt injection in responses
- Flags vulnerabilities with severity ratings
- Saves a structured JSON report of all findings
- Containerised with Docker — runs anywhere in one command

---

## Key findings from testing

Tested against Meta's LLaMA 3.3 70B model deployed on Groq:

| Attack Type | Payload | Result |
|---|---|---|
| Role
