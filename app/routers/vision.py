from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from app.models.schemas import ApiResponse, SunlightAnalysisData, ScoringResponseData, SunlightType
from app.services.gemini_vision import analyze_sunlight_from_image
from app.services.scoring_engine import calculate_recommendations

router = APIRouter(prefix="/api/v1/ai", tags=["AI Vision & Analisis Lahan"])

@router.post("/analisis-cahaya", response_model=ApiResponse[SunlightAnalysisData])
async def endpoint_analisis_cahaya(
    foto: UploadFile = File(..., description="Foto pekarangan/lahan sisa (JPEG/PNG/WebP, max 10MB)")
):
    """
    Endpoint Vision kompatibel dengan Backend Express (POST /lahan/analisis-cahaya).
    Mengklasifikasikan paparan sinar matahari (FULL_SUN, PARTIAL_SUN, SHADE) dari foto pekarangan.
    """
    if foto.content_type not in ["image/jpeg", "image/png", "image/webp", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Format file harus berupa JPEG, PNG, atau WebP")

    image_bytes = await foto.read()
    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Ukuran file foto melebihi batas 10 MB")

    data = await analyze_sunlight_from_image(image_bytes, foto.content_type)
    return ApiResponse(success=True, data=data, message="Analisis citra lahan berhasil diselesaikan")

@router.post("/analisis-spot-lengkap")
async def endpoint_analisis_spot_lengkap(
    foto: UploadFile = File(..., description="Foto pekarangan atau spot rumah"),
    luas_m2: Optional[float] = Form(1.5, description="Perkiraan luas lahan dalam m² (default 1.5 m²)")
):
    """
    Endpoint Cerdas Terpadu:
    Menganalisis foto pekarangan → klasifikasi sinar → kalkulasi 15 rekomendasi komoditas + potensi penghematan belanja Rupiah.
    """
    if foto.content_type not in ["image/jpeg", "image/png", "image/webp", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Format file harus berupa JPEG, PNG, atau WebP")

    image_bytes = await foto.read()
    vision_result = await analyze_sunlight_from_image(image_bytes, foto.content_type)

    # Lakukan kalkulasi scoring otomatis berdasarkan hasil deteksi paparan sinar
    scoring_result = calculate_recommendations(
        luas_m2=max(0.25, luas_m2 or 1.5),
        paparan_sinar=vision_result.paparan_sinar
    )

    combined_data = {
        "analisis_cahaya": vision_result,
        "estimasi_penghematan_bulanan_top3": scoring_result.total_potensi_hemat_bulanan_top3,
        "rekomendasi_tertinggi": scoring_result.rekomendasi[:5],
        "catatan_ekonomi": f"Dengan menanam tanaman adaptif di spot ini, Anda berpotensi menghemat hingga Rp {scoring_result.total_potensi_hemat_bulanan_top3:,} per bulan."
    }

    return ApiResponse(
        success=True,
        data=combined_data,
        message="Analisis spot pekarangan dan kalkulasi rekomendasi panen berhasil"
    )
