from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.core.risk_detector import RiskDetector

app = FastAPI(title="The Equalizer API", version="0.1.0")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def read_root():
    return FileResponse('app/static/index.html')

# Core Models
detector = RiskDetector()

class AnalysisRequest(BaseModel):
    text: str

class AnalysisResponse(BaseModel):
    analysis: str

@app.post("/analyze", response_model=AnalysisResponse)
def analyze_document(request: AnalysisRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Text content is required")
    
    # Optional: Redact PII before sending to external API (Privacy by design)
    # clean_text = compliance.redact_pii(request.text) 
    
    result = detector.analyze_document(request.text)
    return AnalysisResponse(analysis=result)

# Simplifier Endpoint
from app.core.simplifier import DocumentSimplifier
simplifier = DocumentSimplifier()

@app.post("/simplify", response_model=AnalysisResponse)
def simplify_document(request: AnalysisRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Text content is required")
    
    result = simplifier.simplify_text(request.text)
    return AnalysisResponse(analysis=result)

# --- Phase 2: Voice & Translation ---
from app.core.voice_interface import VoiceInterface
voice = VoiceInterface()

class TranslationRequest(BaseModel):
    text: str
    target_language: str

@app.post("/voice/translate", response_model=AnalysisResponse)
def translate_advice(request: TranslationRequest):
    if not request.text or not request.target_language:
         raise HTTPException(status_code=400, detail="Text and target language are required")
    
    result = voice.translate_to_mother_tongue(request.text, request.target_language)
    return AnalysisResponse(analysis=result)

import fitz  # PyMuPDF
import io

@app.post("/analyze/file")
async def analyze_file(file: UploadFile = File(...)):
    allowed_docs = ('.pdf', '.txt')
    allowed_images = ('.jpg', '.jpeg', '.png', '.webp')
    
    filename_lc = file.filename.lower()
    if not filename_lc.endswith(allowed_docs + allowed_images):
        raise HTTPException(status_code=400, detail="Only PDF, TXT, and images (JPG, PNG, WEBP) are supported")
    
    if filename_lc.endswith('.pdf'):
        pdf_content = await file.read()
        doc = fitz.open(stream=pdf_content, filetype="pdf")
        text_content = ""
        image_parts = []
        
        for page in doc:
            text_content += page.get_text()
            # Extract images from page
            image_list = page.get_images(full=True)
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_parts.append({
                    "mime_type": f"image/{base_image['ext']}",
                    "data": image_bytes
                })
        
        # Send text and found images for analysis
        # Limit images to avoid hitting limits (Gemini handles many but let's be safe)
        if len(image_parts) > 10:
            image_parts = image_parts[:10]
            
        # We need a way to pass multiple images to RiskDetector. 
        # For now, let's just use the first page's text if there are too many images, 
        # or combine them. RiskDetector handles one image. 
        # Let's update RiskDetector to handle list of parts.
        
        result = detector.analyze_document(text_content=text_content, image_data=image_parts[0]['data'] if image_parts else None, mime_type=image_parts[0]['mime_type'] if image_parts else None)
    elif filename_lc.endswith(allowed_images):
        image_data = await file.read()
        mime_type = file.content_type or "image/jpeg"
        result = detector.analyze_document(image_data=image_data, mime_type=mime_type)
    else:
        content = (await file.read()).decode('utf-8')
        result = detector.analyze_document(text_content=content)

    return AnalysisResponse(analysis=result)

@app.post("/simplify/file")
async def simplify_file(file: UploadFile = File(...)):
    allowed_docs = ('.pdf', '.txt')
    allowed_images = ('.jpg', '.jpeg', '.png', '.webp')

    filename_lc = file.filename.lower()
    if not filename_lc.endswith(allowed_docs + allowed_images):
        raise HTTPException(status_code=400, detail="Only PDF, TXT, and images (JPG, PNG, WEBP) are supported")
    
    if filename_lc.endswith('.pdf'):
        pdf_content = await file.read()
        doc = fitz.open(stream=pdf_content, filetype="pdf")
        text_content = ""
        for page in doc:
            text_content += page.get_text()
        result = simplifier.simplify_text(text_content=text_content)
    elif filename_lc.endswith(allowed_images):
        image_data = await file.read()
        mime_type = file.content_type or "image/jpeg"
        result = simplifier.simplify_text(image_data=image_data, mime_type=mime_type)
    else:
        content = (await file.read()).decode('utf-8')
        result = simplifier.simplify_text(text_content=content)

    return AnalysisResponse(analysis=result)

# TTS Endpoint using gTTS - TEMPORARILY DISABLED DUE TO VENV ISSUE
# from gTTS import gTTS
# from fastapi.responses import StreamingResponse
# import io
# 
# class SpeakRequest(BaseModel):
#     text: str
#     language: str
# 
# @app.post("/voice/speak")
# def speak_text(request: SpeakRequest):
#     if not request.text:
#        raise HTTPException(status_code=400, detail="Text is required")
#     
#     # Map full language names to gTTS codes
#     lang_map = {
#         'Spanish': 'es', 'French': 'fr', 'Hindi': 'hi',
#         'Tamil': 'ta', 'Telugu': 'te', 'Kannada': 'kn', 'Malayalam': 'ml',
#         'Marathi': 'mr', 'Bengali': 'bn', 'Gujarati': 'gu', 'Punjabi': 'pa',
#         'Chinese': 'zh-cn', 'Arabic': 'ar'
#     }
#     lang_code = lang_map.get(request.language, 'en')
# 
#     # Generate MP3 in memory
#     tts = gTTS(text=request.text, lang=lang_code)
#     mp3_fp = io.BytesIO()
#     tts.write_to_fp(mp3_fp)
#     mp3_fp.seek(0)
#     
#     return StreamingResponse(mp3_fp, media_type="audio/mpeg")

# --- Phase 3: Action Engine ---
from app.core.action_engine import ActionEngine
import os
action_engine = ActionEngine()

class DocumentGenerationRequest(BaseModel):
    template_name: str # e.g., "parking_appeal_template.txt"
    region: str
    case_details: dict

@app.post("/action/generate", response_model=AnalysisResponse)
def generate_document(request: DocumentGenerationRequest):
    # Sanitize path to prevent directory traversal
    template_path = os.path.join("app", "templates", os.path.basename(request.template_name))
    
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="Template not found")

    result = action_engine.generate_document(template_path, request.case_details, request.region)
    return AnalysisResponse(analysis=result)

# --- Phase 4: Compliance ---
from app.core.compliance import ComplianceManager
compliance = ComplianceManager()

@app.post("/compliance/redact", response_model=AnalysisResponse)
def redact_pii(request: AnalysisRequest):
     result = compliance.redact_pii(request.text)
     return AnalysisResponse(analysis=result)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
