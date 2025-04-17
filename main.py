from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os
from io import BytesIO
from utils import extract_text_from_pdf, extract_text_from_docx, analyze_resume_with_gemini

app = FastAPI()

# Optional CORS support for API access
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# === Root endpoint to verify API is running ===
@app.get("/")
async def root():
    return {"message": "Resume Analyzer API is up and running!"}


# === FastAPI endpoint for analysis ===
@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".pdf", ".docx"]:
        return JSONResponse(status_code=400, content={"error": "Unsupported file type. Please upload a PDF or DOCX."})

    content = await file.read()
    file_stream = BytesIO(content)

    if ext == ".pdf":
        text = extract_text_from_pdf(file_stream)
    elif ext == ".docx":
        text = extract_text_from_docx(file_stream)

    result = analyze_resume_with_gemini(text)
    return {"analysis": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
