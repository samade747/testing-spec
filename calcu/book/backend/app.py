# app.py
import os
from fastapi import FastAPI
from pydantic import BaseModel
from qdrant_client import QdrantClient
import openai
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_KEY = os.getenv("QDRANT_API_KEY")
COLL = "calcu_book"

openai.api_key = OPENAI_KEY
qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_KEY)

app = FastAPI()

class QueryReq(BaseModel):
    question: str
    selectionText: str = None
    top_k: int = 4

def embed(text):
    resp = openai.Embedding.create(model="text-embedding-3-large", input=text)
    return resp['data'][0]['embedding']

@app.post("/query")
async def query(req: QueryReq):
    question = req.question
    selection = req.selectionText
    if selection:
        # strict mode: use only the selected text as context
        context_text = selection
    else:
        q_emb = embed(question)
        hits = qdrant.search(collection_name=COLL, query_vector=q_emb, limit=req.top_k)
        pieces = [h.payload.get("text","") for h in hits]
        context_text = "\n\n---\n\n".join(pieces)

    system = ("You are an assistant that MUST use ONLY the provided context to answer. "
              "If the answer is not in the context, reply exactly: \"I don't know from the provided text.\"")
    messages = [
        {"role":"system", "content": system},
        {"role":"user", "content": f"Context:\n{context_text}\n\nQuestion: {question}"}
    ]

    resp = openai.ChatCompletion.create(model="gpt-4o-mini", messages=messages, max_tokens=512)
    answer = resp['choices'][0]['message']['content']
    return {"answer": answer, "context_preview": context_text[:1000]}
