from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="LangGraph Chatbot API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


# TODO: mount routers
# from apps.api.routes import threads, messages
# app.include_router(threads.router, prefix="/threads")
# app.include_router(messages.router, prefix="/threads")
