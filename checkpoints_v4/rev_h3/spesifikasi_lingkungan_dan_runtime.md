# SPESIFIKASI LINGKUNGAN PENGUJIAN & ESTIMASI DURASI KOMPUTASI (BAB 4)

Dokumen ini memuat informasi lengkap spesifikasi perangkat keras (*hardware*), perangkat lunak (*software*), versi pustaka (*library*), serta waktu eksekusi (*runtime*) dari seluruh tahapan eksperimen skripsi untuk kebutuhan penulisan Subbab 4.2 Lingkungan Pengujian.

---

## 1. Spesifikasi Perangkat Keras (Hardware)
| Komponen | Spesifikasi Server / Workstation Eksperimen | Spesifikasi PC Client / Dashboard Demo |
|:---|:---|:---|
| **Sistem Operasi** | Microsoft Windows 11 Pro 64-bit (Build 26300) | Microsoft Windows 10/11 Pro 64-bit |
| **Prosesor (CPU)** | Intel Core i7-1165G7 / Intel64 Family 6 Model 140 | Intel Core i5/i7 (4 Physical Cores / 8 Logical Cores) |
| **Arsitektur CPU** | x86_64 / AMD64 | x86_64 / AMD64 |
| **Memori Utama (RAM)** | 16 GB DDR4 (15.78 GB Usable) | 8 GB - 16 GB DDR4 |
| **Penyimpanan (Storage)** | Solid State Drive (SSD) NVMe PCIe 512 GB | Solid State Drive (SSD) |
| **Akselerator Grafis (GPU)** | Intel Iris Xe Graphics (Pelatihan CPU-based untuk Tree & Statistik) | Integrated GPU / Discrete GPU |

---

## 2. Spesifikasi Perangkat Lunak & Pustaka (Software & Libraries)
| Perangkat Lunak / Pustaka | Versi yang Digunakan | Peran dalam Pipeline Proyek |
|:---|:---|:---|
| **Python** | `3.11.9` (64-bit) | Bahasa pemrograman utama seluruh pipeline. |
| **Pandas** | `2.2.3` | Ekstraksi Excel multi-sheet, manipulasi tabel, aggregasi bulanan, dan ETL. |
| **NumPy** | `2.0.2` | Operasi komputasi array matriks numerik dan perhitungan metrik. |
| **SciPy** | `1.14.1` | Penghalusan Savitzky-Golay filter dan uji statistik Spearman/Pearson. |
| **Scikit-Learn** | `1.7.2` | `HistGradientBoostingRegressor`, `RobustScaler`, `PowerTransformer` (Yeo-Johnson), dan evaluasi. |
| **Statsmodels** | `0.14.6` | Estimasi model deret waktu ARIMA/ARIMAX dan analisis fungsi autokorelasi parsial (PACF). |
| **Pmdarima** | `2.0.4` | Modul pencarian parameter Auto-ARIMA & evaluasi AIC/BIC pada eksperimen eksplorasi awal. |
| **TensorFlow / Keras** | `2.15.0 / 2.16.x` | Arsitektur jaringan saraf sekuensial LSTM multivariat. |
| **Streamlit** | `1.60.0` | Antarmuka web dashboard interaktif (`appDemo.py` port 8501 dan `appPerusahaan.py` port 8502). |
| **Plotly** | `6.5.0` | Pembuatan visualisasi grafik deret waktu interaktif dengan tooltip hover real-time. |
| **Openpyxl** | `3.1.5` | Mesin pembaca dan penulis berkas spreadsheet Excel `.xlsx`. |

---

## 3. Estimasi Durasi Eksekusi Komputasi (Runtime Breakdown)
| Tahapan Pemodelan | Cakupan Proses Komputasi | Estimasi Durasi Waktu | Catatan Teknis & Optimasi |
|:---|:---|:---|:---|
| **Tahap 1: Ekstraksi & Preprocessing (ETL)** | Ekstraksi 3 tahun berkas BBM AAB, Container, Cuaca, filter kelayakan. | **~30 s/d 50 detik** | Membaca multi-sheet Excel dan menghasilkan checkpoint `monthly_full`. |
| **Tahap 2: Grid Search 24 Kombinasi** | 3 Model (ARIMAX, GB, LSTM) x 4 Varian Data Prep x 2 Pendekatan. | **~1 jam s/d 1.5 jam** (per horizon) | LSTM dan ARIMAX mendominasi waktu (~45 menit). Paralelisasi menggunakan `joblib.Parallel(n_jobs=4)` dengan pengelompokan batch. |
| **Tahap 2b: Drill-Down 12 Kombinasi** | Refit 12 kombinasi (Model x Data Prep) per unit & per kriteria. | **~10 s/d 15 menit** | Parameter model memakai pemenang global Tahap 2; cache memori dikosongkan secara berkala (`gc.collect()`). |
| **Tahap Force-GB (Tuning GB Individual)** | Tuning 36 kombinasi hiperparameter GB secara individual per unit target. | **~5 s/d 8 menit** | Menguji variasi *learning rate*, *max_depth*, dan ukuran daun pada unit target. |
| **Tahap 3: Model Final & Future Forecast** | Retrain seluruh riwayat historis 190 unit analisis + recursive rolling forecast 12 bulan. | **35.04 detik** (terukur) | Sangat cepat berkat efisiensi binning integer pada `HistGradientBoostingRegressor`. |
| **Dashboard Operasional PT X (Live Run)** | Unggah berkas Excel baru -> parsing ETL -> retrain 190 unit -> proyeksi masa depan. | **~1 s/d 1.5 menit** (total end-to-end) | Memungkinkan pemutakhiran model langsung oleh staf operasional perusahaan tanpa jeda lama. |
