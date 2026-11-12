import io
import pytest
from fastapi.testclient import TestClient
from PIL import Image
from main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "online"
    assert "version" in json_data

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_komoditas_endpoint():
    response = client.get("/api/v1/ai/komoditas")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) == 15
    assert data[0]["nama"] == "Cabai rawit"

def test_komoditas_harga_endpoint_reports_price_metadata():
    response = client.get("/api/v1/ai/komoditas/harga")
    assert response.status_code == 200
    data = response.json()["data"]

    bawang = next(item for item in data if item["nama"] == "Bawang merah")
    bayam = next(item for item in data if item["nama"] == "Bayam")
    assert bawang["harga_rp_per_kg"] == 31143
    assert bawang["sumber"] == "SLEMAN_DISPERINDAG"
    assert bawang["tanggal_update"] == "2026-11-09"
    assert bawang["wilayah"] == "Sleman"
    assert bayam["sumber"] == "DIY_CURATED_BASELINE"
    assert bayam["tanggal_update"] == "2026-10-13"
    assert bayam["wilayah"] == "DIY"

def test_rekomendasi_scoring_endpoint():
    payload = {
        "luas_m2": 2.0,
        "paparan_sinar": "FULL_SUN",
        "wilayah": "Yogyakarta"
    }
    response = client.post("/api/v1/ai/rekomendasi", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert json_data["data"]["harga_update_terakhir"] == "2026-11-09"
    rekomendasi = json_data["data"]["rekomendasi"]
    assert len(rekomendasi) == 15
    assert rekomendasi[0]["nama"] == "Bawang merah"
    # Cabai rawit di full sun harus memiliki kecocokan COCOK
    cabai = next(c for c in rekomendasi if c["nama"] == "Cabai rawit")
    assert cabai["kesesuaian_sinar"] == "COCOK"

def test_analisis_cahaya_endpoint():
    # Buat dummy image in-memory
    file_bytes = io.BytesIO()
    image = Image.new("RGB", (100, 100), color="green")
    image.save(file_bytes, format="JPEG")
    file_bytes.seek(0)

    response = client.post(
        "/api/v1/ai/analisis-cahaya",
        files={"foto": ("test_lahan.jpg", file_bytes, "image/jpeg")}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert json_data["data"]["paparan_sinar"] in ["FULL_SUN", "PARTIAL_SUN", "SHADE"]

def test_chat_assistant_endpoint():
    payload = {
        "message": "Kenapa daun cabai saya menguning di hari ke-15?",
        "tanaman_aktif": {
            "nama": "Cabai rawit",
            "hari_ke": 15,
            "status": "AKTIF"
        }
    }
    response = client.post("/api/v1/ai/chat", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert "reply" in json_data["data"]
    assert len(json_data["data"]["reply"]) > 10
