FROM python:3.14-slim

RUN pip install uv

WORKDIR /app

COPY . .

RUN uv pip install --system fastapi uvicorn[standard] google-genai google-adk

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "prompt_optimizer.api:app", "--host", "0.0.0.0", "--port", "8000"]
