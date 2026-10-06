"""Script Demo Interaktif Pekarang.in AI Engine
Dapat dijalankan langsung di terminal untuk menguji sistem rekomendasi dan scoring.
"""

from app.models.schemas import SunlightType
from app.services.scoring_engine import calculate_recommendations

def main():
    print("=" * 65)
    print("  🌱 PEKARANG.IN — SMART URBAN FARMING AI SCORING DEMO  ")
    print("  Kompetisi: MAGE 12 ITS (Tahap 2 Realisasi Karya)")
    print("  Tim: Dit Tolongin Dit (AMIKOM Yogyakarta)")
    print("=" * 65)

    print("\nSkenario Uji: Lahan Sempit Mas Budi (1.5 m² di teras rumah cluster)")
    print("Kondisi Sinar: PARTIAL_SUN (Ternaungi sebagian tembok tetangga)\n")

    result = calculate_recommendations(luas_m2=1.5, paparan_sinar=SunlightType.PARTIAL_SUN)

    print(f"{'No':<3} | {'Komoditas':<15} | {'Skor':<7} | {'Hemat/Bulan':<12} | {'Hemat Panen':<12} | {'Panen':<7} | {'Kesesuaian'}")
    print("-" * 85)

    for i, c in enumerate(result.rekomendasi[:10], start=1):
        print(
            f"{i:<3} | {c.nama:<15} | {c.skor_prioritas:<7.1f} | "
            f"Rp {c.estimasi_hemat_rp_per_bulan:<9,} | Rp {c.estimasi_hemat_saat_panen:<9,} | "
            f"{c.waktu_panen_hari} hari | {c.kesesuaian_sinar.value}"
        )

    print("-" * 85)
    print(f"\n💡 Total Potensi Hemat Belanja Dapur (Top 3 Komoditas): Rp {result.total_potensi_hemat_bulanan_top3:,} / bulan")
    print("=" * 85)

if __name__ == "__main__":
    main()
