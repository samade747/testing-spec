# ingest.py
import os, glob, uuid
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
import openai
from markdown_it import MarkdownIt
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_KEY = os.getenv("QDRANT_API_KEY")
COLL = "calcu_book"

openai.api_key = OPENAI_KEY
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_KEY)

# create collection
collections = [c.name for c in client.get_collections().collections]
if COLL not in collections:
    client.recreate_collection(
        collection_name=COLL,
        vectors_config=rest.VectorParams(size=1536, distance=rest.Distance.COSINE),
    )

md = MarkdownIt()
def chunk_text(text, chunk_size=400, overlap=50):
    words = text.split()
    chunks=[]
    i=0
    while i < len(words):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def embed_text(text):
    r = openai.Embedding.create(model="text-embedding-3-large", input=text)
    return r['data'][0]['embedding']

def upsert_points(points):
    client.upsert(
        collection_name=COLL,
        points=points
    )

base = os.path.join(os.path.dirname(__file__), "../book/docs")
paths = glob.glob(os.path.join(base, "**/*.md"), recursive=True)
points=[]
for path in paths:
    with open(path, 'r', encoding='utf-8') as f:
        raw = f.read()
    plain = md.render(raw)
    chunks = chunk_text(plain)
    for idx, c in enumerate(chunks):
        emb = embed_text(c)
        payload = {"source": os.path.relpath(path, base), "chunk_index": idx, "text": c}
        points.append({"id": str(uuid.uuid4()), "vector": emb, "payload": payload})
        if len(points) >= 64:
            upsert_points(points)
            points=[]
if points:
    upsert_points(points)
print("Ingest complete. Indexed docs:", len(paths))
