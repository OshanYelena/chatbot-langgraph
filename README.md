# 🤖 chatbot-langgraph

A production-ready, stateful AI chatbot built with [LangGraph](https://github.com/langchain-ai/langgraph), [FastAPI](https://fastapi.tiangolo.com/), and [PostgreSQL](https://www.postgresql.org/). Designed from the ground up for multi-turn conversations, intelligent intent routing, RAG-powered knowledge retrieval, tool execution, and real-time streaming — with observability and safety as first-class concerns.

---

## ✨ Features

- **Stateful multi-turn conversations** — persistent memory per user and thread via LangGraph checkpointing
- **Intelligent intent routing** — LLM-based classification dispatches to the right handler (chat, RAG, tools, or refusal)
- **RAG pipeline** — query rewriting, top-k retrieval, reranking, and grounded generation
- **Tool execution** — pluggable tool registry with input validation, permission checks, timeouts, and audit logging
- **Streaming responses** — real-time token streaming via Server-Sent Events (SSE)
- **Short & long-term memory** — in-state conversation history + persistent user preferences in PostgreSQL
- **Observability** — LangSmith tracing, structured logging, latency and token usage metrics
- **Safety** — prompt injection protection, output filtering, and a `safe_refusal` path for blocked intents
- **Production deployment** — Dockerized with PostgreSQL and Redis, ready for horizontal scaling

---

## 🏗️ Architecture

```
User → FastAPI → LangGraph Execution → Response Streaming → Persistence → Observability
```

### System layers

| Layer | Technology | Purpose |
|---|---|---|
| API | FastAPI + SSE | Request handling, thread management, auth, rate limiting |
| Orchestration | LangGraph `StateGraph` | Stateful node execution, intent routing, checkpointing |
| Intelligence | LLM + RAG + Tools | Casual chat, knowledge Q&A, tool calling |
| Memory | LangGraph state + PostgreSQL | Short-term context and long-term user memory |
| Persistence | PostgreSQL + checkpointer | Conversation history, state snapshots, resume on failure |
| Observability | LangSmith + structured logs | Tracing, metrics, error tracking |

### LangGraph flow

```
START
  └─► ingest_user_message
        └─► load_context
              └─► route_intent
                    ├─► casual_chat ──────┐
                    ├─► knowledge_qa ─────┤
                    ├─► tool_request ─────┤
                    └─► safe_refusal ─────┘
                                          └─► postprocess_response
                                                └─► END
```

### ChatState schema

```python
class ChatState(TypedDict):
    messages: list        # Full conversation history
    user_id: str          # Identifies the user
    thread_id: str        # Identifies the conversation thread
    intent: str           # casual | knowledge | tool | blocked
    retrieved_docs: list  # Documents surfaced by RAG
    tool_results: list    # Results from tool execution
    response: str         # Final response streamed to client
```

---

## 📁 Project structure

```
chatbot-langgraph/
├── apps/
│   ├── api/                    # FastAPI application
│   │   ├── main.py             # App entrypoint, middleware, router mounts
│   │   ├── routes/             # Thread and message endpoints
│   │   ├── dependencies/       # Auth, DB session, graph instance
│   │   └── schemas/            # Pydantic request/response models
│   └── worker/
│       └── main.py             # Background task worker
│
├── src/
│   ├── graph/
│   │   ├── state.py            # ChatState TypedDict
│   │   ├── builder.py          # Graph wiring (nodes + edges)
│   │   ├── nodes/              # One file per node function
│   │   └── routing/            # choose_route() and intent logic
│   ├── llm/
│   │   ├── provider.py         # LLM client setup (Anthropic / OpenAI)
│   │   ├── prompts/            # Prompt templates per node
│   │   └── safety.py           # Output filtering and guardrails
│   ├── memory/
│   │   ├── short_term.py       # In-state conversation window management
│   │   └── long_term.py        # DB-backed user preferences and facts
│   ├── retrieval/
│   │   ├── pipeline.py         # End-to-end RAG orchestration
│   │   ├── retriever.py        # Vector store retrieval
│   │   └── reranker.py         # Cross-encoder reranking
│   ├── tools/
│   │   ├── registry.py         # Tool registration and lookup
│   │   ├── policies.py         # Validation, permissions, timeouts
│   │   └── implementations/    # Concrete tool implementations
│   ├── persistence/
│   │   ├── checkpoints.py      # LangGraph PostgreSQL checkpointer setup
│   │   ├── models.py           # SQLAlchemy ORM models
│   │   └── repositories/       # DB access layer per model
│   ├── observability/
│   │   ├── tracing.py          # LangSmith integration
│   │   ├── metrics.py          # Latency, token usage, error rate
│   │   └── logging.py          # Structured logging configuration
│   └── config/
│       ├── settings.py         # Pydantic settings (reads from .env)
│       └── feature_flags.py    # Runtime feature toggles
│
├── tests/
│   ├── unit/                   # Node function and utility tests
│   ├── integration/            # Graph execution and DB tests
│   ├── e2e/                    # Full API flow tests
│   └── evals/                  # LLM evaluation datasets and runners
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── scripts/
│   ├── seed_db.py              # Database seeding
│   └── run_evals.py            # Evaluation runner
│
├── .env.example
├── pyproject.toml
└── README.md
```

---

## 🚀 Getting started

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)

