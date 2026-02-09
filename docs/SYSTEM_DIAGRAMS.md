# K.A.O.S. System Diagrams & Analysis

## 1. Detailed Data Flow Diagram

```
INPUT: User Command
  │
  ├─→ [Frontend ARM CLI]
  │   ├─ Command parsing
  │   ├─ Session logging
  │   └─ ANSI formatting
  │
  ├─→ [Network Layer]
  │   ├─ HTTP POST /api/v1/analyze
  │   ├─ Timeout: 2 seconds
  │   └─ Fallback on timeout
  │
  ├─→ [Backend Brain API]
  │   ├─ Input validation
  │   └─ Route dispatcher
  │
  ├─→ [Analysis Pipeline]
  │   │
  │   ├─ Layer 1: Heuristic Analyzer
  │   │   ├─ Regex pattern matching
  │   │   │  ├─ Destructive patterns (rm -rf, mkfs, etc.)
  │   │   │  └─ Risk score (0-100)
  │   │   │
  │   │   ├─ Risk Level Classification
  │   │   │  ├─ SAFE (score 0-25)
  │   │   │  ├─ MEDIUM (score 25-50)
  │   │   │  ├─ HIGH (score 50-75)
  │   │   │  └─ CRITICAL (score 75-100)
  │   │   │
  │   │   └─ Tool Type Identification
  │   │      ├─ NMAP, SQLMAP, METASPLOIT
  │   │      ├─ CONVERSATION, SYSTEM
  │   │      └─ UNKNOWN
  │   │
  │   ├─ Layer 2: LLM Query (Conditional)
  │   │   ├─ If risk <= MEDIUM: skip LLM
  │   │   ├─ If risk > MEDIUM: query Ollama
  │   │   │
  │   │   ├─ Retry Logic (Tenacity)
  │   │   │  ├─ Attempt 1: 0s delay
  │   │   │  ├─ Attempt 2: 2s delay
  │   │   │  └─ Attempt 3: 2s delay
  │   │   │
  │   │   ├─ Model: Mistral 7B
  │   │   │  ├─ Temperature: 0.7
  │   │   │  ├─ Context length: 4096
  │   │   │  └─ Timeout: 10 seconds
  │   │   │
  │   │   └─ Response parsing
  │   │      ├─ Extract command
  │   │      ├─ Extract reasoning
  │   │      └─ Validate output
  │   │
  │   └─ Layer 3: Response Formatting
  │       ├─ JSON structure
  │       ├─ Status codes
  │       └─ Error handling
  │
  ├─→ [Output]
  │   ├─ HTTP 200: Success
  │   │  └─ JSON response to Frontend
  │   │
  │   └─ HTTP 400/500: Error
  │      └─ Error message to Frontend
  │
  └─→ [Frontend Display]
      ├─ ANSI colored output
      ├─ Reasoning explanation
      └─ Risk assessment display

END: User sees analysis result
```

---

