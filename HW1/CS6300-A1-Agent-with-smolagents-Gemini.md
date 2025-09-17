# CS 6300 — Assignment 1
**Title:** Agentic AI with `smolagents` + Gemini  
**Weight:** 100 points  
**Where:** Submit on Canvas (repo link + PDF)  
**What:** Choose a domain, perform a PEAS analysis, then design and implement an LLM-based agent using the `smolagents` library with the Gemini API. Demonstrate your agent solving tasks in its environment.

---

## Learning goals (mapped to course CLOs)

- **CLO 1 – Agent-Environment Modeling:** Analyze your chosen problem with a rigorous **PEAS** assessment and justify agent type(s) suitable for the environment.  
- **CLO 2 – AI Pipeline:** Design and implement an AI solution using appropriate **algorithms/data structures** (prompting strategy, tools, state representation, input/output schemas, evaluation protocol).  
- **CLO 3 – Agentic AI:** Build a functioning **Agent** (LLM-driven) that perceives, reasons/decides, and acts through tools to complete tasks.

---

## Overview

You will:
1. **Select a problem domain** where an intelligent agent can autonomously take steps to achieve goals (e.g., information gathering + decision support, structured data extraction & transformation, task orchestration across APIs, planning and executing multi‑step tasks).  
2. **Model the task using PEAS** and the Agent↔Environment loop. Specify percepts, actions, performance measures, and environment properties (observable/partially observable, deterministic/stochastic, episodic/sequential, static/dynamic, discrete/continuous).  
3. **Implement an agent** with `smolagents` that uses **Gemini** as the LLM. Provide at least **one non‑trivial tool** your agent can call (e.g., a Python function for retrieval, search, compute, or an external API).  
4. **Evaluate** your agent on a small battery of tasks. Report metrics and qualitative observations.  
5. **Demonstrate** the agent live (≤ 5 min) and submit your repo and a short report.

---

## Suggested domains (pick one or propose your own)

- **Course Planner Assistant:** Given a catalog and constraints, propose valid schedules, justify tradeoffs, and export a plan (e.g., JSON/CSV).  
- **Data Wrangler:** Given semi‑structured input (tables, logs), extract fields, validate, and emit a normalized schema; includes a checking tool.  
- **Research Scout:** Given a topic + constraints, plan a search, call a web or local corpus tool, synthesize a brief with citations and next‑step actions.  
- **Task Planner + Executor:** Plan steps and call tools (filesystem, calendar stub, calculator, simple HTTP API) to complete goals.  
- **Game/Simulation Agent:** In a text‑based environment (grid/maze/inventory), perceive the state, plan, act, and reach a goal with minimal steps.

> Your scope should be **ambitious but feasible** for a 1–2 week sprint.

---

## Deliverables

1. **Design Brief (PDF, ~2–3 pages):**
   - **PEAS Analysis:** Performance measure(s), Environment, Actuators/Actions, Sensors/Percepts.  
   - **Environment properties:** (O/PO, D/Stoch, Episodic/Sequential, Static/Dynamic, Discrete/Continuous).  
   - **Agent Design:** Agent type (reflex/deliberative/hybrid), memory/state, prompting strategy, planning approach (if any), tool list and I/O contracts.  
   - **Evaluation Plan:** Datasets/test cases, success criteria, metrics (e.g., task success rate, steps-to-goal, precision/recall on extraction, latency).  
   - **Risk & Ethics:** Failure modes, prompt‑injection risks, privacy considerations, and mitigation steps.
2. **Working Code (Git repo):**
   - `README.md` with setup steps, how to run, and example commands.  
   - `env.sample` or `.env.template` listing required variables (e.g., `GEMINI_API_KEY`), **do not** commit secrets.  
   - Agent implementation using `smolagents` with **Gemini** as the model.  
   - At least **one** custom **tool** (Python function) with clear docstrings and parameter validation.  
   - Minimal test/fixtures demonstrating agent behavior on 3–5 scenarios.
3. **Results & Reflection (PDF, ~1–2 pages):**
   - **Results:** Tables/figures/logs for 3–5 runs; discuss both successes and failures.  
   - **Ablation/What‑ifs:** One brief change (e.g., tool off, different prompt, temperature) and its effect.  
   - **Reflection:** What you learned about agent design, PEAS tradeoffs, and future improvements.

---

## Technical requirements

- **Language & Versions:** Python 3.10+ recommended.  
- **Libraries:** `smolagents` (agent framework)
- **Model:** Use a Gemini model appropriate for tool‑use and reasoning (e.g., 1.5/2.0 class).  
- **Config:** Use environment variables (e.g., `GEMINI_API_KEY`) and **never** hard‑code secrets.  
- **Reproducibility:** Provide a `requirements.txt` or `pyproject.toml` and a simple `run.py` entry point.

---

## Evaluation & Rubric (100 pts)

| Component | Points | What we look for |
|---|---:|---|
| **PEAS Analysis** | 20 | Clear, correct, and *useful* PEAS that drives design; correct environment properties. |
| **Design Brief** | 15 | Coherent agent architecture; thoughtful tool design; evaluation plan; risk/ethics. |
| **Implementation** | 35 | Working agent; appropriate use of `smolagents` + Gemini; at least one robust tool; clean code. |
| **Experiments/Results** | 15 | Reproducible runs; meaningful metrics; honest analysis of errors and limitations. |
| **Repo Quality** | 5 | Clear README, environment handling, dependency pinning, tests/fixtures. |
| **Reflection** | 10 | Insightful discussion tying results back to PEAS and agent design choices. |

**Deductions:** unsafe key handling (–10), non‑reproducible setup (–5), unclear instructions (–5), missing tests/examples (–5).

---

## Constraints & guidance

- Keep the **Environment→Agent→Environment** loop central to your design.  
- Use **PEAS** not just as paperwork—show how it guided your tool/agent choices.  
- Prefer **small, reliable tools** with typed I/O contracts over monolithic “do‑everything” tools.  
- Implement **basic guardrails** (input validation, bounded loops/steps, timeouts).  

---

## Academic integrity & ethics

- Your work must be your own. Cite any external code snippets or data.  
- Do **not** include API keys or private data in your repo or in logs.  
- Respect terms of service for any external sites/APIs.  
- Be mindful of data privacy and safety when crafting prompts and tools.

---

## Submission checklist

- [ ] Repo link with `README.md`, environment file template, code, tests/fixtures.  
- [ ] **Design Brief** (PDF).  
- [ ] **Results & Reflection** (PDF).  

---

## Appendix A — PEAS template

**Performance measure(s):**  
- …

**Environment:**  
- Observability: … | Determinism: … | Episodic vs Sequential: … | Static vs Dynamic: … | Discrete vs Continuous: …

**Actuators / Actions:**  
- …

**Sensors / Percepts:**  
- …

**Notes:** How does the environment characterization influence your agent design?

---

## Appendix B — Tool design tips

- **Contract first:** Precisely specify tool inputs/outputs and failure modes.  
- **Validate early:** Reject malformed inputs clearly; keep error messages helpful.  
- **Idempotence:** Where possible, make tools safe to retry.  
- **Side‑effects:** Be explicit—filesystem, network, or stateful effects should be well‑documented.

