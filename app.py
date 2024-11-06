from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import uvicorn
from chromadb.config import Settings
from chromadb import Client as ChromaClient
from chromadb import Document
from sentence_transformers import SentenceTransformer
from typing import List
import asyncio
import os

# Initialize FastAPI app
app = FastAPI()

# Load SentenceTransformer model (CPU)
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Configure ChromaDB client for persistence
settings = Settings(chromadb_dir='chroma_db', persist=True)
chroma_client = ChromaClient(settings)

@app.post("/ingest/", response_class=JSONResponse)
async def ingest_documents(files: List[UploadFile] = File(...)):
    """ Endpoint to ingest documents for retrieval """
    documents = []
    for file in files:
        # Read file contents
        content = await file.read()
        # Extract text from the document
        text = content.decode('utf-8')
        # Create a new document for ChromaDB
        doc = Document(text=text, metadata={'filename': file.filename})
        documents.append(doc)

    # Perform embedding for documents
    embeddings = [model.encode(doc.text).tolist() for doc in documents]

    # Add documents to ChromaDB
    chroma_client.add(documents, embeddings)
    return JSONResponse(content={"status": "Documents ingested successfully"})

@app.get("/query/", response_class=JSONResponse)
async def query_document(query: str):
    """ Endpoint to query documents """
    # Generate embedding for the query
    query_embedding = model.encode(query).tolist()
    
    # Query ChromaDB
    results = chroma_client.query(query_embedding)
    response = [
        {
            "filename": res.metadata['filename'],
            "score": res.score,
            "text": res.text
        }
        for res in results
    ]
    return JSONResponse(content={"results": response})

@app.get("/database/", response_class=JSONResponse)
async def get_database():
    """ Endpoint to view all documents in the database """
    documents = chroma_client.get_all_documents()
    response = [
        {
            "filename": doc.metadata['filename'],
            "text": doc.text
        }
        for doc in documents
    ]
    return JSONResponse(content={"documents": response})

if _name_ == "_main_":
    # Ensure the database is consistent and persists across sessions
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)