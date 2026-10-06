"""Layanan Analisis Citra Pekarangan menggunakan Gemini Vision API (Google).
Menganalisis kondisi visual pekarangan/lahan sisa, intensitas bayangan gedung sekitar (shadowing effect),
dan mengklasifikasikan paparan sinar ke dalam FULL_SUN, PARTIAL_SUN, atau SHADE.
"""

import json
import re
from typing import Dict, Any, Tuple
from PIL import Image
import io

from app.config import settings
from app.models.schemas import SunlightType, SunlightAnalysisData

# Inisialisasi Google Generative AI
genai_client = None
if settings.has_gemini_key:
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        genai_client = genai
    except Exception as e:
        print(f"⚠️ Warning: Gagal mengonfigurasi google.generativeai: {e}")

VISION_PROMPT = """Anda adalah ahli agronomi perkotaan (Smart Urban Farming Specialist) untuk aplikasi Pekarang.in.
Tugas Anda adalah menganalisis foto pekarangan, teras, balkon, atau sudut sisa rumah yang diunggah pengguna.

Analisis kondisi mikroklimat lahan tersebut, khususnya:
1. Paparan Sinar Matahari:
   - FULL_SUN: Area terbuka tanpa atap/kanopi yang mendapat sinar matahari langsung minimal 6 jam sehari (terik, minim naungan dinding/pohon).
   - PARTIAL_SUN: Area yang mendapat sinar matahari langsung 3 hingga 6 jam sehari (ternaungi sebagian dinding tetangga, kanopi transparan, atau pohon peneduh).
   - SHADE: Area teduh yang mendapat sinar matahari langsung kurang dari 3 jam sehari (tertutup tembok tinggi, lorong sempit, atau kanopi gelap).

2. Karakteristik Fisik Spot:
   - Media (tanah langsung, lantai semen/keramik/paving yang butuh pot/polybag/vertikultur).
   - Keberadaan dinding vertikal untuk tanaman merambat atau rak vertikal.

3. Rekomendasi Tanaman Pangan Adaptif & Potensi Hemat:
   - Berikan 2-3 tanaman pangan yang paling cocok untuk spot ini (misal: Sawi, Kangkung, Bayam jika teduh; Cabai, Tomat, Terong jika terik).
   - Berikan perkiraan potensi penghematan belanja dapur dalam Rupiah (Rp).

KEMBALIKAN HANYA SEBUAH STRING JSON MURNI (tanpa format markdown triple-backtick, tanpa kata pengantar) dengan struktur persis seperti ini:
{
  "paparan_sinar": "FULL_SUN" | "PARTIAL_SUN" | "SHADE",
  "confidence": 0.88,
  "catatan": "Penjelasan ringkas 1-2 kalimat dalam Bahasa Indonesia mengenai kondisi bayangan tembok dan pencahayaan yang terdeteksi.",
  "kondisi_spot": "Penjelasan ringkas kondisi media tanam atau orientasi ruang (misal: Teras berubin paving dengan naungan tembok sisi barat).",
  "rekomendasi_utama": ["Sawi", "Kangkung", "Bayam"],
  "potensi_hemat_panen_rp": 45000
}
"""

def _clean_json_string(raw_text: str) -> str:
    """Membersihkan format markdown codeblock seperti ```json ... ``` dari respon LLM."""
    text = raw_text.strip()
    text = re.sub(r"^```(?:json)?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```$", "", text)
    return text.strip()

async def analyze_sunlight_from_image(image_bytes: bytes, mime_type: str = "image/jpeg") -> SunlightAnalysisData:
    """
    Menganalisis foto pekarangan dengan Gemini Vision.
    Jika API key belum disetel, menggunakan fallback agronomi cerdas untuk pengujian lokal.
    """
    if not settings.has_gemini_key or genai_client is None:
        # Fallback mode jika API key belum diisi di environment
        return SunlightAnalysisData(
            paparan_sinar=SunlightType.PARTIAL_SUN,
            confidence=0.85,
            catatan="[Dev Mode/Simulasi] Terdeteksi pencahayaan moderat dengan naungan parsial dari dinding bangunan sekitar.",
            kondisi_spot="Teras pekarangan semi-terbuka dengan potensi pemanfaatan pot atau polybag.",
            rekomendasi_utama=["Sawi", "Kangkung", "Bayam", "Kemangi"],
            potensi_hemat_panen_rp=40000
        )

    try:
        # Buka gambar menggunakan Pillow untuk validasi citra
        pil_image = Image.open(io.BytesIO(image_bytes))

        model = genai_client.GenerativeModel(settings.GEMINI_MODEL)
        response = model.generate_content([VISION_PROMPT, pil_image])
        raw_text = response.text.strip()

        cleaned_json = _clean_json_string(raw_text)
        data = json.loads(cleaned_json)

        # Validasi enum paparan sinar
        valid_paparan = [e.value for e in SunlightType]
        paparan = data.get("paparan_sinar", "PARTIAL_SUN").upper()
        if paparan not in valid_paparan:
            paparan = SunlightType.PARTIAL_SUN.value

        confidence = float(data.get("confidence", 0.85))
        confidence = max(0.0, min(1.0, confidence))

        return SunlightAnalysisData(
            paparan_sinar=SunlightType(paparan),
            confidence=round(confidence, 2),
            catatan=data.get("catatan", "Analisis pencahayaan lahan pekarangan selesai."),
            kondisi_spot=data.get("kondisi_spot"),
            rekomendasi_utama=data.get("rekomendasi_utama", ["Sawi", "Kangkung"]),
            potensi_hemat_panen_rp=data.get("potensi_hemat_panen_rp", 35000)
        )
    except Exception as err:
        print(f"❌ Error memanggil Gemini Vision: {err}")
        # Kembalikan hasil aman (graceful degradation)
        return SunlightAnalysisData(
            paparan_sinar=SunlightType.PARTIAL_SUN,
            confidence=0.75,
            catatan=f"Analisis citra visual dengan fallback terapan: {str(err)[:100]}",
            kondisi_spot="Kondisi mikroklimat perkotaan umum.",
            rekomendasi_utama=["Sawi", "Kangkung"],
            potensi_hemat_panen_rp=30000
        )