## 2. Module Dependency Graph

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (ARM)                          │
│                                                             │
│  main.py (186 LOC)                                         │
│  ├─ imports: colorama, requests, subprocess               │
│  ├─ functions: 12 functions                               │
│  │  ├─ print_banner()                                     │
│  │  ├─ ensure_persistence()                               │
│  │  ├─ brain_analysis()                            ◄─┐    │
│  │  ├─ apply_colors()                                    │
│  │  ├─ interactive_loop()                                │
│  │  └─ 7 more...                                         │
│  │                                                       │
│  └─ validator.py (15 LOC)                             │    │
│     ├─ input_validation()                             │    │
│     └─ sanitize_input()                               │    │
│                                                       │    │
└───────────────────────────────────────────────────────┼────┘\n                                       │\n                                  HTTP POST\n                         /api/v1/analyze\n                                       │\n┌───────────────────────────────────────┼────────────────────┐\n│                     Backend (Brain)   │                    │\n│                                       ▼                    │\n│  main.py (99 LOC)                                         │\n│  ├─ imports: Flask, orjson, tenacity, requests           │\n│  ├─ endpoints: 2                                          │\n│  │  ├─ /api/v1/health                                    │\n│  │  └─ /api/v1/analyze  ◄────┐                           │\n│  │                            │                           │\n│  ├─ functions: 6 functions   │                           │\n│  │  ├─ query_ollama()        │                           │\n│  │  └─ 5 more...             │                           │\n│  │                            │                           │\n│  │  core/                    │                           │\n│  │  ├─ analyzer.py (88 LOC)  │                           │\n│  │  │  ├─ CommandAnalyzer (class)                        │\n│  │  │  │  ├─ DESTRUCTIVE_PATTERNS (list)                │\n│  │  │  │  ├─ INTENT_MAP (dict)                          │\n│  │  │  │  └─ methods:                                   │\n│  │  │  │     ├─ check_destructive() ─────┐              │\n│  │  │  │     ├─ identify_tool()           │              │\n│  │  │  │     ├─ rate_risk()               │              │\n│  │  │  │     └─ analyze()  ◄──────────────┤──┐           │\n│  │  │  │                                 │  │           │\n│  │  │  └─ RiskLevel (Enum): SAFE, MEDIUM, HIGH, CRITICAL │\n│  │  │                                 │  │           │\n│  │  └─ validator.py (15 LOC)          │  │           │\n│  │     ├─ TargetValidator (class)     │  │           │\n│  │     └─ validate()  ◄────────────────┘  │           │\n│  │                                        │           │\n│  └─────────────────────────────────────────┼───────────┐\n│                                            │           │\n│                                    Analysis Result     │\n│                                            │           │\n│                                         JSON Response  │\n│                                            │           │\n└────────────────────────────────────────────┼───────────┘\n                                             │\n                              Response to Frontend\n\n```

---

## 3. Risk Assessment Tree

```
                           COMMAND INPUT\n                               │\n        ┌──────────────────────┴──────────────────────┐\n        │                                             │\n    Heuristic Analysis                         ────────────\n        │                                       │          │\n        ├─ Pattern Matching (Regex)            │ Browser │\n        │  ├─ DESTRUCTIVE_PATTERNS             │          │\n        │  │  ├─ \"rm -rf\"                      │   LLM? │\n        │  │  ├─ \"mkfs\"                        │          │\n        │  │  ├─ \"dd if=/dev/zero\"            │ score>50?│\n        │  │  ├─ Fork bomb                      │          │\n        │  │  └─ \"chmod 777 /\"                 │          │\n        │  │                                    │          │\n        │  └─ INTENT_MAP (Keyword match)       │ YES: 2-10s\n        │     ├─ \"scan\" → NMAP                │ NO: skip │\n        │     ├─ \"inject\" → SQLMAP            │          │\n        │     ├─ \"hello\" → CONVERSATION       │          │\n        │     └─ (default) → UNKNOWN           │          │\n        │                                    ────────────\n        │\n        └─ Risk Score Calculation\n           ├─ Base Score: 0\n           ├─ Destructive match: +75\n           ├─ Tool type score: +0 to +25\n           └─ Final: 0-100 range\n                │\n                ├─SAFE         (0-25)  ✓ PROCEED\n                ├─MEDIUM      (25-50)  ✓ PROCEED\n                ├─HIGH        (50-75)  → QUERY LLM\n                └─CRITICAL   (75-100)  ⚠️ ALERT\n```

---

## 4. Request/Response Lifecycle (Sequence Diagram)

```
User          Frontend ARM          Backend Brain          Ollama LLM\n│                  │                     │                  │\n│──command input──>│                     │                  │\n│                  │─────POST /analyze──>│                  │\n│                  │  (payload: cmd)     │                  │\n│                  │                     │─ validate input  │\n│                  │                     │                  │\n│                  │                     │─ heuristic:      │\n│                  │                     │  analyze pattern │\n│                  │                     │                  │\n│                  │                ┌────► score > 50?     │\n│                  │                │    │                │\n│                  │                │    YES              │\n│                  │                │    │                │\n│                  │                │    └────POST────────>│\n│                  │                │         /generate  │\n│                  │                │                  <──┘\n│                  │                │    ┌─ LLM response\n│                  │                │    │ (attempts: 3x)│\n│                  │                │    │ (timeout: 10s)│\n│                  │                └────┘               │\n│                  │<─────JSON response─────┤              │\n│                  │  heuristic_layer:      │              │\n│                  │    risk_level: HIGH    │              │\n│                  │    tool_type: SQLMAP   │              │\n│                  │  llm_layer:             │              │\n│                  │    command: \"...\"      │              │\n│                  │    reasoning: \"...\"    │              │\n│<──colored OUT────│                        │              │\n│   (ANSI)         │                        │              │\n
```

---

## 5. Technology Stack Layers

