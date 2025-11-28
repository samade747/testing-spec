from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from qdrant_client import QdrantClient, models
from openai import OpenAI
import os
import httpx # Added for explicit http client configuration

load_dotenv()
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "calcu_book") # Default to 'calcu_book' if not set
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") # This seems to load correctly
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # This seems to load correctly

if not all([QDRANT_API_KEY, OPENAI_API_KEY]): # Only validate API keys now
    raise ValueError("Missing one or more environment variables for Qdrant or OpenAI.")

qdrant_client = QdrantClient(
    host=QDRANT_HOST,
    api_key=QDRANT_API_KEY, # Use the loaded API key
)
openai_client = OpenAI(
    api_key=OPENAI_API_KEY,
    http_client=httpx.Client() # Pass httpx.Client without proxies argument
)

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class QueryRequest(BaseModel):
    question: str
    selectionText: str | None = None

async def get_embedding(text: str):
    response = openai_client.embeddings.create(input=text, model="text-embedding-ada-002")
    return response.data[0].embedding

async def retrieve_context(query: str):
    query_embedding = await get_embedding(query)

    search_result = qdrant_client.query_points(
        collection_name=QDRANT_COLLECTION_NAME,
        query_embedding=query_embedding,
        limit=3, # Retrieve top 3 relevant results
        append_payload=True, # Include payload (original text and source)
    )

    context_texts = [point.payload["text"] for point in search_result.points if point.payload]
    contexts = [
        {"text": point.payload["text"], "source": point.payload["source"]}
        for point in search_result.points if point.payload
    ]
    return context_texts, contexts


@app.get("/")
async def root():
    return {"message": "Calcu Backend is running!"}

@app.post("/query")
async def query(request: QueryRequest):
        retrieved_texts, contexts = await retrieve_context(request.question)

        prompt_messages = [
            {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context. If the answer is not in the context, say 'I don't know'."},
            {"role": "user", "content": f"Context: {' '.join(retrieved_texts)}\n\nQuestion: {request.question}"}
        ]

        if request.selectionText:
            # Add selection text to the prompt for strict mode
            prompt_messages.append({"role": "user", "content": f"Also consider this selected text: {request.selectionText}"})
            # Prioritize selected text in the contexts if it makes sense, or ensure it's included.
            # For simplicity, we'll just add it as an additional context for now.
            contexts.insert(0, {"text": request.selectionText, "source": "user_selection"})


        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=prompt_messages
        )
        answer = response.choices[0].message.content
        return {"answer": answer, "contexts": contexts}

@app.post("/ingest")
async def ingest_data():
    # Placeholder for data ingestion logic
    return {"message": "Ingestion process started (placeholder)."}