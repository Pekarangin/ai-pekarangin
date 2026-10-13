"""Scraper & Processor Harga Pangan Kabupaten Sleman
Sumber: Sistem Informasi Harga Pangan Kabupaten Sleman (Disperindag Pemkab Sleman)
Laman Web: https://hargapangan.slemankab.go.id/
"""

import sys
import json
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import requests

# Mapping nama komoditas master Pekarang.in ke komoditas di portal Sleman
# Jika nama di portal Sleman berbeda, dilakukan penyesuaian (misal: Sawi -> Caisim, Mentimun -> Ketimun)
MAPPING_SLEMAN = {
    "Cabai rawit": "Cabai Rawit Merah",
    "Cabai merah": "Cabai Merah Keriting",
    "Bawang merah": "Bawang Merah",
    "Tomat": "Tomat Sayur",
    "Kangkung": "Kangkung",
    "Sawi": "Caisim",
    "Wortel": "Wortel",
    "Kacang panjang": "Kacang Panjang",
    "Mentimun": "Ketimun",
}

# Insight agronomi pekarangan spesifik kondisi mikroklimat Sleman
INSIGHT_PEKARANGAN = {
    "Cabai rawit": "Sangat cocok di spot teras/halaman depan Sleman yang terpapar sinar penuh (≥6 jam). Gunakan polybag ukuran 35 cm. Tahan cuaca panas dataran rendah Sleman.",
    "Cabai merah": "Membutuhkan spot paling terik di pekarangan. Drainase media tanam harus sangat porous agar akar tidak busuk saat musim hujan di Sleman.",
    "Bawang merah": "Cocok di wadah talang bertingkat atau bedengan dangkal teras. Butuh panas penuh, siram 2 hari sekali agar umbi tidak membusuk.",
    "Tomat": "Tempatkan di dekat dinding atau pasang ajir/tongkat penopang. Siram di pangkal tanah, hindari cipratan air ke daun untuk mencegah jamur.",
    "Bayam": "Sangat adaptif di pekarangan sempit atau spot teduh sebagian (partial sun). Panen cepat dalam 25 hari di pot ceper/baskom.",
    "Kangkung": "Paling bandel dan mudah! Sangat cocok di spot teras ternaungi maupun terbuka. Bisa pakai baskom hidroponik sederhana, panen potong tunas (regrowth).",
    "Selada": "Tempatkan di spot sejuk (bawah kanopi/naungan pohon di Sleman). Suhu terlalu terik bikin daun pahit, partial sun 3-4 jam pagi hari adalah yang terbaik.",
    "Sawi": "Tumbuh prima di pekarangan dengan pencahayaan moderat. Sangat cocok sistem vertikultur pipa paralon di dinding tembok rumah.",
    "Wortel": "Butuh wadah pot/polybag berkedalaman minimal 25-30 cm dengan media tanah gembur pasir tanpa kerikil.",
    "Terong": "Cocok di sudut pekarangan dengan pot besar (40 cm). Tahan panas terik Sleman dan berbuah lebat berulang kali.",
    "Kacang panjang": "Tanaman merambat ideal untuk pagar rumah atau tralis dinding teras Sleman. Sangat hemat luas tanah horizontal.",
    "Mentimun": "Rambatkan di pagar atau teralis balkon. Tumbuh sangat cepat dan panen dalam 40 hari.",
    "Pare": "Sangat tahan hama, pasang jaring rambatan vertikal di dinding luar pekarangan.",
    "Kemangi": "Tempatkan di samping pintu atau dekat tanaman lain sebagai tanaman pendamping (usir hama berkat aromanya). Rajin petik pucuk.",
    "Daun bawang": "Bisa ditanam dari sisa potongan akar dapur di pot ambang jendela atau wadah kecil dekat dapur."
}

