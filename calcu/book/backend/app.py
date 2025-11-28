from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class QueryRequest(BaseModel):
    question: str
    selectionText: str | None = None

@app.get("/")
async def root():
    return {"message": "Calcu Backend is running!"}

@app.post("/query")
async def query(request: QueryRequest):
    # This is a placeholder. Actual RAG logic will go here.
    if request.selectionText:
        # Strict mode: answer only from selectionText
        if "example" in request.selectionText.lower():
            answer = f"You asked about '{request.question}' within the selection: '{request.selectionText}'. The selection contains the word 'example'."
        else:
            answer = "I don't know from the provided text."
        contexts = [{"text": request.selectionText, "source": "selection"}]
    else:
        # Global retrieval mode (placeholder)
        answer = f"You asked: '{request.question}'. This is a global retrieval placeholder response."
        contexts = [{"text": "Global context 1", "source": "book_chapter_1"}]
    
    return {"answer": answer, "contexts": contexts}

@app.post("/ingest")
async def ingest_data():
    # Placeholder for data ingestion logic
    return {"message": "Ingestion process started (placeholder)."}