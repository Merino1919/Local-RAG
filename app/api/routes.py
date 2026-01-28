from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.engine import RAGEngine
import shutil
import os

router = APIRouter()
engine = RAGEngine()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    upload_path = f"./app/data/uploads/{file.filename}"
    os.makedirs("./app/data/uploads", exist_ok=True)
    
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        msg = engine.ingest_document(upload_path)
        return {"message": msg}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query")
async def query_rag(question: str):
    try:
        response = engine.get_response(question)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))