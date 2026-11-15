# Daftar Berkas Kebutuhan Penulisan Buku Skripsi
**Tanggal Pembuatan**: 30 Oktober 2026  
**Folder Utama**: `Kebutuhan Buku 30-10-2026/` (Semua berkas berada langsung di dalam folder ini, tanpa subfolder).

Seluruh berkas telah diberi nomor awalan yang sesuai persis dengan nomor urut pada daftar permintaan Anda agar mudah dicari dan dipahami:

---

### A. Inti Hasil Pengujian (Nomor 1 s/d 9)

| No. File | Nama Berkas di Folder | Folder Asal di Repositori | Peruntukan di Buku Skripsi | Catatan / Spesifikasi |
|---|---|---|---|---|
| **01** | `01_v2_MASTER_SUMMARY_24_kombinasi.xlsx` | `checkpoints_v4/h3bulan/` | Rentang parameter & jumlah kombinasi | Memuat seluruh grid parameter eksplorasi Tahap 2 (24 kombinasi: 4 prep × 3 model × 2 pendekatan). |
| **02** | `02_v2_winner_per_kombinasi.xlsx` | `checkpoints_v4/h3bulan/` | **Tabel 4.5**: Parameter Pemenang 24 Kombinasi | Parameter pemenang per kombinasi data prep, model, dan pendekatan agregasi. |
| **03** | `03_v2b_hasil_12kombinasi_per_unit_kriteria.xlsx` | `checkpoints_v4/rev_h3/` | **Tabel 4.6 & 4.7**: Detail, Best Combo, & Tally | Versi **FINAL 190 Unit Valid** (format penamaan baru `K##_UNIT_###`). Sheet: `Detail_PerUnit`, `Best_Combo_PerUnit`, `Best_Combo_PerKriteria`, `Tally_PerUnit`, `Tally_PerKriteria`. |
| *03b* | `03b_v2b_hasil_12kombinasi_205unit_baseline.xlsx` | `checkpoints_v4/h3bulan/` | Pembanding Baseline Lama | Versi 205 unit baseline sebelum 15 unit anomali disaring. |
| **04** | `04_v4_forcedgb_vs_v2b_comparison.xlsx` | `checkpoints_v4/rev_h3/` | **Tabel 4.8**: Hasil Model Akhir Gradient Boosting | Versi **FINAL 190 Unit Valid** (format `K##_UNIT_###`). Sheet: `Per_Unit` dan `Per_Kriteria`. |
| *04b* | `04b_v4_forcedgb_vs_v2b_comparison_205unit_baseline.xlsx` | `checkpoints_v4/h3bulan/` | Pembanding Baseline Lama | Versi 205 unit baseline sebelum 15 unit anomali disaring. |
| **05** | `05_v4_rolling_vs_direct.xlsx` | `checkpoints_v4/rev_h3/` | **Tabel 4.10**: Direct vs Rolling Forecast | Versi **FINAL 190 Unit Valid**. Sheet: `Per_Unit`, `Per_Kriteria`, `Ringkasan`. |
| *05b* | `05b_v4_rolling_vs_direct_205unit_baseline.xlsx` | `checkpoints_v4/h3bulan/` | Pembanding Baseline Lama | Versi 205 unit baseline. |
| **06a** | `06a_v4_PERBANDINGAN_4BULAN_vs_3BULAN.xlsx` | `checkpoints_v4/` | **Tabel 4.9**: Perbandingan Horizon 4 Bulan vs 3 Bulan | Head-to-head evaluasi per unit dan per kriteria antara horizon 4 bulan vs 3 bulan. |
| **06b** | `06b_v4_RINGKASAN_LINTAS_HORIZON.xlsx` | `checkpoints_v4/` | **Tabel 4.9**: Ringkasan Lintas Horizon | Agregat perbandingan performa forced-GB vs v2b untuk kedua horizon. |
| **07** | `07_perbandingan_eksogen_dan_model.xlsx` | `checkpoints_v4/rev_h3/` | **Tabel 4.11**: 6 Skenario Eksogen & Model | Evaluasi ARIMA vs ARIMAX vs Gradient Boosting (Eksogen $t$ vs Lag-1 vs Tanpa Eksogen) pada 190 unit valid. Sheet: `Ringkasan` dan `Detail_PerUnit`. |
| **08** | `08_mapping_unit_dan_kriteria.xlsx` | `checkpoints_v4/rev_h3/` | Master Referensi Kriteria & Unit | Sheet `Mapping_Unit` (230 unit lengkap) dan `Ringkasan_Kriteria` (85 kriteria kustom dengan rincian spesifikasi & daftar unit). |
| *08b* | `08b_unit_excluded_revisi_summary.xlsx` | `checkpoints_v4/rev_h3/` | Lampiran Unit Diexclude | Daftar resmi **25 unit yang diexclude** murni karena jam kerja nol operasional (18 train nol + 7 test nol). |
| **09** | `09_v4_future_forecast_final.xlsx` | `checkpoints_v4/rev_h3/future_forecast/` | **Pengujian 6**: Proyeksi 12 Bulan (190 Unit) | Hasil proyeksi operating hours Jan–Des 2026 untuk 190 unit valid (kolom `FORECAST_OPERATING_HOURS`). |
| *09b* | `09b_v4_future_forecast_final_205unit_baseline.xlsx` | `checkpoints_v4/h3bulan/future_forecast/` | Pembanding Baseline Lama | Hasil proyeksi 205 unit baseline. |

