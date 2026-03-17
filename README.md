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

- Python
- FastAPI
- Presidio (PII Detection)
- Docker

## AI Assistance

Parts of the project structure and development guidance
were generated with assistance from AI tools such as
ChatGPT and Cursor.

All code has been reviewed and modified by the developer.

## 🧩 Phase 1: PII Detection & Masking Engine

This phase focuses on building the core privacy engine capable of detecting and masking sensitive Indian data.

### ✅ Supported Entities

- 👤 Person Names
- 📱 Indian Mobile Numbers (+91 format)
- 🆔 Aadhaar Numbers
- 🪪 PAN Cards

### 🔐 Masking Method

- Deterministic Token Replacement (e.g., Rahul → [PERSON_1])
- Ensures consistency across multiple occurrences
- Fully reversible using `PIIVault`

### 🔁 Reversible Privacy Vault

- Maintains mapping:
  - Original → Token
  - Token → Original
- Enables safe round-trip AI communication

### 🧪 Testing & Validation

- Automated tests using `pytest`
- Total Tests: **5**
- Passed: **5**
- Reliability: **100%**

### 🎯 Outcome

A fully functional PII detection and masking engine tailored for Indian data formats, forming the foundation for a privacy-first AI proxy.

## 🔁 Phase 2: Proxy Middleware & AI Integration

In this phase, the project evolved from a standalone masking tool into a full privacy-preserving AI proxy.

### ✅ Features Implemented

- 🌐 FastAPI-based backend API
- 🔐 `/mask-prompt` endpoint for raw masking
- 🤖 `/chat` endpoint for full proxy flow:
  - Mask → Send to AI → Receive → Unmask
- 🔄 Deterministic masking using PIIVault
- ⚡ Latency tracking for each request

### 🤖 Multi-Provider Support

- 🖥️ Ollama (Local LLM for full privacy)
- ☁️ OpenAI (Cloud-based inference)
- 🌟 Gemini (Google AI integration)

Users can dynamically choose the provider via API.

### 🔄 Full Round-Trip Flow

```text
User Input → Masking → AI Processing → Unmasking → Final Response

## 🚀 Phase 3: Real-time Audit & Persistence

To enhance compliance and observability, Vishwa-Mask now includes a real-time audit logging system.

### ✅ Features Implemented

- 📦 SQLite Database Integration (`audit_logs.db`)
- 📝 Automatic logging of each PII detection event
- ⚡ Latency tracking for every request
- 📊 Streamlit dashboard connected to live data
- 🔍 Real-time protection logs display
- 🧠 Risk Mitigation Factor (RMF) calculation

### 🔐 Privacy-first Design

- No raw sensitive data is stored
- Only metadata is logged:
  - Entity Type (e.g., Aadhaar, Phone)
  - Provider used (Ollama / Gemini / OpenAI)
  - Latency
  - Timestamp

This ensures compliance with **India's DPDP Act 2023** principles of data minimization and privacy-by-design.

### 📊 Dashboard Insights

- Total prompts processed
- Total PII entities protected
- Average latency
- Protection Ratio
- Risk Mitigation Factor (RMF)
- Real-time logs (latest entries)
