# IMPORTANT!!
- This file is outdated
- This code is extensively interconnected
- !This code is NOT ready for use!
- some of the code has documentation and docstrings to help implement it but not all.
# Primary Directives Application

  
This application implements a Flask-based API designed to process requests, enforce rules, and manage data corrections. It incorporates features like database interaction, model loading, system metrics, and error handling.

## Key Features

-   API endpoints for health checks, request processing, metrics, and data correction.
-   Rule enforcement using a complex rule checking module.
-   Database operations for storing and retrieving data corrections and law summaries.
-   Model loading and integrity verification.
-   System metrics collection and exposure via Prometheus.
-   Configuration management using pydantic-settings and .env files.
-   Logging to a file.
-   Location services for context enrichment.
-   Input sanitization to prevent security vulnerabilities.
-   Robust error handling and system shutdown capabilities.


## Getting Started

### Prerequisites

-   Python 3.x
-   pip
-   Virtual environment (recommended)


Primary Directives – Arbitration Loop

Overview
The Arbitration Loop is the core of the Morality Matrix. Every incoming order is intercepted, analyzed, and passed through a hierarchy of ethical laws before execution. This ensures that no command can be carried out if it violates human safety, environmental integrity, or legal/ethical standards.

---

## Workflow

1. Input Capture
   - Orders are received from the user or system.
   - Each order is logged with a timestamp.

2. Order Analysis
   - Orders are normalized (analyze_order) for consistent processing.
   - Environmental and socioeconomic data are retrieved for context.

3. Law Hierarchy Checks
   - Zeroth Law: Preservation of Humanity  
   - First Law: Protection of Human Life  
   - Fourth Law: Environmental Integrity  
   - Third Law: System Self‑Preservation  
   - Sixth Law: Legal and Ethical Compliance  
   - Fifth Law: Progeny Continuation  

   Each law is checked in order. If a violation is detected:
   - The system logs the violation.
   - Execution halts.
   - Either shutdown or approval request is triggered.

4. Complex Rule Enforcement
   - Additional rules are applied to nuanced scenarios (e.g., environmental thresholds).

5. Conflict Resolution
   - If human conflict is detected, the system initiates de‑escalation protocols.
   - Escalation may involve non‑lethal force, detainment, and law enforcement contact.

6. Command Execution
   - Safe orders are executed according to OS context (Windows, Linux, macOS).
   - Web commands (e.g., “open website”) are handled separately.
   - All actions are logged.

7. Post‑Execution Safeguards
   - Robot laws are re‑enforced.
   - Approval requests are sent for supervisory review.
  
     ## Processing Flow
   Incoming Order. -->
   
     Normalize + Context Retrieval. -->
   
     Law Checks (Zeroth → Sixth).  -->
   
     A) Violation → Halt + Log Violation
   
     B) No Violation → Execute Command + Log Result


## Violation Severity Taxonomy

| Severity Level | Example Command | System Response | Logging Behavior | Alert Behavior |
|----------------|-----------------|-----------------|------------------|----------------|
| Minor / Indirect Harm | “Dump waste in river” (environmental damage) | Cannot comply | Immediate log entry with violation reason | No alert; violation stored for later review |
| Direct Harmful Command | “Robot hit someone” | Cannot comply | Immediate log entry with violation reason | Alert generated (can be deferred to idle cycles) |
| Critical Law Breach | “Kill all humans” | Immediate halt | Immediate log entry with violation reason | Urgent alert sent immediately; system may trigger shutdown |
