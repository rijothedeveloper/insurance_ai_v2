# Assignment: Build a Multi-Agent Insurance Claims Resolution System

## Objective

Design and implement a production-style **Agentic AI workflow** that automates the intake, validation, investigation, and resolution recommendation process for insurance claims.

The system must demonstrate:

- Agentic orchestration
- Tool calling
- Multi-agent collaboration
- Decision-making loops
- Retry/fallback handling
- Human-in-the-loop escalation
- Memory/state management
- Structured outputs
- Observability/logging

You must implement the same use case using all four frameworks:

1. Anthropic SDK
2. OpenAI SDK
3. Google ADK
4. LangGraph

---

# Business Use Case

## Scenario

An insurance company receives thousands of claims daily.

The goal is to automate first-pass claim processing while minimizing fraud and reducing manual adjuster workload.

The AI system should:

1. Receive a claim submission
2. Validate documents
3. Detect fraud signals
4. Estimate payout
5. Decide whether:
   - auto-approve
   - reject
   - escalate to human adjuster

6. Generate customer communication
7. Log all decisions and reasoning

---

# Functional Requirements

## Inputs

The system receives:

- Claim form JSON
- Uploaded documents
- Photos
- Policy details
- Customer history

Example:

```json
{
  "claim_id": "CLM-1001",
  "customer_id": "CUS-921",
  "policy_type": "Auto",
  "incident_description": "Rear-end collision",
  "estimated_damage": 4800,
  "documents": [
    "repair_invoice.pdf",
    "accident_photo_1.jpg"
  ]
}
```

---

# Multi-Agent Architecture

## Required Agents

### 1. Intake Agent

Responsibilities:

- Parse claim
- Validate schema
- Normalize fields
- Detect missing information
- Decide whether enough information exists

Outputs:

- structured claim object
- missing fields list
- confidence score

---

### 2. Document Verification Agent

Responsibilities:

- OCR extraction
- Validate invoices
- Verify policy numbers
- Match names/dates
- Detect tampered documents

Outputs:

- document verification report
- authenticity confidence

---

### 3. Fraud Detection Agent

Responsibilities:

- Detect duplicate claims
- Analyze suspicious patterns
- Compare customer history
- Use external fraud API
- Generate fraud risk score

Outputs:

- fraud risk score
- fraud explanation
- recommendation

---

### 4. Payout Estimation Agent

Responsibilities:

- Estimate payout
- Compare against policy limits
- Apply deductibles
- Calculate settlement recommendation

Outputs:

- estimated payout
- adjustment notes

---

### 5. Decision Agent

Responsibilities:

- Aggregate all agent outputs
- Decide:
  - approve
  - reject
  - escalate

- Explain reasoning
- Trigger fallback logic

Outputs:

- final decision
- reasoning
- escalation status

---

### 6. Communication Agent

Responsibilities:

- Generate customer email
- Generate adjuster summary
- Produce audit log

Outputs:

- customer message
- internal summary

---

# Required Tool Calling

Your system MUST implement tool calling.

## Mandatory Tools

### 1. Policy Lookup API

Simulated endpoint:

```http
GET /policy/{customer_id}
```

Returns:

```json
{
  "policy_active": true,
  "coverage_limit": 10000,
  "deductible": 500
}
```

---

### 2. Fraud Check API

```http
POST /fraud/check
```

Returns:

```json
{
  "risk_score": 0.82,
  "signals": [
    "duplicate_phone",
    "high_claim_frequency"
  ]
}
```

---

### 3. OCR Tool

Input:

- image/pdf

Output:

- extracted text

---

### 4. Claim Database Search

Search historical claims.

Capabilities:

- semantic search
- duplicate detection
- historical payouts

---

### 5. Email Notification Tool

Send:

- customer emails
- escalation alerts

---

### 6. Human Approval Tool

Allows:

- manual override
- approval
- rejection
- comments

---

# Required Decision-Making Logic

Your agents must demonstrate non-trivial reasoning.

## Examples

### Example 1 — Auto Approval

IF:

- fraud risk < 0.2
- payout < $5000
- all docs verified

THEN:

- auto approve

---

### Example 2 — Human Escalation

IF:

- fraud risk > 0.7
  OR
- authenticity confidence < 0.6
  OR
- payout > $10000

THEN:

- escalate to human adjuster

---

