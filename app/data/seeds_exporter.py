"""Script generator untuk mengekspor SQL Seeds dan JSON untuk tim Backend Pekarang.in.
Jalankan file ini untuk memperbarui file seed di folder `seeds/`.
"""

import json
from pathlib import Path
from datetime import date
from app.data.komoditas_master import KOMODITAS_MASTER

SEEDS_DIR = Path(__file__).resolve().parent.parent.parent / "seeds"
SEEDS_DIR.mkdir(parents=True, exist_ok=True)

def generate_sql_komoditas() -> str:
    lines = [
        "-- ============================================================",
        "-- Seed 001: Master Komoditas Pekarang.in (Final 15 Item)",
        "-- Disusun oleh: AI / Data Engineer (Dit Tolongin Dit)",
        "-- Sumber parameter: BPS Susenas, Balai Penelitian Tanaman Sayuran",
        "-- ============================================================\n",
        "INSERT INTO komoditas (nama, kebutuhan_sinar, luas_min_m2, luas_optimal_m2, waktu_panen_hari, konsumsi_rt_kg_per_bulan, tingkat_kesulitan, jadwal_siram_hari, jadwal_pupuk_hari, panduan_singkat)",
        "VALUES"
    ]

    values = []
    for k in KOMODITAS_MASTER:
        panduan_clean = k["panduan_singkat"].replace("'", "''")
        val = (
            f"  ('{k['nama']}', '{k['kebutuhan_sinar']}', {k['luas_min_m2']:.2f}, "
            f"{k['luas_optimal_m2']:.2f}, {k['waktu_panen_hari']}, "
            f"{k['konsumsi_rt_kg_per_bulan']:.2f}, '{k['tingkat_kesulitan']}', "
            f"{k['jadwal_siram_hari']}, {k['jadwal_pupuk_hari']}, '{panduan_clean}')"
        )
        values.append(val)

    lines.append(",\n".join(values))
    lines.append("ON CONFLICT (nama) DO UPDATE SET")
    lines.append("  kebutuhan_sinar = EXCLUDED.kebutuhan_sinar,")
    lines.append("  luas_min_m2 = EXCLUDED.luas_min_m2,")
    lines.append("  luas_optimal_m2 = EXCLUDED.luas_optimal_m2,")
    lines.append("  waktu_panen_hari = EXCLUDED.waktu_panen_hari,")
    lines.append("  konsumsi_rt_kg_per_bulan = EXCLUDED.konsumsi_rt_kg_per_bulan,")
    lines.append("  tingkat_kesulitan = EXCLUDED.tingkat_kesulitan,")
    lines.append("  jadwal_siram_hari = EXCLUDED.jadwal_siram_hari,")
    lines.append("  jadwal_pupuk_hari = EXCLUDED.jadwal_pupuk_hari,")
    lines.append("  panduan_singkat = EXCLUDED.panduan_singkat;\n")

    return "\n".join(lines)


def generate_sql_harga(wilayah: str = "Yogyakarta") -> str:
    today_str = date.today().isoformat()
    lines = [
        "-- ============================================================",
        f"-- Seed 002: Data Harga Komoditas Terkini ({wilayah})",
        "-- Disusun oleh: AI / Data Engineer (Dit Tolongin Dit)",
        "-- Sumber harga: Badan Pangan Nasional (Bapanas) & PIHPS BI",
        "-- ============================================================\n",
        "INSERT INTO harga_komoditas (komoditas_id, harga_rp_per_kg, sumber, tanggal_update, wilayah)"
    ]

    unions = []
    for k in KOMODITAS_MASTER:
        u = (
            f"SELECT id, {k['harga_pasar_per_kg']}, 'BAPANAS', "
            f"'{today_str}'::DATE, '{wilayah}' FROM komoditas WHERE nama = '{k['nama']}'"
        )
        unions.append(u)

    lines.append("\nUNION ALL\n".join(unions) + ";\n")
    return "\n".join(lines)


def export_all():
    # 1. SQL Komoditas
    sql_k_path = SEEDS_DIR / "001_final_komoditas.sql"
    sql_k_path.write_text(generate_sql_komoditas(), encoding="utf-8")

    # 2. SQL Harga
    sql_h_path = SEEDS_DIR / "002_final_harga.sql"
    sql_h_path.write_text(generate_sql_harga(), encoding="utf-8")

    # 3. JSON Data
    json_path = SEEDS_DIR / "data_15_komoditas.json"
    json_path.write_text(json.dumps(KOMODITAS_MASTER, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"✅ Seeds successfully generated in {SEEDS_DIR}")

if __name__ == "__main__":
    export_all()
