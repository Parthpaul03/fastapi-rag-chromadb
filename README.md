FastAPI Document Ingestion and Retrieval API

This FastAPI application provides an API for ingesting, querying, and retrieving documents using ChromaDB for persistent storage and SentenceTransformer for embeddings. It allows users to upload files, query text against the database, and view stored documents.

Features:

Document Ingestion: Upload and store text documents with metadata in ChromaDB.
Query Documents: Perform semantic search against stored documents using SentenceTransformer embeddings.
View Database: Retrieve all stored documents and metadata from ChromaDB.
Tech Stack:

FastAPI: Web framework for building APIs.
ChromaDB: Persistent vector database for storing and querying documents.
SentenceTransformer: Pre-trained transformer models for text embeddings.
Uvicorn: ASGI server for running the FastAPI application.
Installation

Prerequisites:

Python 3.8+
pip (Python package manager)
Setup Instructions
Clone the repository or download the source code:

bash
Copy code
git clone <repository-url>
cd <repository-folder>
Create and activate a virtual environment:

bash
Copy code
python -m venv venv
# Activate on Windows
venv\Scripts\activate
# Activate on macOS/Linux
source venv/bin/activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Run the application:

bash
Copy code
python main.py
Access the API:

Swagger UI: http://127.0.0.1:8000/docs
Redoc: http://127.0.0.1:8000/redoc
API Endpoints
1. Ingest Documents
Endpoint: /ingest/
Method: POST
Description: Upload text files to ingest into ChromaDB.
Request Body:
List of files (e.g., PDF, TXT).
Response:
json
Copy code
{
  "status": "Documents ingested successfully"
}
2. Query Documents
Endpoint: /query/
Method: GET
Description: Perform a semantic search query against stored documents.
Query Parameter:
query (string): The search query text.
Response:
json
Copy code
{
  "results": [
    {
      "filename": "example.txt",
      "score": 0.85,
      "text": "Document content here..."
    }
  ]
}
3. View All Documents
Endpoint: /database/
Method: GET
Description: Retrieve all documents stored in ChromaDB.
Response:
json
Copy code
{
  "documents": [
    {
      "filename": "example.txt",
      "text": "Document content here..."
    }
  ]
}
Project Structure
bash
Copy code
├── main.py               # FastAPI application code
├── requirements.txt      # List of dependencies
├── venv/                 # Virtual environment folder
└── chroma_db/            # Persistent database storage
Development
Run in Development Mode
To enable hot-reloading during development, use Uvicorn with the --reload flag:

bash
Copy code
uvicorn main:app --reload
Troubleshooting
1. Missing Dependencies
Ensure all dependencies are installed:

bash
Copy code
pip install -r requirements.txt
2. CMake/Ninja Issues
Install required build tools as per the instructions in the error logs.

Contributing
Contributions are welcome! Feel free to submit issues or pull requests.

License
This project is licensed under the MIT License.