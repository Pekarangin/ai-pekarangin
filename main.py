"""Pekarang.in — AI & Machine Learning Microservice (FastAPI)
Kompetisi: MAGE 12 ITS (Tahap 2 Realisasi Karya)
Tim: Dit Tolongin Dit (Universitas AMIKOM Yogyakarta)
Role: AI / Machine Learning Engineer
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import vision, recommendation, komoditas, chat

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    Microservice AI & Machine Learning untuk Platform Pekarang.in.
    
    Fitur Utama:
    - 📷 Gemini Vision: Analisis citra spot pekarangan & klasifikasi paparan sinar (FULL_SUN, PARTIAL_SUN, SHADE).
    - 🧮 Crop Priority Scoring Engine: Formula optimasi komoditas pangan mikro perkotaan & estimasi penghematan Rupiah.
    - 🌾 Master Data 15 Komoditas: Parameter budidaya agronomis riil + harga pangan Bapanas/PIHPS.
    - 🤖 AI Farming Assistant: Chatbot konsultasi kontekstual budidaya pangan via Gemini API.
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware agar dapat diakses dari Mobile App (Expo) dan Backend Express
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(vision.router)
app.include_router(recommendation.router)
app.include_router(komoditas.router)
app.include_router(chat.router)

@app.get("/", tags=["Health Check"])
async def root():
    return {
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "gemini_api_configured": settings.has_gemini_key,
        "docs_url": "/docs"
    }

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {
        "status": "healthy",
        "gemini_key_available": settings.has_gemini_key
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
