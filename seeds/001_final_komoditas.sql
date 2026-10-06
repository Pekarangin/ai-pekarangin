-- ============================================================
-- Seed 001: Master Komoditas Pekarang.in (Final 15 Item)
-- Disusun oleh: AI / Data Engineer (Dit Tolongin Dit)
-- Sumber parameter: BPS Susenas, Balai Penelitian Tanaman Sayuran
-- ============================================================

INSERT INTO komoditas (nama, kebutuhan_sinar, luas_min_m2, luas_optimal_m2, waktu_panen_hari, konsumsi_rt_kg_per_bulan, tingkat_kesulitan, jadwal_siram_hari, jadwal_pupuk_hari, panduan_singkat)
VALUES
  ('Cabai rawit', 'FULL_SUN', 0.50, 1.50, 75, 0.50, 'SEDANG', 1, 14, 'Tanam di spot sinar penuh minimal 6 jam. Siram pagi/sore hari secara konsisten. Pupuk NPK diberikan setiap 2 minggu.'),
  ('Cabai merah', 'FULL_SUN', 0.50, 1.50, 80, 0.40, 'SEDANG', 1, 14, 'Butuh sinar terik dan drainase baik agar akar tidak busuk. Jaga kelembaban tanah tanpa menggenang.'),
  ('Bawang merah', 'FULL_SUN', 0.25, 0.75, 60, 0.80, 'SEDANG', 2, 14, 'Tanam umbi bibit yang dipotong ujungnya 1/3 di tanah gembur. Hindari penyiraman berlebih untuk mencegah umbi busuk.'),
  ('Tomat', 'FULL_SUN', 0.50, 1.00, 70, 1.00, 'SEDANG', 1, 14, 'Pasang ajir atau tongkat penopang sejak tinggi 20 cm. Siram pangkal batang langsung, hindari menyiram daun terlalu basah.'),
  ('Bayam', 'PARTIAL_SUN', 0.25, 0.50, 25, 1.50, 'MUDAH', 1, 7, 'Super cepat panen (25 hari). Sangat cocok untuk pemula dan pekarangan sempit dengan intensitas cahaya moderat.'),
  ('Kangkung', 'PARTIAL_SUN', 0.25, 0.50, 25, 1.50, 'MUDAH', 1, 7, 'Dapat ditanam di pot, polybag atau baskom kecil. Panen dengan cara memotong pangkal agar dapat bertunas kembali (regrowth).'),
  ('Selada', 'PARTIAL_SUN', 0.25, 0.50, 30, 0.50, 'MUDAH', 1, 7, 'Sangat adaptif di tempat teduh parsial (hindari terik siang agar tidak pahit). Panen daun dari lapisan terluar.'),
  ('Sawi', 'PARTIAL_SUN', 0.25, 0.50, 30, 1.00, 'MUDAH', 1, 7, 'Tumbuh cepat dan toleran naungan sebagian gedung. Pemupukan organik cair tiap minggu menghasilkan daun renyah.'),
  ('Wortel', 'FULL_SUN', 0.25, 0.75, 75, 0.80, 'SEDANG', 2, 14, 'Membutuhkan media tanam gembur tanpa batu kerikil dengan kedalaman minimal 25 cm agar umbi lurus sempurna.'),
  ('Terong', 'FULL_SUN', 0.50, 1.00, 70, 0.60, 'SEDANG', 1, 14, 'Butuh panas penuh dan ajir penopang saat buah mulai membesar. Bersihkan daun kuning bawah untuk mencegah jamur.'),
  ('Kacang panjang', 'FULL_SUN', 0.50, 1.00, 45, 0.80, 'MUDAH', 1, 14, 'Tanaman merambat vertikal, sangat hemat luas tanah! Pasang tiang atau jaring rambatan di dinding/pagar pekarangan.'),
  ('Mentimun', 'FULL_SUN', 0.50, 1.50, 40, 0.80, 'MUDAH', 1, 14, 'Tumbuh merambat cepat dan panen dalam 40 hari. Sediakan rambatan di teras dan siram teratur saat pembungaan.'),
  ('Pare', 'FULL_SUN', 0.50, 1.50, 45, 0.30, 'MUDAH', 1, 14, 'Tanaman merambat kuat dan tahan hama. Sangat cocok memanfaatkan dinding atau pagar teras sebagai bidang rambatan.'),
  ('Kemangi', 'PARTIAL_SUN', 0.25, 0.50, 30, 0.30, 'MUDAH', 1, 7, 'Aroma kuat membantu mengusir serangga hama lain. Petik pucuk daun secara rutin agar tanaman rimbun bercabang.'),
  ('Daun bawang', 'PARTIAL_SUN', 0.25, 0.50, 45, 0.40, 'MUDAH', 2, 14, 'Dapat ditanam dari sisa potongan akar dapur (kitchen scrap regrowth). Tumbuh subur di pot dangkal/ambang jendela.')
ON CONFLICT (nama) DO UPDATE SET
  kebutuhan_sinar = EXCLUDED.kebutuhan_sinar,
  luas_min_m2 = EXCLUDED.luas_min_m2,
  luas_optimal_m2 = EXCLUDED.luas_optimal_m2,
  waktu_panen_hari = EXCLUDED.waktu_panen_hari,
  konsumsi_rt_kg_per_bulan = EXCLUDED.konsumsi_rt_kg_per_bulan,
  tingkat_kesulitan = EXCLUDED.tingkat_kesulitan,
  jadwal_siram_hari = EXCLUDED.jadwal_siram_hari,
  jadwal_pupuk_hari = EXCLUDED.jadwal_pupuk_hari,
  panduan_singkat = EXCLUDED.panduan_singkat;
