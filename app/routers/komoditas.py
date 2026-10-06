from fastapi import APIRouter
from typing import List, Dict, Any
from app.models.schemas import ApiResponse
from app.data.komoditas_master import KOMODITAS_MASTER

router = APIRouter(prefix="/api/v1/ai", tags=["Master Komoditas & Riset Data"])

@router.get("/komoditas", response_model=ApiResponse[List[Dict[str, Any]]])
async def endpoint_list_komoditas():
    """Mengambil master data 15 komoditas pangan hasil riset AI/Data Engineer."""
    return ApiResponse(
        success=True,
        data=KOMODITAS_MASTER,
        message="Master 15 komoditas berhasil dimuat"
    )

@router.get("/komoditas/harga")
async def endpoint_harga_komoditas():
    """Mengambil rincian data harga pasar pangan terkini (Bapanas / PIHPS)."""
    harga_list = [
        {
            "nama": k["nama"],
            "harga_rp_per_kg": k["harga_pasar_per_kg"],
            "konsumsi_rt_kg_per_bulan": k["konsumsi_rt_kg_per_bulan"],
            "estimasi_hemat_rp_per_bulan": int(round(k["harga_pasar_per_kg"] * k["konsumsi_rt_kg_per_bulan"])),
            "sumber": "BAPANAS & PIHPS BI",
            "wilayah": "Yogyakarta"
        }
        for k in KOMODITAS_MASTER
    ]
    return ApiResponse(
        success=True,
        data=harga_list,
        message="Data harga komoditas berhasil dimuat"
    )
