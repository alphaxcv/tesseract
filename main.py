from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pytesseract
from PIL import Image
import io

app = FastAPI(title="Tesseract OCR API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ocr")
async def ocr(file: UploadFile, lang: str = "eng"):
    """Extract text from image using Tesseract OCR"""
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "File must be an image")
    
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        text = pytesseract.image_to_string(image, lang=lang)
        return {"text": text.strip(), "lang": lang}
    except Exception as e:
        raise HTTPException(500, str(e))
