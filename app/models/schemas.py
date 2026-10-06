from enum import Enum
from typing import List, Optional, Dict, Any, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")

class SunlightType(str, Enum):
    FULL_SUN = "FULL_SUN"
    PARTIAL_SUN = "PARTIAL_SUN"
    SHADE = "SHADE"

class KesesuaianBadge(str, Enum):
    COCOK = "COCOK"
    KURANG_COCOK = "KURANG_COCOK"
    TIDAK_COCOK = "TIDAK_COCOK"

class TingkatKesulitan(str, Enum):
    MUDAH = "MUDAH"
    SEDANG = "SEDANG"
    SULIT = "SULIT"

# Envelope response standar Pekarang.in (sesuai API Contract)
class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    message: Optional[str] = None

# ---- Schemas untuk Vision & Analisis Spot Pekarangan ----
class SunlightAnalysisData(BaseModel):
    paparan_sinar: SunlightType
    confidence: float = Field(..., ge=0.0, le=1.0)
    catatan: str
    kondisi_spot: Optional[str] = None
    rekomendasi_utama: Optional[List[str]] = None
    potensi_hemat_panen_rp: Optional[int] = None

# ---- Schemas untuk Crop Priority Scoring Engine ----
class ScoringRequest(BaseModel):
    luas_m2: float = Field(..., ge=0.25, description="Luas lahan pekarangan dalam m² (min 0.25 m²)")
    paparan_sinar: SunlightType = Field(..., description="Paparan sinar matahari: FULL_SUN, PARTIAL_SUN, atau SHADE")
    wilayah: Optional[str] = Field("Yogyakarta", description="Wilayah pasar harga pangan")

class CropRecommendationItem(BaseModel):
    nama: str
    skor_prioritas: float
    estimasi_hemat_rp_per_bulan: int
    estimasi_hemat_saat_panen: int
    waktu_panen_hari: int
    luas_dibutuhkan_m2: float
    tingkat_kesulitan: TingkatKesulitan
    kesesuaian_sinar: KesesuaianBadge
    harga_pasar_per_kg: int
    konsumsi_rt_kg_per_bulan: float
    jadwal_siram_hari: int
    jadwal_pupuk_hari: int
    panduan_singkat: str

class ScoringResponseData(BaseModel):
    luas_m2: float
    paparan_sinar: SunlightType
    harga_update_terakhir: str
    total_potensi_hemat_bulanan_top3: int
    rekomendasi: List[CropRecommendationItem]

# ---- Schemas untuk AI Farming Assistant (Chatbot) ----
class TanamanKonteks(BaseModel):
    nama: str
    hari_ke: Optional[int] = 1
    status: Optional[str] = "AKTIF"
    catatan_perawatan: Optional[str] = None

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    tanaman_aktif: Optional[TanamanKonteks] = None
    history: Optional[List[Dict[str, str]]] = None

class ChatResponseData(BaseModel):
    reply: str
    konteks_tanaman: Optional[Dict[str, Any]] = None
    tips_agronomi: Optional[List[str]] = None