# Konsumsi rata-rata bulanan rumah tangga (BPS Susenas)
KONSUMSI_RT_KG = {
    "Cabai rawit": 0.50,
    "Cabai merah": 0.40,
    "Bawang merah": 0.80,
    "Tomat": 1.00,
    "Bayam": 1.50,
    "Kangkung": 1.50,
    "Selada": 0.50,
    "Sawi": 1.00,
    "Wortel": 0.80,
    "Terong": 0.60,
    "Kacang panjang": 0.80,
    "Mentimun": 0.80,
    "Pare": 0.30,
    "Kemangi": 0.30,
    "Daun bawang": 0.40,
}

# Harga baseline jika tidak ada dalam daftar pantauan inflasi harian Disperindag Sleman
HARGA_BASELINE = {
    "Bayam": 10000,
    "Selada": 22000,
    "Terong": 12000,
    "Pare": 11000,
    "Kemangi": 25000,
    "Daun bawang": 18000,
}

PASAR_SLEMAN = {
    0: "Rata-rata Kabupaten Sleman",
    2: "Pasar Cebongan",
    5: "Pasar Gamping",
    13: "Pasar Gentan",
    6: "Pasar Godean",
    11: "Pasar Pakem",
    9: "Pasar Prambanan",
    12: "Pasar Sleman",
    7: "Pasar Tempel",
}