### 1. Clone and install

```bash
git clone https://github.com/your-username/chatbot-langgraph.git
cd chatbot-langgraph

pip install -e ".[dev]"
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

```env
ANTHROPIC_API_KEY=your-key-here
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/chatbot
REDIS_URL=redis://localhost:6379
LANGCHAIN_API_KEY=your-langsmith-key   # optional, for tracing
```

### 3. Start services with Docker

```bash
docker compose -f docker/docker-compose.yml up -d
```

### 4. Run database migrations

```bash
python scripts/seed_db.py
```

### 5. Start the API

```bash
uvicorn apps.api.main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

---

## 🔌 API reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/threads` | Create a new conversation thread |
| `POST` | `/threads/{id}/messages` | Send a message and receive a response |
| `GET` | `/threads/{id}` | Retrieve thread history |
| `GET` | `/threads/{id}/stream` | Stream a response via SSE |
| `GET` | `/health` | Health check |

### Example — send a message

```bash
curl -X POST http://localhost:8000/threads/my-thread/messages \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user-123",
    "content": "What is the capital of France?"
  }'
```

### Example — stream a response

```bash
curl -N http://localhost:8000/threads/my-thread/stream \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user-123", "content": "Explain LangGraph in simple terms"}'
```

---

## 🧪 Testing

```bash
# Unit tests
pytest tests/unit

# Integration tests (requires running DB)
pytest tests/integration

# End-to-end tests (requires full stack)
pytest tests/e2e

# Run LLM evaluations
python scripts/run_evals.py
```

---

## 🗺️ Roadmap

| Phase | Status | Scope |
|---|---|---|
| **Phase 1** | 🔧 In progress | Core graph, basic chat, memory, streaming |
| **Phase 2** | 📋 Planned | RAG pipeline, tool execution |
| **Phase 3** | 📋 Planned | LangSmith observability, security hardening, evals |
| **Phase 4** | 📋 Planned | Horizontal scaling, multi-agent extension, personalization |

---

## 🔒 Security

- JWT-based authentication on all endpoints
- Rate limiting per user and IP
- Input validation and sanitization on every request
- Output filtering to prevent sensitive data leakage
- Prompt injection detection in the safety layer
- Tool execution sandboxed with permission checks and timeouts

---

## 🛠️ Tech stack

| Component | Technology |
|---|---|
| API framework | [FastAPI](https://fastapi.tiangolo.com/) |
| Orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) |
| LLM providers | [Anthropic Claude](https://www.anthropic.com/) / [OpenAI](https://openai.com/) |
| Database | [PostgreSQL](https://www.postgresql.org/) via [SQLAlchemy](https://www.sqlalchemy.org/) |
| Cache | [Redis](https://redis.io/) |
| Observability | [LangSmith](https://smith.langchain.com/) |
| Packaging | [Hatchling](https://hatch.pypa.io/) + [pyproject.toml](https://peps.python.org/pep-0518/) |
| Linting | [Ruff](https://github.com/astral-sh/ruff) |
| Testing | [pytest](https://pytest.org/) + [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio) |
| Containerization | [Docker](https://www.docker.com/) + [Docker Compose](https://docs.docker.com/compose/) |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Commit your changes: `git commit -m 'feat: add your feature'`
4. Push to the branch: `git push origin feat/your-feature`
5. Open a Pull Request

Please follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.