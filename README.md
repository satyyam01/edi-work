# Enrollment Operations - EDI Pipeline

An end-to-end fullstack platform for automating the extraction, ingestion, and validation of standardized EDI 834 (Benefit Enrollment and Maintenance) files.

It consists of three powerful systems tightly communicating:
- **Frontend App**: Next.js (React) visual application where caseworkers interact, upload `.edi` documents, and view status. 
- **FastAPI Backend**: Python-based API server bridging CORS cross-origins securely, ingesting the file directly to the local disk.
- **Python Data Pipeline**: Pure extraction algorithm that intelligently scans inputs, translates EDI syntax to clean `.json` dynamically isolated in sequence batch runs, and streams SQL inserts natively to a connected MySQL instance.

## Installation / Starting Fresh on a New System

### 1. Prerequisites 
Ensure you have the following installed on your machine:
- Node.js (v18+)
- Python (3.9+)
- MySQL Server (must be running globally or via Docker)

### 2. Setting Up MySQL Database 
Before running the app, the data tables need to exist. 

1. Boot up your MySQL Instance. 
2. Create your database (e.g. `CREATE DATABASE health_enroll;`)
3. Create a `.env` file in the root of the project directory with your credentials:
```env
DB_HOST="localhost"
DB_USER="root"
DB_PASSWORD="your_password"
DB_NAME="health_enroll"
```
4. Build the structure by running: `python db/table_creation.py`.

### 3. Setup the Python Backend
Install the required packages to support your APIs, data parsers, and MySQL connectors:
```bash
# Strongly recommend using an isolated virtual environment (venv or conda)
pip install fastapi uvicorn python-multipart mysql-connector-python python-dotenv
```

### 4. Setup the React Frontend
Navigate specifically into the `frontend` directory safely and install the web dependencies:
```bash
cd frontend
npm install
cd ..
```

---

## Operating Instructions 

To run the application and test the pipeline, you need two terminals active side-by-side. 

### Terminal 1 - The API Backend
Keep your backend booted so that Next.js has an endpoint to stream uploads into:
```bash
# In the root, start the FastAPI Application 
uvicorn server.main:app --reload
```

### Terminal 2 - The Next.js Interface
Serve your interface to your browser natively:
```bash
cd frontend
npm run dev
```

### Simulating a Pipeline Sync
Now that the server is up and running:
1. Open your browser and navigate to `http://localhost:3000/intake`.
2. Upload any `.edi` files using the drag-and-drop. You will see them process. (The backend streams them identically to the `data/EDI_834_DATA/` folder on your hard drive).
3. Open a terminal to trigger exactly your python pipeline routines sequentially: 
   - Parse them: `python parser.py` (You will see them intelligently output to `parsed_data/X/`)
   - Read and Push: `python db/load_to_db.py`

*(To wipe your Database completely for rapid isolated test runs without permanently damaging table schemas, execute `python db/clean_db.py`)*
