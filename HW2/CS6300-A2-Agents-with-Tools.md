Build an intelligent agent that effectively uses at least 3–4 well-designed tools in a chosen environment. You may extend your Assignment 1 agent in the same environment, or select a new environment and design a new agent.

Learning goals (mapped to course CLOs)
CLO 1 – Agent-Environment Modeling: Deepen your PEAS analysis to include tool-augmented actions and environment interactions.

CLO 2 – AI Pipeline: Design and implement an AI solution with multiple tools, each clearly specified with contracts and behaviors.

CLO 3 – Agentic AI: Build a functioning agent (framework + model of your choice) that perceives, reasons/decides, and acts through multiple tools to solve tasks.

Overview
You will:

Choose or extend an environment. Either continue from Assignment 1 or select a new domain that supports at least 3–4 useful tools.

Design tools. For each tool, provide a clear name, description, inputs, outputs, and failure modes. Tools must be specific and useful.

Implement your agent. Use a well-established agentic AI framework (e.g., smolagents, LangChain, CrewAI, MCP-based, etc.) and a well-established programming language and model.

Evaluate your agent. Show how the tools are used in practice, and compare performance with/without tools where possible.

Document and reflect. Submit a combined Design Brief + Results & Reflection PDF. The PDF must include a link to your GitHub repository.

Deliverables
Design Brief (PDF, ~3–4 pages):

PEAS Analysis: Update from Assignment 1 with a strong focus on actuators/actions = tools.

Environment Properties: Same formal analysis (O/PO, D/Stoch, Episodic/Sequential, etc.).

Tool Specifications: For each tool:

Name

Description

Input(s) and type(s)

Output(s) and type(s)

Possible errors/failure handling

Agent Architecture: Framework chosen, model(s) used, reasoning loop, orchestration strategy (scripted vs model-driven).

Evaluation Plan: Test cases, success metrics, expected behaviors.

Working Code (Git repo):

README.md with installation and run instructions (must be clear and reproducible).

requirements.txt / pyproject.toml or equivalent.

Agent implementation using your chosen framework/model.

At least 3–4 working tools, each documented with docstrings and validated I/O.

Example scripts/tests showing the agent solving tasks.

Results & Reflection (PDF, ~2–3 pages):

Repo Link: Provide your GitHub repository link here.

Results: Tables/figures/logs for multiple runs. Highlight how tools are invoked.

Analysis: Successes, limitations, and “what if” ablations (e.g., removing one tool).

Reflection: What you learned about tool design, orchestration, and PEAS tradeoffs.

Submit one combined PDF containing the Design Brief + Results & Reflection (with repo link).

Technical requirements
Framework: Must use a well-established agentic AI framework (e.g., smolagents, LangChain, CrewAI, MCP server).

Language: Must use a well-established programming language.

Models: Must use a well-established LLM suitable for reasoning and tool-use.

Reproducibility: Must include installation and run instructions in README. Avoid hard-coding secrets.

Evaluation & Rubric (100 pts)
Component	Points	What we look for
PEAS Analysis	15	Correct, detailed, and tool-focused PEAS.
Tool Specifications	25	3–4 tools with clear purpose, I/O contracts, error handling.
Design Brief & Architecture	15	Coherent framework choice, orchestration strategy, evaluation plan.
Implementation	25	Working agent; tools integrated; code is clear and reproducible.
Results	10	Demonstrates tool use across runs; reproducible evidence.
Reflection	10	Insightful discussion of tool design, successes, failures, and learning.
Deductions:

Useless/missing tools (–10 each).

Poorly documented tools (–5 each).

Non-reproducible setup or unclear run instructions (–5).

Unsafe key handling (–10).

Constraints & guidance
Keep the Environment→Agent→Environment loop central.

Tools should be modular, specific, and typed. Avoid vague “do-everything” tools.

At least 3–4 tools are required; if your environment does not naturally support this, choose another.

Consider error handling, retries, and orchestration strategies.

Submission checklist
Repo link included in Results & Reflection PDF.

Repo contains code, README, requirements, and tests/examples.

Combined PDF (Design Brief + Results & Reflection).

All tools clearly documented with name, description, inputs, and outputs.