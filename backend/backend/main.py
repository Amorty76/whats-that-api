from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageOps
import io

app = FastAPI(title="What's That - MVP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(400, "Please upload an image.")
    raw = await file.read()
    try:
        img = ImageOps.exif_transpose(Image.open(io.BytesIO(raw)).convert("RGB"))
    except Exception as e:
        raise HTTPException(400, f"Bad image: {e}")
    w, h = img.size
    return {
        "best_guess": "MVP connected (no AI yet)",
        "confidence": None,
        "details": {"width": w, "height": h, "bytes": len(raw)}
    }