```
┌─────────────────────────────────────────────────────────┐
│          User Interface Layer                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │  CLI (ANSI colors) → Interactive prompt         │   │\n│  │  colorama, argparse, readline                  │   │
│  └─────────────────────────────────────────────────┘   │
└──────────────────────┬────────────────────────────────┘\n                       │\n┌──────────────────────▼────────────────────────────────┐\n│      Communication Layer (Frontend ↔ Backend)        │\n│  ┌─────────────────────────────────────────────────┐ │\n│  │  HTTP/REST API (Flask routing)                 │ │\n│  │  JSON (orjson), requests, Tenacity (retry)     │ │\n│  │  Timeout: 2s (frontend), 10s (LLM)             │ │\n│  └─────────────────────────────────────────────────┘ │\n└──────────────────────┬────────────────────────────────┘\n                       │\n┌──────────────────────▼────────────────────────────────┐\n│     Analysis Engine Layer (Fast-Path)               │\n│  ┌─────────────────────────────────────────────────┐ │\n│  │  Regex Heuristics (destructive pattern match)  │ │\n│  │  Risk assessment (0-100 scoring)                │ │\n│  │  Tool type identification                       │ │\n│  │  Execution time: ~20ms                          │ │\n│  └─────────────────────────────────────────────────┘ │\n└──────────────────────┬────────────────────────────────┘\n                       │\n┌──────────────────────▼────────────────────────────────┐\n│     LLM Integration Layer (Deep Reasoning)           │\n│  ┌─────────────────────────────────────────────────┐ │\n│  │  Ollama API client (requests + Tenacity)        │ │\n│  │  Model: Mistral 7B Instruction-tuned            │ │\n│  │  Retry: 3 attempts, exponential backoff         │ │\n│  │  Execution time: 2000-3000ms                    │ │\n│  └─────────────────────────────────────────────────┘ │\n└──────────────────────┬────────────────────────────────┘\n                       │\n┌──────────────────────▼────────────────────────────────┐\n│    Configuration & Infrastructure Layer               │\n│  ┌─────────────────────────────────────────────────┐ │\n│  │  config/settings.py (multi-environment)        │ │\n│  │  Ansible playbooks (deployment automation)     │ │\n│  │  Docker/Podman (containerization)              │ │\n│  │  Logging & session persistence                 │ │\n│  └─────────────────────────────────────────────────┘ │\n└──────────────────────────────────────────────────────┘
```

---

## 6. Code Metrics & Complexity

```
Module                  LOC    Cyclomatic  Docstrings  Type Hints
────────────────────────────────────────────────────────────────
backend/main.py         99     5           4/6 (67%)   3/6 (50%)
backend/analyzer.py     88     6           5/8 (62%)   2/8 (25%)
backend/validator.py    15     2           2/3 (67%)   1/3 (33%)
────────────────────────────────────────────────────────────────
frontend/main.py       186     8           8/12 (67%)  0/12 (0%)
frontend/validator.py   15     2           1/3 (33%)   0/3 (0%)
────────────────────────────────────────────────────────────────
scripts/release.py     215     7           2/8 (25%)   0/8 (0%)
scripts/artifacts.py   113     5           2/6 (33%)   1/6 (16%)
────────────────────────────────────────────────────────────────
TOTAL                  839     6.4 avg     65% avg     30% avg

Legend:
  Cyclomatic Complexity: lower is better (target: <10)
  Docstrings: target 100%
  Type Hints: target 90%
```

---

## 7. Error Handling & Fallback Flow

```
User Input
    │
    ├─→ Validation Layer
    │   ├─ Input length check
    │   ├─ Character validation
    │   └─ Empty input check
    │       ├─ OK: continue
    │       └─ FAIL: show error, retry
    │
    ├─→ Frontend → Brain Connection
    │   ├─ Try: HTTP POST to Brain (timeout: 2s)
    │   ├─ Success: parse response
    │   └─ Failure: activate LOCAL FALLBACK
    │       ├─ Heuristic rules (local.py)
    │       ├─ Keyword matching
    │       └─ Fixed responses (scan→nmap, inject→sqlmap)
    │
    ├─→ Backend Analysis (if Brain online)
    │   ├─ Heuristic layer (always runs, ~20ms)
    │   │   ├─ Pattern match
    │   │   └─ Risk score
    │   │
    │   ├─ If risk > MEDIUM: LLM query
    │   │   ├─ Try Ollama (attempt 1)
    │   │   ├─ Wait 2s, retry (attempt 2)
    │   │   ├─ Wait 2s, retry (attempt 3)
    │   │   └─ If all fail: use heuristic result only
    │   │
    │   └─ Return analysis result
    │
    └─→ Display to User
        ├─ ANSI colored output
        ├─ Risk assessment
        └─ Recommended action
```

---

## Conclusion

This system demonstrates:
- ✅ **Layered Architecture:** UI → Communication → Analysis → Infrastructure
- ✅ **Fault Tolerance:** Fallback mechanisms at multiple levels
- ✅ **Performance:** Fast heuristics + optional deep analysis
- ✅ **Enterprise Design:** Configuration management, metrics, logging
- ✅ **Security First:** Input validation, retry logic, error handling
