from fastapi import FastAPI
from pydantic import BaseModel

from agent import run_agent


app = FastAPI(title="Support Agent")


class QueryRequest(BaseModel):
    question: str


@app.post("/ask")
def ask(request: QueryRequest):
    result = run_agent(request.question)
    return result