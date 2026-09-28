# 🤖 Multi-Agent Systems with LangGraph & Orchestration Patterns

Multi-agent architectures divide complex reasoning workflows into specialized sub-agents with dedicated roles, state schemas, and verification loops.

---

## 🏗️ Core Architecture: StateGraph Pattern

In LangGraph, agents communicate by mutating a centralized `TypedDict` or Pydantic state graph.

```python
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_step: str
    intermediate_data: dict
    retry_count: int
```

### 1. Supervisor / Hierarchical Routing
A central LLM acts as the router/orchestrator, choosing which specialized agent executes next based on current goal state.

```
       [User Request]
             │
             ▼
     ┌──────────────┐
     │  Supervisor  │ ◄──────────┐
     └──────┬───────┘            │
      ┌─────┴──────┐             │
      ▼            ▼             │
┌───────────┐ ┌───────────┐      │
│ Researcher│ │ Coder     │ ─────┘
└───────────┘ └───────────┘
```

### 2. Evaluator-Optimizer (Reflection Loops)
Instead of returning the first generation, a critic agent audits output against strict criteria:
- **Code verification**: AST validation or sandboxed test runs.
- **Factuality checks**: Hallucination scoring against retrieved context.
- **Conditional edges**: Loop back if quality score < threshold ($N \le 3$).

---

## ⚡ Production Best Practices
- **Idempotent Nodes**: Ensure graph nodes can be safely retried without side effects.
- **Checkpointing**: Use persistent checkpointers (`SqliteSaver` or `PostgresSaver`) for human-in-the-loop approvals.
- **Token Budgeting**: Summarize long conversation history in state reducers before forwarding to subagents.
