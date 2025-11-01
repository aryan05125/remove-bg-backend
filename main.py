from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from rembg import remove
from PIL import Image
import io, os

# 🧩 Local Imports
from database import Base, engine
from models import User
from auth import router as auth_router

# ✅ Initialize FastAPI app
app = FastAPI(title="Background Remover API with Auth")

# ✅ Create database tables
Base.metadata.create_all(bind=engine)

# ✅ Allow frontend (React) access — CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include authentication routes
app.include_router(auth_router)

# ✅ Home route
@app.get("/")
def home():
    return {"message": "🖼️ Background Remover API is running with Authentication!"}

# ✅ Background remover endpoint
@app.post("/remove-bg/")
async def remove_background(file: UploadFile = File(...)):
    try:
        # Read image from upload
        input_image = Image.open(io.BytesIO(await file.read()))
        # Remove background using rembg
        output = remove(input_image)
        # Save output
        output_path = "output.png"
        output.save(output_path)
        print("✅ Background removed successfully! Saved as:", output_path)
        # Return file to frontend
        return FileResponse(output_path, media_type="image/png")
    except Exception as e:
        print("⚠️ Error:", e)
        raise HTTPException(status_code=500, detail=str(e))
