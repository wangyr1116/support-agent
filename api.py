from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
from fastapi.responses import FileResponse
from agent import run_agent


app = FastAPI(title="Support Agent")


class QueryRequest(BaseModel):
    question: str


@app.post("/ask")
def ask(request: QueryRequest):
    result = run_agent(request.question)
    return result

@app.get("/")
def home():
    page = Path(__file__).resolve().parent / "static" / "index.html"
    return FileResponse(page)