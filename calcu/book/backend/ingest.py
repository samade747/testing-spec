import os
import glob
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams
from openai import OpenAI
from typing import List, Dict

# Load environment variables
load_dotenv()

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "calcu_book")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BOOK_DOCS_PATH = "./book/docs" # Path relative to backend/

# Initialize clients (will fail if dependencies are not installed)
try:
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    print(f"Failed to initialize clients. Ensure Qdrant and OpenAI dependencies are installed and environment variables are set: {e}")
    client = None
    openai_client = None


def get_markdown_files(path: str) -> List[str]:
    """Recursively gets all markdown files from a given path."""
    return glob.glob(os.path.join(path, '**/*.md'), recursive=True)

def chunk_text(text: str, file_path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Dict]:
    """
    Splits text into chunks. This is a very basic chunker;
    a more sophisticated one would handle code blocks, headings, etc.
    """
    # Placeholder for more advanced chunking logic
    chunks = []
    current_chunk = ""
    words = text.split()
    
    for word in words:
        if len(current_chunk) + len(word) + 1 > chunk_size:
            chunks.append({"text": current_chunk, "source": file_path})
            current_chunk = word
        else:
            current_chunk += (" " if current_chunk else "") + word
    if current_chunk:
        chunks.append({"text": current_chunk, "source": file_path})
    return chunks

def get_embeddings(text: str) -> List[float]:
    """Generates OpenAI embeddings for a given text."""
    if not openai_client:
        print("OpenAI client not initialized. Cannot generate embeddings.")
        return []
    try:
        response = openai_client.embeddings.create(
            input=text,
            model="text-embedding-ada-002" # Or other suitable model
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return []

def upsert_to_qdrant(chunks: List[Dict]):
    """Upserts chunks and their embeddings to Qdrant."""
    if not client:
        print("Qdrant client not initialized. Cannot upsert data.")
        return

    # Ensure collection exists and has correct vector parameters
    try:
        client.recreate_collection(
            collection_name=QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE) # size depends on embedding model
        )
    except Exception as e:
        print(f"Could not recreate collection (might already exist or API key issue): {e}")
        # Attempt to get collection info to check if it already exists or if there's an auth error
        try:
            client.get_collection(collection_name=QDRANT_COLLECTION_NAME)
        except Exception as get_e:
            print(f"Failed to get collection info, potential Qdrant configuration issue: {get_e}")
            return
    
    points = []
    for i, chunk in enumerate(chunks):
        embedding = get_embeddings(chunk["text"])
        if embedding:
            points.append(
                PointStruct(
                    id=f"{chunk['source']}-{i}", # Unique ID for each chunk
                    vector=embedding,
                    payload={"source": chunk["source"], "chunk_index": i, "text": chunk["text"]}
                )
            )
    
    if points:
        try:
            client.upsert(
                collection_name=QDRANT_COLLECTION_NAME,
                wait=True,
                points=points
            )
            print(f"Upserted {len(points)} points to Qdrant collection '{QDRANT_COLLECTION_NAME}'.")
        except Exception as e:
            print(f"Error upserting points to Qdrant: {e}")
    else:
        print("No points to upsert.")

def main():
    print("Starting data ingestion process...")
    markdown_files = get_markdown_files(BOOK_DOCS_PATH)
    all_chunks = []
    for file_path in markdown_files:
        print(f"Processing file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        chunks = chunk_text(content, file_path)
        all_chunks.extend(chunks)
    
    if all_chunks:
        print(f"Generated {len(all_chunks)} chunks. Upserting to Qdrant...")
        upsert_to_qdrant(all_chunks)
    else:
        print("No markdown content found or chunked.")

if __name__ == "__main__":
    main()