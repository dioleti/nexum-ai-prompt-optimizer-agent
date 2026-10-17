import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, APIRouter
from google.adk.runners import Runner
from google.adk.sessions.database_session_service import DatabaseSessionService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.genai import types

from prompt_optimizer.agent import root_agent
from prompt_optimizer.models import PredictResponse, PredictRequest

SESSION_DB_URL = "sqlite+aiosqlite:///memory.db"
ALLOWED_ORIGINS = ["http://localhost", "http://localhost:8080", "*"]

app = FastAPI(title="Prompt Optimizer API")
session_service = DatabaseSessionService(db_url=SESSION_DB_URL)
memory_service = InMemoryMemoryService()

runner = Runner(
    agent=root_agent,
    app_name="prompt_optimizer",
    session_service=session_service,
    memory_service=memory_service,
)

v1_router = APIRouter(prefix="/v1")
app.include_router(v1_router)

@v1_router.post("/optimize", response_model=PredictResponse)
async def predict(request: PredictRequest):
    try:
        app_name = "prompt_optimizer"
        user_id = "default_user"
        session_id = "default_session"

        session = await session_service.get_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )

        if not session:
            await session_service.create_session(
                app_name=app_name,
                user_id=user_id,
                session_id=session_id
            )

        user_message = types.Content(
            role="user",
            parts=[types.Part.from_text(text=request.prompt)]
        )

        def extract_text(obj) -> str:
            if not obj:
                return ""
            if hasattr(obj, "text") and obj.text:
                return obj.text
            if hasattr(obj, "parts") and obj.parts:
                texts = []
                for p in obj.parts:
                    if hasattr(p, "text") and p.text:
                        texts.append(p.text)
                if texts:
                    return "".join(texts)
            return ""

        final_response = ""

        async for event in runner.run_async(session_id=session_id, user_id=user_id, new_message=user_message):
            content = getattr(event, "content", None)
            token_usage = event.usage_metadata.total_token_count
            extracted = extract_text(content)
            if extracted:
                final_response = extracted
            elif hasattr(event, "text") and event.text:
                final_response = event.text

        if not final_response:
            final_response = "Nenhuma resposta gerada."

        return PredictResponse(optimized_prompt=final_response, total_token_usage=token_usage)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    load_dotenv()
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))