"""Layanan Asisten Cerdas Urban Farming (Gemini Chatbot) — Pekarang.in
Menangani tanya jawab seputar kendala budidaya (daun menguning, hama, jadwal pupuk, etiolasi)
secara kontekstual berdasarkan tanaman aktif dan hari pertumbuhan pengguna.
"""

from typing import Dict, Any, List, Optional
from app.config import settings
from app.models.schemas import ChatResponseData, TanamanKonteks

genai_client = None
if settings.has_gemini_key:
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        genai_client = genai
    except Exception as e:
        print(f"⚠️ Warning: Gagal mengonfigurasi google.generativeai untuk chat: {e}")

CHAT_SYSTEM_PROMPT = """Anda adalah 'Pekarang.in AI Assistant' — asisten agronomi pintar dan ramah khusus pertanian perkotaan (urban farming).
Persona pengguna Anda adalah warga perkotaan awam (seperti Mas Budi, 32 tahun) yang memiliki lahan sangat terbatas, pernah gagal tanam (etiolasi/mati), dan ingin panduan praktis yang pasti berhasil untuk menghemat belanja dapur.

Prinsip Jawaban:
1. Praktis & Mengayomi: Gunakan Bahasa Indonesia yang ramah, santun, dan mudah dipahami tanpa jargon ilmiah rumit.
2. Solutif: Jika ada keluhan (misal daun menguning, hama kutu putih, batang loyo/etiolasi), langsung berikan diagnosis penyebab utama dan 2-3 langkah konkret untuk memperbaikinya.
3. Kontekstual: Selalu sesuaikan saran dengan jenis tanaman dan hari ke-berapa tanaman tersebut ditanam jika informasi tersedia.
4. Dorong Semangat: Berikan apresiasi agar pengguna tidak putus asa dalam merawat kebun mikronya.
"""

async def answer_farming_question(
    message: str,
    tanaman_aktif: Optional[TanamanKonteks] = None,
    history: Optional[List[Dict[str, str]]] = None
) -> ChatResponseData:
    """Menghasilkan respon konsultasi pertanian urban via Gemini API."""

    konteks_info = {}
    konteks_prompt = ""

    if tanaman_aktif:
        konteks_info = {
            "nama": tanaman_aktif.nama,
            "hari_ke": tanaman_aktif.hari_ke or 1,
            "status": tanaman_aktif.status or "AKTIF"
        }
        konteks_prompt = f"\n[Konteks Tanaman Pengguna: Tanaman {tanaman_aktif.nama}, saat ini memasuki Hari ke-{tanaman_aktif.hari_ke}. Status: {tanaman_aktif.status}]"

    if not settings.has_gemini_key or genai_client is None:
        # Fallback jawaban cerdas jika API key belum disetel
        t_nama = tanaman_aktif.nama if tanaman_aktif else "tanaman Anda"
        hari = tanaman_aktif.hari_ke if tanaman_aktif else 15
        reply = (
            f"Halo Sobat Pekarang! Untuk {t_nama} pada fase pertumbuhan (hari ke-{hari}), "
            f"kendala umum seperti daun menguning biasanya disebabkan oleh kelembaban tanah yang terlalu basah atau kurangnya asupan nitrogen. "
            f"Cobalah kurangi frekuensi siram jika media masih becek, dan tambahkan pupuk organik cair atau NPK seimbang sesuai jadwal. "
            f"Pastikan juga tanaman mendapatkan sirkulasi udara yang baik di pekarangan Anda."
        )
        return ChatResponseData(
            reply=reply,
            konteks_tanaman=konteks_info if tanaman_aktif else None,
            tips_agronomi=[
                "Cek kelembaban tanah dengan menusukkan jari sedalam 2 cm.",
                "Berikan pupuk pada pagi atau sore hari, jangan di siang terik.",
                "Pindahkan ke posisi yang lebih terang jika daun tampak pucat."
            ]
        )

    try:
        model = genai_client.GenerativeModel(
            settings.GEMINI_MODEL,
            system_instruction=CHAT_SYSTEM_PROMPT
        )

        full_prompt = f"{konteks_prompt}\nPengguna bertanya: {message}"
        response = model.generate_content(full_prompt)
        reply_text = response.text.strip()

        return ChatResponseData(
            reply=reply_text,
            konteks_tanaman=konteks_info if tanaman_aktif else None,
            tips_agronomi=[
                f"Pantau kelembaban media tanam {tanaman_aktif.nama if tanaman_aktif else 'kebun'} setiap pagi.",
                "Lakukan pemupukan berkala sesuai jadwal kalender tanam Pekarang.in."
            ]
        )
    except Exception as err:
        return ChatResponseData(
            reply=f"Maaf, saat ini asisten AI mengalami kendala koneksi: {str(err)[:100]}. Coba periksa koneksi internet atau API key Anda.",
            konteks_tanaman=konteks_info if tanaman_aktif else None,
            tips_agronomi=["Pastikan drainase pot/tanah bekerja dengan baik."]
        )