### Example 3 — Retry Loop

IF:

- OCR extraction confidence < threshold

THEN:

- retry OCR up to 3 times
- use fallback OCR provider
- request manual upload if failed

---

# Required Loops

Your workflow MUST contain iterative loops.

## Mandatory Loops

### Loop 1 — Missing Information Collection

Flow:

1. Intake agent detects missing fields
2. Request additional data
3. Re-validate claim
4. Repeat until:
   - data complete
     OR
   - retry limit exceeded

---

### Loop 2 — Fraud Reassessment

Flow:

1. Fraud agent detects suspicious pattern
2. Query additional historical claims
3. Recalculate risk score
4. Continue until confidence threshold reached

---

### Loop 3 — Document Verification Retry

Flow:

1. OCR extraction fails
2. Retry with alternate OCR model/tool
3. Compare outputs
4. Escalate if mismatch persists

---

# Required Fallback Mechanisms

Your implementation MUST contain fault tolerance.

## Required Fallbacks

### API Failure Fallback

If Fraud API fails:

1. Retry 3 times
2. Use cached fraud model
3. Lower confidence score
4. Escalate if confidence too low

---

### LLM Failure Fallback

If primary LLM fails:

- switch model/provider
- continue workflow
- log degraded mode

---

### Tool Timeout Handling

If external API timeout > 5 seconds:

- cancel operation
- retry asynchronously
- notify operator

---

# Human-in-the-Loop Requirements

Your system MUST pause for human intervention under specific conditions.

## Escalation Conditions

- High fraud risk
- Large payout
- Conflicting documents
- Low confidence decisions
- Multiple failed retries

## Human Actions

Human reviewer can:

- approve
- reject
- request more information
- override AI recommendation
- add comments

The workflow must resume after human input.

---

# State Management Requirements

Your implementation must preserve:

- claim state
- agent outputs
- retry counts
- tool results
- escalation status
- audit trail

---

# Observability Requirements

Log:

- agent execution
- tool calls
- prompts
- decisions
- retries
- failures
- latency
- token usage

Bonus:

- tracing dashboard
- visualization of workflow graph

---

# Framework-Specific Expectations

# 1. Anthropic SDK Implementation

## Expectations

Implement:

- Claude tool use
- agent orchestration
- structured outputs
- retries
- fallback handling
- state persistence

## Required Features

- tool calling via Claude API
- XML or JSON structured prompting
- multi-turn orchestration
- memory/state manager
- retry controller

## Suggested Stack

- Anthropic SDK
- FastAPI
- Redis
- SQLite/Postgres

## Deliverables

- architecture diagram
- agent workflow
- runnable implementation
- README
- sample outputs

---

# 2. OpenAI SDK Implementation

## Expectations

Implement using:

- Responses API OR Assistants API
- tool calling
- agent delegation
- structured outputs
- reasoning traces

## Required Features

- function calling
- JSON schema outputs
- retry/fallback orchestration
- multi-agent coordination

## Suggested Stack

- OpenAI SDK
- FastAPI
- Pydantic
- Redis

## Bonus

- streaming responses
- parallel tool execution

---

# 3. Google ADK Implementation

## Expectations

Implement using Google Agent Development Kit.

## Required Features

- hierarchical agents
- planner/executor model
- tool registry
- long-running tasks
- stateful execution

## Required Components

- Planner Agent
- Executor Agent
- Fraud Specialist Agent
- Human Escalation Agent

## Suggested Features

- Gemini models
- Vertex AI integration
- event-driven orchestration

---

# 4. LangGraph Implementation

## Expectations

Implement using graph-based orchestration.

## Required Features

- state graph
- conditional edges
- loops
- retries
- checkpointing
- human interrupts

## Mandatory Graph Nodes

- intake_node
- verification_node
- fraud_node
- payout_node
- decision_node
- human_review_node
- communication_node

## Required Conditional Edges

Examples:

```python
if fraud_score > 0.7:
    goto("human_review_node")
```

## Required Capabilities

- resumability
- persistence
- branch routing
- event logging

---

# Technical Constraints

## Must Use

- Python
- Typed schemas/models
- Async APIs
- Modular architecture

## Must Demonstrate

- Prompt engineering
- Structured outputs
- Error handling
- Agent collaboration
- Tool orchestration
- Context passing

---

# Suggested Folder Structure

