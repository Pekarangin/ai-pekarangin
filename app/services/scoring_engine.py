"""Crop Priority Scoring Engine — Pekarang.in
Formula Inti yang dirancang untuk kompetisi MAGE 12 ITS (SSOT §2 & PRD §4).
Menghasilkan ranking komoditas terukur dalam Rupiah berdasarkan kondisi mikro pekarangan.
"""

from datetime import date
from typing import List, Dict, Any
from app.data.komoditas_master import KOMODITAS_MASTER, SUNLIGHT_MATRIX
from app.models.schemas import (
    SunlightType,
    KesesuaianBadge,
    TingkatKesulitan,
    CropRecommendationItem,
    ScoringResponseData
)

def get_sunlight_factor(kebutuhan_sinar: str, paparan_lahan: str) -> float:
    """Mendapatkan koefisien kesesuaian cahaya (1.0, 0.6, atau 0.2)."""
    return SUNLIGHT_MATRIX.get(kebutuhan_sinar, {}).get(paparan_lahan, 0.6)

def map_kesesuaian_badge(factor: float) -> KesesuaianBadge:
    """Memetakan koefisien faktor cahaya ke label badge."""
    if factor >= 1.0:
        return KesesuaianBadge.COCOK
    elif factor >= 0.6:
        return KesesuaianBadge.KURANG_COCOK
    return KesesuaianBadge.TIDAK_COCOK

def calculate_crop_score(
    estimasi_hemat_per_bulan: float,
    luas_min_m2: float,
    waktu_panen_hari: int,
    sunlight_factor: float
) -> float:
    """
    Menghitung skor prioritas sesuai formula SSOT §2:
    Skor = (Estimasi_Hemat_Rp_per_bulan ÷ Luas_Kebutuhan_m2) ÷ Waktu_Panen_hari × Faktor_Kesesuaian_Cahaya
    """
    if luas_min_m2 <= 0 or waktu_panen_hari <= 0:
        return 0.0

    raw_score = (estimasi_hemat_per_bulan / luas_min_m2 / waktu_panen_hari) * sunlight_factor
    return round(raw_score, 2)

def calculate_recommendations(
    luas_m2: float,
    paparan_sinar: SunlightType,
    wilayah: str = "Yogyakarta"
) -> ScoringResponseData:
    """
    Menjalankan kalkulasi scoring komprehensif untuk luas dan paparan sinar tertentu.
    """
    results: List[CropRecommendationItem] = []

    for item in KOMODITAS_MASTER:
        harga_per_kg = item["harga_pasar_per_kg"]
        konsumsi_rt_bulan = item["konsumsi_rt_kg_per_bulan"]
        luas_min = item["luas_min_m2"]
        waktu_panen = item["waktu_panen_hari"]

        # 1. Estimasi hemat belanja dapur per bulan (Rp)
        # = Harga Pasar per kg x Konsumsi RT rata-rata per bulan (kg)
        estimasi_hemat_bulan = int(round(harga_per_kg * konsumsi_rt_bulan))

        # 2. Estimasi hemat saat masa panen tiba (Rp)
        # Berdasarkan durasi siklus panen atau perkiraan yield panen
        estimasi_hemat_panen = int(round((estimasi_hemat_bulan / 30.0) * waktu_panen))

        # 3. Faktor kesesuaian cahaya
        factor = get_sunlight_factor(item["kebutuhan_sinar"], paparan_sinar.value)
        badge = map_kesesuaian_badge(factor)

        # 4. Skor Prioritas Komoditas
        skor = calculate_crop_score(
            estimasi_hemat_per_bulan=estimasi_hemat_bulan,
            luas_min_m2=luas_min,
            waktu_panen_hari=waktu_panen,
            sunlight_factor=factor
        )

        # Penyesuaian jika luas pekarangan user lebih kecil dari luas minimal komoditas
        if luas_m2 < luas_min:
            # Penalti skor karena ruang tidak mencukupi untuk pertumbuhan optimal
            skor = round(skor * 0.5, 2)

        results.append(
            CropRecommendationItem(
                nama=item["nama"],
                skor_prioritas=skor,
                estimasi_hemat_rp_per_bulan=estimasi_hemat_bulan,
                estimasi_hemat_saat_panen=estimasi_hemat_panen,
                waktu_panen_hari=waktu_panen,
                luas_dibutuhkan_m2=luas_min,
                tingkat_kesulitan=TingkatKesulitan(item["tingkat_kesulitan"]),
                kesesuaian_sinar=badge,
                harga_pasar_per_kg=harga_per_kg,
                konsumsi_rt_kg_per_bulan=konsumsi_rt_bulan,
                jadwal_siram_hari=item["jadwal_siram_hari"],
                jadwal_pupuk_hari=item["jadwal_pupuk_hari"],
                panduan_singkat=item["panduan_singkat"]
            )
        )

    # Urutkan berdasarkan skor prioritas tertinggi ke terendah
    results.sort(key=lambda x: x.skor_prioritas, reverse=True)

    # Hitung total penghematan bulanan jika user menanam top 3 komoditas
    top_3_savings = sum(c.estimasi_hemat_rp_per_bulan for c in results[:3])

    return ScoringResponseData(
        luas_m2=luas_m2,
        paparan_sinar=paparan_sinar,
        harga_update_terakhir=date.today().isoformat(),
        total_potensi_hemat_bulanan_top3=top_3_savings,
        rekomendasi=results
    )
