-- ============================================================
-- Seed 002: Data Harga Komoditas Terkini (Kabupaten Sleman - 2026-11-09)
-- Disusun otomatis oleh: Scraper Sleman Pekarang.in
-- Sumber harga: SIHARPA Disperindag Sleman atau baseline DIY terkurasi
-- ============================================================

INSERT INTO harga_komoditas (komoditas_id, harga_rp_per_kg, sumber, tanggal_update, wilayah)
SELECT id, 60429, 'SLEMAN_DISPERINDAG', '2026-11-09'::DATE, 'Sleman' FROM komoditas WHERE nama = 'Cabai rawit'
UNION ALL
SELECT id, 63571, 'SLEMAN_DISPERINDAG', '2026-11-09'::DATE, 'Sleman' FROM komoditas WHERE nama = 'Cabai merah'
UNION ALL
SELECT id, 31143, 'SLEMAN_DISPERINDAG', '2026-11-09'::DATE, 'Sleman' FROM komoditas WHERE nama = 'Bawang merah'
UNION ALL
SELECT id, 10000, 'DIY_CURATED_BASELINE', '2026-10-13'::DATE, 'DIY' FROM komoditas WHERE nama = 'Bayam'
UNION ALL
SELECT id, 13429, 'SLEMAN_DISPERINDAG', '2026-11-09'::DATE, 'Sleman' FROM komoditas WHERE nama = 'Tomat'
UNION ALL
SELECT id, 14000, 'SLEMAN_DISPERINDAG', '2026-11-09'::DATE, 'Sleman' FROM komoditas WHERE nama = 'Wortel'
UNION ALL
SELECT id, 22000, 'DIY_CURATED_BASELINE', '2026-10-13'::DATE, 'DIY' FROM komoditas WHERE nama = 'Selada'
UNION ALL
SELECT id, 12714, 'SLEMAN_DISPERINDAG', '2026-11-09'::DATE, 'Sleman' FROM komoditas WHERE nama = 'Mentimun'
UNION ALL
SELECT id, 6500, 'SLEMAN_DISPERINDAG', '2026-11-09'::DATE, 'Sleman' FROM komoditas WHERE nama = 'Kangkung'
UNION ALL
SELECT id, 8286, 'SLEMAN_DISPERINDAG', '2026-11-09'::DATE, 'Sleman' FROM komoditas WHERE nama = 'Sawi'
UNION ALL
SELECT id, 9714, 'SLEMAN_DISPERINDAG', '2026-11-09'::DATE, 'Sleman' FROM komoditas WHERE nama = 'Kacang panjang'
UNION ALL
SELECT id, 25000, 'DIY_CURATED_BASELINE', '2026-10-13'::DATE, 'DIY' FROM komoditas WHERE nama = 'Kemangi'
UNION ALL
SELECT id, 12000, 'DIY_CURATED_BASELINE', '2026-10-13'::DATE, 'DIY' FROM komoditas WHERE nama = 'Terong'
UNION ALL
SELECT id, 18000, 'DIY_CURATED_BASELINE', '2026-10-13'::DATE, 'DIY' FROM komoditas WHERE nama = 'Daun bawang'
UNION ALL
SELECT id, 11000, 'DIY_CURATED_BASELINE', '2026-10-13'::DATE, 'DIY' FROM komoditas WHERE nama = 'Pare';