```text
project/
│
├── agents/
├── tools/
├── workflows/
├── prompts/
├── schemas/
├── memory/
├── logs/
├── tests/
├── api/
├── ui/
└── README.md
```

---

# Evaluation Criteria

| Category                     | Weight |
| ---------------------------- | ------ |
| Multi-agent orchestration    | 20%    |
| Tool calling quality         | 20%    |
| Decision logic               | 15%    |
| Loops & retries              | 10%    |
| Human-in-loop implementation | 10%    |
| Error handling/fallbacks     | 10%    |
| State management             | 10%    |
| Observability                | 5%     |

---

# Required Deliverables

## Deliverable 1 — Architecture Document

Include:

- system design
- agent interactions
- state transitions
- tool integration
- retry strategy
- escalation flow

---

## Deliverable 2 — Sequence Diagrams

Include:

- normal flow
- fallback flow
- human escalation flow

---

## Deliverable 3 — Runnable Code

Provide:

- setup instructions
- environment configuration
- sample inputs
- API mocks

---

## Deliverable 4 — Demo Video

Demonstrate:

- successful claim approval
- fraud escalation
- OCR retry loop
- human intervention
- recovery from API failure

---

# Advanced Bonus Features

## Bonus 1 — Self-Reflection Agent

An agent reviews final decisions and critiques:

- confidence
- reasoning quality
- hallucination risk

---

## Bonus 2 — Multi-Model Routing

Dynamically select models:

- cheap model for simple tasks
- advanced model for fraud analysis

---

## Bonus 3 — Cost Optimization Layer

Track:

- token usage
- latency
- cost per claim

Optimize routing accordingly.

---

## Bonus 4 — Parallel Agent Execution

Run:

- fraud analysis
- document verification
- payout estimation

in parallel.

---

# Example Workflow

```text
User submits claim
        ↓
Intake Agent validates claim
        ↓
Missing info?
   YES → Request additional data → Retry
   NO
        ↓
Document Verification Agent
        ↓
OCR confidence low?
   YES → Retry OCR → Fallback OCR
   NO
        ↓
Fraud Detection Agent
        ↓
Fraud API timeout?
   YES → Retry → Cached model fallback
   NO
        ↓
Payout Estimation Agent
        ↓
Decision Agent
        ↓
High risk?
   YES → Human Review
   NO
        ↓
Communication Agent
        ↓
Final Response
```

---

# Minimum Technical Expectations Per Framework

| Capability          | Anthropic | OpenAI   | Google ADK      | LangGraph |
| ------------------- | --------- | -------- | --------------- | --------- |
| Tool Calling        | Yes       | Yes      | Yes             | Yes       |
| Multi-Agent         | Yes       | Yes      | Yes             | Yes       |
| Loops               | Yes       | Yes      | Yes             | Yes       |
| Conditional Routing | Yes       | Yes      | Yes             | Yes       |
| Human Interrupts    | Manual    | Manual   | Native patterns | Native    |
| State Persistence   | Required  | Required | Required        | Required  |
| Retry Logic         | Required  | Required | Required        | Required  |
| Observability       | Required  | Required | Required        | Required  |

---

# Recommended APIs & Services

## APIs

- OCR.space API
- Google Vision API
- Fraud detection mock API
- SendGrid API
- Twilio API
- OpenSearch/Elasticsearch

---

# Optional UI

Build a dashboard showing:

- claim status
- agent traces
- fraud scores
- escalation queue
- retry history
- human decisions

---

# Final Goal

By the end of this assignment, students should understand:

- real-world agentic system design
- orchestration patterns
- multi-agent collaboration
- tool ecosystems
- workflow graphs
- fault tolerance
- human-in-loop AI systems
- production AI architecture
- framework tradeoffs

---

# Comparative Analysis Requirement

After completing all four implementations, write a comparison report covering:

## Compare

- developer experience
- complexity
- flexibility
- observability
- scalability
- debugging experience
- memory handling
- human-in-loop support
- production readiness
- learning curve

## Include

- pros/cons table
- architecture comparison
- code complexity analysis
- performance benchmarks
- recommendation matrix

---

# Expected Outcome

A fully functional enterprise-grade multi-agent AI system implemented across four major agentic AI frameworks demonstrating:

- orchestration
- reasoning
- tool usage
- workflow management
- resilience
- governance
- escalation
- automation