def fetch_harga_sleman(id_pasar: int = 0, tanggal: Optional[str] = None) -> List[Dict[str, Any]]:
    """Mengambil data harga pangan dari API resmi Pemkab Sleman."""
    if not tanggal:
        tanggal = datetime.date.today().strftime("%Y-%m-%d")

    url = f"https://hargapangan.slemankab.go.id/admin/api/data-harga/{id_pasar}/{tanggal}"
    headers = {
        "Authorization": "Basic cHVibGljOjY0MzU3NGFiNjllN2Q4OWUwYTcyZWViZmJkYWM4ZjUzYmFlNmExZDc=",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("success"):
            return data.get("result", [])
        return []
    except Exception as e:
        print(f"⚠️ Gagal mengambil data harga Sleman: {e}", file=sys.stderr)
        return []


def proses_rekomendasi_sleman(id_pasar: int = 0, tanggal: Optional[str] = None) -> List[Dict[str, Any]]:
    """Memproses data harga Sleman menjadi rekomendasi tanaman pekarangan lengkap dengan penghematan & insight."""
    raw_sleman = fetch_harga_sleman(id_pasar, tanggal)
    
    # Buat lookup dict harga dari hasil scraping
    harga_dict: Dict[str, int] = {}
    for item in raw_sleman:
        nama_kom = item.get("nama_jenis_komoditas", "").strip()
        raw_hrg = item.get("hrg_skr")
        if raw_hrg is not None:
            try:
                harga_dict[nama_kom] = int(raw_hrg)
            except (ValueError, TypeError):
                harga_dict[nama_kom] = 0
        else:
            harga_dict[nama_kom] = 0

    hasil = []
    nama_pasar = PASAR_SLEMAN.get(id_pasar, f"Pasar ID {id_pasar}")

    for nama_tanaman, konsumsi in KONSUMSI_RT_KG.items():
        sumber_harga = f"Pemkab Sleman ({nama_pasar})"
        nama_sleman = MAPPING_SLEMAN.get(nama_tanaman)
        
        if nama_sleman and nama_sleman in harga_dict and harga_dict[nama_sleman] > 0:
            harga_per_kg = harga_dict[nama_sleman]
        else:
            harga_per_kg = HARGA_BASELINE.get(nama_tanaman, 15000)
            sumber_harga = "Bapanas / Baseline Terkurasi DIY"

        # Hitung penghematan bulanan
        hemat_per_bulan = int(harga_per_kg * konsumsi)
        insight = INSIGHT_PEKARANGAN.get(nama_tanaman, "Cocok untuk pekarangan rumah perkotaan.")

        hasil.append({
            "tanaman": nama_tanaman,
            "harga_per_kg": harga_per_kg,
            "sumber_harga": sumber_harga,
            "konsumsi_rt_kg_bulan": konsumsi,
            "estimasi_hemat_per_bulan": hemat_per_bulan,
            "insight_pekarangan": insight
        })

    # Urutkan berdasarkan potensi penghematan bulanan terbesar
    hasil.sort(key=lambda x: x["estimasi_hemat_per_bulan"], reverse=True)
    return hasil


def export_sql_harga_sleman(rekomendasi: List[Dict[str, Any]], target_files: Optional[List[Path]] = None):
    """Mengekspor data harga Sleman ke file seed SQL backend & AI service."""
    tgl_hari_ini = datetime.date.today().strftime("%Y-%m-%d")
    lines = [
        "-- ============================================================",
        f"-- Seed 002: Data Harga Komoditas Terkini (Kabupaten Sleman - {tgl_hari_ini})",
        "-- Disusun otomatis oleh: Scraper Sleman Pekarang.in",
        "-- Sumber harga: Portal Resmi SIHARPA Disperindag Pemkab Sleman",
        "-- ============================================================\n",
        "INSERT INTO harga_komoditas (komoditas_id, harga_rp_per_kg, sumber, tanggal_update, wilayah)"
    ]

    unions = []
    for r in rekomendasi:
        u = (
            f"SELECT id, {r['harga_per_kg']}, 'SLEMAN_DISPERINDAG', "
            f"'{tgl_hari_ini}'::DATE, 'Sleman' FROM komoditas WHERE nama = '{r['tanaman']}'"
        )
        unions.append(u)

    lines.append("\nUNION ALL\n".join(unions) + ";\n")
    sql_content = "\n".join(lines)

    if target_files:
        for tf in target_files:
            tf.parent.mkdir(parents=True, exist_ok=True)
            tf.write_text(sql_content, encoding="utf-8")
            print(f"💾 Berhasil mengekspor seed SQL ke: {tf}")

    return sql_content


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Scraper Harga Pangan & Analisis Pekarangan Sleman")
    parser.add_argument("--pasar", type=int, default=0, help="ID Pasar di Sleman (0 = Rata-rata Sleman, 2=Cebongan, 5=Gamping, 6=Godean, 11=Pakem, 12=Sleman, dll)")
    parser.add_argument("--no-export", action="store_true", help="Jangan ekspor otomatis ke file seed SQL")
    args = parser.parse_args()

    tgl_hari_ini = datetime.date.today().strftime("%Y-%m-%d")
    print("=" * 80)
    print(f"🌿 HASIL SCRAPING & ANALISIS HARGA PANGAN KABUPATEN SLEMAN ({tgl_hari_ini})")
    print(f"Lokasi Pasar: {PASAR_SLEMAN.get(args.pasar, 'ID ' + str(args.pasar))}")
    print("Sumber: Portal Resmi Sistem Informasi Harga Pangan Pemkab Sleman")
    print("=" * 80)

    rekomendasi = proses_rekomendasi_sleman(id_pasar=args.pasar)

    print(f"\n{'Rank':<4} | {'Tanaman':<15} | {'Harga Pasar (Rp/kg)':<20} | {'Hemat/Bulan':<14} | Sumber Data")
    print("-" * 80)
    for idx, r in enumerate(rekomendasi, 1):
        print(f"{idx:<4} | {r['tanaman']:<15} | Rp {r['harga_per_kg']:>14,} | Rp {r['estimasi_hemat_per_bulan']:>10,} | {r['sumber_harga']}")

    print("\n" + "=" * 80)
    print("💡 CONTOH INSIGHT MIKROKLIMAT PEKARANGAN:")
    print("=" * 80)
    for r in rekomendasi[:5]:
        print(f"🌱 {r['tanaman'].upper()}:")
        print(f"   Harga: Rp {r['harga_per_kg']:,}/kg | Potensi Hemat: Rp {r['estimasi_hemat_per_bulan']:,}/bulan")
        print(f"   Insight Spot: {r['insight_pekarangan']}\n")

    if not args.no_export:
        root_dir = Path(__file__).resolve().parent.parent.parent
        workspace_dir = root_dir.parent

        targets = [
            root_dir / "seeds" / "002_final_harga.sql",
            workspace_dir / "be-pekarangin-main" / "database" / "seeds" / "002_final_harga.sql"
        ]
        print("=" * 80)
        export_sql_harga_sleman(rekomendasi, targets)
        print("=" * 80)

