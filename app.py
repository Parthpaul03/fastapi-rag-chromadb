from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import uvicorn
from chromadb.config import Settings
from chromadb import Client as DBClient
from chromadb import Document as DBDocument
from sentence_transformers import SentenceTransformer
from typing import List
import asyncio
import os

# Initialize FastAPI app
api = FastAPI()

# Load SentenceTransformer model (CPU)
embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Configure ChromaDB client for persistence
db_settings = Settings(chromadb_dir='database_files', persist=True)
db_client = DBClient(db_settings)

@app.post("/upload/", response_class=JSONResponse)
async def upload_documents(files: List[UploadFile] = File(...)):
    """ Endpoint to upload documents for processing """
    docs = []
    for file in files:
        # Read file contents
        file_content = await file.read()
        # Extract text from the file
        file_text = file_content.decode('utf-8')
        # Create a new document for ChromaDB
        document = DBDocument(text=file_text, metadata={'filename': file.filename})
        docs.append(document)

    # Create embeddings for the documents
    doc_embeddings = [embedder.encode(doc.text).tolist() for doc in docs]

    # Add documents to ChromaDB
    db_client.add(docs, doc_embeddings)
    return JSONResponse(content={"message": "Documents uploaded successfully"})


@app.get("/search/", response_class=JSONResponse)
async def search_documents(query: str):
    """ Endpoint to search documents """
    # Generate embedding for the query
    query_embedding = embedder.encode(query).tolist()

    # Query the database
    search_results = db_client.query(query_embedding)
    
    result_data = [
        {
            "filename": res.metadata['filename'],
            "similarity_score": res.score,
            "content": res.text
        }
        for res in search_results
    ]
    return JSONResponse(content={"matches": result_data})


@app.get("/docs/", response_class=JSONResponse)
async def list_documents():
    """ Endpoint to list all documents in the database """
    all_docs = db_client.get_all_documents()
    document_data = [
        {
            "filename": doc.metadata['filename'],
            "content": doc.text
        }
        for doc in all_docs
    ]
    return JSONResponse(content={"documents": document_data})


if __name__ == "__main__":
    # Start the API server
    uvicorn.run(api, host="0.0.0.0", port=8000, reload=True)
