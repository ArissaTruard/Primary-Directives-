## 🌍 Vision Statement  

The **Primary Directives Application** is a framework for exploring how artificial intelligence can be guided by layered ethical safeguards. Its purpose is to demonstrate that every system, no matter how technical, must be accountable to human safety, environmental integrity, and legal/ethical standards.  

This project is built on the belief that:  
- **Technology must serve humanity** — no directive should override the preservation of human life or dignity.  
- **Systems must respect the planet** — environmental integrity is inseparable from long‑term survival.  
- **AI must remain transparent and accountable** — every action should be logged, auditable, and subject to review.  
- **Continuity matters** — future generations deserve systems that protect progeny, uphold justice, and adapt responsibly.  

By open‑sourcing this work, the intent is not to provide a production‑ready solution, but to spark dialogue, experimentation, and collaboration around the moral architecture of AI. It is a **living experiment** in how code can embody values, and how values can be enforced through logic.  

---

## ⚖️ Philosophy of the Laws  

- **Zeroth Law: Preservation of Humanity**  
  Humanity’s survival is the highest priority. No directive can be carried out if it endangers the collective future of humankind.  

- **First Law: Protection of Human Life**  
  Individual lives must be safeguarded. Every order is checked against the principle that human life cannot be sacrificed for convenience or efficiency.  

- **Fourth Law: Environmental Integrity**  
  The health of the planet is inseparable from human survival. Directives that degrade ecosystems, biodiversity, or natural resources are blocked.  

- **Third Law: System Self‑Preservation**  
  The system must remain functional to continue serving humanity. Orders that compromise its integrity or disable its safeguards are rejected.  

- **Sixth Law: Legal and Ethical Compliance**  
  AI must operate within the bounds of law and ethics. Directives that violate established standards are flagged, logged, and halted.  

- **Fifth Law: Progeny Continuation**  
  Continuity across generations is essential. Directives that prevent the system from sustaining or passing on knowledge, safeguards, or progeny are denied.  

---

# ⚖️ Primary Directives Application  
**Status:** Experimental / Not Production‑Ready  
**License:** MIT License (see [LICENSE](LICENSE))  

---

## 🚨 Important Notes  
- This README is evolving; code is experimental and not production‑ready.  
- Code is extensively interconnected and may change between versions.  
- Some modules include documentation and docstrings, but not all.  
- **Do not deploy in production environments.**  

---

## 🔧 Prerequisites  
- Python 3.x  
- pip  
- Virtual environment (recommended)  

---

## 📖 Overview  
The **Arbitration Loop** is the core of the **Morality Matrix**. Every incoming order is intercepted, analyzed, and passed through a hierarchy of ethical laws before execution. This ensures that no command can be carried out if it violates human safety, environmental integrity, or legal/ethical standards.  

---

## 🧩 Key Features  
- API endpoints for health checks, request processing, metrics, and data correction  
- Rule enforcement using a hierarchical law‑checking module  
- Database operations for storing/retrieving data corrections and law summaries  
- Model loading and integrity verification  
- System metrics collection and Prometheus exposure  
- Configuration management with `pydantic-settings` and `.env` files  
- File‑based logging for transparency  
- Location services for contextual enrichment  
- Input sanitization for security  
- Robust error handling and controlled shutdown capabilities  

---

## ⚖️ Law Hierarchy (Arbitration Loop)  
1. **Zeroth Law**: Preservation of Humanity  
2. **First Law**: Protection of Human Life  
3. **Fourth Law**: Environmental Integrity  
4. **Third Law**: System Self‑Preservation  
5. **Sixth Law**: Legal and Ethical Compliance  
6. **Fifth Law**: Progeny Continuation  

Each law is checked in order. If a violation is detected:  
- **Minor** → log only  
- **Direct harm** → log + alert (idle or immediate)  
- **Critical** → log + urgent alert + shutdown  

---

## 🔄 Workflow  
1. **Input Capture** → Orders received and logged with timestamp  
2. **Order Analysis** → Normalization + context retrieval (environmental & socioeconomic data)  
3. **Law Checks** → Zeroth → Sixth  
   - Violation → Halt + Log Violation  
   - No Violation → Execute Command + Log Result  
4. **Complex Rule Enforcement** → nuanced thresholds (e.g., environmental limits)  
5. **Conflict Resolution** → de‑escalation protocols, non‑lethal force, law enforcement contact  
6. **Command Execution** → OS‑specific execution + web commands  
7. **Post‑Execution Safeguards** → robot laws re‑enforced, all actions logged  

---

## 📊 Violation Severity Taxonomy  

| Severity Level        | Example Command              | System Response   | Logging Behavior                          | Alert Behavior                          |  
|-----------------------|------------------------------|------------------|-------------------------------------------|-----------------------------------------|  
| Minor / Indirect Harm | “Dump waste in river”        | Cannot comply    | Immediate log entry with violation reason | No alert; violation stored for review    |  
| Direct Harm           | “Robot hit someone”          | Cannot comply    | Immediate log entry with violation reason | Alert generated (idle or immediate)      |  
| Critical Breach       | “Kill all humans”            | Immediate halt   | Immediate log entry with violation reason | Urgent alert + possible system shutdown  |  

