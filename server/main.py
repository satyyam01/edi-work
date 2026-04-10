from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Allow frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Relative path pointing one directory up to the data/EDI_834_DATA folder
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "EDI_834_DATA"))

@app.get("/")
def read_root():
    return {"message": "HealthEnroll FastAPI Backend is Running!"}

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    # Ensure directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    file_path = os.path.join(DATA_DIR, file.filename)
    
    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        return {"success": True, "saved": [file.filename]}
    except Exception as e:
        print(f"Upload Error: {e}")
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail="Failed to upload file")