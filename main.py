from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from ocr import extract_text
from openai_parser import parse_resume

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg"
}

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    # 🔴 Validate filename
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    # 🔴 Validate extension
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="File format not supported. Upload PDF, JPG, JPEG, or PNG only."
        )

    # 🔴 Validate MIME type (extra safety)
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type."
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_type = "pdf" if ext == "pdf" else "image"

    text = extract_text(file_path, file_type)
    if not text.strip():
        raise HTTPException(
            status_code=422,
            detail="Could not extract text from the uploaded resume."
        )

    parsed_data = parse_resume(text)

    return {
        "status": "success",
        "data": parsed_data
    }