---

### B. EDA untuk Bab 3.3 (Nomor 10 s/d 12)

Seluruh berkas EDA berasal dari direktori [`checkpoints_v4/eda/`](file:///d:/SPIL%20Michael/Folder%20TA/t%20a/checkpoints_v4/eda):

#### 10. Berkas CSV (Tabel Data EDA)
- `10a_eda_00_agregat_bulanan.csv`: Agregat bulanan operating hours, curah hujan, & volume container.
- `10b_eda_04_deskriptif_skewness.csv`: Statistik deskriptif pooled data.
- `10c_eda_08_outlier_iqr.csv`: Deteksi outlier batas 1,5×IQR.
- `10d_eda_08b_outlier_detail.csv`: Rincian baris bulan outlier (April 2023 & April 2025 periode Idul Fitri).
- `10e_eda_12_korelasi_pearson.csv`: Matriks korelasi Pearson.
- `10f_eda_14_skewness_per_unit_detail.csv`: Nilai skewness operating hours individual untuk seluruh unit armada.
- `10g_eda_15_skewness_per_unit_ringkasan.csv`: Sebaran distribusi skewness per unit (simetris, moderat, ekstrem).

#### 11. Berkas PNG (Visualisasi Gambar EDA)
- `11a_trend_operating_hours_total.png`: Grafik tren total operating hours bulanan seluruh armada (36 bulan).
- `11b_trend_operating_hours_mean.png`: Grafik tren rata-rata operating hours per unit.
- `11c_trend_curah_hujan.png`: Grafik tren curah hujan bulanan pelabuhan.
- `11d_trend_volume_container.png`: Grafik tren volume throughput kontainer cabang.
- `11e_dist_operating_hours.png`: Distribusi pooled operating hours (right-skewed).
- `11f_dist_curah_hujan.png`: Distribusi curah hujan.
- `11g_dist_volume_container.png`: Distribusi volume kontainer.
- `11h_box_operating_hours.png`: Boxplot operating hours armada.
- `11i_box_curah_hujan.png`: Boxplot curah hujan.
- `11j_box_volume_container.png`: Boxplot volume kontainer.
- `11k_korelasi_heatmap.png`: Heatmap matriks korelasi Pearson.
- `11l_eda_16_dist_skewness_per_unit.png`: Distribusi nilai kemencengan (skewness) per unit (-3.05 s/d +5.75).

#### 12. PACF & Spearman Hasil Rerun Terbaru
- `12a_analisis_pacf_spearman.csv`: Hasil autokorelasi parsial (PACF Lag 1–5) dan uji korelasi rank Spearman vs Pearson per unit.
- `12b_analisis_pacf_dan_spearman.png`: Grafik 2 panel: bar chart lag PACF terputus tajam $\le 3$ + pie chart dominasi Spearman (55.61% unit lebih kuat dibanding Pearson).

---

### C. Info Teks untuk Bab 4.2 & Pengujian (Nomor 13 s/d 16)
- `13_14_15_info_teks_bab_4_2_dan_runtime.txt`: Berkas teks yang memuat seluruh rincian:
  * Versi software (`Python 3.11.9`, `pandas 2.2.3`, `scikit-learn 1.7.2`, `statsmodels 0.14.6`, dll.)
  * Spesifikasi hardware komputer lokal (Intel Core i7-1165G7, 16 GB RAM, SSD 512 GB)
  * Waktu eksekusi tiap tahap (ETL ~30-50s, Tahap 2 ~1.5-2.5h, Tahap 2b ~20-30m, Tahap 3 terukur 35,04s)
  * Waktu proses upload sampai tampil di `appPerusahaan.py` (total ~75-95 detik)
  * Tabel ringkasan 6 skenario evaluasi eksogen 190 unit (Tabel 4.11)

---

### D. Dokumen Proyek (Nomor 17)
- `17_PROGRESS.md`: Dokumen pelacakan progress lengkap proyek yang memuat catatan metodologi, log bug & resolusi, sintesis akademis bimbingan lanjutan (§20.11 & §20.12), serta arsitektur backend dashboard Streamlit (§21.13).
