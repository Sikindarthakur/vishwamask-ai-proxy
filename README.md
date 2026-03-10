# Vishwa-Mask Privacy Proxy

## Problem Statement

Many AI applications send user prompts directly to cloud-based
LLM providers such as OpenAI or Anthropic.

These prompts often contain Personally Identifiable Information (PII)
such as names, phone numbers, Aadhaar numbers, or PAN numbers.

Under India's Digital Personal Data Protection (DPDP) Act 2023,
organizations must ensure that personal data is protected and
handled responsibly.

Sending raw prompts containing PII to foreign AI servers
creates legal and privacy risks for Indian companies.

## Proposed Solution

Vishwa-Mask is a privacy-preserving proxy that sits between
applications and external AI services.

The system detects sensitive personal data in prompts,
replaces it with masked placeholders before sending the request
to a cloud AI provider, and restores the original data in
the final response.

This ensures that sensitive data never leaves the local environment.

## Tech Stack

Python
FastAPI
Presidio (PII Detection)
Docker

## AI Assistance

Parts of the project structure and development guidance
were generated with assistance from AI tools such as
ChatGPT and Cursor.

All code has been reviewed and modified by the developer.
