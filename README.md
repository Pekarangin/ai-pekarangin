# 🌿 Pekarang.in — AI & Machine Learning Microservice

**Platform Rekomendasi Cerdas untuk Optimalisasi Pemanfaatan Pekarang Melalui Urban Farming**  
**Kompetisi:** MAGE 12 ITS — Tahap 2 (Realisasi Karya)  
**Tim:** Dit Tolongin Dit — Universitas AMIKOM Yogyakarta  
**Role:** AI / Machine Learning Engineer  

---

## 📌 Ringkasan Layanan AI

Microservice ini dibangun menggunakan **FastAPI (Python)** sesuai dengan **Arsitektur Sistem Proposal Bab 7.3**, yang bertindak sebagai mesin kecerdasan buatan terpisah untuk platform **Pekarang.in**:

1. **📷 Gemini Vision API Integration (`POST /api/v1/ai/analisis-cahaya`)**:
   - Menganalisis foto pekarangan/teras/balkon rumah pengguna.
   - Mengidentifikasi kondisi mikroklimat (bayangan tembok gedung sekitar / *shadowing effect*).
   - Mengklasifikasikan tingkat paparan sinar matahari: `FULL_SUN` (≥6 jam), `PARTIAL_SUN` (3–6 jam), atau `SHADE` (<3 jam).
   - Menghasilkan catatan agronomi praktis dan rekomendasi cepat jenis tanaman adaptif.

2. **🧮 Crop Priority Scoring Engine (`POST /api/v1/ai/rekomendasi`)**:
   - Menjalankan formula deterministik inti produk (SSOT §2):
     $$\text{Skor Prioritas} = \frac{\text{Estimasi Hemat Rp/bulan}}{\text{Luas Kebutuhan } m^2 \times \text{Waktu Panen (hari)}} \times \text{Faktor Kesesuaian Cahaya}$$
   - Menghitung potensi penghematan belanja dapur bulanan serta estimasi penghematan ketika panen tiba berdasarkan harga pasar riil (Bapanas / PIHPS) dan rata-rata konsumsi rumah tangga (BPS Susenas).

3. **🤖 AI Farming Assistant (`POST /api/v1/ai/chat`)**:
   - Chatbot pendampingan budidaya kontekstual via Gemini API (P3).
   - Menjawab pertanyaan kendala penanaman pemula (daun menguning, hama kutu putih, etiolasi, jadwal pupuk/siram) berdasarkan tanaman aktif dan hari pertumbuhan pengguna.

4. **🌾 Riset & Deliverable Data 15 Master Komoditas**:
   - Data agronomis valid untuk 15 komoditas pangan perkotaan.
   - Script generator SQL Seed (`seeds/001_final_komoditas.sql` & `seeds/002_final_harga.sql`) siap pakai untuk menggantikan dummy seed di backend tim.

---

## 📁 Struktur Direktori

```text
ai-pekarangin/
├── app/
│   ├── config.py                  # Konfigurasi environment & Gemini API
│   ├── data/
│   │   ├── komoditas_master.py    # Riset parameter 15 komoditas (BPS & Bapanas)
│   │   └── seeds_exporter.py      # Generator file seed SQL & JSON untuk Backend
│   ├── models/
│   │   └── schemas.py             # Skema Pydantic request & response
│   ├── routers/
│   │   ├── vision.py              # Endpoint analisis foto lahan
│   │   ├── recommendation.py      # Endpoint kalkulasi scoring & hemat Rp
│   │   ├── komoditas.py           # Endpoint data komoditas & harga
│   │   └── chat.py                # Endpoint AI Farming Assistant
│   └── services/
│       ├── gemini_vision.py       # Logika pemanggilan Gemini Vision
│       ├── scoring_engine.py      # Implementasi Crop Priority Scoring Engine
│       └── gemini_chat.py         # Logika prompt agronomi Gemini Chat
├── seeds/                         # Output file seed yang diserahkan ke Backend
│   ├── 001_final_komoditas.sql
│   ├── 002_final_harga.sql
│   └── data_15_komoditas.json
├── tests/
│   ├── test_scoring.py            # Unit test formula scoring
│   └── test_api.py                # Integration test FastAPI
├── demo_cli.py                    # Demo interaktif terminal untuk presentasi juri
├── requirements.txt               # Dependensi Python
├── Dockerfile                     # Kontainerisasi Docker
├── .env.example                   # Contoh konfigurasi environment
└── main.py                        # Entrypoint FastAPI
```

---

## 🚀 Cara Menjalankan Secara Lokal

### 1. Masuk ke Folder AI & Aktifkan Virtual Environment

```bash
cd ai-pekarangin
source venv/bin/activate
```

*(Jika membuat venv baru: `python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`)*

### 2. Atur Environment Variables

Salin `.env.example` ke `.env`:

```bash
cp .env.example .env
```

Buka `.env` dan isi `GEMINI_API_KEY` Anda dari [Google AI Studio](https://aistudio.google.com/apikey).  
*(Catatan: Jika API Key belum diisi, service otomatis berjalan dalam mode fallback simulasi cerdas sehingga tidak akan error/crash saat dites).*

### 3. Jalankan Server FastAPI

```bash
uvicorn main:app --reload --port 8000
```

- Server berjalan di: `http://localhost:8000`
- Dokumentasi Interaktif (Swagger UI): `http://localhost:8000/docs`
- Redoc UI: `http://localhost:8000/redoc`

### 4. Menjalankan Unit Test

```bash
pytest tests/
```

### 5. Menjalankan Demo Interaktif Terminal

```bash
python3 demo_cli.py
```

---

## 🔗 Integrasi dengan Backend Teman (`be-pekarangin-main`)

1. **Mengganti Data Dummy Backend**:
   Salin file hasil riset Anda dari `seeds/`:
   ```bash
   cp seeds/001_final_komoditas.sql ../be-pekarangin-main/database/seeds/
   cp seeds/002_final_harga.sql ../be-pekarangin-main/database/seeds/
   ```
2. **Koneksi Endpoint**:
   Backend Express dapat meneruskan request upload foto ke:
   `POST http://localhost:8000/api/v1/ai/analisis-cahaya`
   Atau aplikasi mobile dapat langsung memanggil endpoint ini.

---

## 🐙 Panduan Push ke GitHub (Repository Terpisah)

Agar pekerjaan Anda sebagai AI Engineer memiliki repository tersendiri di GitHub dan tidak bercampur dengan folder backend teman:

```bash
# 1. Masuk ke dalam folder ai-pekarangin
cd /home/dapin/Downloads/PekarangIn/ai-pekarangin

# 2. Inisialisasi Git
git init

# 3. Tambahkan seluruh file (venv dan .env sudah otomatis diabaikan oleh .gitignore)
git add .

# 4. Buat commit pertama
git commit -m "feat(ai): initial release of Pekarang.in AI Microservice (Gemini Vision + Scoring Engine + Chatbot)"

# 5. Buat repository baru di GitHub (misal: ai-pekarangin atau pekarangin-ai)
# 6. Hubungkan ke remote GitHub Anda (ganti URL dengan repository Anda):
git branch -M main
git remote add origin https://github.com/USERNAME_ANDA/ai-pekarangin.git

# 7. Push ke GitHub
git push -u origin main
```
