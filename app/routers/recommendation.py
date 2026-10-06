from fastapi import APIRouter
from app.models.schemas import ApiResponse, ScoringRequest, ScoringResponseData
from app.services.scoring_engine import calculate_recommendations

router = APIRouter(prefix="/api/v1/ai", tags=["Crop Priority Scoring Engine"])

@router.post("/rekomendasi", response_model=ApiResponse[ScoringResponseData])
async def endpoint_rekomendasi_scoring(request: ScoringRequest):
    """
    Menghitung ranking prioritas 15 komoditas pangan perkotaan berdasarkan formula SSOT §2.
    Mengembalikan estimasi penghematan bulanan (Rp), estimasi penghematan saat panen (Rp),
    waktu panen, luas kebutuhan, dan badge kecocokan sinar matahari.
    """
    result = calculate_recommendations(
        luas_m2=request.luas_m2,
        paparan_sinar=request.paparan_sinar,
        wilayah=request.wilayah or "Yogyakarta"
    )

    return ApiResponse(
        success=True,
        data=result,
        message="Perhitungan Crop Priority Scoring Engine berhasil"
    )
