"""Data Master 15 Komoditas Pekarang.in
Hasil riset dan kurasi parameter agronomis & ekonomi oleh AI/Data Engineer.
Sumber data:
- Konsumsi RT/Bulan: BPS (Survei Sosial Ekonomi Nasional / Susenas)
- Harga Pasar: Badan Pangan Nasional (Bapanas) & PIHPS Bank Indonesia (Pilot: Yogyakarta)
- Parameter Tanam: Balai Penelitian Tanaman Sayuran (Balitsa) & Kementan RI
"""

from typing import List, Dict, Any

KOMODITAS_MASTER: List[Dict[str, Any]] = [
    {
        "nama": "Cabai rawit",
        "kebutuhan_sinar": "FULL_SUN",
        "luas_min_m2": 0.50,
        "luas_optimal_m2": 1.50,
        "waktu_panen_hari": 75,
        "konsumsi_rt_kg_per_bulan": 0.50,
        "tingkat_kesulitan": "SEDANG",
        "jadwal_siram_hari": 1,
        "jadwal_pupuk_hari": 14,
        "harga_pasar_per_kg": 85000,
        "estimasi_hasil_panen_per_m2_kg": 1.20,
        "panduan_singkat": "Tanam di spot sinar penuh minimal 6 jam. Siram pagi/sore hari secara konsisten. Pupuk NPK diberikan setiap 2 minggu."
    },
    {
        "nama": "Cabai merah",
        "kebutuhan_sinar": "FULL_SUN",
        "luas_min_m2": 0.50,
        "luas_optimal_m2": 1.50,
        "waktu_panen_hari": 80,
        "konsumsi_rt_kg_per_bulan": 0.40,
        "tingkat_kesulitan": "SEDANG",
        "jadwal_siram_hari": 1,
        "jadwal_pupuk_hari": 14,
        "harga_pasar_per_kg": 65000,
        "estimasi_hasil_panen_per_m2_kg": 1.50,
        "panduan_singkat": "Butuh sinar terik dan drainase baik agar akar tidak busuk. Jaga kelembaban tanah tanpa menggenang."
    },
    {
        "nama": "Bawang merah",
        "kebutuhan_sinar": "FULL_SUN",
        "luas_min_m2": 0.25,
        "luas_optimal_m2": 0.75,
        "waktu_panen_hari": 60,
        "konsumsi_rt_kg_per_bulan": 0.80,
        "tingkat_kesulitan": "SEDANG",
        "jadwal_siram_hari": 2,
        "jadwal_pupuk_hari": 14,
        "harga_pasar_per_kg": 40000,
        "estimasi_hasil_panen_per_m2_kg": 1.00,
        "panduan_singkat": "Tanam umbi bibit yang dipotong ujungnya 1/3 di tanah gembur. Hindari penyiraman berlebih untuk mencegah umbi busuk."
    },
    {
        "nama": "Tomat",
        "kebutuhan_sinar": "FULL_SUN",
        "luas_min_m2": 0.50,
        "luas_optimal_m2": 1.00,
        "waktu_panen_hari": 70,
        "konsumsi_rt_kg_per_bulan": 1.00,
        "tingkat_kesulitan": "SEDANG",
        "jadwal_siram_hari": 1,
        "jadwal_pupuk_hari": 14,
        "harga_pasar_per_kg": 14000,
        "estimasi_hasil_panen_per_m2_kg": 2.50,
        "panduan_singkat": "Pasang ajir atau tongkat penopang sejak tinggi 20 cm. Siram pangkal batang langsung, hindari menyiram daun terlalu basah."
    },
    {
        "nama": "Bayam",
        "kebutuhan_sinar": "PARTIAL_SUN",
        "luas_min_m2": 0.25,
        "luas_optimal_m2": 0.50,
        "waktu_panen_hari": 25,
        "konsumsi_rt_kg_per_bulan": 1.50,
        "tingkat_kesulitan": "MUDAH",
        "jadwal_siram_hari": 1,
        "jadwal_pupuk_hari": 7,
        "harga_pasar_per_kg": 12000,
        "estimasi_hasil_panen_per_m2_kg": 1.80,
        "panduan_singkat": "Super cepat panen (25 hari). Sangat cocok untuk pemula dan pekarangan sempit dengan intensitas cahaya moderat."
    },
    {
        "nama": "Kangkung",
        "kebutuhan_sinar": "PARTIAL_SUN",
        "luas_min_m2": 0.25,
        "luas_optimal_m2": 0.50,
        "waktu_panen_hari": 25,
        "konsumsi_rt_kg_per_bulan": 1.50,
        "tingkat_kesulitan": "MUDAH",
        "jadwal_siram_hari": 1,
        "jadwal_pupuk_hari": 7,
        "harga_pasar_per_kg": 10000,
        "estimasi_hasil_panen_per_m2_kg": 2.00,
        "panduan_singkat": "Dapat ditanam di pot, polybag atau baskom kecil. Panen dengan cara memotong pangkal agar dapat bertunas kembali (regrowth)."
    },
    {
        "nama": "Selada",
        "kebutuhan_sinar": "PARTIAL_SUN",
        "luas_min_m2": 0.25,
        "luas_optimal_m2": 0.50,
        "waktu_panen_hari": 30,
        "konsumsi_rt_kg_per_bulan": 0.50,
        "tingkat_kesulitan": "MUDAH",
        "jadwal_siram_hari": 1,
        "jadwal_pupuk_hari": 7,
        "harga_pasar_per_kg": 25000,
        "estimasi_hasil_panen_per_m2_kg": 1.20,
        "panduan_singkat": "Sangat adaptif di tempat teduh parsial (hindari terik siang agar tidak pahit). Panen daun dari lapisan terluar."
    },
    {
        "nama": "Sawi",
        "kebutuhan_sinar": "PARTIAL_SUN",
        "luas_min_m2": 0.25,
        "luas_optimal_m2": 0.50,
        "waktu_panen_hari": 30,
        "konsumsi_rt_kg_per_bulan": 1.00,
        "tingkat_kesulitan": "MUDAH",
        "jadwal_siram_hari": 1,
        "jadwal_pupuk_hari": 7,
        "harga_pasar_per_kg": 12000,
        "estimasi_hasil_panen_per_m2_kg": 1.60,
        "panduan_singkat": "Tumbuh cepat dan toleran naungan sebagian gedung. Pemupukan organik cair tiap minggu menghasilkan daun renyah."
    },
    {
        "nama": "Wortel",
        "kebutuhan_sinar": "FULL_SUN",
        "luas_min_m2": 0.25,
        "luas_optimal_m2": 0.75,
        "waktu_panen_hari": 75,
        "konsumsi_rt_kg_per_bulan": 0.80,
        "tingkat_kesulitan": "SEDANG",
        "jadwal_siram_hari": 2,
        "jadwal_pupuk_hari": 14,
        "harga_pasar_per_kg": 18000,
        "estimasi_hasil_panen_per_m2_kg": 1.40,
        "panduan_singkat": "Membutuhkan media tanam gembur tanpa batu kerikil dengan kedalaman minimal 25 cm agar umbi lurus sempurna."
    },
    {
        "nama": "Terong",
        "kebutuhan_sinar": "FULL_SUN",
        "luas_min_m2": 0.50,
        "luas_optimal_m2": 1.00,
        "waktu_panen_hari": 70,
        "konsumsi_rt_kg_per_bulan": 0.60,
        "tingkat_kesulitan": "SEDANG",
        "jadwal_siram_hari": 1,
        "jadwal_pupuk_hari": 14,
        "harga_pasar_per_kg": 15000,
        "estimasi_hasil_panen_per_m2_kg": 2.20,
        "panduan_singkat": "Butuh panas penuh dan ajir penopang saat buah mulai membesar. Bersihkan daun kuning bawah untuk mencegah jamur."
    },
    {
        "nama": "Kacang panjang",
        "kebutuhan_sinar": "FULL_SUN",
        "luas_min_m2": 0.50,
        "luas_optimal_m2": 1.00,
        "waktu_panen_hari": 45,
        "konsumsi_rt_kg_per_bulan": 0.80,
        "tingkat_kesulitan": "MUDAH",
        "jadwal_siram_hari": 1,
        "jadwal_pupuk_hari": 14,
        "harga_pasar_per_kg": 14000,
        "estimasi_hasil_panen_per_m2_kg": 1.80,
        "panduan_singkat": "Tanaman merambat vertikal, sangat hemat luas tanah! Pasang tiang atau jaring rambatan di dinding/pagar pekarangan."
    },
    {
        "nama": "Mentimun",
        "kebutuhan_sinar": "FULL_SUN",
        "luas_min_m2": 0.50,
        "luas_optimal_m2": 1.50,
        "waktu_panen_hari": 40,
        "konsumsi_rt_kg_per_bulan": 0.80,
        "tingkat_kesulitan": "MUDAH",
        "jadwal_siram_hari": 1,
        "jadwal_pupuk_hari": 14,
        "harga_pasar_per_kg": 10000,
        "estimasi_hasil_panen_per_m2_kg": 2.50,
        "panduan_singkat": "Tumbuh merambat cepat dan panen dalam 40 hari. Sediakan rambatan di teras dan siram teratur saat pembungaan."
    },
    {
        "nama": "Pare",
        "kebutuhan_sinar": "FULL_SUN",
        "luas_min_m2": 0.50,
        "luas_optimal_m2": 1.50,
        "waktu_panen_hari": 45,
        "konsumsi_rt_kg_per_bulan": 0.30,
        "tingkat_kesulitan": "MUDAH",
        "jadwal_siram_hari": 1,
        "jadwal_pupuk_hari": 14,
        "harga_pasar_per_kg": 12000,
        "estimasi_hasil_panen_per_m2_kg": 1.50,
        "panduan_singkat": "Tanaman merambat kuat dan tahan hama. Sangat cocok memanfaatkan dinding atau pagar teras sebagai bidang rambatan."
    },
    {
        "nama": "Kemangi",
        "kebutuhan_sinar": "PARTIAL_SUN",
        "luas_min_m2": 0.25,
        "luas_optimal_m2": 0.50,
        "waktu_panen_hari": 30,
        "konsumsi_rt_kg_per_bulan": 0.30,
        "tingkat_kesulitan": "MUDAH",
        "jadwal_siram_hari": 1,
        "jadwal_pupuk_hari": 7,
        "harga_pasar_per_kg": 30000,
        "estimasi_hasil_panen_per_m2_kg": 1.00,
        "panduan_singkat": "Aroma kuat membantu mengusir serangga hama lain. Petik pucuk daun secara rutin agar tanaman rimbun bercabang."
    },
    {
        "nama": "Daun bawang",
        "kebutuhan_sinar": "PARTIAL_SUN",
        "luas_min_m2": 0.25,
        "luas_optimal_m2": 0.50,
        "waktu_panen_hari": 45,
        "konsumsi_rt_kg_per_bulan": 0.40,
        "tingkat_kesulitan": "MUDAH",
        "jadwal_siram_hari": 2,
        "jadwal_pupuk_hari": 14,
        "harga_pasar_per_kg": 20000,
        "estimasi_hasil_panen_per_m2_kg": 1.30,
        "panduan_singkat": "Dapat ditanam dari sisa potongan akar dapur (kitchen scrap regrowth). Tumbuh subur di pot dangkal/ambang jendela."
    }
]

# Matriks Kesesuaian Cahaya (SSOT §2)
# Kebutuhan Tanaman vs Paparan Sinar Aktual Lahan
SUNLIGHT_MATRIX: Dict[str, Dict[str, float]] = {
    "FULL_SUN": {
        "FULL_SUN": 1.0,     # Sesuai
        "PARTIAL_SUN": 0.6,  # Kurang sesuai
        "SHADE": 0.2         # Tidak sesuai
    },
    "PARTIAL_SUN": {
        "FULL_SUN": 0.6,     # Kurang sesuai (risiko terbakar/terlalu panas)
        "PARTIAL_SUN": 1.0,  # Sesuai
        "SHADE": 0.6         # Kurang sesuai
    },
    "SHADE": {
        "FULL_SUN": 0.2,     # Tidak sesuai
        "PARTIAL_SUN": 0.6,  # Kurang sesuai
        "SHADE": 1.0         # Sesuai
    }
}
