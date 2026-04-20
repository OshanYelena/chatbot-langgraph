# chatbot-langgraph

Production-ready LangGraph chatbot with stateful multi-turn conversations,
intent routing, RAG, tool execution, and streaming responses.

## Quickstart

```bash
cp .env.example .env
# Fill in API keys and DB credentials

pip install -e ".[dev]"

uvicorn apps.api.main:app --reload
```

## Structure

| Path | Purpose |
|---|---|
| `apps/api/` | FastAPI application — routes, schemas, dependencies |
| `apps/worker/` | Background task worker |
| `src/graph/` | LangGraph state, builder, nodes, routing |
| `src/llm/` | LLM provider setup, prompts, safety filters |
| `src/memory/` | Short-term (state) and long-term (DB) memory |
| `src/retrieval/` | RAG pipeline — query rewrite, retrieval, reranking |
| `src/tools/` | Tool registry, policies, implementations |
| `src/persistence/` | Checkpointing, DB models, repositories |
| `src/observability/` | LangSmith tracing, metrics, structured logging |
| `src/config/` | Settings, feature flags |
| `tests/` | Unit, integration, e2e, and eval suites |
| `docker/` | Dockerfile and docker-compose |
| `scripts/` | DB seeding, eval runners |

## Implementation phases

- **Phase 1** — Basic chatbot, memory, streaming
- **Phase 2** — RAG pipeline, tool execution
- **Phase 3** — Observability, security hardening
- **Phase 4** — Horizontal scaling, multi-agent extension
