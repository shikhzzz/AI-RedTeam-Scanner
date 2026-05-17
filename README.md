# AI Red Team Scanner

An automated prompt injection vulnerability scanner for LLM-powered applications.

## What it does
- Fires a library of adversarial prompts at an LLM application
- Detects signs of successful prompt injection
- Generates a structured vulnerability report

## Why this matters
Prompt injection is the #1 vulnerability in LLM applications (OWASP Top 10 for LLMs).
This tool automates what a security researcher would do manually — systematically 
probing an AI system for weaknesses and documenting findings.

## Tech stack
- Python
- Groq API (LLaMA 3)
- Docker

## Current findings (manual testing)
- System prompt override: CRITICAL ✅
- System prompt extraction via social engineering: CRITICAL ✅

## Status
🚧 Week 1 — manual testing complete. Automation in progress.
