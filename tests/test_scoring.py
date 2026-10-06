import pytest
from app.services.scoring_engine import (
    calculate_crop_score,
    get_sunlight_factor,
    calculate_recommendations
)
from app.models.schemas import SunlightType

def test_sunlight_factor():
    # FULL_SUN
    assert get_sunlight_factor("FULL_SUN", "FULL_SUN") == 1.0
    assert get_sunlight_factor("FULL_SUN", "PARTIAL_SUN") == 0.6
    assert get_sunlight_factor("FULL_SUN", "SHADE") == 0.2

    # PARTIAL_SUN
    assert get_sunlight_factor("PARTIAL_SUN", "PARTIAL_SUN") == 1.0
    assert get_sunlight_factor("PARTIAL_SUN", "FULL_SUN") == 0.6

    # SHADE
    assert get_sunlight_factor("SHADE", "SHADE") == 1.0
    assert get_sunlight_factor("SHADE", "FULL_SUN") == 0.2

def test_crop_priority_scoring_formula():
    # Formula: (Estimasi_Hemat_Rp ÷ Luas_m2) ÷ Waktu_Panen_hari × Faktor_Cahaya
    # Contoh: Sawi (Hemat 12000, Luas 0.25 m2, Panen 30 hari, Faktor 1.0)
    # (12000 / 0.25) / 30 * 1.0 = 48000 / 30 = 1600.0
    score = calculate_crop_score(
        estimasi_hemat_per_bulan=12000,
        luas_min_m2=0.25,
        waktu_panen_hari=30,
        sunlight_factor=1.0
    )
    assert score == 1600.0

def test_recommendations_ranking():
    response = calculate_recommendations(luas_m2=1.5, paparan_sinar=SunlightType.PARTIAL_SUN)
    assert len(response.rekomendasi) == 15
    # Cek ranking terurut menurun
    scores = [item.skor_prioritas for item in response.rekomendasi]
    assert scores == sorted(scores, reverse=True)
    # Di kondisi PARTIAL_SUN, tanaman sayuran cepat panen seperti Bayam/Kangkung/Sawi/Selada harus berada di jajaran atas
    top_crops = [item.nama for item in response.rekomendasi[:5]]
    assert any(c in top_crops for c in ["Bayam", "Kangkung", "Sawi", "Selada"])
