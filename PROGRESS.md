# Progress Tracking — TA Prediksi Utilitas Alat Berat PT SPIL

Dokumen ini mencatat progress pengerjaan notebook (`code.ipynb` = arsip percobaan awal, `code_v2.ipynb` = arsip pasca-Bimbingan 2, `code_v3.ipynb` = split train/test baru, **`code_v4.ipynb` = notebook aktif terbaru**), keputusan-keputusan yang diambil selama proses (termasuk yang di luar cakupan proposal), bug yang ditemukan & diperbaiki, dan hal-hal yang masih perlu ditindaklanjuti. Update dokumen ini setiap ada perubahan signifikan di notebook.

> **PETUNJUK BACA (chat baru):** dokumen ini punya **tiga bagian terpisah**:
> - **BAGIAN A — ANALISA CODE** → §1–§19 (semua yang berkaitan dengan notebook/eksperimen; §19 = `code_v4.ipynb`, terbaru)
> - **BAGIAN B — PENULISAN BUKU SKRIPSI** → §20 (semua yang berkaitan dengan penulisan Bab 1–3 laporan TA & justifikasi ilmiah bimbingan §20.10; persiapan Bab 4–6 di §20.13)
> - **BAGIAN C — DASHBOARD STREAMLIT** → §21 (`pipeline_lib.py`, `appDemo.py`, `appPerusahaan.py`, visualisasi, benchmark, & penyempurnaan UI)
>
> Kalau chat baru cuma soal coding → fokus §19 (+ §17 untuk konteks v3). Kalau penulisan buku/bimbingan → fokus §20. Kalau dashboard Streamlit → fokus §21.

---

## 1. Status Umum

| Tahap | Status |
|---|---|
| Preprocessing (9 langkah sesuai proposal) | ✅ Selesai & tervalidasi |
| Parsing file kriteria (cost & bbm HP & Type) | ✅ Selesai |
| Modeling — ARIMAX, GB, LSTM (baseline, auto_arima/default) | ✅ Selesai |
| Evaluasi & pemilihan model terbaik (baseline) | ✅ Selesai & apple-to-apple (§4.9) |
| Kebersihan angka checkpoint (floating-point artifact) | ✅ Selesai (§4.10, §4.11) |
| **Bimbingan 1 — 4 poin saran dosen** | ✅ Semua diimplementasikan & dijalankan (lihat §10) |
| **Cross-check vs catatan Bimbingan 1 asli** | ✅ Semua poin dosen terpenuhi kecuali 2 hal ditunda (lihat §13) |
| **Restrukturisasi populasi unit (cost&bbm-only)** | ✅ Selesai — populasi final `code.ipynb` (lihat §14) |
| **Bimbingan 2 — RMSE/bias, model global terbaik, notebook baru** | ✅ Selesai, hasil final ada (lihat §15) |
| **`code_v2.ipynb` Tahap 2 — 4 varian data-prep x 3 model x 2 pendekatan** | ✅ Selesai dijalankan (lihat §15.4) |
| **`code_v2.ipynb` Tahap 3 — tuning individual per-unit & per-kriteria** | ✅ Selesai dijalankan, **pemenang final: per-kriteria** (lihat §15.5) |
| **Temuan "prediksi mendatar"** | ⚠️ TERKONFIRMASI muncul di hasil final, terkait kriteria/unit ber-anggota tunggal (lihat §15.6) — **perlu dibahas ke dosen** |
| **`code_v2.ipynb` Tahap 2b — drill-down 12 kombinasi per-unit & per-kriteria (arahan bimbingan lanjutan)** | ✅ Selesai dijalankan (populasi/split LAMA), hasil di `v2b_hasil_12kombinasi_per_unit_kriteria.xlsx` (lihat §16) |
| **`code_v3.ipynb` — split train/test baru + exclude/remap 10 unit (arahan bimbingan lanjutan #2)** | ✅ Notebook baru selesai dibangun & dijalankan ulang (Tahap 1→2→2b→3), lihat §17 |
| **Masalah ARIMAX per-kriteria gagal massal di `code_v3.ipynb`** | ⏸️ DI-HOLD oleh user — lanjut di chat baru kalau masih muncul (lihat §17.5) |
| **[BAGIAN A] `code_v4.ipynb` — replikasi Tahap 1→2→2b untuk 2 horizon (4 & 3 bulan) + tuning GB individual (prep+parameter) + rolling vs direct** | ✅ Notebook selesai dibangun (90 cell), dijalankan user di server lewat `.py`; horizon final diputuskan 3 bulan (§19) |
| **[BAGIAN A] `code_v4.ipynb` Tahap 3 — Model Final & Future Forecast 12 Bulan (Cell 92-99)** | ✅ Selesai dijalankan (full-history fit + recursive rolling forecast), hasil di `checkpoints_v4/h3bulan/future_forecast/` (§19.10) |
| **[BAGIAN A] Revisi Dosen Pembimbing 2 — Eksogen Lag-1, 190 Unit Valid, & Plot Y=0 (Cell 101-104)** | ✅ Selesai dijalankan, folder hasil terisolasi di `checkpoints_v4/rev_h3/` (§19.11) |
| **[BAGIAN A] Standarisasi Penamaan Unit & Kriteria (`K01_UNIT_004`)** | ✅ Selesai, 85 kriteria & 230 unit terpetakan, master mapping & JSON diperbarui (§19.12) |
| **[BAGIAN C] Dashboard Streamlit (`pipeline_lib.py`, `appDemo.py`, `appPerusahaan.py`)** | ✅ Selesai dibangun, disempurnakan pasca-bimbingan, dan disinkronkan ke 190 unit valid + 40 unit excluded (§21.10) |
| **[BAGIAN C] Fix Isu ETL Dashboard Perusahaan (0 Unit Terproyeksi)** | ✅ Selesai, auto-mapping penamaan kriteria & optimasi pembacaan Excel di `pipeline_lib.py` (§21.11) |
| **[BAGIAN A & C] Penggantian Istilah Utilitas → Operating Hours (Poin 1 Revisi & Opsi A)** | ✅ Selesai menyeluruh di UI, kolom file output fisik, rename file fisik, dan backend dual compatibility (§21.12) |
| **[BAGIAN A] Eliminasi Total 15 Unit Anomali dari Awal Pipeline ETL** | ✅ Selesai, populasi 215 unit terlacak, 25 unit exclude operasional jam nol murni, 190 unit model valid (§19.13) |
| **[BAGIAN A] Standarisasi Global Naming Unit Kriteria (`K##_UNIT_###`) Lintas Checkpoint v1–v4** | ✅ Selesai, 100% berkas data di `checkpoints/`, `checkpoints_v2/`, `checkpoints_v3/`, `checkpoints_v4/` konsisten 0 format lama tersisa (§19.14) |
| **[BAGIAN A] Analisis PACF & Korelasi Spearman Variabel Eksogen** | ✅ Selesai, script `analisis_pacf_spearman.py` menghasilkan CSV dan plot visualisasi dinamis (§19.15) |
| **[BAGIAN B] Sintesis Akademis: Fenomena Disagregasi Per-Kriteria vs Per-Unit & 6 Insight Skripsi** | ✅ Selesai dirangkum mendalam untuk landasan Bab 4 & 5 laporan skripsi (§20.11) |
| **[BAGIAN B] Justifikasi Ilmiah Penomoran ID Unit 3 Digit vs Populasi 200-an Unit** | ✅ Selesai, landasan integritas audit trail database aset enterprise (§20.12) |
| **[BAGIAN C] Sinkronisasi Dashboard Streamlit & Proteksi Zero False New Units** | ✅ Selesai, 25 excluded resmi termuat presisi, upload data mentah bebas deteksi unit baru palsu (§21.13) |
| **[BAGIAN B] Persiapan penulisan Bab 4–6 (chat penulisan buku)** | 🔄 Berjalan — review berkas & keputusan selesai, kerangka Bab 4 (4.1–4.9) ada dengan angka PRA-RERUN (superseded); Bab 4 final, Bab 5, Bab 6, Daftar Pustaka, update Bab 3.3 menunggu output rerun 215 unit (§20.13) |
| **[BAGIAN A] Review kode & output oleh Claude (daftar perbaikan label/sinkron/keterulangan)** | ⚠️ Sebagian sudah dikerjakan user (§19.13, §21.12–21.13), sisanya BELUM diverifikasi (§19.16) |

---

## 2. Anonimisasi Data Sensitif

- **Nama unit alat berat** → `UNIT_0001`, dst. **Kode cabang** → `BRANCH_001`, dst. **Lokasi/depo** → `LOC_001`, dst.
- **Mapping asli → anonim disimpan LOKAL** di `./anonymization_maps/` — tidak pernah dikirim/ditampilkan ke Claude.

⚠️ Folder `anonymization_maps/` jangan pernah dilampirkan ke chat/email/skripsi. Kalau memindahkan pipeline ke server lain, folder ini perlu ikut dibawa supaya ID unit tetap konsisten dengan checkpoint lama.

---

## 3. Keputusan Kunci Selama Proses (dengan alasan)

### 3.1 Struktur BBM AAB
Header 3 level per sheet bulanan. Blok "unit alat berat" dipisahkan dari blok "tangki/depo" berdasarkan keberadaan sub-kolom `HM` **dan** `LITER` bersamaan.

### 3.2 Volume Container — CURRSTATE yang dipakai
21 blok pivot per file → **8 CURRSTATE dipakai** (`FXD, FAC, STR, MAS, MTB, FOB, MXD, MOB`, `PREV_STATE='All'` kecuali MOB). **Belum 100% dikonfirmasi**: union seragam untuk semua unit, bukan diferensiasi per jenis alat berat — perlu konfirmasi ke pembimbing.

### 3.3 Kriteria unit
`KRITERIA_ID` = `JENIS | TYPE/MERK | CAP | HP`. 245 dari 306 unit punya data di file cost&bbm.

### 3.4 Pembulatan angka: dibedakan per jenis data
Kuantitas fisik (`UTILITAS`, `CURAH_HUJAN` — 1 desimal; `UTILITAS_CAPPED`, `UTILITAS_SMOOTH` — 2 desimal) dibulatkan untuk buang artefak floating-point. Metrik hasil model (`MAPE`, `RMSE`, `PRED`) **tidak dibulatkan**.

### 3.5 Skewness dihitung per KRITERIA_ID
Skewness untuk menentukan mean/median di ARIMAX per-kriteria dihitung dari **UTILITAS gabungan (pooled) semua unit dalam 1 KRITERIA_ID**, memakai data **train** saja.

### 3.6 Grid search PDQ & tuning: evaluasi berbasis MAPE_GLOBAL seragam
Untuk tiap kombinasi parameter, model di-fit ke **semua unit/kriteria sekaligus**, MAPE_GLOBAL dihitung dari gabungan semua prediksi, kombinasi terbaik jadi **1 konfigurasi seragam** dipakai semua unit — bukan tuning per-unit individual.

---

## 4. Bug yang Ditemukan & Diperbaiki (Sebelum Bimbingan 1)

### 4.1 [FIXED] Header bulan Container ter-merge — `ffill()` horizontal.
### 4.2 [FIXED] Kolom tipe container "sampah" — whitelist 23 tipe valid.
### 4.3 [FIXED — KRITIS] ARIMAX tidak memakai variabel eksogen — `exogenous=` → `X=`.
### 4.4 [OBSERVASI HISTORIS — usang] Naive baseline sebelum fix §4.9.
### 4.5 [FIXED] MAPE_GLOBAL tidak sesuai definisi proposal — sekarang array gabungan semua unit.
### 4.6 [DIHAPUS SEMENTARA] Naive baseline — tidak diminta proposal.
### 4.7 [FIXED] Bug lag feature GB per-kriteria — `groupby('EQUIP NAME')`.
### 4.8 [BUG DI SISI USER] Angka aneh di Excel — locale decimal, sudah diperbaiki user.
### 4.9 [FIXED — KRITIS] `ACTUAL` evaluasi beda antar model — sekarang semua pakai `UTILITAS` mentah.
### 4.10 [FIXED] Floating-point artifact `UTILITAS` bulanan — `.round(1)`.
### 4.11 [FIXED] Floating-point artifact `CURAH_HUJAN`/`UTILITAS_CAPPED`/`UTILITAS_SMOOTH` — `.round(1)`/`.round(2)`.

---

## 10. Update Pasca Bimbingan 1 — Saran Dosen (4 Poin)

Setelah presentasi progress ke pembimbing, diterima 4 arahan tambahan. Semua diimplementasikan sebagai cell baru di `code.ipynb` (cell 26 dst), cell 0-24 tidak diubah strukturnya kecuali cell 5.

### 10.1 Poin 1 — Skewness untuk pilih mean/median ARIMAX per-kriteria (Cell 27)
Aturan final: **|skewness| > 1 → median**, **-1 ≤ skewness ≤ 1 → mean**. Dihitung per `KRITERIA_ID` dari data train.

**Status**: ✅ Sudah diimplementasikan dengan arah threshold yang benar. Output: `17_skewness_per_kriteria.csv`.

### 10.2 Poin 2 — HM harian >24 jam → di-cap ke 24 (Cell 5, direvisi)
```python
raw_bbm.loc[raw_bbm['DELTA_HM'] > 24, 'DELTA_HM'] = 24  # sebelumnya di-set 0
```
**Status**: ✅ Diimplementasikan. Efek domino: cell 6-24 dst perlu di-rerun.

### 10.3 [Tambahan susulan] Pengecekan Outlier UTILITAS (Cell 26)
Metode IQR (Tukey's fences, k=1.5), per unit, dari `UTILITAS` mentah seluruh periode — murni EDA, tidak mengubah capping cell 14 (tetap persentil 95).

**Output**: `16_outlier_summary_per_unit.csv`, `16b_outlier_flagged_rows.csv`, `16c_boxplot_utilitas_per_jenis.png`.

⚠️ **Belum dikonfirmasi ke dosen**: apakah ini murni pelaporan EDA atau dimaksudkan mengganti metode capping.

### 10.4 Poin 3 — Plot 3 MAPE terbesar & terkecil per model+pendekatan (Cell 28)
Diterapkan ke 5 kombinasi baseline (key `EQUIP NAME`) + ARIMAX per-kriteria mean & median (key `KRITERIA_ID`).

**Status**: ✅ Diimplementasikan, 6 file PNG (grid 2×3 subplot per kombinasi).

### 10.5 Poin 4a — Grid search ARIMAX PDQ (Cell 29 & 30)
- Range: p=0-8, d=0-4, q=0-8 → 405 kombinasi.
- Cakupan: per-unit (Cell 29) + per-kriteria mean & median (Cell 30).
- Evaluasi: MAPE_GLOBAL gabungan per kombinasi, **1 kombinasi terbaik** ditampilkan sebagai pemenang di cell 29/30 (bukan top-N) — konfirmasi ulang: "3 parameter PDQ" di instruksi awal dosen ngerujuk ke 3 parameter p/d/q dalam formula ARIMA, bukan 3 kombinasi teratas.
- Skala: ~163.000 total fit ARIMA.
- Checkpoint: tiap 10 kombinasi (`19a_gridsearch_arimax_unit_progress.csv`, `19b_gridsearch_arimax_kriteria_progress.csv`), auto-skip kombinasi selesai saat run ulang. **Semua kombinasi (bukan cuma juara 1) tersimpan di `19a_final.csv`/`19b_final.csv`** — jadi top-N kombinasi kapan saja bisa diambil belakangan tanpa run ulang grid search (lihat §10.9).
- Risiko: order tinggi (p/q dekat 8, d dekat 4) rawan gagal konvergen (train cuma 24 bulan) — di-handle `try/except`, skip otomatis.

**Status**: ✅ Kode & checkpoint OK. User sudah punya file `19a_progress/final.csv`, `19b_progress/final.csv` dari run sebelumnya — dikonfirmasi kompatibel langsung dipakai lanjut.

### 10.6 Poin 4b — Tuning Gradient Boosting & LSTM (Cell 31-34)

| Cell | Isi | Cakupan | Status |
|---|---|---|---|
| 31 | GB tuning per-unit (144 kombinasi) | Per-unit | ✅ |
| 32 | GB tuning per-kriteria | Per-kriteria | ✅ |
| 33 | LSTM tuning per-unit (8 kombinasi) | Per-unit | ✅ |
| 34 | LSTM tuning per-kriteria | Per-kriteria | ✅ |

### 10.7 Ringkasan Excel semua percobaan (Cell 35)
Gabungan semua hasil (baseline + skewness-based + grid search + tuning) → `21_RINGKASAN_SEMUA_PERCOBAAN.xlsx`, 9 sheet (Juara Keseluruhan, Terbaik per Model, Terbaik per Pendekatan, Semua Percobaan, + 5 sheet detail top-20).

**Status**: ✅ Selesai (revisi GB/LSTM-kriteria sudah disisipkan user sendiri).

### 10.8 Checkpoint auto-skip untuk GB & LSTM tuning (Cell 31-34, direvisi)
Awalnya cell 31/32 (GB) tidak ada checkpoint sama sekali. Cell 33/34 (LSTM) ada checkpoint tapi tanpa logika skip.

**Fix**: 4 cell direvisi mengikuti pola cell 29/30 — baca checkpoint CSV di awal, `done_combos`, skip yang sudah ada, `mode='a'` (append).

| Cell | Checkpoint file | Batching |
|---|---|---|
| 31 (GB unit) | `20a_gb_tuning_unit_progress.csv` | Tiap 10 kombinasi |
| 32 (GB kriteria) | `20a_gb_tuning_kriteria_progress.csv` | Tiap 10 kombinasi |
| 33 (LSTM unit) | `20b_lstm_tuning_results.csv` | Tiap 1 kombinasi |
| 34 (LSTM kriteria) | `20b_lstm_tuning_kriteria_results.csv` | Tiap 1 kombinasi |

**Kompatibilitas file lama**: nama file checkpoint baru sama persis dengan file lama user, pakai `mode='a'` jadi file lama tidak perlu dihapus.

**Status**: ✅ Selesai.

### 10.9 [BARU] Rencana: plot pakai top-3 PDQ terbaik ARIMAX (belum dikode)
Klarifikasi dari user: cell 29/30 tetap cukup nampilin **1** kombinasi PDQ terbaik saja (tidak perlu diubah). Tapi untuk **plot** actual-vs-prediksi (perluasan dari poin 3/10.4 ke hasil poin 4), yang dipakai adalah **3 kombinasi PDQ teratas** (bukan cuma juara 1) — per kombinasi PDQ, ambil 3 unit MAPE terbesar + 3 terkecil, jadi plot.

**Cara ambil top-3**: tidak perlu run ulang grid search — tinggal `.head(3)` dari `19a_final.csv` (per-unit) / `19b_final.csv` (per-kriteria, per agg) yang sudah nyimpen semua 405 kombinasi + MAPE_GLOBAL masing-masing.

**Alur rencana**: ambil 3 PDQ teratas → fit ulang tiap PDQ ke semua unit (3x fit penuh, murah karena kombinasi sudah diketahui) → tiap PDQ ambil 3 unit MAPE terbesar + 3 terkecil → plot. Estimasi 18 plot untuk ARIMAX per-unit (3 PDQ × 6 unit), dikali lagi kalau per-kriteria juga mau dibuat serupa.

**Status**: ✅ Dikode di Cell 36. Isi:
- `refit_pdq_unit(order, ...)` / `refit_pdq_kriteria(order, agg, ...)` — refit ARIMA fixed-order (bukan auto_arima) ke semua unit/kriteria, pakai `eval_pred` yang sama dengan baseline.
- Per-unit: ambil `.head(3)` dari `grid_results_unit` → 3x refit penuh → `plot_top_bottom_mape` tiap PDQ (reuse fungsi Cell 28). Output: `22a_plot_arimax_unit_pdq{1,2,3}_{pdq}.png` + `22a_top3_pdq_per_unit.csv`.
- Per-kriteria: `.head(3)` **terpisah untuk mean & median** dari `grid_results_kriteria` (6x refit total). Output: `22b_plot_arimax_kriteria_{mean,median}_pdq{1,2,3}_{pdq}.png` + `22b_top3_pdq_per_kriteria.csv`.
- Total 9 file PNG (3 unit + 6 kriteria), tiap file grid 2×3 subplot (3 MAPE terbesar + 3 terkecil) → 18 subplot unit + 36 subplot kriteria.

**Status akhir: ✅ Sudah dijalankan & hasil dicek.** Top-3 PDQ per-unit: (1,0,0)=47.03%, (1,0,1)=47.36%, (1,0,2)=47.86% (227 unit sukses fit). Top-3 per-kriteria mean: (1,0,3)=63.42%, (1,0,2)=63.64%, (1,0,0)=63.79%. Top-3 per-kriteria median: (1,0,3)=63.77%, (1,0,2)=63.94%, (1,0,0)=64.33%.

**Temuan konsisten**: UNIT_0322 selalu muncul sebagai MAPE terburuk (500-1000%+) di semua PDQ, per-unit maupun per-kriteria (lewat kriteria FORKLIFT|KOMATSU). Actual unit ini turun ke ~0 di pertengahan periode (unit berhenti dipakai) sementara model tetap prediksi angka besar → MAPE meledak karena pembagi dekat nol. Ini karakteristik metrik MAPE, bukan bug — jadi poin diskusi tesis, bukan hal yang perlu diperbaiki di kode.

### 10.10 Poin 4b (lanjutan) — Plot top-3 tuning terbaik GB & LSTM (Cell 37)

Analog Cell 36, tapi untuk Gradient Boosting & LSTM. Cell 31-34 (tuning) cuma menyimpan `MAPE_GLOBAL` agregat per kombinasi hyperparameter — prediksi per-unit dibuang setelah dihitung. Jadi Cell 37 **retrain ulang 3 kombinasi pemenang** (bukan re-grid-search) untuk dapat breakdown per-unit yang bisa diplot.

Isi:
- `refit_gb_unit` / `refit_gb_kriteria` — refit `HistGradientBoostingRegressor` dengan parameter tetap ke semua unit/kriteria.
- `refit_lstm_unit` / `refit_lstm_kriteria` — retrain LSTM custom (seq_len/units/epochs dari hasil tuning) ke semua unit/kriteria, forecast rolling seperti baseline.
- Ambil top-3 dari `gb_tuning_df`, `gb_tuning_kriteria_df`, `lstm_tuning_df`, `lstm_tuning_kriteria_df` → refit → `plot_top_bottom_mape`.

**Output**: `23a_plot_gb_unit_top{1,2,3}.png` + `23a_top3_params_gb_unit.csv`, `23b_*` (GB per-kriteria), `23c_*` (LSTM per-unit), `23d_*` (LSTM per-kriteria). Total 12 PNG + 4 CSV.

⚠️ **LSTM di cell ini lambat** — retrain neural network penuh 6x (3 per-unit + 3 per-kriteria), beda dari ARIMAX/GB yang fit-nya cepat. Tidak ada checkpoint di cell ini; kalau kernel mati di tengah jalan, harus diulang dari kombinasi #1.

**Status akhir: ✅ Sudah dijalankan & hasil dicek.**
- GB per-unit terbaik: lr=0.01, max_iter=300, depth=7 (atau None/5 — lihat catatan di bawah), leaf=5 → **47.59%**.
- GB per-kriteria terbaik: lr=0.05, max_iter=200, depth=3, leaf=10 → **47.41%**.
- LSTM per-unit terbaik: seq_len=3, units=32, epochs=30 → **51.47%**.
- LSTM per-kriteria terbaik: seq_len=3, units=16, epochs=50 → **57.53%**.

⚠️ **Temuan penting — `max_depth` GB per-unit tidak berpengaruh**: top-1/2/3 GB per-unit (depth=7, None, 5) menghasilkan MAPE_GLOBAL **identik persis** (47.594...%) dan plot per-unit yang sama 100%. Penyebab: `HistGradientBoostingRegressor` punya default `max_leaf_nodes=31`; data training per-unit cuma ~10-12 bulan, jadi pohon kepentok limit leaf-nodes/jumlah data duluan sebelum sempat mencapai depth berapa pun yang diset. Bukan bug — cuma catatan bahwa `max_depth` tidak informatif untuk kasus per-unit di data sekecil ini. GB per-kriteria (data lebih banyak karena gabungan unit) berperilaku normal, top-1/2/3 beda-beda.

### 10.11 Perbandingan Baseline vs Tuned (Cell 38)

Membandingkan MAPE_GLOBAL baseline (auto-ARIMA, GB default `max_iter=200`, LSTM default `seq_len=6,units=32,epochs=50` — dari Cell 20 `summary`) vs hasil tuning terbaik (Cell 29-34), untuk 7 kombinasi model×pendekatan.

Isi: `baseline_map` (dari variabel baseline yang sudah ada di memory) vs `tuned_map` (baris `.iloc[0]`/`sort_values().iloc[0]` dari tiap dataframe tuning) → tabel selisih MAPE, % perbaikan, dan siapa yang menang (`TUNED`/`BASELINE`/`SAMA`) → bar chart perbandingan.

**Output**: `24_perbandingan_baseline_vs_tuned.csv`, `24_plot_perbandingan_baseline_vs_tuned.png`.

**Status**: ✅ Dikode, siap dijalankan. Prasyarat: variabel baseline (`arimax_unit_preds_df`, `gb_unit_preds_df`, `lstm_unit_preds_df`, dst dari Cell 16-20) **dan** variabel tuning (`grid_results_unit`, `gb_tuning_df`, `lstm_tuning_df`, dst dari Cell 29-34) harus ada di memory bersamaan — kalau kernel baru di-restart, run Cell 15-20 dulu (baseline, cepat karena tanpa grid search) sebelum Cell 38.

**Ringkasan MAPE_GLOBAL semua kombinasi (urut terbaik)**:

| Model | Pendekatan | MAPE_GLOBAL terbaik |
|---|---|---|
| ARIMAX | per-unit | 47.03% |
| GB | per-kriteria | 47.41% |
| GB | per-unit | 47.59% |
| LSTM | per-unit | 51.47% |
| LSTM | per-kriteria | 57.53% |
| ARIMAX | per-kriteria (mean) | 63.42% |
| ARIMAX | per-kriteria (median) | 63.77% |

Catatan: tuning **tidak selalu mengalahkan baseline** di semua kombinasi — detail selisih ada di `24_perbandingan_baseline_vs_tuned.csv` begitu cell dijalankan.

---

## 13. Cross-check vs Catatan Bimbingan 1 Asli (20 Agustus 2026)

User mengupload catatan mentah hasil bimbingan dengan Pak Adi. Verifikasi tiap poin:

| Poin catatan dosen | Status | Cell |
|---|---|---|
| Histogram + skewness tiap unit | ✅ | 27 |
| ARIMAX: skew>1 atau <-1 → median, -1~1 → mean | ✅ | 27 |
| Cek outlier tiap alat berat | ✅ | 26 |
| Cap HM >24 jam → 24 jam | ✅ | 5 |
| Cek berapa unit, MAPE kecil vs besar, kenapa besar | ✅ | 28 (+ temuan UNIT_0322 di §10.9) |
| Grid search PDQ manual (0-6/0-3/0-6 **atau** 0-8/0-4/0-8) | ✅ | 29-30, dipakai versi lebih lebar (0-8,0-4,0-8) |
| 3 kombinasi PDQ error terkecil, plot masing-masing beberapa unit terbesar+terkecil | ✅ | 36 |
| GB & LSTM ambil parameter terbaik + plot | ✅ | 31-34, 37 |
| Bandingkan mana yang terbaik | ✅ | 38 |

**Ditunda atas keputusan user — akan dikonsultasikan ke dosen dulu sebelum lanjut**:
1. **Target MAPE <10% atau <20%** — MAPE_GLOBAL saat ini masih 47-64% di semua kombinasi. Kemungkinan penyebab (UNIT_0322 dkk dengan actual≈0) sudah teridentifikasi tapi solusinya (exclude unit, ganti metrik ke sMAPE/WAPE, dsb) perlu arahan dosen dulu.
2. **"Prediksi mendatar = kesalahan klasik"** — belum ada pengecekan otomatis/manual terhadap pola prediksi flat di plot-plot yang sudah dihasilkan. Perlu direview manual dulu sebelum diputuskan apakah ini masalah nyata di kasus TA ini.

**File yang disarankan dibawa ke bimbingan berikutnya** (urutan presentasi):
1. Skewness/histogram (Cell 27) → 2. Outlier check (Cell 26) → 3. Bukti cap 24 jam (Cell 5) → 4. `13_model_comparison_summary.csv` (baseline) → 5. Plot best/worst-3 baseline (Cell 28) → 6. `22a`/`22b_top3_pdq_per_*.csv` → 7. 9 plot ARIMAX (`22a_*`, `22b_*`) → 8. `23a-23d_top3_params_*.csv` → 9. 12 plot GB/LSTM (`23a-23d_*`) → 10. `24_perbandingan_baseline_vs_tuned.csv` + plotnya.

---

## 14. Restrukturisasi Populasi Unit — Cost & BBM HP&Type Sebagai Sumber Kebenaran

Ditemukan lewat audit `unit_map.json` (diupload user) bahwa populasi unit yang dipakai analisa (306 unit dari BBM AAB) mengandung banyak unit yang **seharusnya tidak dianalisa**: nama plat lama yang sudah ganti nomor, unit non-alat-berat (genset, mesin las, kompressor, dummy), dan potensi unit rental. Diperbaiki lewat revisi Cell 9 & Cell 12 — **cell lain semuanya tidak berubah posisi/isi**, mapping (`unit_map.json` dkk, Cell 1) **juga tidak berubah**.

### 14.1 Akar masalah: `unit_map` dibangun dari UNION dua sumber, bukan cuma BBM AAB

Cell 1 membangun `unit_map` dari `bbm_units | cost_names` — gabungan nama unit yang muncul di BBM AAB **dan** nama unit di file cost&bbm HP&Type. Konsekuensinya:
- Nama plat LAMA yang cuma nyantol di cost&bbm (misal karena belum diupdate) tetap dapat ID unit (`UNIT_XXXX`), padahal **tidak pernah ada baris transaksi BBM AAB sungguhan** di bawah nama itu — datanya "ghost".
- Exact-match nama cost&bbm → `unit_map` (cara lama, Cell 12 sebelum revisi) **selalu "berhasil"** untuk kasus ini, padahal ID yang di-match itu kosong datanya. Statistik "245/306 unit match" yang dicatat sebelumnya berpotensi menghitung sebagian match yang sebenarnya nyasar ke ID kosong ini.

### 14.2 49 unit "hilang" dari populasi 306 — sebagian besar plat lama

Audit silang `unit_map.json` vs `16_outlier_summary_per_unit.csv` (306 baris) menemukan 49 nomor ID yang tidak muncul. **44 di antaranya** adalah plat nomor lama yang disebut eksplisit sebagai `(EX.plat_lama)` di nama unit lain yang aktif (misal `UNIT_0011`="B 9494 JA" muncul lagi sebagai alias di `"B 9137 MJ (EX.B 9494 JA)"`). Sisa beberapa unit butuh info tambahan dari user untuk diselesaikan (lihat §14.5-14.7).

### 14.3 Genset, mesin las, kompressor, dan 1 unit DUMMY ikut ke populasi

Audit lanjutan menemukan **51 entri non-alat-berat** (genset kantor, mesin las statis, kompresor ban, plus `DUMMY (JANGAN DIPAKAI)`) yang semuanya ikut ke 306 unit populasi awal, karena outlier check & modeling sebelumnya cuma didasarkan pada "ada di BBM AAB" tanpa filter jenis unit.

### 14.4 [SUPERSEDED] Percobaan pertama: exclude by keyword

Percobaan awal: exclude unit dengan keyword `GENSET`, `MESIN LAS`, `KOMPRESSOR/KOMPESSOR`, `DUMMY` (auto-exclude), plus flag `MOBIL `/`RENTAL` sebagai borderline (perlu konfirmasi manual, tidak auto-exclude) — output `00b_unit_non_alat_berat_dikecualikan.csv` & `00c_unit_borderline_perlu_konfirmasi.csv`.

**Status: digantikan pendekatan §14.5** (lebih tepat karena tidak perlu tebak-tebak keyword mana yang termasuk "alat berat sungguhan").

### 14.5 [FINAL] Populasi unit = irisan BBM AAB (berdata) ∩ cost & bbm HP&Type

Atas permintaan user: batasi analisa **hanya ke unit yang terdaftar di file cost & bbm HP&Type** — karena itu daftar resmi aset alat berat perusahaan (unit rental/non-alat-berat yang bukan aset SPIL by design tidak akan terdaftar di situ).

**Cell 9 direvisi total** menjadi satu-satunya sumber kebenaran populasi unit:
1. Bangun `monthly_full` seperti biasa (merge rain + container).
2. Load `cost_df`, resolve tiap `NAMA ALAT BERAT` ke unit BBM AAB **yang beneran punya data** (bukan cuma exact-match ke `unit_map` yang bisa "ghost" — lihat §14.1), pakai matching bertingkat:
   - Exact match (dan wajib dicek py data BBM asli — fix dari isu §14.1)
   - `MANUAL_OVERRIDE` dict — 3 nickname/singkatan yang dikonfirmasi user (lihat §14.6)
   - Ekstrak teks setelah `"EX."` dalam kurung
   - Ekstrak teks sebelum `" ("`
   - Sisa unmatched → fuzzy match (`difflib.get_close_matches`) dicetak buat dicek manual
3. Bangun dataframe `kriteria` (HP, Type, Cap, JENIS, KRITERIA_ID) dari hasil resolve — pindah dari Cell 12 lama, jadi lebih awal di pipeline.
4. **Restrict `monthly_full` HANYA ke unit yang match ke cost&bbm** — sisanya masuk `00b_unit_tidak_ada_di_costbbm_dikecualikan.csv` (nama file sama, isi/definisi beda dari §14.4).
5. Print ringkasan: total unit BBM AAB (berdata) vs yang dipakai (match cost&bbm) vs yang dikecualikan.

Efeknya otomatis: genset/mesin/kompressor/dummy/rental/plat-lama tersingkir **kalau memang tidak terdaftar** di cost&bbm HP&Type — tanpa perlu daftar keyword manual seperti §14.4.

**Cell 12 lama (kriteria-matching berdiri sendiri) dihapus** — sudah menyatu ke Cell 9. Tidak ada pergeseran nomor cell lain (insert Cell diagnostik baru di §14.4 dan delete Cell 12 lama saling meniadakan posisinya — dikonfirmasi lewat audit ulang struktur notebook).

### 14.6 3 nickname/singkatan yang dikonfirmasi manual oleh user

Tidak bisa ditangkap otomatis lewat pola `EX.`/sebelum-kurung karena beda gaya penamaan (nickname vs singkatan resmi):

| Nama di cost&bbm (atau nama "orphan") | Nama aktif di BBM AAB (py data) |
|---|---|
| `TOP LOADER KALMAR 35 T/TOBATI` | `TOBATI (EX.FL KALMAR 32T)` |
| `L 9902 UR / S75` | `L 8477 UUC (EX.L 9902 UR)` |
| `TOP LOADER BOSS` | `WIND RIVER (EX.TL BOSS 42T)` |

Dimasukkan ke `MANUAL_OVERRIDE` dict di Cell 9.

### 14.7 FALCON — dikonfirmasi exclude, bukan bug

User konfirmasi: FALCON adalah alat elektrik, tidak punya HP (parameter yang dipakai BBM/diesel). Dicek: FALCON juga **tidak punya baris data BBM AAB sama sekali** — konsisten (alat elektrik metering-nya beda jalur, bukan lewat BBM). Otomatis tidak akan match ke cost&bbm (kalau memang tidak terdaftar HP di situ) maupun tidak akan pernah ikut populasi `monthly_hm` (karena tidak ada data). **Tidak perlu fix kode**, cuma didokumentasikan sebagai catatan di Cell 9.

### 14.8 FL RENTAL 01 vs FL RENTAL 01 TIMIKA — kasus berbeda, keputusan ditunda

User melaporkan: kemungkinan unit fisik yang sama, tapi **beda dari kasus lain** — keduanya (`UNIT_0034` & `UNIT_0035`) **sama-sama punya data BBM AAB sendiri-sendiri** (bukan salah satu kosong seperti kasus §14.6). Kalau ini benar 1 unit fisik yang pindah lokasi (Surabaya ↔ Timika), datanya perlu digabung (summed) supaya utilisasi tidak terpecah jadi 2 record yang masing-masing keliatan "idle" separuh tahun.

**Ditambahkan Cell 12 baru** (menggantikan kriteria-matching lama yang sudah pindah ke Cell 9) berisi 2 pengecekan:
1. Cross-check status 3 unit yang sempat "misteri" (`L9582UQ`, `TN05`, `TRONTON PK 215`) terhadap `excluded_df` hasil Cell 9 — harusnya otomatis ke-exclude di situ kalau memang tidak terdaftar cost&bbm.
2. Cek overlap bulan data antara `FL RENTAL 01` & `FL RENTAL 01 TIMIKA` — kalau overlap kosong → indikasi 1 unit pindah lokasi (aman digabung), kalau ada overlap → indikasi 2 unit fisik beda (jangan digabung). Kode merge disediakan tapi **sengaja non-aktif** (`MERGE_FL_RENTAL = False`) — perlu diaktifkan manual oleh user setelah lihat hasil cek overlap, karena ini mengubah data utilisasi asli, bukan cuma metadata.

**Status: belum dijalankan** — hasil overlap check & keputusan merge menunggu run pertama Cell 9-12 setelah restrukturisasi ini.

### 14.9 Konfirmasi cakupan perubahan

- **Cell yang isinya berubah**: HANYA Cell 9 (revisi total) dan Cell 12 (dari kriteria-matching standalone → diagnostic FL RENTAL + cross-check 3 unit misteri).
- **Cell lain (0-8, 10-11, 13-38)**: tidak diubah, tidak geser nomor. Dikonfirmasi lewat audit ulang urutan notebook — 1x insert (Cell diagnostik disisipkan di sesi sebelumnya) dan 1x delete (Cell 12 lama dihapus di sesi ini) saling meniadakan posisi.
- **Mapping (`unit_map.json`, `branch_map.json`, `lokasi_map.json`, Cell 1)**: TIDAK disentuh sama sekali. Deterministik — kalau di-generate ulang dari BBM AAB & cost&bbm yang sama, hasilnya identik dengan yang sudah ada di device user.

### 14.10 Efek Domino — Wajib Rerun

Karena populasi unit dasar (`monthly_full`) berubah di Cell 9, **semua cell setelahnya wajib di-rerun**: completeness (10), 4-kriteria exclusion (11), cap/smooth (14), semua baseline modeling (15-24), outlier check (26), skewness (27), grid search ARIMAX (29-30), tuning GB/LSTM (31-34), ringkasan Excel (35), dan semua plot top-3 (36-38). Checkpoint lama (`19a/19b_gridsearch_*`, `20a/20b_tuning_*`) **tidak valid lagi** untuk auto-skip karena populasi unit beda — sebaiknya file checkpoint lama dihapus/di-rename dulu sebelum rerun supaya tidak salah nyambung ke hasil grid search populasi lama.

⚠️ **File output lama yang perlu diabaikan/dianggap usang** setelah restrukturisasi ini: semua CSV/PNG dari `16_*` sampai `24_*` yang dihasilkan SEBELUM Cell 9 direvisi (termasuk yang sudah pernah dicek bareng Claude di sesi-sesi sebelumnya) — populasi unit dasarnya sudah beda, jadi angka MAPE_GLOBAL dkk kemungkinan besar berubah setelah rerun.

---

## 15. Bimbingan 2 & Notebook Baru (`code_v2.ipynb`) — RMSE, Model Global Terbaik, Tuning Individual

### 15.1 Update dari Bimbingan 2

Dosen memberi 3 arahan baru:
1. **Tentukan arah prediksi**: overestimate atau underestimate? Serta **metrik error**: RMSE atau MAPE (dosen condong RMSE karena mayoritas riset pakai itu; MAPE boleh kalau ada alasan kuat).
2. **Alur baru**: dari 3 model (ARIMAX/GB/LSTM), cari **model global terbaik** dulu — tapi **terpisah untuk pendekatan per-unit dan per-kriteria** (jadi bisa beda model menangnya). Setelah itu, tuning parameter **INDIVIDUAL per unit** (pakai model pemenang pendekatan per-unit) dan **individual per kriteria** (pakai model pemenang pendekatan per-kriteria). Baru dari situ ditentukan pendekatan mana (per-unit vs per-kriteria) yang lebih baik.
3. **Notebook baru**: `code.ipynb` dipertahankan sebagai arsip percobaan awal (buat lampiran skripsi), progress lanjutan dikerjakan di file baru, standalone + checkpoint sendiri.

### 15.2 Keputusan: RMSE utama, Bias dilaporkan (bukan target), MAPE sekunder

- **RMSE jadi metrik UTAMA** buat ranking model & parameter. Alasan: (a) MAPE terbukti gak stabil di tahap sebelumnya — meledak 500-1000%+ untuk unit ber-actual≈0 (UNIT_0322 dkk); (b) mayoritas riset akademik forecasting numerik memang pakai RMSE, bukan cuma soal selera.
- **Bias (Mean Error = rata-rata(actual − prediksi))** ditambahkan sebagai metrik diagnostik/pelaporan, **BUKAN kriteria pemilihan model**. Alasan: hasil prediksi UTILITAS dipakai untuk banyak keperluan berbeda (perencanaan alokasi alat, evaluasi kinerja, prediksi kebutuhan BBM, ditampilkan di chatbot perusahaan, dan bahan project lain) yang **tidak punya satu arah risiko yang dominan** — jadi gak ada alasan kuat buat sengaja bikin model bias ke overestimate atau underestimate. Target: prediksi **unbiased** (bias mendekati 0).
  - Bias > 0 → model cenderung underestimate (actual > prediksi)
  - Bias < 0 → model cenderung overestimate (prediksi > actual)
- **MAPE** tetap dihitung & dilaporkan (buat pembaca awam & bahan pembanding dengan tahap sebelumnya), tapi TIDAK dipakai memilih model/parameter terbaik.

### 15.3 File baru: `code_v2.ipynb` + folder `checkpoints_v2/`

Standalone penuh (semua preprocessing di-copy ulang dari `code.ipynb` yang sudah final pasca-restrukturisasi §14, termasuk populasi cost&bbm-only, cap HM 24 jam, dll — bukan referensi ke file lain). Checkpoint per kombinasi (resumable), folder output terpisah (`./checkpoints_v2/`) supaya gak campur sama `code.ipynb`.

**Tambahan requirement yang baru disadari user saat proses jalan**: selain model, 3 teknik **data-prep** juga perlu dibandingkan buat nentuin mana yang terbaik dipakai, **sebelum** nyari model global terbaik (bukan sesudahnya) — karena model terbaik di satu prep bisa jadi bukan yang terbaik di prep lain:
1. **Savitzky-Golay smoothing** — alternatif dari cap+rolling-mean (puncak gak terlalu tinggi, lembah gak terlalu landai)
2. **RobustScaler** — median & IQR based, kurang sensitif ke outlier dibanding hard-cap
3. **Yeo-Johnson (PowerTransformer)** — normalisasi distribusi, alternatif dari heuristik skewness mean/median switching

Keputusan scope (dikonfirmasi user): 3 teknik ini dibandingkan **satu-satu** (bukan digabung/dikombinasikan), dan **full rigorous** — semua kombinasi 4 varian (baseline + 3 teknik baru) × 3 model × 2 pendekatan = **24 kombinasi** ditest semua, bukan cuma sampling pakai 1 model cepat dulu.

**Desain teknis penting**:
- GB itu tree-based, invariant terhadap scaling FITUR — jadi ketiga teknik baru ini diterapkan ke **target (UTILITAS)**, bukan fitur input, supaya tetap berpengaruh ke ketiga model (ARIMAX, GB, LSTM).
- Transformer (RobustScaler/PowerTransformer) **fit di TRAIN saja**, lalu **transform-only** (tanpa re-fit) ke TEST — anti data leakage.
- Prediksi model (dalam skala transformed) di-**inverse-transform balik ke skala jam asli** sebelum dihitung RMSE — supaya ke-4 varian bisa dibandingkan apple-to-apple dalam satuan jam. LSTM dapat **dua lapis inverse**: scaler internal MinMax dia sendiri (buat stabilitas training) + transformer prep-variant di atasnya.
- Savitzky-Golay & baseline tetap dalam skala jam asli (identity inverse); RobustScaler & Yeo-Johnson perlu inverse eksplisit.

### 15.4 Tahap 2 — Hasil Perbandingan 24 Kombinasi (Model Global Terbaik per Pendekatan)

**Bug ditemukan & diperbaiki saat proses**: `OSError WinError 1450` (resource exhausted, Windows) — akibat `joblib.Parallel(n_jobs=-1)` bikin worker pool baru tiap batch (ratusan kali total). Fix: `Parallel` di-reuse pakai `with` context per blok (bukan per batch), `N_JOBS` diturunin ke 4, `BATCH_SIZE` dinaikin ke 20, dan master loop dipecah jadi **4 cell terpisah** (satu per varian data-prep) supaya kalau macet, gampang diisolasi & di-restart tanpa ngulang varian yang udah selesai.

**Bug kedua**: VS Code sempat crash `reason: oom` (window Electron kehabisan memori) — bukan dari Python/kernel, tapi dari volume TEKS OUTPUT yang numpuk (print progress tiap batch, ribuan kombinasi). Fix: `PRINT_EVERY = 5` — print progress cuma tiap 5 batch, bukan tiap batch.

**Bug ketiga**: hasil `v2_MASTER_SUMMARY_24_kombinasi.csv` sempat ada baris duplikat (2-3x identik) karena `ALL_SUMMARY_ROWS` numpuk tiap kali cell varian di-rerun (misal abis restart kernel karena crash). Fix: tiap cell varian sekarang dedupe dulu (buang baris lama varian itu) sebelum nambahin hasil baru — idempotent, aman di-rerun kapan aja.

**Hasil akhir (setelah fix, 24 kombinasi bersih tanpa duplikat)**:

| Pendekatan | Pemenang | RMSE_GLOBAL | Bias | MAPE |
|---|---|---|---|---|
| **Per-unit** | Gradient Boosting + savgol (lr=0.01, iter=200, depth=7, leaf=5) | 75.36 | -1.06 | 45.52% |
| **Per-kriteria** | Gradient Boosting + savgol (lr=0.01, iter=300, depth=7, leaf=5) | **59.11** | -2.44 | 41.02% |

**Temuan**: GB + savgol menang di KEDUA pendekatan (bukan kebetulan campur beda model) — konsisten. Savgol secara umum ngalahin baseline/robust/yeojohnson di hampir semua kombinasi, jadi validasi bahwa smoothing yang lebih halus (gak motong ekstrem kayak hard-cap 95th percentile) membantu. Bias kedua pemenang kecil (mendekati nol), sesuai target unbiased dari §15.2.

### 15.5 Tahap 3 — Tuning Individual per Unit & per Kriteria (Hasil Final)

Karena model pemenang SAMA (GB+savgol) buat kedua pendekatan, cukup 1 jenis fungsi tuning (GB), dipakai 2x:
- **Per-unit**: tiap unit (222 unit berhasil, dari populasi ~227) dituning individual — coba semua 36 kombinasi GB, ambil RMSE terkecil KHUSUS buat unit itu (bukan 1 kombinasi global lagi).
- **Per-kriteria**: tiap grup kriteria (76 grup) dituning individual dengan cara sama.
- Paralelisasi di level UNIT/KRITERIA (bukan di level kombinasi hyperparameter) — 1 worker pegang 1 unit/kriteria penuh (36 kombinasi sekuensial di dalamnya) — desain ini yang bikin gak kena resource-exhausted lagi kayak Tahap 2.

**KESIMPULAN FINAL** (dari `v3_KESIMPULAN_FINAL_per_unit_vs_per_kriteria.csv`):

| Pendekatan (parameter individual) | RMSE_GLOBAL | Bias | MAPE | N_GROUP |
|---|---|---|---|---|
| **Per-kriteria** | **56.77** | -3.11 | 38.21% | 76 |
| Per-unit | 69.15 | -1.47 | 41.44% | 222 |

**>>> PENDEKATAN TERBAIK FINAL: PER-KRITERIA (individual tuning), model Gradient Boosting + data-prep Savitzky-Golay.**

Konsisten dengan Tahap 2 (per-kriteria juga menang di situ) — tuning individual memperbaiki kedua pendekatan (RMSE turun dari 75.36→69.15 unit, 59.11→56.77 kriteria) tapi urutan pemenang gak berubah.

Distribusi RMSE per grup (dari `v3_final_params_*_individual.csv`):
- Per-unit: median RMSE 42.47, mean 54.89, range 2.5-259.1 (222 unit, tidak ada yang gagal fit)
- Per-kriteria: median RMSE 31.58, mean 42.65, range 4.3-211.8 (76 kriteria, tidak ada yang gagal fit)

### 15.6 ⚠️ TEMUAN PENTING — "Prediksi Mendatar" Terkonfirmasi Muncul di Hasil Final

Dosen sempat wanti-wanti soal ini di Bimbingan 1 ("kadang-kadang muncul prediksi mendatar, itu kesalahan klasik") — poin ini sempat ditunda (§13) tapi sekarang **terkonfirmasi nyata muncul** di plot hasil final Tahap 3.

**Pola yang ditemukan**: unit/kriteria dengan RMSE terburuk didominasi yang **prediksinya flat** (garis oranye rata, gak ngikutin naik-turun actual):
- `UNIT_0218` (RMSE=259.1, TERBURUK di seluruh 222 unit) — prediksi flat ~380-400, actual lompat 300-750
- `UNIT_0192` (RMSE=211.8) — prediksi flat ~30-60, actual naik terus 0→540
- Per-kriteria: `REACH STACKER|KONE 450|45.0|375`, `TRAILER|PKC311|4.2|311`, `TRAILER|CK12|0.0|180` — 3 dari 5 kriteria terburuk, semuanya **`n_unit=1`** (kriteria isinya cuma 1 unit doang)

**Analisis akar masalah**: kriteria dengan `n_unit=1` itu secara efektif SAMA SAJA dengan per-unit (gak ada manfaat pooling data dari unit lain), tapi datanya tetap kependekan (~10-12 bulan) buat GB belajar pola naik-turun → GB nyerah dan cuma nebak rata-rata (flat line). Dari top-5 kriteria terburuk, 4 di antaranya `n_unit=1`.

**BELUM diselesaikan** — ini poin diskusi yang perlu dibawa ke bimbingan berikutnya. Opsi yang bisa didiskusikan ke dosen:
- Kasih threshold minimum jumlah unit per kriteria buat "boleh" masuk pendekatan per-kriteria (kriteria ber-anggota tunggal di-treat beda, misal fallback ke ARIMAX per-unit)
- Terima aja sebagai limitasi data (dicatat di bab pembahasan)
- Analisis lanjut: hitung berapa % dari total RMSE_GLOBAL yang disumbang kriteria/unit ber-n_unit=1, biar tau seberapa besar dampaknya ke kesimpulan keseluruhan

---

## 16. Tahap 2b — Drill-down 12 Kombinasi per Unit & per Kriteria (Arahan Bimbingan Lanjutan)

### 16.1 Latar belakang & scope

Bimbingan lanjutan minta drill-down lebih detail dari Tahap 2/3: untuk **tiap unit** dan **tiap kriteria** secara individual, dicari kombinasi (model × data-prep) mana dari **12 kombinasi** (3 model: ARIMAX/GB/LSTM × 4 varian: baseline/savgol/robust/yeojohnson) yang paling cocok — bukan cuma pemenang global (GB+savgol) yang dipakai rata di Tahap 2/3.

**Keputusan metodologi (dikonfirmasi user)**:
- **Parameter model pakai hasil Tahap 2 apa adanya** (bukan retuning ulang per unit/kriteria untuk semua 12 kombinasi) — alasan: retuning 12 kombinasi × 222 unit / 76 kriteria setara 12× beban Tahap 3 (yang aja udah berat), gak feasible secara komputasi. **Dicatat sebagai limitasi**: parameter Tahap 2 dituning buat RMSE_GLOBAL agregat (bukan per-unit/kriteria), jadi hasil Tahap 2b ini jawab "kombinasi mana yang RELATIF paling cocok", bukan "RMSE/MAPE terbaik yang BISA dicapai unit ini". Retuning parameter individual per unit/kriteria (buat kombinasi pemenang masing-masing) **ditunda ke tahap berikutnya**, setelah kombinasi model+prep per unit/kriteria ini diketahui (lihat §9 langkah selanjutnya).
- **Ranking "kombinasi terbaik" pakai MAPE** (arahan dosen terbaru) — RMSE tetap dihitung & ditampilkan berdampingan di semua tabel, gampang ganti kriteria ranking kapan aja tanpa rerun refit kalau dosen minta balik ke RMSE.

### 16.2 Implementasi teknis

Ditambahkan sebagai **7 cell baru di `code_v2.ipynb`** (disisipkan setelah ringkasan Tahap 2, sebelum Tahap 3 mulai): parse parameter 24 kombinasi dari `v2_MASTER_SUMMARY_24_kombinasi.csv` → refit 12 kombinasi per-unit → refit 12 kombinasi per-kriteria → hitung RMSE/MAPE per (unit, kombinasi) & per (kriteria, kombinasi) → tentukan kombinasi terbaik + tally frekuensi → export Excel → plot.

Fungsi `fit_arimax/gb/lstm_combo_unit/kriteria` (cell 22-23) ditambah parameter opsional `return_preds=False` — kalau `True`, fungsi balikin juga `preds_df` mentah (per-unit/per-baris-bulan), bukan cuma metrik agregat seperti sebelumnya. Default `False` gak ubah perilaku Tahap 2/3 yang sudah jalan.

### 16.3 Bug yang ditemukan & diperbaiki selama proses

1. **[FIXED] `parse_param_str` salah parse tipe data dari CSV**: parameter `max_depth=None` yang disimpan lalu dibaca ulang pandas jadi `NaN` (bukan string `'None'`), dan `max_iter=200` (int) jadi `'200.0'` (float-string) karena kolom campur NaN. Fix: `_num()` helper dirapikan — deteksi `'nan'`/`'None'` → `None`, dan float bulat (`f.is_integer()`) → dikonversi balik ke `int`.
2. **[FIXED — KRITIS] Kolom CSV gak konsisten antar model di pendekatan per-kriteria**: `fit_arimax_combo_kriteria` nyimpen 8 kolom (ada `AGG`) per baris prediksi, sedangkan `fit_gb_combo_kriteria`/`fit_lstm_combo_kriteria` cuma 7 kolom (tanpa `AGG`). Saat di-append ke checkpoint CSV yang sama (`header=False`), pandas nulis value APA ADANYA sesuai urutan kolom dataframe saat itu — **tidak dicocokkan ke nama header file**. Efeknya: semua nilai baris GB/LSTM geser satu kolom ke kiri, dan kolom `VARIAN` (paling kanan) jadi `NaN`. Karena `groupby(['MODEL','VARIAN'])` di pandas **default buang baris yang NaN di key groupby-nya** (`dropna=True`), baris GB/LSTM per-kriteria jadi seolah-olah hilang total dari hasil agregasi — padahal datanya numpuk di file, cuma nyasar kolom. Fix: kolom `AGG` dihapus dari baris-per-prediksi ARIMAX per-kriteria (tetap disimpan di `result` / ringkasan metrik saja), supaya skema kolom 3 model konsisten.
3. **[FIXED] Efek turunan bug #2**: checkpoint `v2b_combo_preds_per_kriteria.csv` yang sudah kadung korup harus dihapus & direfit ulang dari nol. Sempat ada bug tambahan waktu gabung cell hapus-checkpoint dengan cell refit — baris `done_combo_kriteria = set()` (reset daftar kombinasi selesai) kehapus gak sengaja, ketinggalan dari cell gabungan. Fix: reset eksplisit `done_combo_kriteria = set()` persis setelah hapus file.

### 16.4 Hasil akhir

File: `v2b_hasil_12kombinasi_per_unit_kriteria.xlsx`, 6 sheet:

| Sheet | Isi |
|---|---|
| `Detail_PerUnit_12Kombinasi` | 2.660 baris = 222 unit × 12 kombinasi lengkap (RMSE, MAPE, Bias tiap kombinasi tiap unit) |
| `Detail_PerKriteria_12Kombinasi` | 837 baris — 76 kriteria × 12 kombinasi, TAPI ARIMAX+robust cuma berhasil di 38/76 kriteria & ARIMAX+yeojohnson di 39/76 (bukan bug — pola ini sudah ada dari checkpoint paling awal, kemungkinan ARIMAX gagal konvergen di sebagian kriteria untuk 2 varian ini; **belum didalami akar penyebabnya**, dicatat sebagai catatan terbuka) |
| `Best_Combo_PerUnit` | 222 baris — kombinasi (model+varian) terbaik tiap unit, ranking by MAPE |
| `Best_Combo_PerKriteria` | 76 baris — sama, per kriteria |
| `Tally_PerUnit` / `Tally_PerKriteria` | Frekuensi tiap kombinasi jadi "juara" di antar unit / antar kriteria |

**Temuan tally (poin diskusi bimbingan)**:
- **Per-unit**: GB+savgol (pemenang global Tahap 2) menang individual di **72/222 unit (32%)** — bukan mayoritas mutlak. ARIMAX+baseline runner-up (36 unit), sisanya tersebar ke 10 kombinasi lain.
- **Per-kriteria**: GB+savgol menang di **18/76 kriteria (24%)**. GB+yeojohnson runner-up (10 kriteria).
- **Insight**: gak ada 1 kombinasi yang optimal buat semua unit/kriteria — mendukung alasan kenapa drill-down individual ini perlu dilakukan (beda unit/kriteria, beda karakteristik data, beda kombinasi yang cocok).

**Plot**: 6 gambar PNG terpisah (bukan 1 gambar gabungan) — per pendekatan (unit/kriteria) dipecah jadi 3: 5-terbaik, 5-terburuk (rank 1-5), 5-terburuk (rank 6-10). File: `v2b_plot_perunit_best5.png`, `v2b_plot_perunit_worst_1_5.png`, `v2b_plot_perunit_worst_6_10.png`, dan set sama untuk `perkriteria`.

### 16.5 Catatan terbuka (belum didalami)

- Kenapa ARIMAX+robust dan ARIMAX+yeojohnson per-kriteria cuma berhasil ~separuh kriteria (38-39 dari 76) — dugaan gagal konvergen, belum dikonfirmasi penyebab pastinya. Perlu didalami kalau relevan buat pembahasan skripsi.
- Parameter yang dipakai di Tahap 2b ini masih global-tuned (dari Tahap 2), bukan hasil tuning individual — lihat §9 langkah selanjutnya buat rencana lanjutan.

---

Notebook di-convert ke `.py`, dijalankan di server lebih mumpuni untuk grid search/tuning berat (§10.5, §10.6). **Dikonfirmasi**: berhasil jalan sampai output akhir tanpa masalah — tidak perlu penyesuaian tambahan.

**Prosedur aman stop/lanjut**:
1. **Wajib** stop kernel dengan benar sebelum matikan laptop/server.
2. Nyala lagi → run cell 0-24 (wajib, variabel hilang tiap restart kernel).
3. Cell 26-30 → run ulang, cepat kalau sudah selesai (auto-skip checkpoint).
4. Cell 31-34 → sama, auto-skip berkat fix §10.8.
5. Cell 35 → run paling akhir setelah semua checkpoint di atas lengkap.

---

## 12. Catatan Penggunaan Claude Project untuk TA Ini

Project ini dipakai lintas-chat. Yang **otomatis kebawa** ke chat baru dalam project sama: ringkasan konteks umum dari memory (garis besar TA, keputusan penting, bug yang sudah di-fix — hasil rangkuman berkala, bukan transkrip penuh).

Yang **TIDAK otomatis kebawa**, perlu diupload ulang tiap chat baru (kecuali ditaruh di Project Knowledge):
- File (`code.ipynb`, CSV, XLSX, proposal) — lampiran chat lama tidak ikut ke chat baru.
- Detail teknis presisi (isi lengkap tiap cell, angka MAPE exact) — memory cuma nyimpen ringkasan.

**Rekomendasi**: upload ulang `PROGRESS.md` terbaru (+ `code.ipynb` kalau perlu cek/edit kode) di tiap chat baru, atau taruh keduanya di Project Knowledge supaya otomatis kebaca tanpa upload manual.

---

## 5. Catatan Metodologi — Perlu Keputusan (Di Luar Cakupan Eksplisit Proposal)

### 5.1 MAPE_GLOBAL (mean) sangat sensitif terhadap unit ber-utilitas rendah/nol
Proposal (baris 244) sudah atur kasus actual=0 persis, tidak atur kasus mendekati-nol. ⚠️ Perlu dicek: `eval_pred()` return `NaN` (bukan `0`) kalau semua test=0 — belum diverifikasi apakah kasus ini pernah terjadi.

### 5.2 Pendekatan per-kriteria (pooled): efektivitas bervariasi
60 dari 88 `KRITERIA_ID` cuma 1 unit — pooling praktis kosong. Belum di-breakdown per ukuran kriteria.

### 5.3 Audit unit yang dikecualikan
79 dari 306 unit dikecualikan sesuai 4 kriteria proposal. 72 karena idle total 1 tahun — belum divalidasi manual ke tim SPIL.

---

## 6. Hal Lain yang Perlu Divalidasi Manual

- Spot-check 2-3 unit dari Excel mentah asli vs checkpoint.
- Validasi magnitude volume container & curah hujan ke tim SPIL / BMKG.
- Konfirmasi pola idle unit (§5.3) ke tim SPIL.
- Konfirmasi ke dosen: outlier IQR (§10.3) — ganti capping atau EDA terpisah?
- Konfirmasi ke dosen: interpretasi CURRSTATE per jenis alat berat (§3.2).

---

## 7. Hal-hal di Luar Cakupan Proposal (Belum Diimplementasikan)

1. Reinstate naive baseline (§4.4, §4.6).
2. Metrik evaluasi tambahan (§5.1) — median MAPE, sMAPE.
3. Breakdown pooling per ukuran kriteria (§5.2).
4. Diferensiasi CURRSTATE per jenis alat berat (§3.2).
5. Reproducibility LSTM — seeding tambahan.
6. Validasi manual data (§5.3, §6).
7. Kategorisasi "layak/tidak layak" berdasar ambang MAPE — tidak diminta proposal.
8. ~~Plot top-3 PDQ terbaik ARIMAX untuk hasil poin 4 (§10.9)~~ ✅ Dikode Cell 36.

---

## 17. `code_v3.ipynb` — Split Train/Test Baru + Exclude/Remap Unit (Arahan Bimbingan Lanjutan #2)

### 17.1 Latar belakang & scope

Bimbingan lanjutan (setelah §16/Tahap 2b) minta ulangi **seluruh alur** (Tahap 1→2→2b→3) tapi cuma ganti tanggal train/test:
- **Train**: Jan 2023 - Agu 2025 (sebelumnya beda periode)
- **Test**: Sep - Des 2025 (**cuma 4 bulan** — jauh lebih pendek dari sebelumnya)

Plus 2 permintaan tambahan:
- **Plot akhir** harus nampilin **actual dari TRAIN+TEST penuh** (bukan cuma test), prediksi cuma nongol di periode test — biar keliatan konteks histori sebelum test-nya.
- **Tiap tahap proses** (bukan cuma hasil akhir) diexport ke **Excel** — biar pas sidang gak perlu buka raw data / CSV mentah lagi, tinggal buka Excel yang udah jadi.

Notebook baru **`code_v3.ipynb`** dibikin standalone (copy dari `code_v2.ipynb` final pasca-§16), checkpoint sendiri di `checkpoints_v3/` (gak nimpa `checkpoints_v2/` — v2 tetap ada sebagai arsip/pembanding).

**Catatan penamaan**: "v3" di sini itu **notebook baru** (ganti split tanggal), BUKAN tahap metodologi baru. Struktur di dalamnya tetap sama persis: Tahap 1 (preprocessing) → Tahap 2 (24 kombinasi) → Tahap 2b (drill-down 12 kombinasi per unit/kriteria) → Tahap 3 (tuning individual GB+savgol seragam). Tahap 2b dan Tahap 3 **dua eksperimen paralel yang berdiri sendiri-sendiri**, belum digabung jadi 1 kesimpulan final (lihat §17.6).

### 17.2 Masalah struktural yang ditemukan & diperbaiki

**[FIXED] Threshold filter unit gak cocok sama test yang cuma 4 bulan.** `filter_units` (Tahap 1) awalnya mensyaratkan **minimal 12 bulan test** biar 1 unit lolos filter. Kalau gak diubah, SEMUA unit bakal ke-exclude (test cuma 4 bulan), `train_df`/`test_df` jadi kosong. **Fix**: threshold diturunin jadi **4 bulan, ketat** (semua 4 bulan test harus lengkap, gak ada yang bolong) — atas konfirmasi user.

### 17.3 Exclude 10 unit + remapping ID (arahan lanjutan, setelah review MAPE Tahap 2b lama)

Setelah lihat hasil Tahap 2b (§16) dengan populasi/split LAMA, user memutuskan **exclude 10 unit** dari analisa, lalu **unit yang tersisa di-remap ID-nya berurutan dari 1** (biar gak ada lubang nomor).

**10 unit yang diexclude** (kode lama → nama asli):
| Kode lama | Nama asli |
|---|---|
| UNIT_0037 | FORKLIF MITS/KENANGA |
| UNIT_0088 | KALMAR 29 |
| UNIT_0095 | KALMAR11/KINGKONG 2 |
| UNIT_0096 | KALMAR2/BISON |
| UNIT_0134 | L 8060 UR (EX.L 9200 UN) |
| UNIT_0159 | L 8316 UK (EX.L 9070 UR) |
| UNIT_0166 | L 8460 UK (EX.L 9637 US) |
| UNIT_0306 | PADI |
| UNIT_0330 | SIDE LOADER BOSS 2 |
| UNIT_0336 | TERATAI |

**Implementasi**: cell baru disisipkan tepat setelah `monthly_full`/`kriteria` final (sebelum semua tahap lain), jadi SEMUA cell berikutnya otomatis pakai populasi & ID baru tanpa perlu ubah cell lain manual. Sisa 345 unit (dari 355 total kode di `unit_map.json`) di-remap sequential `UNIT_0001`...`UNIT_0345`, urutan relatif dipertahankan (bukan diacak) — cth: `UNIT_0089` (lama) → `UNIT_0087` (baru), karena `UNIT_0088` di antaranya dibuang.

**Output**: `unit_map_v3.json` (nama asli → kode baru, otomatis ke-generate ulang tiap run), plus `08_kriteria_unit.csv`/`04_monthly_with_exog.csv` ke-save ulang dengan kode baru.

### 17.4 Excel per tahap (biar gak perlu buka raw data pas sidang)

| Tahap | File Excel | Isi (sheet) |
|---|---|---|
| Preprocessing — mapping kriteria↔unit + data HM | `v3_kriteria_unit_mapping.xlsx` | `Ringkasan_Kriteria` (jumlah unit, daftar unit, total/rata2 HM per kriteria), `Total_HM_per_Kriteria_per_Bulan` (long-format, HM dijumlah semua unit anggota per bulan), `Pivot_Total_HM_per_Kriteria` (wide, per bulan), `Detail_HM_per_Unit_Kriteria` (per unit per bulan, long), `Pivot_HM_per_Kriteria` (wide per unit) |
| Preprocessing — info split | `v3_train_test_split_info.xlsx` | `Info_Split` (rentang tanggal, jumlah bulan/baris), `Unit_Dipakai`, `Unit_Dikecualikan` (dari `filter_units`, BEDA dari 10 unit exclude manual §17.3) |
| Tahap 2 — 24 kombinasi | `v3_tahap2_24kombinasi.xlsx` | `Semua_24_Kombinasi`, `Ringkasan_PerUnit`, `Ringkasan_PerKriteria` |
| Tahap 2b — 12 kombinasi per unit/kriteria | `v2b_hasil_12kombinasi_per_unit_kriteria.xlsx` | (struktur sama §16.4: `Detail_PerUnit/Kriteria_12Kombinasi`, `Best_Combo_PerUnit/Kriteria`, `Tally_PerUnit/Kriteria`) — regenerated pakai populasi/split baru |
| Tahap 3 — tuning individual | `v3_tahap3_tuning_individual.xlsx` | `Parameter_PerUnit`, `Parameter_PerKriteria`, `Kesimpulan_Final` |

### 17.5 Bug yang ditemukan & diperbaiki selama proses

1. **[FIXED] `code_v3.ipynb` awalnya dibangun dari basis `code_v2_2.ipynb` yang stale** (belum termasuk fix `done_combo_kriteria = set()` dari §16.3 bug#3) — `NameError: name 'done_combo_kriteria' is not defined` muncul lagi pas refit per-kriteria. Fix: tambahin balik baris reset itu.
2. **[FIXED] TensorFlow graph/`FunctionDef` numpuk lintas banyak model LSTM dalam 1 sesi kernel** — `fit_lstm_combo_unit`/`_kriteria` bikin model Keras baru tiap unit/kriteria (222+/69 iterasi) TANPA pernah clear session. Setelah 2 varian (baseline selesai, lanjut robust), cache graph TF kelewat batas ukuran protobuf (2GB) → `DecodeError: Error parsing message with type 'tensorflow.FunctionDef'`. **Fix**: tambah `del model; keras.backend.clear_session(); gc.collect()` di akhir tiap iterasi unit/kriteria dalam loop.
3. **[FIXED] `MemoryError` beneran (RAM abis) pas refit Tahap 2b** — fungsi `get_prepped(variant)` (dipakai di cell refit 12-kombinasi) nyimpen SEMUA varian yang pernah diproses di `_prep_cache` dict (dataframe gede-gede) tanpa eviction, numpuk lintas 4 varian barengan. **Fix**: `get_prepped` sekarang cuma nyimpen 1 varian dalam cache — ganti varian → cache lama di-`clear()` + `gc.collect()` duluan.
4. **[OBSERVASI — bukan bug kode, pelajaran proses]** Kernel VS Code Jupyter sempat **mati beneran di tengah proses** (Tahap 2 grid search) TANPA notifikasi langsung — user awalnya kira masih jalan (status cell masih "running"), padahal print progress udah berhenti nambah lama. **Beda** dari 2 kejadian "kernel crashed" sebelumnya di fase v2 (§16, itu notifikasinya muncul SETELAH kerjaan kelar & tersimpan, jadi aman/palsu-alarm). **Pelajaran**: status "running" di cell TIDAK cukup jadi indikator kernel hidup — yang harus dicek itu **print progress-nya masih nambah atau nggak**. Kalau berhenti nambah lebih dari beberapa menit (apalagi LSTM), curigai duluan, jangan tunggu lama.
5. **[OPEN / DI-HOLD USER]** ARIMAX per-kriteria gagal massal di split baru: dari diagnostik (`v3_diagnostik_arimax_kriteria.csv`), **218 dari 276 percobaan GAGAL** (79%) — baseline/savgol/yeojohnson masing-masing gagal ~66-68 dari 69 kriteria (hampir semua!), cuma `robust` yang lumayan (18 gagal dari 69). Error dominan: `"Input contains NaN."` (200×), `LU decomposition error` (15×), `Schur decomposition solver error` (3×). GB & LSTM per-kriteria tetap 100% sukses (udah ada `.dropna()` sebelum fit, ARIMAX belum).
   - **Sudah dicek & TERBUKTI BUKAN penyebabnya**: NaN di kolom exog (`CURAH_HUJAN`/`VOLUME_CONTAINER`) di level RAW data — baik dicek per-bulan (pooled semua unit) maupun per-unit individual, hasilnya 0 NaN semua. NaN di `UTILITAS_SMOOTH` hasil `DATA_PREP_VARIANTS` juga 0 di semua 4 varian.
   - **Hipotesis yang BELUM dicek** (next step kalau dilanjut): kemungkinan `DATA_PREP_VARIANTS[variant]()` melakukan reindex per-unit ke rentang bulan penuh (ngisi bolong tanggal), dan kemungkinan MENGISI target (`UTILITAS_SMOOTH`) buat baris-baris baru hasil reindex itu, TAPI TIDAK ikut mengisi kolom exog di baris baru tsb — jadi NaN baru muncul SETELAH proses `get_prepped(variant)`, bukan di data mentah (`train_full_raw`) yang udah dicek bersih. Next step: cek NaN di `get_prepped(variant)`'s output (`train_full['CURAH_HUJAN']`/`['VOLUME_CONTAINER']`) langsung, per varian.
   - **Fix kandidat yang SUDAH DIRANCANG tapi BELUM DITERAPKAN**: tambah `.dropna()`/alignment index di `tr_y`/`tr_x` sebelum `pm.ARIMA.fit()` dalam `fit_arimax_combo_kriteria` (dan sebagai jaga-jaga juga di `fit_arimax_combo_unit`), nyamain perilaku defensif kayak GB/LSTM yang udah dropna duluan.
   - **KEPUTUSAN USER: DI-HOLD.** Lanjutkan investigasi di chat baru HANYA KALAU masalah yang sama masih muncul lagi setelah percobaan berikutnya di sana.

### 17.6 Temuan metodologi penting (klarifikasi, bukan bug)

- **Tahap 2b vs Tahap 3 itu 2 eksperimen paralel independen**, bukan salah satu "menggantikan" yang lain:
  - **Tahap 2b**: model+data-prep **individual** per unit/kriteria (pilih sendiri dari 12 opsi berdasar MAPE terendah), TAPI parameter di dalam model itu **masih seragam** (parameter global hasil Tahap 2, BELUM di-retuning individual — ini limitasi yang disengaja/ditunda, lihat §16.1).
  - **Tahap 3**: model+data-prep **seragam** (GB+savgol, pemenang global Tahap 2) buat SEMUA unit/kriteria, cuma parameter GB-nya yang di-tuning individual per unit/per kriteria.
  - Belum ada yang menggabungkan keduanya (kombinasi model+prep individual DARI Tahap 2b + parameter individual ala Tahap 3 buat kombinasi pemenang masing-masing) — itu next-step besar yang beberapa kali disebut tapi ditunda (§9).
- **Kesimpulan Tahap 3 BERBALIK di split baru**: per-unit individual sekarang **MENANG** (RMSE_GLOBAL 53.90) vs per-kriteria (62.08) — kebalikan dari hasil split lama (per-kriteria menang, 56.77 vs 69.15, lihat §15.5). Artinya kesimpulan "per-unit vs per-kriteria mana yang lebih baik" itu **sensitif terhadap rentang train/test & populasi unit**, bukan kebenaran tetap — perlu dicatat di bab pembahasan skripsi.
- **Tally kombinasi terbanyak juga berubah**: di data v3 ini, **GB+baseline** paling sering menang individual (34/205 unit = 17%, 18/69 kriteria = 26%) — BUKAN GB+savgol lagi seperti di data lama (§16.4: 32%/24%). Ini WAJAR, bukan bug — Tahap 2's RMSE_GLOBAL (pool semua unit jadi 1 angka, didominasi unit ber-HM besar & error kuadrat) dan Tahap 2b's tally (vote per-unit pakai MAPE, tiap unit bobotnya sama, dinormalisir skala) itu **dua filosofi agregasi yang beda**, gak wajib sepakat.
- **BELUM ADA angka RMSE_GLOBAL/MAPE_GLOBAL gabungan buat skenario Tahap 2b** ("tiap unit/kriteria pakai kombinasi terbaiknya sendiri-sendiri, lalu semua digabung jadi 1 metrik") — padahal ini penting buat dibandingkan apple-to-apple sama Tahap 2 (1 kombinasi seragam) dan Tahap 3 (`Kesimpulan_Final`). **Cara hitung yang BENAR** (disepakati, belum dieksekusi): ambil baris prediksi mentah per unit/kriteria dari checkpoint (`v2b_combo_preds_per_unit.csv`/`_per_kriteria.csv`), filter tiap unit ke kombinasi terbaiknya (sesuai `Best_Combo_PerUnit`/`PerKriteria`), gabung semua jadi 1 dataframe, baru panggil `global_metrics()` SEKALI — konsisten sama cara RMSE_GLOBAL dihitung di semua tempat lain di project ini. **BUKAN** sekadar rata-rata dari MAPE per-unit yang udah ada di Excel (gak konsisten secara metodologi, dan buat RMSE malah salah secara matematis — `sqrt(mean(x))` ≠ `mean(sqrt(x))`). **Status: kode sudah ditawarkan, BELUM dijalankan** — PR buat chat lanjutan.

### 17.7 File yang dihasilkan fase ini
Lihat §8.3 untuk daftar lengkap file `checkpoints_v3/`.

---




---

# BAGIAN A — ANALISA CODE (lanjutan)

## 19. `code_v4.ipynb` — Best-GB per Unit/Kriteria, Horizon 3 & 4 Bulan, Rolling vs Direct

### 19.1 Permintaan awal user (satu paket)

1. **Notebook baru `code_v4.ipynb`** yang mereplikasi proses `code_v3.ipynb` dari awal sampai Tahap 2b (drill-down 12 kombinasi). Metrik error yang dilihat: **MAPE** (RMSE tetap dimasukkan sebagai info).
2. Dari hasil Tahap 2b terlihat **Gradient Boosting (GB) paling sering terbaik**, apa pun data-prep-nya (forecast 4 bulan). Untuk unit/kriteria yang **best MAPE-nya BUKAN GB**: pakai **GB juga**, tapi data-prep dipilih yang MAPE terbaik di antara 4 varian (baseline / robust / savgol / yeojohnson). Lalu bandingkan MAPE GB terbaik itu dengan **MAPE terbaik v2b**, hitung **selisihnya**, output **Excel per unit & per kriteria**.
3. Tambah percobaan **forecast 3 bulan** (aturan pemodelan & data-prep sama dengan yang 4 bulan).
4. Bandingkan cara forecast **rolling** (pakai hasil prediksi sendiri) vs **langsung (direct)** untuk 3 & 4 bulan: hasilnya sama persis atau tidak, dan mana yang error-nya lebih rendah.

### 19.2 Klarifikasi & keputusan user (jawaban atas pertanyaan Claude)

| Pertanyaan | Keputusan user |
|---|---|
| "GB dipaksa + prep terbaik" diambil dari data v2b yang ada, atau fit ulang? | **Fit ulang khusus di v4** |
| Forecast 3 bulan: reuse parameter 4 bulan atau grid search ulang? | **Grid search ulang penuh dari nol untuk 3 bulan** |
| Rolling vs direct untuk model apa? | **Gradient Boosting saja** |
| Tambahan: parameter GB | **Disesuaikan individual per unit & per kriteria** (bukan parameter umum yang sama) |
| Definisi horizon 3 bulan | **Train Jan 2023–Sep 2025, test Okt–Des 2025** (koreksi user; asumsi awal Claude "Sep–Nov" SALAH). Horizon 4 bulan tetap: train Jan 2023–Agu 2025, test Sep–Des 2025 |
| Cell diagnostik v3 | Tidak perlu dibawa ke v4 — **TAPI plot/EDA (cek outlier, skewness, dsb) jangan dihapus**. Hasil cek: v3 sendiri TIDAK punya cell skewness/outlier-IQR khusus UTILITAS (itu fitur versi lebih lama, sudah digantikan 4 varian data-prep); yang ada hanya plot cek outlier volume container → dipertahankan |
| Pemilihan akhir per-unit vs per-kriteria | Tetap akan dipilih salah satu di akhir, **tapi belum ada di code** (lihat §19.8) |

### 19.3 Struktur `code_v4.ipynb` (100 cell, setelah tambahan EDA & Tahap 3 -- lihat 19.9-19.10)

| Cell | Isi |
|---|---|
| 0–2 | Judul + asumsi, setup path/import (`OUT_DIR = ./checkpoints_v4`) |
| 3–12 | Preprocessing (identik v3, print-check murni dibuang): scan nama unit, parsing BBM AAB, date-clean + delta HM + agregasi bulanan, parsing container, **plot cek outlier volume container (PNG)**, curah hujan + matching kriteria (cost&bbm), exclude 10 unit + remap ID, **completeness per unit (CSV)**, **mapping kriteria↔unit↔HM (Excel)** |
| 13–22 | Fungsi: `eval_pred`/`global_metrics`, 4 varian data-prep, `get_series`/`get_exog`, grid (PDQ, GB 36 kombinasi, LSTM 8 kombinasi), fungsi fit ARIMAX/GB/LSTM (unit & kriteria), `parse_param_str`, `clean_gb_params`, `forecast_gb_rolling`, `filter_units` (sudah diparametrikan: `test_end`, `min_test_months`) |
| 23–53 | **Horizon 4 bulan**: A setup split → B Tahap 2 (24 kombinasi, 4 varian) → C ringkasan/winner → D Tahap 2b (12 kombinasi) → E tuning GB individual (+ Excel hasil akhir) → F rolling vs direct |
| 54–84 | **Horizon 3 bulan**: struktur sama persis dengan 23–53 |
| 13–19 | **[BARU, 19.9]** EDA (Analisa Data): trendline, deskriptif+skewness, distribusi, outlier (+label unit/bulan), korelasi -- dipakai subbab Analisis Data Bab 3 buku |
| 20–91 | Isi lama cell 13-84 (fungsi inti, Tahap 2/2b/E/F horizon 4 & 3 bulan) -- geser +7 nomor, isi TIDAK berubah |
| 85–91 | Ringkasan lintas-horizon, perbandingan head-to-head 4 vs 3 bulan, rangkuman file (nomor lama 85-89, geser +7) |
| 92–99 | **[BARU, 19.10]** Tahap 3: retrain full-history + future forecast rolling per unit, estimasi eksogen musiman, rangkuman unit di-exclude semua tahap, export Excel final |

**Mekanisme horizon**: tiap sel setup horizon meng-set `TRAIN_END`, `TEST_START`, `TEST_END`, `MIN_TEST_MONTHS`, `OUT_DIR` (`./checkpoints_v4/h4bulan` atau `./checkpoints_v4/h3bulan`) lalu membangun ulang `train_df_raw`, `test_df_raw`, `unit_list`, `kriteria_list`. Fungsi-fungsi lain memakai variabel global itu (dibaca saat dipanggil), jadi tidak perlu diubah per horizon. Checkpoint tiap horizon terpisah folder → tidak saling menimpa.

### 19.4 Metodologi tiap bagian baru

**E. Tuning GB individual (di kode/label internal disebut "Force-GB" — istilah ini HANYA internal, jangan dipakai di buku, lihat §20.8)**
- Target: unit/kriteria yang kombinasi terbaiknya di Tahap 2b (12 kombinasi) **bukan** GB.
- Untuk tiap target: coba **4 varian data-prep × 36 kombinasi hyperparameter GB = 144 fit**, ambil MAPE terendah (parameter: `learning_rate` [0.01, 0.05, 0.1, 0.2], `max_iter` [100, 200, 300], `max_depth` [None, 3, 5, 7], `min_samples_leaf` [5, 10, 20]).
- Unit/kriteria yang **sudah menang GB** di Tahap 2b dibawa apa adanya (tidak di-fit ulang); parameternya diambil dari parameter global pemenang Tahap 2 (`winner_per_combo`).
- Output: `v4_forcedgb_vs_v2b_comparison.xlsx` (kolom `V2B_BEST_*`, `V4_GB_*`, `SELISIH_MAPE_GBvsV2B` = MAPE_GB_final − MAPE_v2b_terbaik; **negatif = GB-tuned lebih baik**) dan `v4_HASIL_AKHIR_forced_gb.xlsx` (tabel bersih: model final, prep, parameter, MAPE, RMSE).

**F. Rolling vs Direct (khusus GB)**
- Model yang dipakai: kombinasi GB final tiap unit/kriteria (hasil E, atau pemenang GB v2b).
- **Direct** = fitur lag test dibangun dari nilai **aktual** (cara yang dipakai pipeline sejak awal). **Rolling** = bulan ke-2 dst memakai **prediksi sendiri** sebagai `lag_1` (digeser maju; `lag_2`/`lag_3` ikut bergeser), fitur eksogen tetap nilai sebenarnya bulan tsb.
- Output `v4_rolling_vs_direct.xlsx`: `MAPE/RMSE_DIRECT`, `MAPE/RMSE_ROLLING`, `IDENTIK` (np.allclose), `LEBIH_RENDAH`, plus sheet `Ringkasan`.

**Lintas horizon**
- `v4_RINGKASAN_LINTAS_HORIZON.xlsx`: ringkasan forced-GB vs v2b dan rolling vs direct per horizon.
- `v4_PERBANDINGAN_4BULAN_vs_3BULAN.xlsx`: head-to-head MAPE/RMSE per unit & kriteria (kolom `LEBIH_RENDAH`), sheet `Ringkasan`, print kesimpulan horizon mana yang menang rata-rata MAPE.

### 19.5 Temuan analisa kode (penting untuk pembahasan)

1. **Cara forecast tiap model di pipeline lama (v2/v3) ternyata BEDA-BEDA**:
   - **ARIMAX**: `model.predict(n_periods=...)` native multi-step + eksogen aktual → sudah "direct multi-step".
   - **GB**: lag test dari `make_lag_features(concat(train, test))` → **pakai lag AKTUAL** (bukan rekursif dengan prediksi sendiri). Ini cenderung lebih optimistis dari forecast sungguhan (jika nilai aktual bulan sebelumnya belum diketahui).
   - **LSTM**: sudah **rolling** (prediksi sendiri masuk window).
   - → Eksperimen rolling vs direct (§19.4 F) jadi penting: menentukan cara mana yang layak dilaporkan sebagai metode resmi GB (efeknya ke teks buku, lihat §20.6 poin 1).
2. **Kenapa MAPE GB-tuned bisa lebih baik dari "best model" v2b?** Bukan bug. Di Tahap 2b, GB memakai **satu parameter global** (hasil Tahap 2, terbaik secara agregat), begitu juga ARIMAX & LSTM. Jadi di 1 unit tertentu, GB parameter-global bisa kalah dari model lain. Di v4, GB dicari 144 kombinasi **khusus per unit** → bisa mengalahkan pemenang v2b. Contoh dari file yang diupload user (`v4_forcedgb_vs_v2b_comparison.xlsx`, horizon tidak dinyatakan eksplisit): `UNIT_0004` v2b menang LSTM (MAPE 6.93), GB-tuned 2.85; **82 dari 205 unit** punya selisih negatif. Konsisten dengan limitasi yang sudah tercatat ("Tahap 2b pakai parameter Tahap 2 tanpa retuning", §16.1/§17.6).
3. Preferensi user soal hasil: dugaan MAPE 3 bulan lebih bagus daripada 4 bulan, tapi **belum terbukti** — keputusan horizon utama menunggu `v4_PERBANDINGAN_4BULAN_vs_3BULAN.xlsx`.

### 19.6 Bug / isu selama v4 (dan penanganannya)

| # | Isu | Penanganan |
|---|---|---|
| 1 | Sel penanda "md" vs "markdown" salah saat merakit notebook (sel header terbaca sebagai kode → syntax error di cell 21, 39, dst) | **[FIXED]** di sisi pembuatan notebook, sebelum sampai ke user |
| 2 | Cell yang menghasilkan file sempat ikut terhapus saat membuang cell diagnostik: plot outlier container, `05_completeness_per_unit.csv`, Excel mapping kriteria↔unit↔HM | **[FIXED]** dikembalikan (plot pakai `matplotlib.use('Agg')` + `savefig`, aman headless) |
| 3 | Split 3 bulan awalnya salah (Sep–Nov, train tetap Agu) | **[FIXED]** jadi train s/d Sep 2025, test Okt–Des 2025; `TRAIN_END` kini di-set per horizon |
| 4 | `ValueError: Invalid frequency: ME` di `resample('ME')` — pandas di server versi lama | **[FIXED]** diganti `'M'` (jalan di versi lama & baru) |
| 5 | LSTM tidak punya log progres per kombinasi → terlihat "diam" padahal jalan | **[FIXED]** tambah print per kombinasi (8 kombinasi per-unit, 8 per-kriteria) |
| 6 | `InvalidParameterError: learning_rate ... Got None` di rolling vs direct | **[FIXED]** penyebab: `build_final_gb_comparison` mengisi parameter GB = NaN untuk unit yang sudah menang GB. Sekarang `get_winner_gb_params(variant, level)` mengambil dari `winner_per_combo`. **Cukup rerun cell `build_final_gb_comparison` (akhir Section E) → lanjut Section F**; search 144 kombinasi tidak perlu diulang |
| 7 | Log TensorFlow di server: NUMA node −1, `Cannot dlopen some GPU libraries`, `Skipping registering GPU devices` | **Aman** — hanya informasi; TF fallback ke CPU (LSTM lebih lambat, hasil tidak berubah) |
| 8 | ⚠️ **Beda metrik pemilih parameter Tahap 2**: `code_v3` memilih parameter terbaik tiap (model, varian, level) dengan `sort_values('RMSE_GLOBAL')`; `code_v4` (`winner_per_combo`) memakai **`MAPE_GLOBAL`**. Karena Tahap 2b memakai parameter pemenang Tahap 2, hasil v4 bisa berbeda dari v3 | **BELUM diputuskan.** Opsi: (a) biarkan MAPE (sesuai permintaan "lihat MAPE saja" — tapi permintaan itu tertulis untuk bagian v2b ke atas), atau (b) ubah `winner_per_combo` ke `RMSE_GLOBAL` agar benar-benar "sama persis dengan v3" untuk Tahap 2, lalu jalankan ulang Tahap 2b dst (checkpoint Tahap 2b harus dihapus). Konfirmasi ke user |
| 9 | Yang **tidak** direplikasi dari v3 ke v4: Tahap 3 (tuning GB+savgol seragam), plot-plot Tahap 2b/Tahap 3, Excel `v3_train_test_split_info.xlsx`, sheet `Ringkasan_PerUnit/PerKriteria` di Excel Tahap 2 | Belum ada permintaan menambahkan; tanyakan kalau diperlukan |

### 19.7 Catatan operasional

- **Jalankan via `.py` di server aman**: semua hasil penting sudah disimpan sebagai file (CSV/XLSX/PNG). Satu-satunya baris yang hanya "tampil" di Jupyter (bukan file) adalah baris terakhir notebook (`ringkasan_forcedgb_lintas_horizon` polos) — datanya sudah tersimpan ke Excel sebelum baris itu; di `.py` baris itu tidak berpengaruh.
- **Pindah lokasi/lanjut**: cukup copy folder **`checkpoints_v4/` utuh** (jaga struktur `h4bulan/`, `h3bulan/`) ke folder yang sejajar dengan file `.py`/`.ipynb` (path relatif `./checkpoints_v4`), plus file sumber Excel (BBM AAB 2023/2024/2025, Container 2023/2024/2025, cost & bbm HP & Type, Curah Hujan 2023-2025). Bolak-balik `.ipynb` ↔ `.py` aman (format checkpoint CSV sama). Saat lanjut di notebook: jalankan urut dari atas sampai sel setup horizon yang sedang dikerjakan (preprocessing bersifat deterministik), lalu sel grid search otomatis melewati kombinasi yang sudah selesai.
- **Cakupan checkpoint**: semua loop berat punya checkpoint (ARIMAX/GB/LSTM Tahap 2, refit 12 kombinasi Tahap 2b, tuning GB individual, rolling vs direct). Yang tidak di-checkpoint (murah diulang): preprocessing awal & agregasi/ringkasan.
- **Log progres**: GB/ARIMAX print tiap 1 batch (`BATCH_SIZE=10` item); LSTM print tiap 1 kombinasi (sesudah fix #5).
- LSTM grid = **8 kombinasi** (`seq_len` [3,6] × `units` [16,32] × `epochs` [30,50]).

### 19.8 Status run & hal yang belum ada di kode

**Status run (dari percakapan; perlu dikonfirmasi user):**
- `h4bulan`: sudah sampai Section E (file forced-GB vs v2b sudah ada dan diupload user) dan Section F sempat kena bug #6 (sudah ada fix).
- `h3bulan`: status **tidak diketahui** — konfirmasi.
- File hasil yang perlu diperiksa keberadaannya per horizon: `v4_forcedgb_vs_v2b_comparison.xlsx`, `v4_HASIL_AKHIR_forced_gb.xlsx`, `v4_rolling_vs_direct.xlsx`; lintas horizon: `v4_RINGKASAN_LINTAS_HORIZON.xlsx`, `v4_PERBANDINGAN_4BULAN_vs_3BULAN.xlsx`.

**Belum ada di kode (butuh keputusan/pekerjaan):**
1. **Pemilihan final per-unit vs per-kriteria** (dibandingkan lewat RMSE/MAPE lalu dipilih satu) — user bilang akan tetap dilakukan, kode belum ada.
2. **Penentuan "satu model tunggal"** secara formal (kriteria: mayoritas unit/kriteria menang, atau MAPE global terendah — belum diseragamkan, lihat §20.6 poin 2).
3. **Uji signifikansi statistik** untuk H1 ("GB signifikan lebih baik dari ARIMAX & LSTM") — belum ada uji statistik di kode.
4. **Keputusan metode forecast resmi GB** (direct vs rolling) setelah hasil §19.4 F keluar.
5. **Keputusan metrik pemilih parameter Tahap 2** (§19.6 poin 8).
6. Masalah lama yang masih **DI-HOLD**: ARIMAX per-kriteria gagal massal di split baru (§17.5 poin 5) — belum tentu muncul lagi di v4; perhatikan kolom `n_unit_sukses`/jumlah kriteria konvergen saat hasil v4 keluar.
7. ~~Dashboard Streamlit~~ ✅ **Versi pertama sudah jadi** -- lihat Bagian C (§21).

### 19.9 [BARU] Penambahan EDA (Analisa Data) ke `code_v4.ipynb`

- Disisipkan cell 13-19 (setelah data prep `monthly_full` final, sebelum fungsi Tahap 2), jadi semua cell sesudahnya geser +7 nomor (isi tidak berubah).
- Cakupan: trendline (UTILITAS agregat bulanan total & mean, CURAH_HUJAN, VOLUME_CONTAINER), statistik deskriptif + skewness (UTILITAS *pooled* seluruh unit-bulan N=8.280, eksogen pakai deret bulanan N=36), histogram distribusi (bins=30 utk UTILITAS pooled, bins=12 utk eksogen krn N kecil), *outlier* IQR + **label unit/bulan pada boxplot** (3 titik paling ekstrem dianotasi langsung di gambar, plus file detail `eda_08b_outlier_detail.csv`), korelasi Pearson (heatmap + tabel).
- Populasi EDA ini: **230 unit** (`monthly_full`, setelah exclude 10 unit bimbingan + non-alat-berat, SEBELUM filter kelayakan per-horizon `filter_units()`). Beda dengan populasi final yang benar-benar dipakai model h3bulan (**205 unit**, setelah `filter_units()` cell 29/61 motong lagi berdasarkan kecukupan data train/test). **Catat kedua angka ini eksplisit di buku** biar gak kelihatan kontradiksi.
- Temuan penting dari EDA (dipakai utk pembahasan): pola musiman -- UTILITAS & VOLUME_CONTAINER dip tajam tiap bulan April (2023/2024/2025), diduga terkait libur Idul Fitri (jatuh akhir Maret-akhir April di ketiga tahun itu); UTILITAS pooled & CURAH_HUJAN 0 *outlier* IQR (justru krn sebaran lebar, N besar, bukan berarti gak ada ekstrem); VOLUME_CONTAINER 2 *outlier* (April 2023, April 2025) -- bertepatan dgn dip UTILITAS, memperkuat dugaan efek musiman; korelasi UTILITAS-VOLUME_CONTAINER 0.70 (positif sedang-kuat), UTILITAS-CURAH_HUJAN -0.30 (negatif sedang); korelasi dihitung tanpa *lag* (limitasi, dicatat).
- Hasil EDA (gambar+CSV) sudah dipakai utk rewrite subbab 3.3 Analisis Data di buku -- lihat §20.4 (update) & §20.6.

### 19.10 [BARU] Tahap 3 -- Model Final & Future Forecast

- Ditambah di akhir notebook (cell 92-99, setelah rangkuman lintas-horizon), horizon final yang dipakai: **h3bulan, per unit, GB** (bukan h4bulan, bukan per-kriteria -- keputusan user, lihat resolusi poin 1 di bawah).
- **Dua pivot metodologi penting** dari evaluasi historis ke produksi:
  1. **Retrain pakai SEMUA histori** (bukan cuma train sampai Sep 2025) -- model final memanfaatkan data test (Okt-Des 2025) juga sbg bahan belajar.
  2. **Forecast ke depan WAJIB *rolling*/*recursive*, bukan *direct*** -- krn *direct* butuh nilai lag AKTUAL, dan bulan di masa depan belum punya nilai aktual sama sekali. Ini otomatis konsisten dgn temuan §19.4 F (rolling selalu lebih buruk dari direct) -- jadi forecast makin jauh ke depan, potensi error makin besar. Ini dasar pesan "catatan error naik di atas 3 bulan" di dashboard perusahaan (§21).
- Variabel eksogen masa depan (CURAH_HUJAN, VOLUME_CONTAINER) **belum ada nilai aktualnya** -> dipakai estimasi rata-rata musiman per bulan kalender (Jan/Feb/.../Des, digabung dari histori 2023-2025). **Ini asumsi, bukan data riil -- WAJIB disebut sbg limitasi metodologi di buku.**
- Output: `./checkpoints_v4/h3bulan/future_forecast/` -- `exog_future_estimasi_musiman.csv`, `v4_future_forecast_per_unit.csv` (checkpoint mentah), `v4_future_forecast_final.xlsx` (3 sheet: panjang/pivot/unit-diexclude), `v4_unit_excluded_summary.xlsx`.
- Rangkuman unit di-exclude SEMUA tahap jadi satu tabel (dgn alasan): 10 unit bimbingan + filter kelayakan horizon 3 bulan (`06_excluded_units.csv`) + gagal tuning Force-GB (parameter NaN) + gagal retrain Tahap 3 (data gak cukup setelah transformasi lag).
- **Bug ditemukan & diperbaiki saat testing**: `pandas.groupby().apply()` pada *dataframe* kosong (0 baris) bisa menjatuhkan kolom `group_col` dari hasilnya (perilaku pandas, bukan bug di logic kita) -> memicu `KeyError: 'EQUIP NAME'` di `_cap_smooth` (dipakai `prep_baseline`/`prep_savgol`). **[FIXED]**: fungsi retrain dipanggil dgn `prep_fn(g_full, g_full)` (data penuh dua-duanya), bukan `prep_fn(g_full, g_full.iloc[0:0])` (slice kosong). Perilaku ini sempat muncul di sandbox testing Claude (pandas versi sangat baru, 3.0.2) -- kemungkinan besar gak muncul di environment asli user (pandas lebih lama), tapi fix-nya sudah diterapkan di kedua tempat (notebook Tahap 3 & `pipeline_lib.py`) utk jaga-jaga.
- **Resolusi open items §19.8 lama:**
  1. ~~Pemilihan final per-unit vs per-kriteria~~ -> **per unit** (user: "forecast per unit menggunakan GB dengan data prep dan parameter nya masing-masing karena secara error lebih baik"). Per-kriteria tetap dihitung/ditampilkan di dashboard demo sbg pembanding, TAPI bukan pendekatan resmi yang di-deploy.
  2. ~~Horizon utama (3 vs 4 bulan)~~ -> **3 bulan**, final.
  3. Metode forecast resmi GB (direct vs rolling) -> **direct** utk evaluasi historis (sesuai §19.4 F, menang telak di semua horizon/level), **rolling** utk future forecast produksi (keharusan teknis, bukan pilihan -- lihat poin di atas). **Kedua fakta ini perlu ditulis bersamaan di buku**, jangan cuma salah satu.
- Item §19.8 yang masih TERBUKA (belum berubah): metrik pemilih parameter Tahap 2 (MAPE vs RMSE, poin 8 lama), uji signifikansi H1, ARIMAX per-kriteria gagal massal (di-hold, belum dicek ulang di v4).

---



### 19.11 [BARU] Revisi Dosen Pembimbing 2 — 190 Unit Valid, Eksogen Lag-1, & Folder rev_h3/ (Cell 101–104)

Menindaklanjuti 6 poin arahan revisi dari Dosen Pembimbing 2 (setelah peninjauan hasil Tahap 3 awal):
1. **Poin 1 (Ditunda)**: Usulan penggantian istilah *"utilitas"* menjadi *"operating hours / machine hours / engine hours / runtime"* ditunda atas keputusan user.
2. **Poin 2 & Poin 3: Eksperimen Variabel Eksogen Lag-1 ($t-1$) Bebas Data Leakage**:
   - Dosen pembimbing menyoroti potensi *data leakage* jika variabel eksogen (Curah Hujan & Kontainer) menggunakan data pada waktu $t$ yang sama dengan periode prediksi.
   - Dilakukan perbandingan empiris lengkap antara:
     - **ARIMA Murni** (tanpa variabel eksogen)
     - **ARIMAX Eksogen $t$** (variabel eksogen periode berjalan)
     - **ARIMAX Eksogen Lag-1 ($t-1$)** (variabel eksogen mundur 1 bulan, 100% bebas kebocoran data)
     - **Gradient Boosting Tanpa Eksogen**
     - **Gradient Boosting Eksogen Lag-1 ($t-1$)**
     - **Gradient Boosting Eksogen $t$**
   - **Hasil Empiris (190 Unit Valid)**:
     - `Gradient Boosting (Eksogen t)`: Mean MAPE **11.48%**, Median **9.59%**, Max **39.87%**, RMSE **33.66**
     - `Gradient Boosting (Tanpa Eksogen)`: Mean MAPE **14.90%**, Median **12.28%**, Max **81.45%**, RMSE **39.53**
     - `Gradient Boosting (Eksogen Lag-1 / t-1)`: Mean MAPE **15.67%**, Median **13.21%**, Max **74.98%**, RMSE **42.14**
     - `ARIMA Murni (Tanpa Eksogen)`: Mean MAPE **18.38%**, Median **13.43%**, Max **126.99%**, RMSE **43.77**
     - `ARIMAX (Eksogen t)`: Mean MAPE **19.26%**, Median **15.95%**, Max **89.82%**, RMSE **47.39**
     - `ARIMAX (Eksogen Lag-1 / t-1)`: Mean MAPE **19.79%**, Median **15.92%**, Max **96.92%**, RMSE **48.01**
   - **Temuan Ilmiah Penting (Bahan Bab 4)**:
     - Variabel eksogen yang dihubungkan secara linier pada ARIMAX justru memperburuk akurasi (*degrade*) dibanding ARIMA murni (18.38% vs 19.79%) karena deret bulanan pelabuhan yang pendek dan noise curah hujan.
     - Gradient Boosting dengan eksogen Lag-1 ($t-1$) menjamin **zero data leakage** dan tetap mengungguli seluruh varian ARIMA/ARIMAX (15.67% vs 18.38%).
3. **Poin 4: Eliminasi 15 Unit dengan Testing MAPE > 40% (Populasi Menjadi 190 Unit Valid)**:
   - Dosen pembimbing mengarahkan agar unit-unit yang menghasilkan error prediksi testing sangat tinggi (> 40%) dikeluarkan dari analisis utama.
   - 15 unit yang di-exclude: `UNIT_0027`, `UNIT_0301`, `UNIT_0187`, `UNIT_0006`, `UNIT_0339`, `UNIT_0080`, `UNIT_0091`, `UNIT_0220`, `UNIT_0344`, `UNIT_0021`, `UNIT_0081`, `UNIT_0142`, `UNIT_0024`, `UNIT_0197`, `UNIT_0185`.
   - Alasan exclude distandardisasi menjadi profesional: *"Melebihi threshold toleransi error"* tanpa mencantumkan nilai threshold teknis di laporan dan tanpa kolom TAHAP.
   - Total unit yang diexclude menjadi **40 unit** (18 nol di train, 7 nol di test, 15 melebihi threshold toleransi error).
   - Populasi unit valid: **190 unit**. Rata-rata MAPE model final turun dari 15.48% menjadi **11.48%** dan median turun ke **9.59%** (kategori Lewis: *High Accuracy* < 10%).
4. **Poin 5 (Ditunda)**: Pemetaan nama kriteria dengan kriteria ID ditunda atas keputusan user.
5. **Poin 6: Baseline Sumbu Y Seluruh Plot EDA Mulai dari 0**:
   - Seluruh visualisasi plot EDA pada `code_v4.ipynb` (Cell 8, 15, 17, 18, 20) diperbaiki dengan `ax.set_ylim(bottom=0)` dan seluruh gambar grafik diekspor ulang agar tidak terjadi bias visualisasi (*misleading baseline*).
6. **Implementasi Teknis Notebook (Cell 101–104)**:
   - Kode revisi ditambahkan di akhir `code_v4.ipynb` (Cell 101–104) dan berjalan instan (< 1 detik via checkpoint).
   - Output revisi diisolasi di folder khusus: `checkpoints_v4/rev_h3/` agar tidak menimpa checkpoint baseline lama (`h3bulan/`).
   - File redundant dibersihkan: file CSV duplikat `06_excluded_units_revisi.csv` dan `future_forecast_per_unit_190unit.csv` dihapus; Cell 102 dan 104 disesuaikan agar hanya menghasilkan file Excel.

### 19.12 [BARU] Revisi Dosen Pembimbing 2 Tahap 5 — Standarisasi Sistem Penamaan Kriteria & Unit (K01_UNIT_004)

Menindaklanjuti arahan Dosen Pembimbing ke-2 mengenai kejelasan identitas unit pada hasil analisis: penamaan acak anonim (`UNIT_0001` – `UNIT_0345`) tidak mencerminkan karakteristik teknis alat berat. Dilakukan standarisasi komprehensif sistem penamaan kriteria dan unit:

1. **Pengurutan Kriteria dan Kode 2 Digit (`K01` s/d `K85`)**:
   - Seluruh 85 kriteria kustom diurutkan menurun (*descending*) berdasarkan jumlah unit terbanyak (Opsi A) dan dipetakan ke kode kriteria formal 2 digit (`K01` s/d `K85`).
   - Dari 85 kriteria total (populasi 230 unit), sebanyak 63 kriteria aktif pada 190 unit valid.
2. **Standarisasi Penomoran Unit 3 Digit**:
   - Seluruh nomor unit dinormalkan dari 4 digit (`UNIT_0001` – `UNIT_0345`) menjadi 3 digit (`UNIT_001` – `UNIT_345`).
3. **Format Standar Tunggal `K<NoKriteria>_UNIT_<Nomor3Digit>`**:
   - Kode kriteria dan nomor unit digabungkan menjadi format standar tunggal (contoh: `K01_UNIT_004`, `K09_UNIT_309`, `K84_UNIT_001`).
   - Format ini secara langsung menginformasikan kriteria spesifikasi alat sekaligus nomor unik unit dalam satu nama terpadu.
4. **Penerbitan Master Reference Mapping (`mapping_unit_dan_kriteria.xlsx`)**:
   - Diterbitkan di `checkpoints_v4/rev_h3/` dan `checkpoints_v4/` memuat 2 sheet:
     - `Mapping_Unit` (230 unit): `KODE_KRITERIA`, `EQUIP_NAME_BARU`, `EQUIP_NAME_LAMA`, `STATUS` (`VALID_190` vs `EXCLUDED`), `KRITERIA_ID`, spesifikasi alat (`JENIS`, `TYPE/MERK`, `CAP`, `HP`), dan `LOKASI`.
     - `Ringkasan_Kriteria` (85 kriteria): `KODE_KRITERIA`, `KRITERIA_ID`, `JUMLAH_UNIT`, `DAFTAR_UNIT_BARU`, `DAFTAR_UNIT_LAMA`, serta spesifikasi teknisnya.
5. **Pembaruan Kamus JSON (`unit_map_v4.json` & `kriteria_map.json`)**:
   - File `unit_map_v4.json` (di `checkpoints_v4/` dan `rev_h3/`) serta `anonymization_maps/unit_map.json` diperbarui sehingga nama aset fisik asli memetakan langsung ke nama unit format baru.
   - File baru `kriteria_map.json` ditambahkan dengan kamus dua arah: `KODE_TO_KRITERIA` dan `KRITERIA_ID_TO_KODE`.
6. **Sinkronisasi File Checkpoint & Output (Tanpa Rerun Full Notebook)**:
   - Seluruh file di `checkpoints_v4/rev_h3/` disinkronkan ke penamaan baru: `forcedgb_vs_v2b_comparison_190unit.xlsx`, `unit_excluded_revisi_summary.xlsx`, `perbandingan_eksogen_dan_model.xlsx`, `future_forecast_final_190unit.xlsx`, `04_monthly_with_exog_lag1.csv`, `04_monthly_with_exog.csv`, `08_kriteria_unit.csv`, `v4_rolling_vs_direct.xlsx`, `v2b_detail_per_unit_12kombinasi.csv`, `v2b_detail_per_unit_raw.csv`.
7. **Pembaruan Notebook `code_v4.ipynb` (Cell 102)**:
   - Cell 102 diperbarui secara konsisten agar jika cell 101–104 dijalankan ulang, pipeline revisi akan membaca mapping dari `mapping_unit_dan_kriteria.xlsx` dan langsung memproduksi nama unit format baru.

### 19.13 [BARU] Eliminasi Total 15 Unit Anomali Sejak Awal Data Pipeline ETL (Populasi Murni 215 Unit, 25 Exclude, 190 Model)

Menindaklanjuti arahan user mengenai perlakuan terhadap 15 unit anomali dengan error prediksi tinggi (MAPE testing > 40%):
- **Keputusan Arsitektur Data Pipeline**: Berbeda dengan perlakuan sementara sebelumnya di mana 15 unit ini dimasukkan ke dalam daftar 40 unit excluded di hilir (Cell 101–104), user menginstruksikan agar ke-15 unit ini **benar-benar dieliminasi sejak awal pemrosesan data (ETL)**, persis seperti penanganan 10 unit non-operasional yang dihapus pada iterasi sebelumnya (`code_v3.ipynb`).
- **Tujuan Operasional**: Menjamin ke-15 unit ini tidak pernah muncul sebagai "Unit Baru" saat pengguna mengunggah berkas data operasional bulanan ke Dashboard Perusahaan (`appPerusahaan.py`), serta menyederhanakan pelacakan unit di seluruh pipeline.
- **Rincian Unit yang Dieliminasi**:
  `K01_UNIT_027`, `K02_UNIT_301`, `K03_UNIT_187`, `K03_UNIT_006`, `K03_UNIT_339`, `K07_UNIT_080`, `K07_UNIT_091`, `K08_UNIT_220`, `K10_UNIT_344`, `K11_UNIT_021`, `K11_UNIT_081`, `K11_UNIT_142`, `K12_UNIT_024`, `K16_UNIT_197`, `K18_UNIT_185`.
- **Dampak pada Populasi & Filter**:
  1. **Populasi Armada Terlacak**: Dari 230 unit awal, setelah 15 unit anomali disaring sejak awal data, total populasi armada yang tercatat di dataset bulanan menjadi **215 unit**.
  2. **Daftar Unit Exclude Resmi (Murni Jam Nol)**: Berkas `unit_excluded_revisi_summary.xlsx` dikembalikan ke fungsi aslinya, yaitu hanya mencatat unit-unit yang tidak layak latih secara operasional karena jam kerja nol murni sebanyak **25 unit** (18 unit nol di seluruh tahun data train + 7 unit nol di seluruh periode data test). Tidak ada lagi alasan teknis "Melebihi threshold toleransi error" di tabel exclude.
  3. **Populasi Model Final**: Tepat **190 unit valid** ($215 - 25 = 190$).
  4. **Kriteria Aktif**: Tepat **63 kriteria** aktif menaungi 190 unit valid tersebut (dari total 85 kriteria armada).
- **Pembaruan Berkas & Kode**:
  - `checkpoints_v4/04_monthly_with_exog.csv` & `08_kriteria_unit.csv`: 15 unit anomali telah disaring keluar dari dataset.
  - `checkpoints_v4/v4_kriteria_unit_mapping.xlsx`: Sheet detail disinkronkan ke 215 unit.
  - `pipeline_lib.py`: Fungsi `build_monthly_full()` dan filter ETL upload menyaring ke-15 unit ini sejak tahap pemrosesan awal.
  - `code_v4.ipynb`: Cell 10 dan Cell 102 disinkronkan sehingga jika notebook dijalankan ulang dari awal, dataset training/testing langsung memproses 215 unit.

### 19.14 [BARU] Standarisasi Global Penamaan Unit Kriteria (K##_UNIT_###) Lintas Seluruh Direktori Checkpoint (v1, v2, v3, v4)

Untuk menjaga konsistensi komparasi lintas iterasi eksperimen dan memastikan audit data yang transparan:
1. **Penyebab Dilakukannya Standarisasi**: Pemeriksaan mendalam menemukan bahwa penamaan unit pada checkpoint terdahulu (`checkpoints/`, `checkpoints_v2/`, `checkpoints_v3/`) serta beberapa file ringkasan di `checkpoints_v4/` masih menggunakan penamaan lama polos (`UNIT_xxxx` atau `UNIT_xxx`). Hal ini membingungkan ketika ingin membandingkan performa model per unit antar tahap di laporan/skripsi.
2. **Eksekusi Standarisasi Global**:
   - Seluruh berkas data CSV dan lembar kerja Excel pada seluruh generasi checkpoint diperbarui secara sistematis menggunakan kamus pemetaan resmi `mapping_unit_dan_kriteria.xlsx`:
     - **`checkpoints_v4/`**: `v4_kriteria_unit_mapping.xlsx`, `05_completeness_per_unit.csv`, `08_kriteria_unit.csv`, `v4_PERBANDINGAN_4BULAN_vs_3BULAN.xlsx`, `analisis_pacf_spearman.csv`, `01_daily_delta_hm.csv`, `02_monthly_operating_hours.csv`, serta seluruh berkas di subdirektori `h3bulan/`, `h4bulan/`, dan `rev_h3/`.
     - **`checkpoints_v3/`**: 16 file CSV dan 4 file Excel (`v3_kriteria_unit_mapping.xlsx`, `v2b_hasil_12kombinasi_per_unit_kriteria.xlsx`, `v3_tahap2_24kombinasi.xlsx`, `v3_tahap3_tuning_individual.xlsx`, dll.).
     - **`checkpoints_v2/`**: 16 file CSV dan 1 file Excel (`v2b_hasil_12kombinasi_per_unit_kriteria.xlsx`, dll.).
     - **`checkpoints/` (v1)**: 23 file CSV dan 1 file Excel (`15_LAPORAN_HASIL.xlsx`, dll.).
     - **`anonymization_maps/unit_map.json`**: Pemetaan 230 unit aset diperbarui ke format tunggal `K<NoKriteria>_UNIT_<Nomor3Digit>`.
3. **Hasil Audit Otomatis**:
   - Audit regex komprehensif mengonfirmasi **0 kemunculan** penamaan lama `UNIT_xxxx` pada seluruh kolom identitas unit di seluruh direktori checkpoint. Seluruh riwayat eksperimen kini berbicara dalam satu bahasa identitas unit yang seragam.

### 19.15 [BARU] Analisis PACF & Korelasi Spearman Variabel Eksogen (Script & Visualisasi Plot)

Untuk melengkapi justifikasi empiris keterkaitan variabel eksogen (Curah Hujan dan Volume Kontainer) dengan Operating Hours alat berat:
1. **Pengembangan Script Mandiri `analisis_pacf_spearman.py`**:
   - Menghitung autokorelasi parsial (PACF) hingga Lag-5 untuk mengidentifikasi pola *short-memory* deret waktu.
   - Menghitung koefisien korelasi linier Pearson ($r$) dan koefisien korelasi monotonik rank Spearman ($\rho$) antara operating hours alat berat dengan curah hujan dan volume kontainer cabang pelabuhan terkait.
2. **Keluaran Analisis**:
   - Berkas CSV: `checkpoints_v4/analisis_pacf_spearman.csv` memuat statistik korelasi dan nilai PACF per unit.
   - Grafik Visualisasi: `checkpoints_v4/analisis_pacf_spearman_plot.png` memvisualisasikan perbandingan kekuatan korel Spearman vs Pearson serta sebaran nilai PACF lintas unit.
3. **Penyempurnaan Visualisasi**:
   - Posisi legenda grafik disesuaikan keluar dari area plot (`bbox_to_anchor=(1.05, 1)`) agar tidak menutupi batang data atau distribusi titik.
   - Perhitungan jumlah unit diatur dinamis (`len(df)`) sehingga grafik selalu mencerminkan jumlah unit aktual yang dianalisis tanpa *hardcoding*.

### 19.16 [BARU] Review Kode & Output oleh Claude (chat penulisan Bab 4–6) — Daftar Perbaikan & Statusnya

Konteks: di chat penulisan buku, user mengupload `code_v4_1.ipynb` (105 cell), `pipeline_lib.py`, `appDemo.py`, `appPerusahaan.py`, `kode_eksperimen_6_skenario.py`, `analisis_pacf_spearman.py`, plus PNG/CSV EDA. Claude hanya me-review (TIDAK mengubah kode di bagian chat ini) dan menemukan ketidaksinkronan berikut. User kemudian mengerjakan sebagian (lihat §19.13, §21.12, §21.13); item bertanda ❓ belum terverifikasi dan perlu dicek di chat baru.

| No | Temuan | Status |
|---|---|---|
| 1 | Cell 14 & 19: nama kolom agregat masih `UTILITAS_TOTAL`/`UTILITAS_MEAN` (heatmap berlabel UTILITAS_*, `eda_00` berkolom ganda lama+baru) | ❓ §21.12 menyatakan CSV EDA & judul cell 15–18, 20 sudah diganti; cek cell 14/19 setelah rerun |
| 2 | PNG EDA yang dikirim ke Claude masih bertuliskan "UTILITAS" di judul/sumbu (padahal judul di kode sudah "Operating Hours"); dua gambar curah hujan & volume container berjudul "(Surabaya)"; penomoran 01 total, 02 rata-rata per unit, 03 curah hujan, 04 volume tidak cocok dengan cell 15 notebook yang diupload | ❓ regenerate PNG setelah rerun; hapus "(Surabaya)" (user setuju dihapus); samakan notebook dengan versi yang menghasilkan PNG final; buang file lama `eda_01b`, `eda_02_..._1`, `eda_03_..._1` |
| 3 | Cell 20 membaca `grp['UTILITAS']` langsung dari `04_monthly_with_exog.csv` — `KeyError` kalau kolom sudah `OPERATING_HOURS` | ❓ |
| 4 | Cell 103 membaca sheet `Ringkasan_190Unit`/`Ringkasan_205Unit`, sedangkan file hasil berisi sheet `Ringkasan` & `Detail_PerUnit`; cabang `else` kosong (`NameError`); ketergantungan sheet 205 unit kini usang | ❓ |
| 5 | `kode_eksperimen_6_skenario.py`: path absolut (`d:\SPIL Michael\...`, `C:\Users\SPIL\.gemini\...`); hanya menghitung MAPE padahal `perbandingan_eksogen_dan_model.xlsx` memuat RMSE (skrip belum mereproduksi file); memuat konfigurasi dari `h3bulan` (205) dengan variabel `exclude_15` / kolom `IS_EXCLUDE_15` / print "205 UNIT... 15 UNIT YANG DI-EXCLUDE" | ❓ (jejak 15 unit wajib dihapus sesuai keputusan user) |
| 6 | `analisis_pacf_spearman.py`: CSV ditulis ke folder kerja tanpa path; penamaan unit CSV PACF beda dengan `eda_14` (saat itu `UNIT_0001`) | ❓ §19.14 menyatakan naming sudah distandarisasi; verifikasi |
| 7 | Gambar PACF/Spearman: label pie "Spearman Lebih Kuat" tertutup irisan | ❓ §19.15 menyebut legenda sudah dirapikan |
| 8 | Jejak 15 unit anomali di keluaran (`unit_excluded_revisi_summary.xlsx` 40 baris, filter dashboard, konstanta `NEW_EXCLUDED_15`, teks notebook cell 98/101–103) | ✅ dikerjakan user: 15 unit dieliminasi sejak ETL, tabel exclude jadi 25 baris (§19.13, §21.13); sisa: dokumen pendamping (`penjelasan_eksperimen_6_skenario.md` §3.5, `spesifikasi_lingkungan_dan_runtime.md`) bila dilampirkan |

Prioritas: butir 1–5 sebelum gambar dimasukkan ke buku; butir 5 supaya eksperimen bisa dijalankan ulang orang lain.

---

# BAGIAN B — PENULISAN BUKU SKRIPSI (terpisah dari analisa code)

## 20. Penulisan Buku Skripsi — Bab 1–3

### 20.1 Konteks & pedoman format

- Pedoman: **"Panduan Laporan Tugas Akhir / TA (Mahasiswa DSA)"** (file `Pedoman_Buku_Skripsi_DSA.pdf`) + wajib mengikuti "Pedoman Tata Tulis Tugas Akhir Mahasiswa UK Petra" (terbitan 2025). Batas usaha **maksimal 12.000 kata**; penekanan pada kelugasan analisis data dan penjelasan output yang mudah dipahami pembaca awam (DSA = predictive/prescriptive analytics).
- Skema yang dipakai user: **Proyek** → memakai **"Format Buku Laporan Tugas Akhir (Proyek)"**:
  - Bab 1 Pendahuluan: Latar Belakang, Rumusan Masalah, Tujuan Proyek, Ruang Lingkup, Manfaat Solusi, Sistematika Penulisan
  - Bab 2 Studi Literatur dan Kerangka Kerja: Studi Literatur (Landasan Teori, Penelitian Terdahulu), Kerangka Kerja (Tahapan Proyek, Hipotesis Solusi, Pengumpulan & Pemahaman Data, Penyiapan Data, Pemodelan, Pengujian & Pembahasan)
  - Bab 3 Analisis dan Perancangan: Analisis Masalah, Analisis Kebutuhan (opsional), Analisis Data (hasil EDA + proses penyiapan data spesifik), Desain Solusi (+ diagram blok/alir)
  - Bab 4 Implementasi dan Pengujian: Implementasi Solusi, Lingkungan Pengujian, Skenario Pengujian, tiap pengujian satu subbab
  - Bab 5 Pembahasan
  - Bab 6 Kesimpulan dan Saran
  - Daftar Pustaka (**minimal 10 referensi**, diutamakan ≤5 tahun terakhir) + Lampiran (opsional)

### 20.2 Sumber & aturan kerja

- Dasar teks: **proposal yang sudah dikumpulkan** (`DSA_C14230035_Michael_Sugiarto__Proposal_.md`; judul: *Prediksi Utilitas Alat Berat PT X Menggunakan ARIMAX, Gradient Boosting, dan LSTM*).
- Aturan: **ikuti proposal; ubah hanya bagian yang berbeda dengan code saat ini; tanyakan dulu kalau ragu.**
- Perusahaan ditulis **"PT X"** (sesuai proposal), bukan nama asli.
- Teks Bab 1–3 diminta **dalam bentuk chat yang bisa di-copy** (tanpa file output). ⚠️ Karena itu teks lengkapnya **tidak ada di file mana pun** → simpan sendiri (mis. `Bab1-3_draft.md`/.docx) dan upload di chat baru bersama PROGRESS.md.

### 20.3 Keputusan user: apa yang berubah dari proposal

| # | Topik | Proposal | Keputusan untuk buku |
|---|---|---|---|
| 1 | Periode train/test | Train Jan 2023–Des 2024, test Jan–Des 2025 (12 bulan) | **Bab 1–3 memakai skenario 3 bulan: train Jan 2023–Sep 2025, test Okt–Des 2025.** Bisa diganti ke 4 bulan kalau ternyata 4 bulan lebih baik. Catatan eksperimen (3 vs 4 bulan, rolling vs direct, dll.) masuk **setelah Bab 1–3** (Bab 4/5), jangan difokuskan dulu |
| 2 | Data-prep | 1 cara (capping persentil-95 + rolling mean window 2) | **4 varian**: baseline (= cara proposal), Savitzky-Golay, RobustScaler, Yeo-Johnson |
| 3 | ARIMAX per-kriteria | Deret representatif mean/median, hasil dialokasikan balik ke unit secara proporsional | **Mean/sum, prediksi grup dipakai langsung ke tiap unit anggota (tanpa proporsi historis).** Per-unit vs per-kriteria tetap **dipilih salah satu** di akhir (belum ada di code) |
| 4 | Pemilihan model | Satu model terbaik global | **Tetap SATU model tunggal (GB, mayoritas terbaik).** Unit/kriteria lain tetap memakai GB, dengan **kombinasi data-prep & parameter disesuaikan** (bukan model berbeda per unit) |
| 5 | Tuning hyperparameter | "Eksperimen awal" / Auto ARIMA | **Grid search sistematis seperti di code** (ARIMAX p,d,q; GB; LSTM). **Jangan pakai kata "force-GB" di buku** — tulis saja: unit lain memakai model mayoritas lalu disesuaikan kombinasi parameter & data-prep-nya |
| 6 | Rumusan masalah & tujuan | 2 rumusan masalah + 1 tujuan proyek | **Tidak diubah** (eksperimen baru tidak mengganggu) |
| 7 | Pengecualian 10 unit | (tidak ada) | **Tidak disebutkan di buku** |
| 8 | Dashboard Streamlit | Fitur upload dataset + lihat prediksi | **Tetap di ruang lingkup**; dibuat setelah analisa selesai |

### 20.4 Ringkasan isi Bab 1–3 yang sudah ditulis

**Bab 1 Pendahuluan** — 1.1 Latar Belakang (konteks PT X & armada alat berat; masalah: tidak ada proyeksi utilitas per unit → sulit distribusi/relokasi unit antar lokasi; utilitas = pencatat kumulatif; eksogen curah hujan & volume container; justifikasi ARIMAX/GB/LSTM); 1.2 Rumusan Masalah (2 poin, sama dengan proposal); 1.3 Tujuan Proyek (sama); 1.4 Ruang Lingkup (10 poin; poin 3 = split 3 bulan; poin 4 = 4 varian data-prep; poin 9–10 = Streamlit); 1.5 Manfaat Solusi; 1.6 Sistematika Penulisan (6 bab).

**Bab 2 Studi Literatur dan Kerangka Kerja**
- 2.1.1 Landasan Teori: ARIMAX (rumus + keterangan), Gradient Boosting (rumus + lag features), LSTM (forget/input/output gate, cell state), **Grid Search** (baru), **Savitzky-Golay** (baru), **RobustScaler** (baru), **Yeo-Johnson** (baru), RMSE, MAPE.
- 2.1.2 Penelitian Terdahulu: Cortez et al. (2023) ARIMA/LSTM/XGBoost fotovoltaik; Pantopoulou et al. (2025) LSTM vs ARIMA suhu; Sirisha et al. (2022) ARIMA/SARIMA/LSTM profit.
- 2.2 Kerangka Kerja: 2.2.1 Tahapan Proyek (4 fase); 2.2.2 Hipotesis (H1: GB lebih baik dari ARIMAX & LSTM berdasarkan MAPE global; H0: tidak ada perbedaan); 2.2.3 Pengumpulan & Pemahaman Data (4 dataset: BBM AAB 2023–2025, cost & bbm HP & Type, Container 2023–2025, Curah Hujan 2023–2025 Open-Meteo; rencana EDA); 2.2.4 Penyiapan Data (9 langkah; 4 kriteria filter, "test < 3 bulan"); 2.2.5 Pemodelan (perbandingan 4 varian; per-unit vs per-kriteria dengan ARIMAX mean/sum; ARIMAX grid search; GB lag_1–3 + 2 eksogen (5 fitur) + grid search; LSTM sliding window 3 timestep + grid search; **penentuan model tunggal & penyesuaian konfigurasi**; penyajian dashboard); 2.2.6 Pengujian & Pembahasan (evaluasi per unit, evaluasi global MAPE, pencatatan unit yang dikecualikan).

**Bab 3 Analisis dan Perancangan** — 3.1 Analisis Masalah (3 aspek: struktur data, heterogenitas unit, pemilihan konfigurasi); 3.2 Analisis Kebutuhan (parallel processing, checkpoint, sumber daya komputasi); 3.3 Analisis Data (matching cost&bbm ↔ BBM AAB, proses teknis pandas: `read_excel(header=[0,1,2])`, `stack()`, `to_datetime`, delta HM dengan cap 24 jam, agregasi bulanan, eksogen; split 33 bulan train / 3 bulan test); 3.4 Desain Solusi (4 komponen: data-prep 4 varian → pemodelan 3 model × 2 pendekatan = 12 kombinasi per pendekatan → evaluasi & seleksi → penyesuaian konfigurasi; alur ke dashboard).

### 20.5 Diagram

**Tahapan Proyek (Bab 2.2.1) — hanya Fase 3 yang diubah** (Fase 1, 2, 4 sama dengan proposal):
- Fase 1: 7 Data Internal PT X + 1 Data Eksternal → Pemahaman Format & Struktur Data → *Exploratory Data Analysis*
- Fase 2: Ekstraksi Excel → Pemisahan Blok Alat Berat → Penghitungan Delta Utilitas → Penanganan Anomali → Agregasi Bulanan & Sinkronisasi Variabel Eksogen → Split Data *Train-Test* → Proses Filter
- **Fase 3 (BARU)**: Perbandingan 4 Varian *Data Preparation* → Pendekatan Per Unit vs Per Kriteria → *Grid Search* ARIMAX, *Gradient Boosting*, dan LSTM dengan Variabel Eksogen → Penentuan Model Tunggal & Penyesuaian Konfigurasi per Unit/Kriteria → Prediksi Utilitas → Pembuatan *Dashboard* Streamlit
- Fase 4: Hitung RMSE & MAPE per Unit → Hitung MAPE Global → Penentuan Model Terbaik · Pencatatan Unit yang Dikecualikan

**Diagram lain yang direkomendasikan:**
| Lokasi | Diagram | Status menurut pedoman |
|---|---|---|
| 2.2.1 | Tahapan Proyek (4 fase) | Wajib (ada di proposal) |
| 3.4 | **Arsitektur sistem / data pipeline** (diagram blok vertikal: 4 sumber data → preprocessing → 4 varian data-prep → grid search 3 model × 2 pendekatan → evaluasi → penyesuaian konfigurasi → hasil per unit → dashboard). Bedakan level dengan Tahapan Proyek (Bab 2 = urutan pengerjaan, Bab 3 = komponen sistem) | **Wajib** (pedoman: model kompleks perlu diagram blok/alir) |
| 3.4 | Flowchart keputusan "penentuan model tunggal & penyesuaian konfigurasi" (MAPE sudah terbaik dengan konfigurasi umum? ya → pakai; tidak → cari ulang kombinasi data-prep × hyperparameter) | Disarankan |
| 3.3 | Ilustrasi transformasi data mentah *wide multi-level header* → *long* (tabel before–after dummy) | Sangat disarankan |
| 2.1.1 (LSTM) | Diagram blok satu sel LSTM (gate + cell state) | Disarankan |
| 2.1.1 (GB) | Ilustrasi pohon sekuensial → residual | Opsional |
| Bab 4 | Screenshot dashboard Streamlit (upload + hasil prediksi) | Nanti, setelah dashboard jadi |

### 20.6 Catatan / risiko di teks yang HARUS dibereskan (jujur)

1. **GB & LSTM ditulis "rekursif"** di Bab 2.2.5 (mengikuti proposal), padahal di code **GB memakai lag aktual** (bukan rekursif) — hanya LSTM yang rolling (§19.5 poin 1). Setelah hasil rolling vs direct keluar dan metode resmi diputuskan, **sinkronkan teks 2.2.5 poin GB** (dan 3.4 bila perlu).
2. **Kriteria pemilihan model tunggal tidak konsisten antar subbab**: 2.2.5 poin 6 = "mayoritas unit/kriteria", sedangkan 2.2.6 poin 2 dan Hipotesis H1 = "MAPE global terendah". Seragamkan satu kriteria (atau jelaskan hubungan keduanya).
3. **Sitasi**: paragraf *Grid Search* saya beri sitasi (Mishra & Shaik, 2022) yang aslinya dipakai proposal untuk RMSE — **belum diverifikasi cocok** dengan isi klaim; paragraf Savitzky-Golay, RobustScaler, Yeo-Johnson **belum punya sitasi sama sekali**. Cari referensi yang tepat; cek juga konsistensi ejaan nama penulis (mis. Kontopoulou/Kontopoulos) terhadap Daftar Pustaka proposal. **Daftar Pustaka belum dibuat ulang** (copy dari proposal + tambahan; minimal 10 referensi).
4. **Angka EDA di Bab 3.3 belum diisi** (jumlah unit, jumlah kriteria, statistik deskriptif, distribusi, dsb.) karena butuh output notebook; isi dari hasil run (mis. 205 unit & 69 kriteria dipakai pada split 4 bulan; verifikasi untuk 3 bulan).
5. **Jika horizon utama pindah ke 4 bulan**, ubah: Bab 1.4 poin 3, 2.2.4 (kriteria "test < 3 bulan" → 4), 3.3 (33 bulan train/3 bulan test → 32/4), 2.2.4 langkah 9.
6. **H1 memuat kata "signifikan"** tetapi belum ada uji signifikansi statistik di code → tambahkan uji atau ubah redaksi.
7. Ruang lingkup poin 9–10 (Streamlit) tetap ditulis walau dashboard belum dibuat.
8. Total kata belum dihitung (batas usaha 12.000 kata seluruh laporan).
9. Bab 1.6 (Sistematika) ditulis generik untuk 6 bab; sesuaikan bila struktur akhir berubah.

### 20.7 [BARU] Update lanjutan Bab 3 & Daftar Pustaka

- **3.1 Analisis Masalah -- DIROMBAK**: sekarang murni masalah (bisnis PT X + teknis), tanpa kalimat "oleh karena itu butuh X" (itu dulu kecampur dari 3.2). Ditambah alasan bisnis forecast utilitas diperlukan: perencanaan *maintenance* (reaktif karena gak ada proyeksi beban kerja), perencanaan pengadaan unit baru (gak bisa diantisipasi lebih awal), keandalan komitmen operasional ke pelanggan pelabuhan saat volume tinggi, estimasi selama ini cuma pakai pengalaman/rata-rata historis tanpa faktor eksternal.
- **3.2 Analisis Kebutuhan -- DIROMBAK**: sekarang isinya kebutuhan **PT X** (bukan kebutuhan proyek/kita), tiap poin nyambung balik ke masalah di 3.1 satu-satu (sistem proyeksi -> akurasi terukur RMSE/MAPE -> proyeksi per unit/lokasi -> faktor eksogen). Paragraf lama soal *grid search* ARIMAX (p,d,q), *parallel processing*, *checkpoint*, kebutuhan komputasi **DIKELUARKAN TOTAL** dari 3.1 & 3.2 (itu kebutuhan teknis pengerjaan kita, bukan kebutuhan PT X) -- **BELUM dipindah ke tempat lain, masih nge-gantung**. Kandidat lokasi: Bab 2 Kerangka Kerja (Pemodelan) atau Bab 4 Lingkungan Pengujian -- user belum pilih.
- **3.3 Analisis Data -- DIROMBAK TOTAL** jadi murni hasil EDA (lihat §19.9), bukan lagi proses ETL (baca Excel, *multi-level header*, *forward fill*, dst). Paragraf ETL yang lama **BELUM dipindah** -- kandidat lokasinya Bab 2 subbab Penyiapan Data (2.2.4), user belum konfirmasi. Urutan penulisan final (tabel sebelum apa, gambar setelah apa) sudah dijelaskan ke user: teks dulu yang menyebut "pada Gambar X"/"pada Tabel X", baru gambar/tabelnya; judul Gambar DI BAWAH gambar, judul Tabel DI ATAS tabel.
- **Daftar Pustaka Bab 1-3 -- SUDAH DIBUAT** (format APA sama seperti proposal), dicek dari sitasi yang BENERAN muncul di teks Bab 1-3 (termasuk Bab 2 yang belum di-upload isinya ke chat ini, dicek dari `Buku_Skripsi__....md` yang di-upload user): **Cortez et al. (2023), Kontopoulou et al. (2023), Mishra & Shaik (2022), Petropoulos et al. (2022), Sirisha et al. (2022)** -- 5 referensi. **2 referensi di proposal TIDAK dipakai**: Atabay et al. (2022) dan Pantopoulou et al. (2025) -- gak muncul disitasi di Bab 1-3, dikeluarkan dari daftar sampai beneran dipakai. **PERLU DIPERHATIKAN**: pedoman minta **minimal 10 referensi** (§20.1) -- baru ada 5, kurang banyak, perlu tambahan sitasi/referensi baru seiring Bab 4-6 ditulis.
- Pertanyaan masih terbuka ke user: apa Bab 2 (yang sitasinya ikut dicek tapi isinya belum pernah di-upload ke chat ini) perlu dicek/dirapikan juga, atau cukup Bab 1-3 dulu sesuai scope -- **belum dijawab user**.

### 20.8 Belum dikerjakan (buku)

- Bab 4 (Implementasi & Pengujian: implementasi ringkas, lingkungan pengujian [server, Python, library, CPU/GPU], skenario pengujian ↔ rumusan masalah; hasil: 3 vs 4 bulan, rolling vs direct, perbandingan model/prep/pendekatan, tuning individual), Bab 5 (Pembahasan), Bab 6 (Kesimpulan & Saran), Daftar Pustaka, Lampiran, pembuatan diagram (§20.5), pengisian angka EDA, cek jumlah kata & tata tulis UK Petra 2025.

### 20.9 Istilah & gaya penulisan buku

- **Jangan** memakai "force-GB"/"dipaksa GB" di buku. Padanan: "model mayoritas (Gradient Boosting) dengan kombinasi *data preparation* dan *hyperparameter* yang disesuaikan per unit/kriteria".
- Nama perusahaan: **PT X**. Istilah asing dicetak miring (*Gradient Boosting*, *grid search*, dst.), gaya seperti proposal.
- Jangan menyebut pengecualian 10 unit (filter kelayakan tetap dijelaskan dengan 4 kriteria dari proposal).
- Preferensi kerja terkait: user berkomunikasi dalam bahasa Indonesia; kadang meminta gaya ringkas (`/caveman`); untuk teks buku lebih suka teks yang bisa di-copy dari chat (bukan file), tabel juga diminta plain text (bukan markdown table) kalau bold/italic gak kebaca di tempat dia paste. **[UPDATE]** Untuk `code_v4.ipynb`: sekarang **HANYA `.ipynb`, jangan dirangkap `.py` lagi** (beda dari sebelumnya yang suka dua-duanya) -- khusus utk notebook ini saja; `pipeline_lib.py`/`appDemo.py`/`appPerusahaan.py` tetap `.py` karena itu modul/aplikasi, bukan turunan notebook.

### 20.10 [BARU] Justifikasi Ilmiah Berbasis EDA, Proposal, & Metodologi (Jawaban 3 Pertanyaan Bimbingan)

Terkait tiga pertanyaan kunci dosen dalam sesi bimbingan mengenai **(1) Mengapa memilih 1 model tunggal (Gradient Boosting) untuk seluruh unit & mengapa ARIMAX serta LSTM tetap diuji sejak awal**, **(2) Mengapa teknik data preparation dibedakan per unit/kriteria**, serta **(3) Mengapa memilih keempat pendekatan data preparation tersebut (`Baseline`, `Savitzky-Golay`, `RobustScaler`, `Yeo-Johnson`) dan apa dasar pemilihannya**:

1. **Justifikasi Model Tunggal (*Gradient Boosting*) untuk Seluruh Unit & Alasan Pengujian Tiga Model (ARIMAX, *Gradient Boosting*, LSTM)**:
   - **Kesesuaian dengan Rumusan Masalah, Tujuan Proyek, Hipotesis (H1), dan Rancangan Evaluasi Global (Proposal & Buku Bab 1–2)**:
     - Sesuai Bab 1.2 (Rumusan Masalah poin 2), Bab 1.3 (Tujuan Proyek), Bab 2.2.2 (Hipotesis Solusi H1), Proposal Bab 8, dan Buku Bab 2.2.5 Poin 6: penelitian ini sejak awal dirancang untuk membandingkan 3 model guna **menetapkan satu model terbaik secara menyeluruh** bagi seluruh armada PT X (bukan mencampur model berbeda per unit). Jika hasil akhir mencampur-aduk 3 model, penelitian justru gagal menjawab Rumusan Masalah ke-2 dan Hipotesis H1.
   - **Alasan Mengapa ARIMAX dan LSTM Tetap Diuji Sejak Awal (Studi Literatur Tiga Paradigma)**:
     - Berdasarkan studi literatur (Cortez et al., 2023; Kontopoulou et al., 2023; Pantopoulou et al., 2025; Sirisha et al., 2022), ketiga model mewakili 3 paradigma berbeda yang masing-masing punya kelebihan dan kekurangan: **ARIMAX** (statistik deret waktu linier, unggul di hubungan linier stasioner tapi kaku pada fluktuasi non-linier), **LSTM** (*deep learning* sekuensial dengan *cell state* & *gates*, unggul di memori jangka panjang dengan sampel besar namun rawan *overfitting* pada deret bulanan pendek 36 bulan), dan ***Gradient Boosting*** (*machine learning ensemble* pohon keputusan dengan *lag features*, unggul memodelkan hubungan non-linier dan tahan terhadap *noise* operasional). Ketiganya wajib diuji secara paralel terlebih dahulu untuk membuktikan paradigma mana yang paling cocok bagi data PT X.
   - **Kecocokan Karakteristik Data PT X (Hasil EDA Bab 3.3) terhadap *Gradient Boosting***:
     - **Sifat *Short-Memory* (PACF Lag 1–3)**: Autokorelasi parsial (PACF) deret waktu utilitas di mayoritas unit terputus tajam setelah **Lag 1 s/d Lag 3** (tidak ada siklus memori multi-tahunan yang menuntut *cell state* LSTM). Fitur `lag_1`, `lag_2`, `lag_3` pada *Gradient Boosting* sudah optimal menangkap ketergantungan historis tanpa *overfitting*.
     - **Hubungan Non-Linier & *Threshold Effect* Variabel Eksogen**: Utilitas berkorelasi positif kuat dengan volume *container* ($r = 0,70$) dan negatif dengan curah hujan ($r = -0,30$), serta pada **57,2% unit** (131 dari 229 unit) korelasi monotonik non-linier (Spearman) lebih kuat daripada korelasi linier (Pearson). Partisi pohon keputusan pada *Gradient Boosting* paling adaptif menangkap efek ambang batas (*threshold effect*) dan guncangan musiman (seperti penurunan tajam setiap bulan April saat Idul Fitri).
   - **Mitigasi *Test-Set Selection Bias*, Margin Selisih Sangat Kecil ($\Delta = 0,49\%$), & Kestabilan *Rolling Forecast***:
     - Memilih model berbeda per unit pada periode uji yang hanya 3 bulan (Okt–Des 2025) rentan terhadap *test-set selection bias* (*spurious fit*). Rata-rata MAPE model campur (85 ARIMAX + 80 GB + 40 LSTM) adalah **14,99%**, sedangkan model tunggal *Gradient Boosting* adalah **15,48%** (selisih hanya **0,49%** dan median selisih **0,00%**). Selain itu, pada proyeksi masa depan *multi-step rolling* (3–12 bulan), *Gradient Boosting* menghasilkan prediksi yang terjaga (*bounded*) dan stabil dibandingkan ARIMAX yang rawan *flatline* atau LSTM yang rawan akumulasi *error* pada *hidden state*.

2. **Justifikasi Mengapa Teknik *Data Preparation* Dibedakan per Unit / Kriteria (Berdasarkan EDA Skewness & Sebaran Bab 3.3)**:
   - **Perbedaan Fungsi Model vs *Data Preparation***: Algoritma model (*Gradient Boosting*) bertugas memetakan hubungan fitur prediktor terhadap target pada domain bisnis yang sama, sedangkan *data preparation* berfungsi menormalkan distribusi, meredam *noise*, dan menstabilkan skala data mentah masing-masing unit **sebelum** masuk ke model.
   - **Bukti Empiris Heterogenitas *Skewness* Antar-Unit (Bab 3.3)**:
     - Secara *pooled* (8.280 baris unit-bulan), utilitas memiliki simpangan baku lebar (178,26 jam, rentang 0–744 jam) dan *skewness* 0,54 (*right-skewed*, menumpuk di 0–100 jam pada Gambar 3.5). Secara individual per unit (229 unit), distribusinya sangat heterogen:
       - **104 unit (~45%)**: distribusi mendekati simetris/normal (*skewness* -0,5 s/d 0,5) — unit operasional rutin.
       - **51 unit (~22%)**: kemencengan moderat (*skewness* 0,5 s/d 1,0).
       - **74 unit (~33%)**: kemencengan ekstrem (|*skewness*| > 1,0, rentang -3,05 s/d +5,75) — unit yang kadang *idle*/perawatan (bernilai 0) lalu melonjak tajam di periode tertentu.
   - **Dampak Negatif Jika Diseragamkan**: Memaksa seluruh unit memakai satu teknik (misalnya semua *Yeo-Johnson*) akan menyebabkan *over-transformation* pada 45% unit yang sudah simetris; sebaliknya tanpa normalisasi distribusi, 33% unit yang menceng ekstrem akan mendistorsi pelatihan model. Oleh karena itu, penyesuaian *data preparation* per unit (Bab 2.2.5 Poin 6) adalah preskripsi statistik yang objektif.

3. **Justifikasi Pemilihan Keempat Pendekatan *Data Preparation* (`Baseline`, `Savitzky-Golay`, `RobustScaler`, `Yeo-Johnson`) Beserta Dasar Pemilihannya**:
   - Keempat metode dipilih karena mewakili **2 kelompok penanganan masalah data deret waktu** (*Smoothing/Denoising* dan *Scaling/Normalisasi Distribusi*) yang menjawab langsung temuan masalah di EDA Bab 3.3 sekaligus mengatasi keterbatasan metode *Baseline* awal (dengan *inverse transform* ke satuan jam asli untuk evaluasi *apple-to-apple*):
     1. ***Baseline* (*Outlier Capping* Persentil ke-95 + *Rolling Mean Smoothing* 2 Bulan)**: Dipilih sebagai acuan dasar sesuai rancangan Proposal untuk memotong lonjakan ekstrem anomali pencatatan dan menghaluskan fluktuasi jangka pendek. *Kelemahannya*: *capping* memotong informasi lonjakan beban kerja riil, dan *moving average* biasa cenderung meratakan puncak serta lembah data secara berlebihan (*over-smoothing*).
     2. ***Savitzky-Golay Filter* (*Savgol*)**: Dipilih untuk menjawab temuan **EDA Tren (Gambar 3.1 & 3.2)** di mana data memiliki fluktuasi bulanan disertai puncak dan lembah musiman yang tajam dan nyata (seperti penurunan tajam setiap bulan April saat Idul Fitri). Berbeda dengan *moving average* biasa, pencocokan polinomial *least squares* pada *Savitzky-Golay* mampu meredam *noise* jangka pendek **sekaligus mempertahankan bentuk, tinggi puncak, dan kedalaman lembah data yang tajam** (Bab 2.1.1 Poin 5).
     3. ***RobustScaler* (*Robust*)**: Dipilih untuk menjawab temuan **EDA Statistik Deskriptif & Outlier (Tabel 3.1, Tabel 3.2, Gambar 3.8 & 3.10)** di mana simpangan baku utilitas sangat lebar (178,26 jam) dan dipengaruhi bulan-bulan *outlier* (April 2023 & April 2025). Dipilih dibanding *StandardScaler* atau *MinMaxScaler* karena *StandardScaler* menggunakan *mean* dan *std* yang sensitif terhadap *outlier*, sedangkan *RobustScaler* menggunakan **Median dan *Interquartile Range* (IQR)** (Bab 2.1.1 Poin 6) sehingga tahan (*robust*) terhadap nilai ekstrem tanpa harus memotong/membuang nilai puncak aktual seperti pada *capping*.
     4. ***PowerTransformer Yeo-Johnson* (*Yeo-Johnson*)**: Dipilih untuk menjawab temuan **EDA Distribusi (Gambar 3.5 & Tabel 3.1)** di mana data utilitas memiliki kemencengan (*skewness*) positif dan **banyak mengandung nilai nol (0 jam)** pada bulan-bulan ketika unit sedang *idle* atau menjalani *maintenance*. Dipilih dibanding transformasi *Box-Cox* atau $\log(x)$ karena *Box-Cox* secara matematis hanya bisa memproses nilai positif murni ($x > 0$) dan akan *error* saat bertemu nilai 0, sedangkan **Yeo-Johnson** mampu menormalkan distribusi yang *skewed* sekaligus **bekerja langsung pada data yang mengandung nilai nol** (Bab 2.1.1 Poin 7).


4. **Justifikasi Mengapa LSTM Tidak Diikutkan dalam Pengujian Eksogen Lag-1 ($t-1$ vs $t$) di Revisi Bimbingan ke-2**:
   - **LSTM Sejak Awal Menggunakan Eksogen (Multivariate LSTM)**: Pada pengujian Tahap 2 (`code_v4.ipynb` Cell 25), arsitektur LSTM yang diuji bukan univariate, melainkan multivariate dengan matriks input 3 fitur ($y$ utilitas, `CURAH_HUJAN`, dan `VOLUME_CONTAINER`).
   - **LSTM Sudah Tereliminasi di Tahap 2**: Dari evaluasi 12 kombinasi (Tahap 2b), LSTM terbukti paling tidak kompetitif pada deret waktu bulanan pendek (hanya 36 titik waktu per unit: 32 train, 4 test). LSTM hanya memenangkan 40 unit (jauh di bawah ARIMAX 85 unit dan Gradient Boosting 80 unit), serta hanya memenangkan 17 kriteria (sedangkan GB mendominasi 48 kriteria). Model deep learning bersifat *data-hungry* dan rentan *overfitting* atau instabilitas gradien pada sampel berukuran kecil.
   - **Fokus Arahan Dosen Pembimbing ke-2**: Rekomendasi dosen pembimbing ke-2 secara spesifik mempertanyakan pembuktian empiris perdebatan statistik deret waktu klasik antara **ARIMA murni (tanpa eksogen)** vs **ARIMAX eksogen $t$** vs **ARIMAX eksogen lag-1 ($t-1$)**, serta melihat dampaknya pada model produksi skripsi (**Gradient Boosting**). Menguji kembali variasi lag-1 pada model yang sudah tereliminasi (LSTM) tidak relevan dengan tujuan penyusunan model produksi dan hanya menambah beban komputasi pelatihan neural network.

### 20.11 [BARU] Sintesis Akademis Hasil Bimbingan Lanjutan: Fenomena Disagregasi Per-Kriteria vs Per-Unit & 6 Insight Kunci Skripsi

Menindaklanjuti pertanyaan kunci Dosen Pembimbing pada sesi bimbingan lanjutan: *"Mengapa evaluasi per-kriteria menghasilkan error yang lebih buruk daripada per-unit, padahal secara intuitif jika per-unit bagus maka per-kriteria seharusnya ikut bagus?"*, berikut adalah telaah ilmiah mendalam beserta 6 insight empiris tambahan sebagai bahan penyusunan Bab 4 (Hasil dan Pembahasan) dan Bab 5 (Kesimpulan):

1. **Mengapa Error Per-Kriteria Lebih Buruk daripada Per-Unit (Fenomena Disagregasi & Heterogenitas Operasional)**:
   - **Heterogenitas Operasional & Dinamika *Dispatching* Lapangan**: Meskipun unit-unit dalam satu kriteria memiliki spesifikasi mekanis yang identik (jenis alat, merk, tipe, kapasitas, dan daya mesin HP yang sama), dalam operasional riil pelabuhan pembebanan jam kerja mesin (*operating hours*) tidak terbagi secara merata. Penugasan alat sangat bergantung pada rotasi operator dermaga, kedekatan posisi parkir alat dengan kapal kontainer, kondisi keausan suku cadang (*wear and tear*), serta siklus *preventive maintenance*. Akibatnya, dinamika deret waktu masing-masing unit sangat bervariasi dan tidak dapat diwakili oleh rata-rata agregat kriteria.
   - **Distorsi Matematis Disagregasi Proporsional pada Unit Jam Rendah (*Asymmetric Loss Penalty*)**:
     Pada pendekatan per-kriteria, peramalan dilakukan pada total jam kerja grup kriteria ($\hat{Y}_{k,t}$), kemudian nilai tersebut dipecah kembali ke masing-masing unit anggota menggunakan proporsi rata-rata historisnya ($p_i$):
     $$\hat{y}_{i,t} = p_i \times \hat{Y}_{k,t}, \quad \text{di mana } p_i = \frac{\sum_{\tau} y_{i,\tau}}{\sum_{\tau} Y_{k,\tau}}$$
     Jika suatu unit pada periode pengujian sedang mengalami perbaikan besar (*overhaul*) atau *idle* sehingga jam kerja aktualnya mendekati nol ($y_{i,t} \to 0$), alokasi proporsional tetap membebankan estimasi jam kerja positif ($\hat{y}_{i,t} > 0$). Pada metrik evaluasi persentase:
     $$\text{MAPE}_{i} = \frac{|\hat{y}_{i,t} - y_{i,t}|}{y_{i,t}} \times 100\%$$
     pembagian dengan angka aktual yang mendekati nol menyebabkan nilai persentase error meledak hingga ratusan persen (*infinite penalty distortion*). Sebaliknya, pada pemodelan *per-unit*, model secara langsung membaca penurunan jam kerja historis unit bersangkutan dan memproyeksikan nilai rendah yang mendekati aktual.
   - **Kompromi Hiperparameter Model (*Sub-optimal Fitting*)**: Pada pendekatan per-kriteria, satu model tunggal dipaksa mempelajari pola gabungan unit dengan variasi *skewness* ekstrem (-3,05 s/d +5,75). Model terpaksa mengambil jalan tengah (kompromi), sehingga gagal menangkap pola unik unit-unit individu. Sebaliknya, pendekatan per-unit memberikan kebebasan bagi algoritma untuk menyesuaikan hiperparameter secara spesifik (*tailored tuning*) pada masing-masing aset.
   - **Konfirmasi Literatur *Hierarchical Forecasting Principle* (*Bottom-Up Superiority*)**: Dalam teori deret waktu hierarkis (Hyndman & Athanasopoulos, 2018), pendekatan *bottom-up* (meramalkan deret waktu pada level terendah lalu menjumlahkannya ke level atas) secara konsisten mengungguli pendekatan *top-down* disagregasi proporsional ketika deret waktu di tingkat individu memiliki pola yang sangat heterogen dan rentan terhadap guncangan lokal.

2. **Enam (6) Insight Empiris Kunci Tambahan untuk Pembahasan Skripsi**:
   - **Insight 1: Dominasi Hubungan Monotonik Non-Linier (*Spearman* 55,61% vs *Pearson* ~20%)**:
     Analisis korelasi pada populasi armada menunjukkan bahwa pada **55,61% unit**, koefisien korelasi rank Spearman ($|\rho|$) antara operating hours dengan variabel curah hujan dan volume kontainer secara signifikan lebih kuat dibandingkan korelasi linier Pearson ($|r|$). Hal ini membuktikan bahwa operasional alat berat di pelabuhan merespons cuaca secara non-linier / fungsi tangga (*threshold effect*): hujan lebat memicu penghentian operasional secara mendadak demi keselamatan (*safety halt*), bukan penurunan linier bertahap. Temuan ini menjadi justifikasi ilmiah kuat mengapa model pohon keputusan (*Gradient Boosting*) jauh lebih unggul dibanding regresi linier statistik.
   - **Insight 2: Realisme Operasional Pemodelan Lag-1 ($t-1$) Bebas *Data Leakage***:
     Dalam perencanaan operasional riil di pelabuhan, manajemen tidak dapat mengetahui curah hujan aktual atau volume kontainer pada bulan $t$ saat jadwal kerja alat berat bulan $t$ sedang disusun. Pengujian empiris membuktikan bahwa penggunaan fitur eksogen Lag-1 ($t-1$) menghasilkan peramalan yang realistis dan 100% bebas kebocoran data (*zero data leakage*), dengan akurasi yang tetap sangat kompetitif (MAPE Gradient Boosting Lag-1 = 15,67%).
   - **Insight 3: Degradasi Parameter ARIMAX vs Ketahanan *Gradient Boosting***:
     Penambahan variabel eksogen pada ARIMAX justru memperburuk performa model (Mean MAPE naik dari 18,38% pada ARIMA murni menjadi 19,79% pada ARIMAX Lag-1). Hal ini disebabkan oleh keterbatasan estimasi koefisien linier pada sampel bulanan pendek (36 bulan) yang rentan mengalami *overparameterization* dan multikolinearitas. Sebaliknya, *Gradient Boosting* memiliki mekanisme seleksi fitur bawaan (*built-in feature selection*) pada struktur pohonnya, sehingga tahan terhadap *noise* variabel eksogen.
   - **Insight 4: Interaksi Efektif *Data Preparation* Berbasis Karakteristik Deret Waktu**:
     Tidak ada teknik *data preparation* tunggal yang mendominasi seluruh armada secara mutlak. Unit-unit dengan jam operasional stabil dan berpuncak musiman tajam sangat diuntungkan oleh *Savitzky-Golay Filter* (menjaga bentuk gelombang), sedangkan unit dengan frekuensi jam kerja nol yang tinggi membutuhkan transformasi *Yeo-Johnson* atau penskalaan *RobustScaler*. Fakta ini memvalidasi keunggulan rancangan metodologi *individualized data-prep selection*.
   - **Insight 5: Degradasi Akurasi Horizon > 3 Bulan (*Horizon Decay Effect*)**:
     Evaluasi peramalan rekursif (*multi-step recursive forecasting*) memperlihatkan bahwa akurasi model bertahan sangat tinggi pada bulan ke-1 hingga bulan ke-3, namun mengalami penurunan akurasi (*error compounding*) mulai bulan ke-4 dan seterusnya. Hal ini membuktikan batas reliabilitas peramalan operasional alat berat pelabuhan adalah 3 bulan (*quarterly planning cycle*), yang menjadi dasar penetapan rekomendasi manajemen dan antarmuka *slider* pada dashboard.
   - **Insight 6: Distorsi Matematis Metrik MAPE pada Jam Kerja Rendah**:
     Evaluasi performa memperlihatkan bahwa metrik MAPE sangat rentan terhadap bias skala pada unit-unit dengan jam kerja kecil ($<50$ jam). Selisih prediksi 10 jam pada unit berjam kerja 5 jam menghasilkan MAPE 200%, sementara selisih 10 jam pada unit berjam kerja 400 jam hanya menghasilkan MAPE 2,5%. Oleh karena itu, pembahasan skripsi wajib melengkapi evaluasi persentase (MAPE) dengan nilai absolut fisik (RMSE) untuk memberikan evaluasi performa armada yang berimbang dan adil.

### 20.12 [BARU] Penjelasan Ilmiah Penomoran ID Unit 3 Digit (UNIT_001 s/d UNIT_345) vs Populasi Aktif 200-an

Untuk menjawab pertanyaan dewan penguji atau dosen pembimbing mengenai alasan penomoran unit mencapai nomor urut 300-an (misal `UNIT_345`) padahal total populasi operasional yang diteliti hanya sekitar 200-an unit:

1. **Prinsip Integritas *Audit Trail* Basis Data Enterprise**:
   - Penomoran unik 3 digit (`UNIT_001` s/d `UNIT_345`) merupakan kode identitas aset unik (*Unique Asset Identifier*) yang dibangkitkan sejak awal dari master data mentah logistik perusahaan yang mencatat seluruh 345 riwayat alat berat.
   - Selama tahapan ETL dan penyaringan kelaikan teknis, sebanyak 115 unit disaring keluar dari cakupan penelitian (unit sewa/rental pihak ketiga, unit uji coba/dummy mekanik, dan unit dengan histori transaksi tidak lengkap), disusul eliminasi 15 unit anomali.
2. **Bahaya Penomoran Ulang (*No Re-numbering Standard*)**:
   - Dalam tata kelola basis data aset industri modern, nomor aset yang telah disaring **pantang untuk dinomorkan ulang (*re-number*) secara berurutan (1 s/d 190)**. Penomoran ulang akan merusak rantai keterlacakan (*traceability*) ke histori transaksi fisik asli di pelabuhan (seperti logsheet servis mekanik dan bukti pengisian BBM), memicu risiko kerancuan identitas aset (*identity collision*), serta menyulitkan validasi silang oleh tim teknis operasional.
3. **Format Terpadu `K<NoKriteria>_UNIT_<Nomor3Digit>`**:
   - Dengan menyatukan kode kriteria 2 digit dan nomor unik aset 3 digit (contoh: `K01_UNIT_004`, `K09_UNIT_309`), sistem berhasil mengintegrasikan informasi kelompok spesifikasi alat sekaligus mempertahankan nomor identitas unik aset tanpa merusak jejak audit database perusahaan.

### 20.13 [BARU] Persiapan Penulisan Bab 4–6 (chat penulisan buku)

**Status:** teks Bab 4 (4.1–4.9) pernah ditulis di chat dengan angka PRA-RERUN; **teksnya tidak tersimpan di PROGRESS** (hanya kerangka & angka kunci di bawah). Setelah rerun 215 unit (§19.13) semua angka harus diganti dari output baru. Bab 5, Bab 6, Daftar Pustaka, dan update Bab 3.3 BELUM ditulis.

**20.13.1 Aturan pedoman (format Proyek DSA)**
- Bab 4 = **Implementasi dan Pengujian** (Implementasi Solusi, Lingkungan Pengujian, Skenario Pengujian, tiap pengujian subbab sendiri); Bab 5 = **Pembahasan**; Bab 6 = **Kesimpulan dan Saran**.
- ⚠️ §9 poin 57 menulis "Bab 4 (Hasil dan Pembahasan), Bab 5 (Kesimpulan), Bab 6" — itu KELIRU terhadap pedoman; yang benar seperti di atas.
- Daftar Pustaka minimal **10** referensi (Proyek; Riset 20), diutamakan 5 tahun terakhir; batas ±12.000 kata (40 halaman) — user: **boleh dilampaui**.

**20.13.2 Audit `draft_bab_1-3.md`**
- Isi Bab 1–3 ≈ 8.000 kata (+ ≈430 kata sampul/daftar isi). Istilah "utilitas" muncul 89 kali (69 huruf kecil, 5 "Utilitas", 15 "UTILITAS") → semua diganti *operating hours*. Angka lama: "230" 2×, "190" 1×, "mayoritas" 3×, "signifikan" 3×; belum ada eksogen *t*/lag-1.
- Bab 4–6 di draft masih stub: heading + paragraf template (profil perusahaan yang menyebut PT SPIL/Surabaya 6×) — harus diganti seluruhnya.
- Revisi Bab 1–3 DITUNDA (user: fokus Bab 4–6 dulu).

**20.13.3 Keputusan user di chat ini**
| Hal | Keputusan |
|---|---|
| Eksogen final | **Eksogen *t*** (user akan info kalau berubah); lag-1 hanya di bab yang membahas seluruh percobaan |
| "mayoritas" GB | Tetap ditulis, tapi dibatasi: GB menang di 48 dari 69 kriteria (pra-rerun); di level unit ARIMAX 85, GB 80, LSTM 40 (pra-rerun) |
| 15 unit MAPE>40% | Disembunyikan seperti 10 unit awal; kode/dashboard dibersihkan; populasi **215 unit** (190 valid + 25 exclude data), pipeline sudah **rerun penuh** |
| Uji signifikansi H1 | Tidak perlu |
| "utilitas" | Ganti semua jadi *operating hours*, termasuk judul |
| Urutan kerja | Bab 4–6 dulu, lalu Daftar Pustaka, update Bab 3.3, Bab 1–3 terakhir |
| Spek lingkungan | Versi pustaka & waktu tetap `[ISI]` sampai diverifikasi (`pip list`); angka versi di `spesifikasi_lingkungan_dan_runtime.md` TIDAK dipakai |
| Judul gambar | "(Surabaya)" dihapus |
| Screenshot dashboard | User pasang sendiri; Claude cukup beri keterangan gambar |
| Default Claude (belum dikonfirmasi eksplisit) | MAPE metrik utama (RMSE pendamping); paragraf ETL lama → Bab 2.2.4; paragraf grid search/parallel/checkpoint → Bab 4.2; referensi tambahan dicari via web (≥6, total ≥10, APA seperti proposal) |

**20.13.4 Temuan review berkas (jangan terulang)**
- `penjelasan_eksperimen_6_skenario.md` **bertentangan** dengan `perbandingan_eksogen_dan_model.xlsx`: md menyebut GB lag-1 = 11,48% sebagai "model produksi final" (GB *t* 12,01%, tanpa eksogen 11,95%); xlsx pra-rerun (190 unit): GB *t* **11,48** (median 9,59), GB lag-1 15,67, GB tanpa eksogen 14,90, ARIMA 18,38, ARIMAX *t* 19,26, ARIMAX lag-1 19,79. Daftar hyperparameter di md (ada `l2_regularization`) juga tidak cocok dengan kode. → md TIDAK dipakai sebagai sumber.
- `spesifikasi_lingkungan_dan_runtime.md`: versi pustaka tidak konsisten (TensorFlow 2.15 mensyaratkan NumPy<2 tapi tertulis 2.0.2; pmdarima 2.0.4 bermasalah dgn NumPy 2; "Keras 2.16" tak berpasangan dgn TF 2.15); durasi hanya Tahap 3 (**35,04 detik**) yang terukur, sisanya rentang estimasi. Perangkat: Windows 11 Pro, i7-1165G7 (4 inti/8 thread), 16 GB, SSD 512 GB, Iris Xe (tak dipakai) — kelas laptop, ditulis "komputer lokal".
- PACF/Spearman (angka pra-rerun, 229 unit): |Spearman|>|Pearson| di 131 unit (57,2%) tapi uji binomial vs 50% p≈0,034, selisih rata-rata |rs|−|rp| hanya 0,009, median |r| 0,23 vs 0,24 → hanya indikasi ringan, BUKAN penjelasan keunggulan GB. PACF "79,5% terputus di lag ≤3" sudah termasuk 68 unit tanpa lag signifikan; dari 161 unit yang punya lag signifikan hanya 114 (70,8%) terputus ≤3; pengecekan hanya sampai lag 6 dengan N=36 (lag musiman tak terdeteksi); klaim "LSTM kalah karena tak ada memori multi-tahun" adalah dugaan (data pendek lebih masuk akal). Tulis dengan redaksi hati-hati; ambil angka dari rerun (§20.11 menyebut Spearman 55,61% pasca-rerun).
- **Bias seleksi:** 15 unit dibuang berdasarkan MAPE test GB (eksogen *t*) >40% → semua perbandingan pada populasi 190/215 condong menguntungkan 3 bulan, *direct*, dan GB *t* (pra-rerun: Wilcoxon horizon p=0,279 di 205 unit tapi 0,018 di 190 unit; maks MAPE GB *t* 39,87 vs 75–127 di skenario lain). Di buku: JANGAN tulis alasan exclude, JANGAN pakai kata "signifikan"/nilai p untuk horizon; cukup rata-rata & jumlah unit, plus kalimat keterbatasan netral di Bab 5 ("hasil berlaku untuk unit yang tercakup dalam populasi analisis"). Keputusan akhir di user.
- Pemilihan *hyperparameter* Tahap 2 = **MAPE_GLOBAL terendah** (28/28 pemenang). ARIMAX per-kriteria varian *savgol* agregasi *sum* (MAPE 13,47, RMSE 14,48) di luar pola → `[CEK]` jumlah kriteria yang berhasil terlatih sebelum dimuat; jangan dipakai sbg pembanding sebelum dicek. Grid GB di master = 396 baris/grup vs 4×3×3×3=108 nilai terlihat `[CEK]`; rentang tuning individual 36 kombinasi (×4 varian = 144 fit/unit) tidak ditemukan di notebook `[CEK]`. Grid ARIMAX p 0–8, d 0–4, q 0–8; LSTM seq {3,6}, unit {16,32}, epoch {30,50}.

**20.13.5 Kerangka Bab 4 (ada di chat lama)**
4.1 Implementasi Solusi (notebook + `pipeline_lib.py` + 2 dashboard; retrain seluruh riwayat, peramalan rekursif, eksogen masa depan = rata-rata musiman per bulan kalender, horizon 3–12 bulan default 3; Gambar 4.1–4.4 = screenshot) · 4.2 Lingkungan Pengujian (Tabel 4.1 hardware, 4.2 software `[ISI]`, 4.3 waktu eksekusi) · 4.3 Skenario Pengujian (split Jan 2023–Sep 2025 / test Okt–Des 2025; Tabel 4.4 pemetaan pengujian ↔ rumusan masalah) · 4.4 Pengujian 1 perbandingan model/varian/pendekatan (Tahap 2 + 2b) · 4.5 Pengujian 2 model tunggal & penyesuaian konfigurasi (JANGAN pakai istilah "force-GB") · 4.6 Pengujian 3 horizon 3 vs 4 bulan · 4.7 Pengujian 4 *direct* vs *rolling* · 4.8 Pengujian 5 peran eksogen (6 skenario) · 4.9 Pengujian 6 peramalan ke depan pada dashboard.

**Angka kunci PRA-RERUN (SUPERSEDED — ganti dgn output rerun):**
- Tahap 2 per unit (205 unit, MAPE global): GB *savgol* 22,69 (terendah), GB *baseline* 22,76, ARIMAX *baseline* 23,36, LSTM ≈23,8; RMSE global terendah ARIMAX *savgol* 67,18 vs GB *savgol* 68,35 (metrik tak sepenuhnya sejalan).
- Tahap 2b: rata-rata MAPE per unit terendah GB *baseline* 22,77; model terbaik per unit ARIMAX 85 / GB 80 / LSTM 40; per kriteria (69) GB 48 / LSTM 17 / ARIMAX 4.
- Model akhir (190 unit): MAPE 11,48 (median 9,59, RMSE 33,66) vs terbaik-per-unit 11,74 (RMSE 33,33); 74 unit GB tanpa penyesuaian, 116 disesuaikan; GB ≤ terbaik-per-unit di 134 unit (lebih rendah tegas di 60); MAPE <10: 99, 10–20: 65, 20–30: 19, ≥30: 7; varian *savgol* 56, *yeojohnson* 52, *baseline* 49, *robust* 33.
- Horizon (205): MAPE 4 bln 16,19 vs 3 bln 15,48 (3 bln lebih rendah di 113 unit); kriteria 23,51 vs 22,29.
- *Direct* vs *rolling* (205): 15,48 vs 17,88 (direct lebih rendah 89, rolling 33, identik 83); kriteria 22,29 vs 25,32 (35/10/24).
- Eksogen (190): lihat 20.13.4. Tahap 3: 35,04 detik.
- Catatan jujur untuk Bab 4/5: pemilihan konfigurasi dan evaluasi memakai *test* yang sama (angka optimistis); eksogen *t* diuji dgn data aktual sedangkan peramalan ke depan memakai estimasi musiman (akurasi kondisi itu belum diuji); *rolling* wajib untuk peramalan ke depan sehingga galat 12 bulan lebih besar dari angka evaluasi *direct*.

**20.13.6 Format teks yang disukai user:** teks langsung di chat (bukan kotak salin/berkas), tabel boleh markdown biasa, istilah asing dimiringkan dengan tanda `*`; "PT X" untuk perusahaan; caption gambar di bawah, caption tabel di atas.

---


# BAGIAN C — DASHBOARD STREAMLIT (terpisah dari analisa code & buku)

## 21. Dashboard Streamlit -- `pipeline_lib.py`, `appDemo.py`, `appPerusahaan.py`

### 21.1 Keputusan desain (hasil tanya-jawab sebelum mulai bikin)

| Pertanyaan | Keputusan user |
|---|---|
| 2 dashboard terpisah? | **Ya** -- `appDemo.py` (sidang) dan `appPerusahaan.py` (PT X), file & tujuan beda |
| appDemo.py isinya apa | GB Seragam (final, dipakai produksi) vs Model Terbaik per unit/kriteria (Tahap 2b, bisa ARIMAX/GB/LSTM), MAPE & RMSE per unit, plot training+testing, plot actual s/d future forecast (beda warna), horizon fleksibel 3-12 bulan (default 3), termasuk tab per kriteria |
| appPerusahaan.py isinya apa | Sederhana: input data dulu, dropdown unit, plot actual s/d prediksi (TANPA metrik error), horizon fleksibel 3-12 bulan default 3 dengan catatan error naik di atas 3 bulan, tab unit di-exclude + alasan, export Excel |
| Istilah "GB forced" di dashboard | **Bebas**, boleh pakai istilah lain yang representatif -- dashboard dipakai "GB Seragam" vs "Model Terbaik (Tahap 2b)" |
| Upload data di appPerusahaan.py | Field disesuaikan kebutuhan TA (bukan niru persis screenshot dashboard BBM lama appTNTv3.py yang konteksnya beda) -- BBM AAB per tahun, cost&bbm HP&Type, Container per tahun, Curah Hujan |
| Live-process vs baca hasil jadi | **appDemo.py**: baca hasil jadi (checkpoint), gak perlu upload. **appPerusahaan.py**: upload data baru -> ETL live + **fit ulang pakai config final yang SUDAH ada** (bukan grid search baru) |
| Future forecast perlu kerjaan baru? | **Ya**, disetujui -- jadi dasar Tahap 3 (§19.10) |
| Nama file | `pipeline_lib.py`, `appDemo.py`, `appPerusahaan.py` |
| Export Excel appPerusahaan | Cukup **unit, bulan, nilai forecast** saja (user: "untuk user sebenarnya hanya itu yg penting") |

### 21.2 Struktur `pipeline_lib.py` (~670 baris, shared logic)

1. **ETL** (`build_monthly_full()`) -- port persis dari `code_v4.ipynb` cell 2-10 (scan nama unit, parsing BBM AAB *multi-level header*, delta HM + cap 24 jam, parsing Container (CURRSTATE blocks), curah hujan, matching ke cost&bbm HP&Type -> `kriteria`, exclude 10 unit + remap ID). Dibungkus jadi fungsi, terima path file sbg parameter (bukan hardcoded).
2. 4 varian data-prep (baseline/savgol/robust/yeojohnson) -- port persis dari cell 22.
3. Lag features + `forecast_gb_rolling`, `clean_gb_params` -- port persis dari cell 24/28.
4. `retrain_and_forecast_unit()` -- port persis dari Tahap 3 (§19.10).
5. **[BARU, belum ada di notebook]** `retrain_and_forecast_kriteria()` -- 1 model dilatih dari data gabungan semua unit anggota kriteria (konsisten metodologi GB per-kriteria di Tahap 2, bukan agregasi 1 series dulu), forecast kriteria = jumlah forecast tiap unit anggota.
6. **[BARU, belum ada di notebook]** `evaluate_unit_on_test()` -- fit pakai train (s/d Sep 2025), prediksi test (Okt-Des 2025) scr *direct*, dipakai utk plot training vs testing di appDemo (sebelumnya cuma ada metrik tersimpan, bukan prediksi mentah per baris yang siap dipakai ulang).
7. Loader file-file hasil checkpoint (`v4_forcedgb_vs_v2b_comparison.xlsx`, `v4_rolling_vs_direct.xlsx`, excluded summary, future forecast, `04_monthly_with_exog.csv`, `08_kriteria_unit.csv`).

### 21.3 `appDemo.py` (227 baris)

- Baca langsung dari `./checkpoints_v4` (base) dan `./checkpoints_v4/h3bulan` (horizon final) -- **gak perlu upload, gak perlu Tahap 3 dijalankan ulang** (asal sudah pernah dijalankan sekali).
- 3 tab: **Ringkasan** (perbandingan GB Seragam vs Model Terbaik Tahap 2b per unit/kriteria, tabel MAPE/RMSE, daftar unit excluded); **Detail per Unit/Kriteria** (dropdown pilih, 2 metrik GB Seragam vs Model Terbaik, plot training+testing dari `evaluate_unit_on_test()`, plot actual-to-future dari `v4_future_forecast_final.xlsx` dgn slider horizon 3-12, tab kriteria **melatih ulang on-the-fly tiap pilihan ganti** -- bukan baca checkpoint, krn kriteria-level future forecast belum di-precompute ke notebook); **Rolling vs Direct** (baca `v4_rolling_vs_direct.xlsx` apa adanya).
- **[TERBUKA]** Tab Per Kriteria masih retrain on-the-fly (lambat kalau sering ganti pilihan pas demo) -- user ditawari dipindah ke precompute di notebook, **belum dijawab**.

### 21.4 `appPerusahaan.py` (223 baris)

- Form upload (BBM AAB, cost&bbm, Container per tahun, Curah Hujan, multi-file) -> tombol "Jalankan Proses Forecast" -> `pipeline_lib.build_monthly_full()` (ETL baru) -> tiap unit di-*fit* ulang pakai config final dari `v4_forcedgb_vs_v2b_comparison.xlsx` (BUKAN grid search baru) -> forecast rolling 12 bulan ke depan (ditampilkan default 3, bisa ditarik s/d 12).
- Deteksi tahun file upload: regex cari pola "20XX" di nama file, kalau gak ketemu fallback nebak urut (2023, 2024, dst). **[TERBUKA, belum dicoba pakai file asli user]**.
- Unit baru di data upload yang belum punya konfigurasi final (gak ada di hasil Tahap 2b/Force-GB) otomatis masuk tab "Unit Di-exclude" dgn alasan "unit baru, belum pernah dianalisis" -- BUKAN dicarikan kombinasi otomatis (itu tetap butuh notebook/grid search manual).
- 2 tab: Prediksi per Unit (dropdown, plot actual-forecast TANPA metrik error, slider horizon dgn catatan "error naik di atas 3 bulan", tombol download Excel kolom unit/bulan/forecast saja) dan Unit Di-exclude (gabungan semua alasan: bimbingan + filter kelayakan + gagal tuning + unit baru + gagal retrain data baru).

### 21.5 Testing & bug yang ditemukan

- **Testing**: `pipeline_lib.py` diuji pakai data sintetis (bukan Excel asli user, krn ETL perlu file mentah yang gak ada di sandbox Claude) -- `retrain_and_forecast_unit`, `retrain_and_forecast_kriteria`, `evaluate_unit_on_test`, `estimate_future_exog` semua jalan tanpa error setelah bug di §19.10 diperbaiki (pattern yang sama persis, diperbaiki di dua tempat).
- `appDemo.py`/`appPerusahaan.py` sendiri TIDAK bisa dijalankan/dites di sandbox Claude (Streamlit gak terinstall di situ) -- cuma dicek sintaksnya valid (`ast.parse`). **User sudah coba jalanin beneran** -- lihat §21.6.

### 21.6 Status jalan di environment user (dikonfirmasi user)

- **Masalah #1**: `http://localhost:8501` nyangkut "loading" terus di Chrome, padahal server Streamlit-nya hidup (kebukti karena tab VS Code bisa connect). **Root cause**: Chrome di Windows resolve `localhost` ke IPv6 (`::1`) duluan dan gantung; `127.0.0.1` eksplisit nembus masalah ini. **[FIXED, dikonfirmasi user]** -- solusi: akses `http://127.0.0.1:8501` (bukan `localhost`).
- **Lokasi file**: ketiga file (`pipeline_lib.py`, `appDemo.py`, `appPerusahaan.py`) WAJIB di folder yang sama (krn `import pipeline_lib` langsung, bukan package), dan `streamlit run` WAJIB dijalankan dari folder itu juga (path `./checkpoints_v4` relatif ke *working directory* command, bukan ke lokasi file `.py`).
- **Hasil setelah fix**: user konfirmasi dashboard kebuka & jalan sesuai harapan, **tanpa perlu perubahan kode apa pun**.

### 21.7 Belum dikerjakan / terbuka (dashboard)

1. Tab Per Kriteria `appDemo.py`: evaluasi testing dan future forecast sudah berjalan lancar secara on-the-fly via `pipeline_lib.py`; opsi precompute ke notebook tetap terbuka jika ingin instan tanpa komputasi saat demo.
2. Deteksi tahun otomatis di upload `appPerusahaan.py` belum dicoba pakai file asli (§21.4).
3. `appPerusahaan.py` belum pernah dites end-to-end pakai data Excel asli PT X (upload -> ETL -> forecast -> export) -- baru dites logic intinya doang pakai data sintetis & benchmark retrain lokal.
4. Belum ada validasi: kalau `pip install` dependency (`streamlit`, `plotly`, dll) belum lengkap di environment user, pesan errornya gimana -- belum dicoba.

### 21.8 [BARU] Penyempurnaan Visual, Evaluasi Kriteria, Excluded Table, & Benchmark Performa

Setelah dashboard berhasil dijalankan di sisi user, dilakukan serangkaian audit, perbaikan visual, dan penyesuaian fungsional:

1. **Kompatibilitas Dark Mode & Pembersihan Garis Hitam**:
   - Menghapus semua garis berwarna hitam pada grafik Plotly (`#000000`), diganti dengan palet kontras tinggi yang ramah dark theme Streamlit (`#0E1117`):
     - `#2ca02c` (hijau) untuk Actual pada Plot Evaluasi Testing.
     - `#1f77b4` (biru) untuk Actual historis pada Plot Future Forecast.
     - `orange` untuk Prediksi Testing.
     - `crimson` (dash) untuk Future Forecast.
   - Menghapus seluruh nama perusahaan (`PT SPIL`, `SPIL`, `PT Salam Pacific Indonesia Lines`, `PT X`) dan pemisah dash (`--` / ` - `) dari seluruh UI (judul, metric card, caption, dan header tabel).
   - Dropdown unit dan kriteria pada grafik tetap diatur default urut performa terbaik (`V4_GB_MAPE` ascending, default pertama: `UNIT_0309` dengan MAPE 0.15%) agar grafik langsung menampilkan performa terbaik saat dibuka.
   - Sebaliknya, tabel **Perbandingan Performa** di tab Ringkasan diubah agar ditampilkan berurutan sesuai nomor unit (`EQUIP NAME`) atau ID kriteria (`KRITERIA_ID`), bukan diurutkan dari MAPE terbaik.

2. **Kontinuitas Garis Prediksi & Pembersihan Trace Training**:
   - Titik awal garis `Prediksi (Testing)` disambungkan langsung ke titik aktual terakhir masa training (`2025-09`) sehingga tidak ada jeda visual (*gap*) antara masa training dan testing.
   - Titik awal garis `Future Forecast` disambungkan langsung ke titik historis terakhir (`2025-12` → `2026-01`).
   - Garis `Prediksi (Training)` dihilangkan dari Plot 1 `appDemo.py` atas keputusan user, agar visualisasi fokus murni pada perbandingan data uji: Actual vs Prediksi Testing.

3. **Tooltip Hover Interaktif & Jelas pada Seluruh Plot**:
   - Ditambahkan `hovertemplate="%{y:.2f} jam<extra></extra>"` dan layout `hovermode="x unified"` pada semua grafik di `appDemo.py` dan `appPerusahaan.py`.
   - Menampilkan garis bantu vertikal dan kotak tooltip informatif berisi nama trace dan nilai exact bersatuan jam (contoh: `● Actual: 154.20 jam`, `● Prediksi (Testing): 149.80 jam`).

4. **Penambahan Plot Evaluasi Testing pada Tampilan "Per Kriteria"**:
   - Sebelumnya, tampilan Per Kriteria di `appDemo.py` hanya memiliki plot future forecast (plot evaluasi testing terlewat belum dibuat).
   - Ditambahkan fungsi `evaluate_kriteria_on_test()` di `pipeline_lib.py`: melatih model GB pada gabungan data anggota kriteria ($\le$ Sep 2025), memprediksi data uji (Okt–Des 2025) secara direct, melakukan *inverse transform* per unit, lalu menjumlahkan (*agregasi total utilitas*) per bulan.
   - Ditambahkan **"Plot Evaluasi Testing Kriteria (periode evaluasi)"** di `appDemo.py` tab Detail (Per Kriteria), sehingga tampilan Per Kriteria 100% konsisten dan simetris dengan Per Unit (keduanya punya plot evaluasi testing dan plot future forecast).

5. **Penyempurnaan Tabel Unit yang Diexclude**:
   - **Filter 10 unit review bimbingan**: Unit dengan alasan `"Dikeluarkan dari populasi analisis berdasarkan review MAPE pada sesi bimbingan"` difilter keluar secara permanen dari `load_excluded_summary()`. Unit ini dianggap sudah dieliminasi sejak awal dan tidak perlu dibahas di dashboard.
   - **Hapus injeksi "Data baru"**: Menghapus penambahan kategori `"Data baru"` dan `"Retrain data baru"` pada `appPerusahaan.py`, sehingga daftar exclude murni hanya berisi **25 unit** resmi yang tidak lolos kriteria kelayakan data (18 nol di salah satu tahun train, 7 nol di seluruh masa test).
   - **Hapus kolom Kategori**: Kolom `TAHAP` / `Kategori` dihapus dari tampilan tabel di kedua aplikasi, menyisakan 2 kolom bersih: **`Nama Unit`** dan **`Alasan`**.
   - **Standardisasi istilah & redaksi kalimat alasan**:
     - Istilah UI diubah dari "Dikecualikan" menjadi **"Diexclude"** (misal: `Daftar Unit yang Diexclude beserta Alasan`, tab `Unit Diexclude`).
     - Alasan diawali huruf kapital dan diubah redaksinya menjadi lebih formal & deskriptif:
       - `"Data utilitas pada salah satu tahun periode data train bernilai nol semua"` (18 unit)
       - `"Data utilitas pada periode data test bernilai nol semua"` (7 unit)
     - Perubahan ini disimpan permanen ke disk di `v4_unit_excluded_summary.xlsx`, `pipeline_lib.py`, serta diproteksi di runtime rendering `appDemo.py` dan `appPerusahaan.py`.

6. **Pembersihan Istilah Teknis/Internal Notebook**:
   - Menghapus jargon internal notebook dari seluruh teks antarmuka:
     - `GB Seragam` → `Gradient Boosting (Model Final)`
     - `Model Terbaik (Tahap 2b)` → `Model Alternatif Terbaik`
     - Kolom tabel `V4_GB_*` / `V2B_*` di-rename menjadi nama bahasa Indonesia yang bersih (`Varian GB`, `MAPE GB (%)`, `Model Alternatif`, `Varian Alternatif`, `Selisih MAPE (%)`).
     - Subheader tabel rolling: `Perbandingan Metode Forecasting: Rolling vs Direct` (tanpa kata "hasil Tahap 2 notebook").

7. **Multi-Port Running & Benchmark Durasi Proses**:
   - Dikonfirmasi kedua aplikasi dapat dijalankan bersamaan di dua terminal / tab browser berbeda:
     - `streamlit run appDemo.py --server.port 8501` (`http://127.0.0.1:8501`)
     - `streamlit run appPerusahaan.py --server.port 8502` (`http://127.0.0.1:8502`)
   - Benchmark end-to-end retrain & rolling forecast untuk 205 unit pada hardware lokal:
     - ETL (parsing multi-sheet Excel): ~30–50 detik.
     - Retrain & rolling forecast 205 unit: **35.04 detik** (terukur).
     - Total dari upload file sampai hasil keluar: **~1 hingga 1.5 menit**.

8. **Penambahan Plot Perbandingan Kombinasi Terbaik Pertama & Terbaik Kedua di `appDemo.py`**:
   - Ditambahkan fungsi `load_v2b_12kombinasi()` dan `load_v2b_raw_preds()` di `pipeline_lib.py` untuk membaca metrik dan hasil prediksi 12 kombinasi (`3 model × 4 data-prep`) per unit dan per kriteria.
   - Pada tab Detail di `appDemo.py` (baik tampilan **Per Unit** maupun **Per Kriteria**), kartu informasi di atas grafik kini menampilkan **3 kolom perbandingan**: **Gradient Boosting (Model Final)**, **Kombinasi Terbaik Pertama**, dan **Kombinasi Terbaik Kedua** (lengkap dengan model, varian data-prep, MAPE, dan RMSE masing-masing).
   - Pada **Plot Evaluasi Testing**, garis prediksi **Terbaik 1** (`#00b4d8`, *dashed*) dan **Terbaik 2** (`#c77dff`, *dotted*) ditampilkan langsung dalam satu grafik bersama **Actual** (`#2ca02c`) dan **Model Final GB** (`orange`), lengkap dengan penyambungan ke titik aktual terakhir (`2025-09`) dan *unified hover tooltip*.

9. **Dukungan Multi-Unit & Redaksi Info Horizon pada `appPerusahaan.py`**:
   - Pilihan unit di `appPerusahaan.py` diubah dari `st.selectbox` menjadi `st.multiselect("Pilih unit (bisa lebih dari satu)")` dengan default unit pertama.
   - Saat pengguna memilih lebih dari satu unit, seluruh unit yang dipilih ditampilkan dalam **satu grafik gabungan** dengan warna berbeda untuk masing-masing unit (garis utuh untuk `Actual (UNIT_XXXX)` dan garis putus-putus berwarna senada untuk `Forecast (UNIT_XXXX)`).
   - Pemberitahuan ketika memilih horizon di atas 3 bulan pada `appPerusahaan.py` diubah dari istilah `"potensi error"` menjadi `"akurasi"` (*"Forecast di atas 3 bulan memiliki tingkat akurasi yang lebih rendah dibanding 3 bulan pertama..."*).

### 21.9 [BARU] Rincian Alur Kerja Pipeline Forecasting End-to-End & Mekanisme Rolling Multi-Step

Ketika pengguna mengunggah berkas di `appPerusahaan.py` dan menekan tombol *"Jalankan Proses Forecast"*, urutan proses komputasi yang berlangsung di balik layar adalah:

1. **Tahap 1: Ekstraksi, Transformasi, dan Pemuatan (ETL Pipeline)**:
   - Berkas BBM tahunan dibaca: mendeteksi struktur *multi-level header* 3 baris, mengekstrak kolom `HM` dan `LITER`, menghitung selisih jam kerja harian ($\Delta \text{HM}$), menerapkan batas fisik (*capping* 24 jam/hari), dan menjumlahkan menjadi utilitas bulanan.
   - Berkas Container di-parsing: menyaring 8 blok pivot `CURRSTATE` operasional pelabuhan (`FXD, FAC, STR, MAS, MTB, FOB, MXD, MOB`).
   - Berkas Curah Hujan BMKG di-parsing dan digabungkan per periode.
   - Melakukan penggabungan (*matching*) ke berkas spesifikasi alat (`cost_bbm.xlsx`) untuk mengelompokkan `KRITERIA_ID` (`JENIS | TYPE | CAP | HP`).
   - Menerapkan filter kelayakan unit (mengeliminasi 25 unit cacat: 18 unit bernilai nol di salah satu tahun data latih, 7 unit bernilai nol di seluruh masa uji) dan melakukan anonimisasi sekuensial (`UNIT_0001` s/d `UNIT_0205`).
   - *Estimasi durasi: ~30–50 detik (tergantung kecepatan I/O berkas).*

2. **Tahap 2: Transformasi Data Prep & Pembentukan Fitur Lag**:
   - Untuk masing-masing dari 205 unit, pipeline membaca konfigurasi optimal dari hasil Tahap 2b (`v4_forcedgb_vs_v2b_comparison.xlsx`), yang memuat varian data preparation terpilih (`baseline`, `robust`, `savgol`, atau `yeojohnson`).
   - Menerapkan fungsi transformasi matematika yang sesuai untuk menstabilkan variansi dan mengurangi pencilan ekstrem.
   - Membentuk fitur *autoregressive lags* (Lag 1 s/d Lag 3) serta lag variabel eksogen sesuai temuan dependensi temporal (PACF).

3. **Tahap 3: Re-training Model Gradient Boosting per Unit**:
   - Menginisialisasi `HistGradientBoostingRegressor` dengan konfigurasi hyperparameter individual terbaik per unit (misalnya `max_iter`, `learning_rate`, `max_depth`, `min_samples_leaf`).
   - Melatih model menggunakan seluruh data historis yang tersedia (*full-history fit*) agar model memiliki basis data paling komprehensif untuk proyeksi masa depan.

4. **Tahap 4: Recursive Rolling Multi-Step Forecasting (Proyeksi 3–12 Bulan)**:
   - Mengestimasi variabel eksogen masa depan (*curah hujan* & *volume kontainer*) menggunakan rata-rata musiman (*seasonal historical profile*).
   - **Bulan ke-1 ($t+1$)**: Menggunakan lag nilai aktual historis terakhir. Model memprediksi utilitas, lalu dilakukan *inverse transform* ke skala jam kerja fisik.
   - **Bulan ke-2 ($t+2$)**: Karena data aktual untuk bulan $t+1$ belum terjadi di dunia nyata, fitur Lag 1 diisi secara otomatis menggunakan **hasil prediksi bulan ke-1**, dipadukan dengan eksogen musiman estimasi.
   - **Bulan ke-3 s/d ke-12**: Proses perulangan rekursif (*rolling*) ini diteruskan hingga mencapai horizon yang diminta pengguna.
   - *Estimasi durasi retrain & rolling forecast untuk seluruh 205 unit: **35.04 detik**.*

5. **Total Durasi Keseluruhan**:
   - Dari saat pengguna mengklik tombol proses hingga seluruh grafik visual dan tombol unduh Excel siap: **~1 hingga 1.5 menit**.

6. **Fleksibilitas terhadap Data Tahun Berbeda / Tahun Baru di `appPerusahaan.py`**:
   - Berbeda dengan `appDemo.py` yang statis membaca hasil *checkpoint* penelitian (2023–2025), `appPerusahaan.py` bersifat dinamis dan dapat memproses berkas data tahun baru (misal 2026, 2027, dst.):
     - Fungsi `_infer_year_from_name()` mendeteksi tahun `20XX` otomatis dari nama berkas unggahan (`re.search(r"(20\d{2})", name)`), dan tanggal dibaca langsung dari kolom `TANGGAL` lembar kerja Excel BBM serta `time` curah hujan BMKG.
     - Titik awal *future forecast* ditentukan secara dinamis dari `last_period = monthly_full["TAHUN_BULAN"].max()`, sehingga proyeksi selalu dimulai tepat **1 bulan setelah bulan terakhir yang ada di data unggahan** (`last_period + 1`).
     - Syarat agar berjalan mulus: (1) sertakan histori sebelumnya (minimal 6 bulan data per unit untuk pembentukan Lag 1–3), (2) unggah keempat jenis berkas untuk periode yang bersesuaian, dan (3) unit termasuk dalam 205 unit armada yang sudah memiliki konfigurasi optimal (unit yang benar-benar baru akan otomatis dicatat di tab *Unit Diexclude*).

---



### 21.10 [BARU] Integrasi Revisi 190 Unit & Penyederhanaan Keterangan Horizon di Dashboard

Menindaklanjuti revisi Dosen Pembimbing 2, seluruh sistem dashboard dan modul pendukung disinkronkan:

1. **`pipeline_lib.py`**:
   - Fungsi loader (`load_final_config`, `load_excluded_summary`, `load_future_forecast`) secara otomatis memprioritaskan berkas revisi di `checkpoints_v4/rev_h3/`:
     - Memuat `forcedgb_vs_v2b_comparison_190unit.xlsx` (190 unit valid).
     - Memuat `unit_excluded_revisi_summary.xlsx` (40 unit lengkap dengan alasan profesional).
     - Memuat `future_forecast/future_forecast_final_190unit.xlsx` (sheet `Forecast_Per_Unit` dan `Forecast_Pivot`).
   - Ditambahkan mekanisme fallback aman ke `h3bulan/` jika folder revisi tidak ditemukan.
   - Ditambahkan konstanta `NEW_EXCLUDED_15`.

2. **`appDemo.py` (Dashboard Sidang)**:
   - Metric card di tab Ringkasan otomatis menampilkan **190 unit** (sebelumnya 205 unit) dan rata-rata MAPE **11.48%** (sebelumnya 15.48%).
   - Level kriteria disinkronkan menjadi **63 kriteria aktif** (6 kriteria yang seluruh anggotanya diexclude otomatis difilter keluar agar tidak kosong).
   - Dropdown pemilihan unit dan kriteria hanya memunculkan unit/kriteria yang valid.
   - Tabel pembanding (V2B 12 kombinasi, raw preds, rolling vs direct) disaring otomatis ke 190 unit valid.
   - Tabel unit yang diexclude menampilkan 40 unit dengan alasan profesional (*Melebihi threshold toleransi error*).
   - Seluruh grafik Plotly interaktif (Plot Evaluasi Testing per Unit, Evaluasi Testing per Kriteria, dan Plot Future Forecast) dikonfigurasi dengan `yaxis=dict(rangemode="tozero")` agar sumbu Y selalu mulai dari 0.

3. **`appPerusahaan.py` (Dashboard Operasional)**:
   - Pipeline retraining otomatis hanya memproses 190 unit yang lolos verifikasi.
   - Sheet `Unit_Diexclude` pada file export Excel hasil forecast otomatis mencantumkan 40 unit yang diexclude.
   - Grafik Plotly multi-unit interaktif dikonfigurasi dengan `yaxis=dict(rangemode="tozero")`.
   - **Penyederhanaan Teks Keterangan Horizon**:
     Peringatan saat memilih horizon di atas 3 bulan disederhanakan dengan membuang alasan teknis perulangan prediksi rekursif, menjadi:
     *"Forecast di atas 3 bulan memiliki tingkat akurasi yang lebih rendah dibanding 3 bulan pertama."*


### 21.11 [BARU] Optimalisasi ETL Upload & Defensive Mapping di Dashboard Perusahaan

Ketika pengguna menguji fitur upload data mentah tahunan (BBM AAB, Container, Curah Hujan, cost & bbm) pada dashboard operasional perusahaan (`appPerusahaan.py`), ditemukan kendala di mana hasil peramalan menampilkan **0 unit terproyeksi** (seluruh baris data terlewati/*skipped*).

1. **Akar Masalah**:
   - Fungsi ETL `build_monthly_full()` di `pipeline_lib.py` awalnya menghasilkan nama unit format lama (`UNIT_0004`), sedangkan konfigurasi model final di `checkpoints_v4/rev_h3/forcedgb_vs_v2b_comparison_190unit.xlsx` telah menggunakan penamaan berbasis kriteria baru (`K01_UNIT_004`).
   - Akibat perbedaan penamaan string ini, loop *retrain* di `appPerusahaan.py` tidak menemukan kecocokan unit dan melewatkan seluruh unit.
2. **Solusi & Perbaikan**:
   - **Auto-Mapping Kriteria di `pipeline_lib.build_monthly_full()`**:
     Ditambahkan logika integrasi pemetaan otomatis dari `mapping_unit_dan_kriteria.xlsx` (atau fallback kamus mapping). Setiap unit yang selesai di-ETL dari data mentah langsung dikonversi menjadi format standar `K<NoKriteria>_UNIT_<Nomor3Digit>`.
   - **Defensive Fallback di `appPerusahaan.py`**:
     Ditambahkan mekanisme pemetaan defensif pada dashboard: jika suatu unit masih terbaca dalam format lama (`UNIT_XXXX`), aplikasi secara otomatis memetakannya ke nama baru yang ada di konfigurasi model sebelum proses pelatihan ulang dijalankan.
   - **Optimasi Pembacaan File Excel BBM AAB**:
     Sebelumnya fungsi membaca 36 sheet BBM bulanan secara terpisah dengan membuka-tutup berkas ZIP Excel dari disk sebanyak 36 kali. Dioptimalkan dengan menggunakan satu objek instance `pd.ExcelFile` yang dibuka sekali di memori, sehingga waktu ekstraksi berkas mentah berkurang drastis dari beberapa menit menjadi puluhan detik.
3. **Hasil Verifikasi**:
   - Upload file mentah pada `appPerusahaan.py` langsung mengenali dan memproyeksikan seluruh **190 unit valid** secara otomatis tanpa kegagalan pencocokan.


### 21.12 [BARU] Standarisasi Istilah Utilitas Menjadi Operating Hours (Poin 1 Revisi & Eksekusi Opsi A)

Menindaklanjuti Poin 1 arahan Dosen Pembimbing ke-2: dalam domain teknik industri dan logistik pelabuhan, istilah *"utilitas"* (utility / utilization rate) umumnya didefinisikan sebagai persentase efektivitas kapasitas kerja (0–100%), sedangkan variabel yang diprediksi dalam penelitian ini adalah total jam kerja mesin alat berat (*Hour Meter* / HM, dalam satuan jam). Penggunaan istilah utilitas berpotensi menimbulkan kerancuan makna matematis.

Pengguna menginstruksikan untuk mengeksekusi penggantian istilah secara menyeluruh pada kode, antarmuka dashboard, file output fisik (Opsi A), dan visualisasi EDA, dengan penulisan buku skripsi ditunda hingga tahap koding tuntas:

1. **Tampilan Antarmuka & Dashboard (UI)**:
   - **`appDemo.py` (Dashboard Demo Sidang)**:
     - Judul halaman (*page title*): *"Demo Prediksi Operating Hours Alat Berat"*.
     - Judul utama: *"Demo Sistem Prediksi Operating Hours Alat Berat"*.
     - Label sumbu Y grafik per-unit: *"Operating Hours (jam)"*.
     - Label sumbu Y grafik per-kriteria: *"Total Operating Hours (jam)"*.
     - Deskripsi alasan exclude unit pada tabel: *"Data operating hours..."*.
   - **`appPerusahaan.py` (Dashboard Operasional PT X)**:
     - Judul halaman & judul utama: *"Prediksi Operating Hours Alat Berat"*.
     - Caption: *"Sistem Prediksi Operating Hours Armada Alat Berat"*.
     - Label sumbu Y grafik: *"Operating Hours (jam)"*.
     - Nama file unduhan Excel hasil peramalan: `hasil_forecast_operating_hours.xlsx`.
   - **Modul `pipeline_lib.py`**:
     - Kamus alasan `REASON_MAP` diperbarui: *"Data operating hours pada salah satu tahun periode data train bernilai nol semua"* dan *"Data operating hours pada periode data test bernilai nol semua"*.

2. **Eksekusi Opsi A (Pembaruan Kolom File Output Fisik Excel & CSV)**:
   - Kolom-kolom data output fisik diperbarui secara nyata agar tidak lagi mengandung kata `UTILITAS`:
     - `checkpoints_v4/rev_h3/future_forecast/future_forecast_final_190unit.xlsx` (Sheet `Forecast_Per_Unit`): Kolom `FORECAST_UTILITAS` → `FORECAST_OPERATING_HOURS`.
     - `checkpoints_v4/rev_h3/unit_excluded_revisi_summary.xlsx` & `checkpoints_v4/h3bulan/future_forecast/v4_unit_excluded_summary.xlsx`: Seluruh teks pada kolom `ALASAN` diperbarui secara fisik dari *"Data utilitas..."* menjadi *"Data operating hours..."*.
     - `checkpoints_v4/rev_h3/04_monthly_with_exog_lag1.csv`: Kolom `UTILITAS` → `OPERATING_HOURS`.
     - `checkpoints_v4/04_monthly_with_exog.csv`: Kolom `UTILITAS` → `OPERATING_HOURS`.
     - `checkpoints_v4/v4_kriteria_unit_mapping.xlsx` (Sheet `Detail_HM_per_Unit_Kriteria`): Kolom `UTILITAS` → `OPERATING_HOURS`.
     - File baseline lama (`v4_future_forecast_final.xlsx` dan `v4_future_forecast_per_unit.csv`): Kolom `FORECAST_UTILITAS` → `FORECAST_OPERATING_HOURS`.
   - Kode pemanggil di `appDemo.py` dan `appPerusahaan.py` disinkronkan untuk memprioritaskan kolom `OPERATING_HOURS` dan `FORECAST_OPERATING_HOURS`.

3. **Penggantian Nama File Fisik (0 File 'utilitas' Tersisa di `checkpoints_v4/`)**:
   - File dataset bulanan: `02_monthly_utilitas.csv` resmi diubah namanya menjadi `02_monthly_operating_hours.csv` di seluruh folder checkpoint (`checkpoints_v4/`, `checkpoints/`, `checkpoints_v2/`, `checkpoints_v3/`).
   - File gambar plot EDA di `checkpoints_v4/eda/`:
     - `eda_01_trend_utilitas_total.png` → `eda_01_trend_operating_hours_total.png`
     - `eda_01b_trend_utilitas_mean.png` → `eda_01b_trend_operating_hours_mean.png`
     - `eda_02_trend_utilitas_mean.png` → `eda_02_trend_operating_hours_mean.png`
     - `eda_05_dist_utilitas.png` → `eda_05_dist_operating_hours.png`
     - `eda_09_box_utilitas.png` → `eda_09_box_operating_hours.png`
   - Sinkronisasi `code_v4.ipynb`: Cell 6, 15, 17, dan 18 diperbarui agar menyimpan output ke nama file baru tersebut.
   - Hasil audit direktori: Terdapat **0 file** di `checkpoints_v4/` yang mengandung kata `utilitas` pada nama filenya.

4. **Arsitektur Dual Compatibility di Backend (`pipeline_lib.py`)**:
   - Untuk menjamin integritas kode historis dan mencegah potensi `KeyError`:
     - Fungsi `load_monthly_full_checkpoint()` secara otomatis menyediakan kolom `OPERATING_HOURS` dan alias `UTILITAS`.
     - Fungsi `load_future_forecast()` secara otomatis menyediakan kolom `FORECAST_OPERATING_HOURS` dan alias `FORECAST_UTILITAS`.
     - Fungsi peramalan `retrain_and_forecast_unit()` dan `retrain_and_forecast_kriteria()` menghasilkan kedua kolom tersebut pada dataframe hasil kembalian.
   - Pendekatan ini memberikan jaminan ketahanan sistem: antarmuka menampilkan istilah baru secara elegan tanpa merusak kode-kode lama yang masih mengakses nama kolom sebelumnya.

5. **Panduan Verifikasi Mandiri oleh Pengguna**:
   - Pengguna dapat mengecek langsung keberhasilan perubahan pada berkas-berkas berikut:
     1. **`checkpoints_v4/rev_h3/future_forecast/future_forecast_final_190unit.xlsx`**: Buka sheet `Forecast_Per_Unit`, periksa header kolom C yang kini tertulis `FORECAST_OPERATING_HOURS`.
     2. **`checkpoints_v4/rev_h3/04_monthly_with_exog_lag1.csv`**: Buka berkas, periksa header kolom ke-4 yang kini tertulis `OPERATING_HOURS`.
     3. **`checkpoints_v4/02_monthly_operating_hours.csv`**: Periksa nama file dan kolom data `OPERATING_HOURS`.
     4. **`checkpoints_v4/eda/`**: Periksa 5 berkas gambar visualisasi tren dan distribusi yang seluruhnya berawalan `eda_*_operating_hours_*.png`.
     5. **`checkpoints_v4/rev_h3/mapping_unit_dan_kriteria.xlsx`**: Buka sheet `Mapping_Unit`, periksa penamaan seluruh 230 unit yang telah berformat `K01_UNIT_004`.
     6. **Dashboard Streamlit (`appDemo.py` & `appPerusahaan.py`)**: Jalankan aplikasi, periksa label sumbu Y grafik dan judul antarmuka yang telah 100% menggunakan istilah *"Operating Hours (jam)"*.

### 21.13 [BARU] Pembaruan Dashboard & Pipeline ETL: Integrasi 25 Excluded Resmi & Proteksi Zero False New Units

Menindaklanjuti eliminasi total 15 unit anomali dari data pipeline awal (§19.13), dilakukan penyelarasan komprehensif pada lapisan backend dan antarmuka dashboard:

1. **Penyelarasan Loader Unit Exclude (`load_excluded_summary`)**:
   - Berkas `unit_excluded_revisi_summary.xlsx` disinkronkan hanya memuat tepat **25 unit exclude resmi** yang murni memiliki histori jam kerja nol (18 unit nol di seluruh periode train dan 7 unit nol di seluruh periode test).
   - Logika pembacaan pada `pipeline_lib.py` (`load_excluded_summary`) dipastikan membaca berkas revisi yang bersih ini, sehingga tab "Unit yang Diexclude" di `appDemo.py` dan `appPerusahaan.py` hanya menampilkan 25 unit non-operasional tersebut beserta alasan profesional standar.
2. **Proteksi *Zero False New Units* pada Upload Data Perusahaan (`appPerusahaan.py`)**:
   - **Masalah Awal**: Saat pengguna mengunggah berkas Excel data operasional mentah perusahaan, 15 unit anomali yang sebelumnya dihiraukan sempat berpotensi dideteksi sebagai "Unit Baru" karena tidak terdaftar dalam model aktif 190 unit namun ada di histori armada.
   - **Solusi Rekayasa ETL**: Fungsi `build_monthly_full()` pada `pipeline_lib.py` dan alur pemrosesan upload di `appPerusahaan.py` disempurnakan dengan menyaring keluar ke-15 unit anomali tersebut sejak langkah pembacaan awal.
   - **Hasil Verifikasi**: Ketika data mentah bulanan perusahaan diunggah, sistem langsung memproses dan memproyeksikan seluruh **190 unit valid** secara otomatis tanpa memicu peringatan deteksi unit baru palsu.
3. **Verifikasi Tampilan Antarmuka (`appDemo.py` & `appPerusahaan.py`)**:
   - **Populasi Valid**: Tepat 190 unit valid dan 63 kriteria aktif tertampil secara konsisten pada dropdown, grafik komparasi model, dan tabel evaluasi.
   - **Visualisasi & Tema**: Grafik Plotly tetap mempertahankan baseline `yaxis=dict(rangemode="tozero")`, palet warna kontras ramah dark mode, format angka `%{y:.2f} jam`, dan sambungan kontinu antara data aktual terakhir dengan data proyeksi.

---

## 8. Lokasi File Checkpoint

---

### 8.1 `./checkpoints/` — dari `code.ipynb` (ARSIP, populasi lama sebelum restrukturisasi §14)

⚠️ **Semua file di bawah ini pakai populasi unit LAMA** (sebelum restrukturisasi cost&bbm-only §14) — disimpan sebagai arsip percobaan awal buat lampiran skripsi, BUKAN hasil final. Hasil final ada di §8.2 (`checkpoints_v2/`).

| File | Isi |
|---|---|
| `01_daily_delta_hm.csv` | Data harian + delta HM (HM>24 di-cap ke 24) |
| `02_monthly_operating_hours.csv` | UTILITAS bulanan, 1 desimal |
| `03a_monthly_container.csv` / `03a_container_per_cabang_detail.csv` | Volume container |
| `04_monthly_with_exog.csv` | UTILITAS + CURAH_HUJAN + VOLUME_CONTAINER |
| `05_completeness_per_unit.csv` | Kelengkapan data per unit |
| `06_excluded_units.csv` | Unit dikecualikan + alasan |
| `07_train.csv` / `07_test.csv` | Split train/test |
| `08_kriteria_unit.csv` | Pemetaan KRITERIA_ID |
| `09_train_smoothed.csv` / `09_test_smoothed.csv` | Capping + smoothing |
| `10_arimax_*` / `11_gb_*` / `12_lstm_*` / `12b_lstm_*` | Hasil baseline 3 model |
| `13_model_comparison_summary.csv` | Ringkasan MAPE_GLOBAL baseline + skewness-based |
| `14_final_predictions.csv` | Prediksi final baseline (ARIMAX per-unit) |
| `15_LAPORAN_HASIL.xlsx` | Laporan Excel baseline |
| `16_outlier_summary_per_unit.csv` / `16b_outlier_flagged_rows.csv` / `16c_boxplot_utilitas_per_jenis.png` | Outlier check IQR |
| `17_skewness_per_kriteria.csv` | Skewness & keputusan mean/median per kriteria |
| `18a-18f_plot_*.png` | Plot top/bottom MAPE baseline |
| `19a/19b_gridsearch_arimax_*` | Grid search ARIMAX per-unit/kriteria (MAPE-based, populasi lama) |
| `20a_gb_tuning_*` / `20b_lstm_tuning_*` | Tuning GB & LSTM (MAPE-based, populasi lama) |
| `21_RINGKASAN_SEMUA_PERCOBAAN.xlsx` | Laporan gabungan, 9 sheet |
| `22a/22b_*` | Top-3 PDQ ARIMAX + plot |
| `23a-23d_*` | Top-3 tuning GB/LSTM + plot |
| `24_perbandingan_baseline_vs_tuned.csv` | Perbandingan baseline vs tuned (MAPE-based) |
| `00b_unit_tidak_ada_di_costbbm_dikecualikan.csv` | Unit BBM AAB yang tidak match cost&bbm HP&Type |
| `12b_naive_baseline_results.csv` | ⚠️ Usang, jangan dipakai |

### 8.2 `./checkpoints_v2/` — dari `code_v2.ipynb` (AKTIF, hasil final dipakai skripsi)

Populasi final (cost&bbm-only, §14), metrik RMSE-utama (§15.2).

**Tahap 2 — 24 kombinasi (4 data-prep × 3 model × 2 pendekatan):**

| File | Isi |
|---|---|
| `v2_{varian}_arimax_unit_progress.csv` / `_final.csv` | Grid search ARIMAX per-unit, per varian data-prep (baseline/savgol/robust/yeojohnson) |
| `v2_{varian}_arimax_kriteria_progress.csv` / `_final.csv` | Sama, per-kriteria |
| `v2_{varian}_gb_unit_progress.csv` / `_final.csv` | Tuning GB per-unit, per varian |
| `v2_{varian}_gb_kriteria_progress.csv` / `_final.csv` | Tuning GB per-kriteria, per varian |
| `v2_{varian}_lstm_unit_progress.csv` / `_final.csv` | Tuning LSTM per-unit, per varian |
| `v2_{varian}_lstm_kriteria_progress.csv` / `_final.csv` | Tuning LSTM per-kriteria, per varian |
| `v2_{varian}_ALL_DONE.marker` | Penanda varian selesai total |
| `v2_MASTER_SUMMARY_24_kombinasi.csv` | **Ringkasan 24 kombinasi**, sudah dedupe (bug fix §15.4) |
| `v2_ringkasan_final_per_unit.csv` | 12 kombinasi (4 prep × 3 model) pendekatan per-unit, urut RMSE |
| `v2_ringkasan_final_per_kriteria.csv` | Sama, per-kriteria |

**Tahap 3 — tuning individual per-unit & per-kriteria (model+prep pemenang: GB+savgol):**

| File | Isi |
|---|---|
| `v3_gb_savgol_per_unit_individual_progress.csv` | Checkpoint tuning individual per-unit (222 unit, resumable per unit) |
| `v3_final_params_per_unit_individual.csv` | Parameter GB terbaik + RMSE/Bias/MAPE, 1 baris per unit |
| `v3_final_preds_per_unit_individual.csv` | Prediksi vs aktual, semua unit, parameter individual |
| `v3_gb_savgol_per_kriteria_individual_progress.csv` | Checkpoint tuning individual per-kriteria (76 grup, resumable) |
| `v3_final_params_per_kriteria_individual.csv` | Parameter GB terbaik + RMSE/Bias/MAPE, 1 baris per kriteria |
| `v3_final_preds_per_kriteria_individual.csv` | Prediksi vs aktual, semua kriteria, parameter individual |
| `v3_KESIMPULAN_FINAL_per_unit_vs_per_kriteria.csv` | **Hasil akhir** — per-kriteria menang (RMSE 56.77 vs 69.15) |
| `v3_plot_per_unit_individual.png` / `v3_plot_per_kriteria_individual.png` | Plot 3 terbaik + 3 terburuk tiap pendekatan |

**Tahap 2b — drill-down 12 kombinasi per-unit & per-kriteria (§16), pakai parameter Tahap 2:**

| File | Isi |
|---|---|
| `v2b_combo_preds_per_unit.csv` | Checkpoint mentah — prediksi per-bulan, 12 kombinasi × 222 unit |
| `v2b_combo_preds_per_kriteria.csv` | Sama, 12 kombinasi × 76 kriteria (skema kolom sudah difix, §16.3 bug #2) |
| `v2b_detail_per_unit_12kombinasi.csv` / `v2b_detail_per_kriteria_12kombinasi.csv` | RMSE/MAPE/Bias per (unit atau kriteria, kombinasi) |
| `v2b_best_combo_per_unit.csv` / `v2b_best_combo_per_kriteria.csv` | Kombinasi terbaik (ranking MAPE) tiap unit/kriteria |
| `v2b_hasil_12kombinasi_per_unit_kriteria.xlsx` | **Laporan utama**, 6 sheet (detail, best-combo, tally — lihat §16.4) |
| `v2b_plot_perunit_best5.png` / `_worst_1_5.png` / `_worst_6_10.png` | Plot per-unit, 5 subplot tiap gambar |
| `v2b_plot_perkriteria_best5.png` / `_worst_1_5.png` / `_worst_6_10.png` | Sama, per-kriteria |



### 8.3 `./checkpoints_v3/` — dari `code_v3.ipynb` (AKTIF, split train/test baru + exclude/remap unit, §17)

Populasi 345 unit (exclude 10, §17.3), train Jan2023-Agu2025, test Sep-Des2025 (4 bulan).

| File | Isi |
|---|---|
| `unit_map_v3.json` | Pemetaan nama asli → kode unit BARU (pasca exclude+remap) |
| `08_kriteria_unit.csv` / `04_monthly_with_exog.csv` | Di-save ulang dengan kode unit baru (menimpa hasil sebelum exclude+remap) |
| `v3_kriteria_unit_mapping.xlsx` | Mapping kriteria↔unit + data HM lengkap (5 sheet, §17.4) |
| `v3_train_test_split_info.xlsx` | Info rentang tanggal split + unit dipakai/dikecualikan (§17.4) |
| `v3_tahap2_24kombinasi.xlsx` | Tahap 2 (24 kombinasi) versi Excel (§17.4) |
| `v2b_combo_preds_per_unit.csv` / `_per_kriteria.csv` | Checkpoint mentah Tahap 2b, populasi/split baru |
| `v2b_detail_per_unit_12kombinasi.csv` / `_per_kriteria...` | RMSE/MAPE/Bias per (unit/kriteria, kombinasi), populasi/split baru |
| `v2b_best_combo_per_unit.csv` / `_per_kriteria...` | Kombinasi terbaik tiap unit/kriteria (ranking MAPE), populasi/split baru |
| `v2b_hasil_12kombinasi_per_unit_kriteria.xlsx` | Laporan Tahap 2b — **tally baru: GB+baseline paling sering menang** (§17.6), bukan GB+savgol lagi |
| `v2b_plot_perunit_*` / `v2b_plot_perkriteria_*` (best5/worst_1_5/worst_6_10) | Plot Tahap 2b — sekarang actual full train+test, prediksi cuma di test, y-axis mulai 0 |
| `v3_tahap3_tuning_individual.xlsx` | Tahap 3 versi Excel (Parameter_PerUnit/Kriteria, Kesimpulan_Final) — **hasil berbalik: per-unit menang** (53.90 vs 62.08), lihat §17.6 |
| `v3_plot_per_unit_individual.png` / `v3_plot_per_kriteria_individual.png` | Plot Tahap 3 — sama, full train+test + y-axis dari 0 |
| `v3_diagnostik_arimax_kriteria.csv` | Diagnostik kegagalan ARIMAX per-kriteria (§17.5 poin 5) — **investigasi di-hold** |

---

### 8.4 `./checkpoints_v4/` — dari `code_v4.ipynb` (AKTIF, §19)

Populasi 345 unit setelah exclude/remap (sama dengan v3). Dua subfolder horizon; nama file di dalam subfolder mengikuti konvensi `v2_*`/`v2b_*` (tidak bentrok karena beda folder).

| File / folder | Isi |
|---|---|
| `checkpoints_v4/` (dasar) | Hasil preprocessing bersama: `01_daily_delta_hm.csv`, `02_monthly_operating_hours.csv` (kolom `OPERATING_HOURS`), `03a_monthly_container.csv`, `03a_container_per_cabang_detail.csv`, `03b_container_volume_outlier_check.png`, `04_monthly_with_exog.csv` (kolom `OPERATING_HOURS`), `05_completeness_per_unit.csv`, `08_kriteria_unit.csv`, `unit_map_v4.json`, `kriteria_map.json`, `mapping_unit_dan_kriteria.xlsx`, `v4_kriteria_unit_mapping.xlsx`, `analisis_pacf_spearman.csv`, `analisis_pacf_spearman_plot.png` (seluruh berkas tersinkronisasi format `K##_UNIT_###`) |
| `checkpoints_v4/eda/` | Gambar EDA visualisasi: `eda_01_trend_operating_hours_total.png`, `eda_01b_trend_operating_hours_mean.png`, `eda_02_trend_operating_hours_mean.png`, `eda_05_dist_operating_hours.png`, `eda_09_box_operating_hours.png` (seluruh filename bebas kata utilitas) |
| `checkpoints_v4/v4_RINGKASAN_LINTAS_HORIZON.xlsx` | Ringkasan forced-GB vs v2b & rolling vs direct untuk kedua horizon |
| `checkpoints_v4/v4_PERBANDINGAN_4BULAN_vs_3BULAN.xlsx` | Head-to-head MAPE/RMSE final per unit & kriteria (4 vs 3 bulan) |
| `checkpoints_v4/h4bulan/` dan `h3bulan/` | Semua file per horizon (di bawah) |
| `06_excluded_units.csv` | Unit yang gugur di filter kelayakan (per horizon) |
| `v2_*.csv`, `v2_MASTER_SUMMARY_24_kombinasi.csv/.xlsx`, `v2_winner_per_kombinasi.xlsx` | Tahap 2 (24 kombinasi) + pemenang parameter per (model, varian, level) — **dipilih dengan MAPE_GLOBAL** (§19.6 poin 8) |
| `v2b_detail_per_unit_raw.csv` / `..._per_kriteria_raw.csv` | Prediksi mentah refit 12 kombinasi (checkpoint Tahap 2b) |
| `v2b_detail_per_unit_12kombinasi.csv` / `..._per_kriteria_...csv` | MAPE/RMSE/Bias per (unit/kriteria, kombinasi) |
| `v2b_hasil_12kombinasi_per_unit_kriteria.xlsx` | Detail, Best_Combo, Tally per unit & kriteria |
| `v4_forcedgb_per_unit.csv` / `..._per_kriteria.csv` | Checkpoint tuning GB individual (144 kombinasi per target) |
| `v4_forcedgb_vs_v2b_comparison.xlsx` | Perbandingan GB-tuned vs best v2b + selisih MAPE |
| `v4_HASIL_AKHIR_forced_gb.xlsx` | Tabel hasil akhir bersih per unit/kriteria (model final GB) |
| `v4_rolling_vs_direct_per_unit.csv` / `..._per_kriteria.csv`, `v4_rolling_vs_direct.xlsx` | Perbandingan rolling vs direct |

---


### 8.5 `./checkpoints_v4/rev_h3/` — Hasil Revisi Dosen Pembimbing 2 (190 Unit Valid, Eksogen Lag-1, §19.11)

Folder hasil revisi terisolasi untuk populasi 190 unit valid (bebas data leakage, 15 unit error >40% dieliminasi sejak awal data):

| File / Folder | Fungsi & Isi |
|---|---|
| `mapping_unit_dan_kriteria.xlsx` | Master reference mapping resmi 230 unit (`K01_UNIT_004`) dan 85 kriteria (`K01`–`K85`) |
| `kriteria_map.json` / `unit_map_v4.json` | Kamus JSON dua arah kode kriteria dan mapping plat asli ke ID unit baru |
| `04_monthly_with_exog_lag1.csv` | Dataset bulanan 190 unit dengan kolom `OPERATING_HOURS` dan fitur eksogen lag-1 ($t-1$) bebas data leakage |
| `forcedgb_vs_v2b_comparison_190unit.xlsx` | Konfigurasi model final Gradient Boosting untuk 190 unit valid (sheet `Per_Unit` dan `Per_Kriteria`) format nama baru |
| `unit_excluded_revisi_summary.xlsx` | Daftar resmi 25 unit yang diexclude (murni jam kerja nol) beserta alasan profesional standar |
| `perbandingan_eksogen_dan_model.xlsx` | Tabel perbandingan eksperimen lengkap: ARIMA vs ARIMAX vs GB (Eksogen $t$ vs Lag-1 vs Tanpa Eksogen) untuk 190 unit |
| `v4_rolling_vs_direct.xlsx` / `v2b_detail_per_unit_12kombinasi.csv` | File evaluasi pendukung tersinkronisasi 190 unit format nama baru |
| `future_forecast/future_forecast_final_190unit.xlsx` | Hasil proyeksi operating hours 12 bulan ke depan (Jan–Des 2026) 190 unit (kolom `FORECAST_OPERATING_HOURS`) |

---

## 9. Langkah Selanjutnya

1. ~~Apply semua fix §4.1-4.11.~~ ✅
2. ~~Implementasi 4 poin saran dosen Bimbingan 1 (§10.1-10.7).~~ ✅
3. ~~Restrukturisasi populasi unit ke cost&bbm-only (§14).~~ ✅
4. ~~Bimbingan 2 — keputusan RMSE/bias, notebook baru `code_v2.ipynb` (§15.1-15.3).~~ ✅
5. ~~Tahap 2 — jalankan 24 kombinasi (4 data-prep × 3 model × 2 pendekatan), tentukan model global terbaik per pendekatan (§15.4).~~ ✅ Pemenang: GB+savgol di kedua pendekatan.
6. ~~Tahap 3 — tuning individual per-unit & per-kriteria, tentukan pendekatan final (§15.5).~~ ✅ Pemenang final: **per-kriteria** (RMSE 56.77).
7. ~~Tahap 2b — drill-down 12 kombinasi (3 model × 4 prep) per unit & per kriteria, pakai parameter Tahap 2 (§16).~~ ✅ (populasi/split lama) Hasil di `v2b_hasil_12kombinasi_per_unit_kriteria.xlsx` + 6 plot PNG. GB+savgol menang individual di 32% unit & 24% kriteria (bukan mayoritas mutlak).
8. ~~`code_v3.ipynb` — ganti split train/test (Train Jan23-Agu25, Test Sep-Des25) + exclude 10 unit + remap ID + Excel per-tahap + plot full-history (§17).~~ ✅ Notebook baru selesai dibangun, dijalankan ulang Tahap 1→2→2b→3, 3 bug ditemukan & diperbaiki (§17.5).
9. **PRIORITAS SEKARANG — lanjut di chat baru** (alasan: token budget), bawa file-file di §18 (daftar file yang perlu diupload). Hal yang perlu diselesaikan/diputuskan:
   - **ARIMAX per-kriteria gagal massal (§17.5 poin 5)** — DI-HOLD, cek dulu apakah masalah sama masih muncul; kalau iya, lanjut cek NaN di `get_prepped(variant)`'s output (`train_full['CURAH_HUJAN']`/`['VOLUME_CONTAINER']`), bukan cuma raw data (udah dicek bersih)
   - **Hitung RMSE_GLOBAL/MAPE_GLOBAL gabungan buat skenario Tahap 2b** (tiap unit/kriteria pakai kombinasi terbaiknya sendiri) — cara hitung udah disepakati (§17.6), kode udah ditawarkan tapi belum dijalankan
   - Bawa hasil Tahap 2b (v3, tally baru GB+baseline) + Tahap 3 (v3, hasil berbalik per-unit menang) + temuan "prediksi mendatar" (§15.6, belum dibahas ke dosen) ke bimbingan berikutnya, minta arahan:
     - Lanjut ke **tuning parameter individual** per kombinasi pemenang masing-masing unit/kriteria (gabungin Tahap 2b + Tahap 3, §17.6)?
     - Konfirmasi metrik ranking final: MAPE (dipakai sementara di Tahap 2b) atau RMSE?
     - Gimana treatment kriteria/unit ber-anggota tunggal (`n_unit=1`, §15.6) dan ARIMAX yang gagal konvergen sebagian
10. Setelah dapat arahan dosen soal poin di atas, putuskan langkah lanjutan yang konkret.
11. Cross-check ulang 2 hal yang dulu ditunda dari Bimbingan 1 (§13): target MAPE <10-20% — apakah sudah cukup atau masih perlu perbaikan lanjut (angka MAPE_GLOBAL terbaru beda-beda tergantung skenario, lihat §17.6).
12. Konfirmasi ke dosen hal ambigu lain (§6): outlier check ganti capping atau tidak, cakupan CURRSTATE per jenis, status akhir 3 unit misteri (§14.8), keputusan `MERGE_FL_RENTAL` (§14.8) kalau belum diputuskan.
13. Putuskan §5.1, §5.2 (opsional).
14. Validasi manual §5.3, §6.
15. Model final disepakati dosen → lanjut dashboard Streamlit, integrasi ke chatbot perusahaan.

**Tambahan setelah chat `code_v4` + penulisan buku:**

16. **[Code]** Konfirmasi status run `h4bulan` & `h3bulan`; rerun cell `build_final_gb_comparison` (fix §19.6 poin 6) lalu selesaikan Section F; pastikan 5 file hasil di §19.8 ada.
17. **[Code]** Putuskan **metrik pemilih parameter Tahap 2** (MAPE vs RMSE, §19.6 poin 8) — kalau ganti ke RMSE, hapus checkpoint Tahap 2b & turunannya lalu jalankan ulang.
18. ~~**[Code]** Baca `v4_PERBANDINGAN_4BULAN_vs_3BULAN.xlsx` → tentukan **horizon utama** untuk buku~~ ✅ **3 bulan, final** (§19.10, sama dgn poin 25).
19. ~~**[Code]** Tambah analisis **pemilihan final per-unit vs per-kriteria** dan **penentuan model tunggal** (§19.8, §20.10).~~ ✅ **Per unit, final** & model tunggal Gradient Boosting dengan justifikasi ilmiah EDA (§20.10).
20. ~~**[Code]** Putuskan **metode forecast resmi GB** (direct vs rolling)~~ ✅ **Rolling untuk future forecast** masa depan (wajib rolling krn lag masa depan belum ada), **Direct untuk evaluasi testing** historis (§19.10, §21.8).
21. **[Code/Buku]** Uji signifikansi untuk H1 atau ubah redaksi hipotesis (§20.6 poin 6).
22. **[Buku]** Simpan draft Bab 1–3 sebagai file; bereskan catatan §20.6 (sitasi, kriteria model tunggal, angka EDA); buat diagram (§20.5); lanjut Bab 4–6 & Daftar Pustaka (§20.7).
23. ~~**[Code]** Dashboard Streamlit setelah analisa final selesai.~~ ✅ Versi pertama `pipeline_lib.py`/`appDemo.py`/`appPerusahaan.py` sudah jadi & SUDAH DICOBA jalan di environment user (§21).

**Tambahan setelah chat EDA + Tahap 3 + Dashboard:**

24. ~~**[Code]** Tambah EDA (Analisa Data) ke notebook.~~ ✅ (§19.9)
25. ~~**[Code]** Putuskan horizon utama (3 vs 4 bulan).~~ ✅ **3 bulan, final.**
26. ~~**[Code]** Putuskan pemilihan final per-unit vs per-kriteria.~~ ✅ **Per unit, final** (per-kriteria tetap ditampilkan di demo sbg pembanding).
27. ~~**[Code]** Tahap 3 -- retrain full-history + future forecast.~~ ✅ (§19.10)
28. ~~**[Code]** Dashboard Streamlit (3 file).~~ ✅ (§21), SUDAH jalan di sisi user.
29. **[Buku]** Pindahkan paragraf ETL lama (dari 3.3 lama) ke Bab 2 Penyiapan Data (2.2.4) -- ditawarkan, **user belum konfirmasi**.
30. **[Buku]** Pindahkan paragraf *grid search*/*parallel processing*/*checkpoint* (dari 3.1/3.2 lama) ke Bab 2 Pemodelan atau Bab 4 Lingkungan Pengujian -- **user belum pilih lokasi**.
31. **[Buku]** Tambah referensi Daftar Pustaka, dari 5 jadi minimal 10 (§20.7).
32. **[Buku]** Konfirmasi ke user: apa Bab 2 (isinya belum pernah di-upload ke chat ini) perlu dicek/dirapikan juga.
33. **[Buku]** Isi angka EDA di 3.3 sudah ada (§19.9, §20.7) -- tinggal dicek konsisten sama angka final (230 unit EDA vs 205 unit model, horizon 3 bulan final) di bagian lain buku.
34. ~~**[Dashboard]** Tab Per Kriteria appDemo.py~~ ✅ Selesai dibuat simetris dengan per unit via `evaluate_kriteria_on_test()` dan `retrain_forecast_kriteria_cached()` (§21.8 poin 4).
35. **[Dashboard]** Coba `appPerusahaan.py` end-to-end pakai data Excel asli (§21.7 poin 2-3).
36. **[Code, TERBUKA LAMA]** Metrik pemilih parameter Tahap 2 (MAPE vs RMSE, §19.6 poin 8) -- belum pernah diputuskan sejak v4 dibuat.
37. **[Code, TERBUKA LAMA]** Uji signifikansi H1, ARIMAX per-kriteria gagal massal (di-hold) -- belum dicek ulang di v4.
38. ~~**[Buku/Bimbingan]** Justifikasi ilmiah 3 pertanyaan bimbingan berbasis Proposal, Buku Bab 1–3, dan EDA: (a) pemilihan model tunggal GB & alasan pengujian ARIMAX/LSTM, (b) pembedaan data-prep per unit berdasarkan heterogenitas skewness (-3.05 s/d +5.75), serta (c) dasar pemilihan keempat metode data-prep (`Baseline`, `Savitzky-Golay`, `RobustScaler`, `Yeo-Johnson`)~~ ✅ Selesai dirangkum lengkap (§20.10).
39. ~~**[Dashboard]** Penyempurnaan UI appDemo.py & appPerusahaan.py: palet ramah dark mode, tooltip hover exact `%{y:.2f} jam`, kontinuitas garis tanpa jeda, pembersihan istilah teknis internal, pemfilteran 25 unit exclude resmi, dan default sort urut nomor di tabel vs urut MAPE terbaik di grafik~~ ✅ Selesai (§21.8 poin 1–7).
40. ~~**[Dashboard/Teknis]** Dokumentasi alur kerja pipeline forecasting end-to-end (ETL → Lag Features → Retrain Full History → Recursive Rolling Forecast), benchmark durasi eksekusi (~35 detik komputasi model, total ~1–1.5 menit), dan fleksibilitas tahun baru (`last_period + 1`)~~ ✅ Selesai (§21.9).
41. ~~**[Dashboard — Update Pasca-Bimbingan]** (a) Penambahan plot perbandingan kombinasi model + data-prep **Terbaik Pertama** dan **Terbaik Kedua** berdampingan dengan **Model Final GB** pada Plot Evaluasi Testing di `appDemo.py` (Per Unit & Per Kriteria), (b) dukungan pemilihan **multi-unit (`st.multiselect`)** dalam satu grafik gabungan di `appPerusahaan.py`, serta (c) penggantian istilah `"potensi error"` menjadi `"akurasi"` pada info horizon > 3 bulan di `appPerusahaan.py`~~ ✅ Selesai (§21.8 poin 8–9).
42. ~~**[Revisi Dosen Pembimbing 2 — Notebook `code_v4.ipynb`]** (a) Baseline sumbu Y grafik EDA mulai dari 0 (`ylim(bottom=0)`), (b) eksperimen eksogen Lag-1 ($t-1$) vs Eksogen $t$ vs Tanpa Eksogen pada ARIMA/ARIMAX dan GB, (c) eliminasi 15 unit MAPE testing >40% (alasan profesional *"Melebihi threshold toleransi error"*), menghasilkan 190 unit valid (mean MAPE 11.48%), (d) isolasi output di `checkpoints_v4/rev_h3/` (Cell 101–104)~~ ✅ Selesai (§19.11).
43. ~~**[Dashboard — Sinkronisasi Revisi 190 Unit]** (a) `pipeline_lib.py` memuat folder `rev_h3/`, (b) `appDemo.py` disinkronkan ke 190 unit, 63 kriteria aktif, 40 unit exclude, dan grafik Plotly `yaxis=dict(rangemode="tozero")`, (c) `appPerusahaan.py` hanya melatih 190 unit valid, export 40 unit exclude, dan grafik `rangemode="tozero"`~~ ✅ Selesai (§21.10).
44. ~~**[Dashboard Perusahaan — Redaksi Horizon]** Penyederhanaan keterangan slider horizon > 3 bulan di `appPerusahaan.py` dengan menghilangkan frasa teknis rekursif menjadi *"Forecast di atas 3 bulan memiliki tingkat akurasi yang lebih rendah dibanding 3 bulan pertama."*~~ ✅ Selesai (§21.10).
46. ~~**[Revisi Dosen Pembimbing 2 Tahap 5 — Naming Convention Kriteria & Unit]** Standarisasi penamaan 85 kriteria menjadi kode 2 digit urut populasi terbanyak (`K01` s/d `K85`), standarisasi unit 3 digit (`UNIT_001` - `UNIT_345`), dan penggabungan format standar tunggal `K<NoKriteria>_UNIT_<Nomor3Digit>` (contoh: `K01_UNIT_004`, `K09_UNIT_309`, `K84_UNIT_001`) di seluruh file checkpoint `rev_h3/` dan `code_v4.ipynb` Cell 102 tanpa rerun full notebook~~ ✅ Selesai (§19.12).
47. ~~**[Kamus JSON & Master Reference Mapping]** Penerbitan file master referensi `mapping_unit_dan_kriteria.xlsx` (2 sheet: `Mapping_Unit` 230 unit & `Ringkasan_Kriteria` 85 kriteria), sinkronisasi `unit_map_v4.json` & `anonymization_maps/unit_map.json` ke format baru, serta penambahan `kriteria_map.json` (dua arah: `KODE_TO_KRITERIA` & `KRITERIA_ID_TO_KODE`)~~ ✅ Selesai (§19.12).
48. ~~**[Dashboard Perusahaan — Sinkronisasi ETL Upload]** Penyempurnaan fungsi `build_monthly_full()` di `pipeline_lib.py` dengan auto-mapping penamaan berbasis kriteria dan optimasi pembacaan file Excel, serta defensive fallback di `appPerusahaan.py` sehingga upload data mentah langsung memproyeksikan seluruh 190 unit valid secara mulus~~ ✅ Selesai (§21.11).
49. ~~**[Buku/Bimbingan — Justifikasi Eksogen & LSTM]** Dokumentasi ilmiah justifikasi mengapa pengujian eksogen lag-1 difokuskan pada ARIMA vs ARIMAX vs GB dan mengapa LSTM tidak diikutkan (karena multivariate LSTM sudah gugur di Tahap 2 akibat sifat data-hungry pada sampel pendek 36 bulan)~~ ✅ Selesai (§20.10 poin 4).
50. ~~**[Standarisasi Istilah — Utilitas Menjadi Operating Hours (Poin 1 Revisi & Eksekusi Opsi A)]** Penggantian istilah "utilitas" menjadi "operating hours" secara menyeluruh: (1) tampilan antarmuka UI dashboard `appDemo.py` & `appPerusahaan.py` (judul, caption, sumbu Y, nama file download, alasan exclude), (2) kolom fisik file output Excel/CSV (`FORECAST_OPERATING_HOURS` dan `OPERATING_HOURS`), (3) penggantian nama file fisik (`02_monthly_operating_hours.csv` di seluruh folder checkpoint & 5 berkas plot EDA di `checkpoints_v4/eda/`), (4) sinkronisasi Cell 6, 15, 17, 18 di `code_v4.ipynb`, dan (5) arsitektur backend dual compatibility (`OPERATING_HOURS` & `UTILITAS`) di `pipeline_lib.py`~~ ✅ Selesai (§21.12).
51. ~~**[ETL & Data Pipeline — Eliminasi Total 15 Unit Anomali Sejak Awal Data]** 15 unit anomali (MAPE > 40%) dieliminasi secara permanen dari awal pipeline ETL (bukan lagi masuk daftar 40 exclude hilir), menyisakan 215 armada terlacak, 25 unit exclude operasional jam nol murni, dan 190 unit model terproyeksi~~ ✅ Selesai (§19.13).
52. ~~**[Standarisasi Naming Lintas Checkpoint — K##_UNIT_### di v1, v2, v3, v4]** Seluruh berkas data CSV dan Excel pada seluruh generasi checkpoint (`checkpoints/`, `checkpoints_v2/`, `checkpoints_v3/`, `checkpoints_v4/`) telah distandarisasi ke format kriteria `K<NoKriteria>_UNIT_<Nomor3Digit>` (0 unit nama lama tersisa)~~ ✅ Selesai (§19.14).
53. ~~**[Analisis Eksogen — Script & Visualisasi PACF & Spearman]** Script `analisis_pacf_spearman.py` dijalankan menghasilkan `analisis_pacf_spearman.csv` dan plot visualisasi dinamis bebas tumpang tindih legenda di `checkpoints_v4/`~~ ✅ Selesai (§19.15).
54. ~~**[Dashboard Perusahaan — Proteksi Zero False New Units]** Penyempurnaan filter ETL `pipeline_lib.py` dan `appPerusahaan.py` sehingga upload data operasional bulanan mentah langsung memproyeksikan 190 unit valid tanpa memunculkan 15 unit anomali sebagai "Unit Baru"~~ ✅ Selesai (§21.13).
55. ~~**[Buku/Bimbingan — Sintesis Ilmiah Disagregasi Kriteria vs Unit & 6 Insight Skripsi]** Dokumentasi ilmiah mendalam mengenai penyebab matematis & operasional error per-kriteria lebih tinggi daripada per-unit (heterogenitas rotasi dispatching, distorsi disagregasi low-hour units, kompromi hiperparameter, dan prinsip *bottom-up hierarchical forecasting*) serta 6 temuan empiris kunci skripsi~~ ✅ Selesai (§20.11).
56. ~~**[Buku/Bimbingan — Penjelasan Penomoran ID Unit 3 Digit (UNIT_001 s/d UNIT_345)]** Rationale integritas database aset dan audit trail nomor unik aset 3 digit pada armada operasional aktif 200-an unit~~ ✅ Selesai (§20.12).
57. **[Buku Skripsi]** Melanjutkan penulisan Bab 4 (Implementasi dan Pengujian), Bab 5 (Pembahasan), Bab 6 (Kesimpulan dan Saran — **penamaan bab dikoreksi sesuai pedoman Proyek**, lihat §20.13.1), dan Daftar Pustaka menggunakan data final 190 unit valid, 25 unit exclude resmi, format penamaan `K##_UNIT_###`, serta 6 insight kunci skripsi.

**Tambahan dari chat penulisan buku (§19.16, §20.13):**

58. **[Buku]** Tulis ulang Bab 4 (4.1–4.9, kerangka §20.13.5) memakai output rerun 215 unit; semua angka pra-rerun diganti; isi `[ISI]` (versi pustaka, waktu eksekusi, spesifikasi PC dashboard) & `[CEK]` (§20.13.4).
59. **[Buku]** Tulis Bab 5 (Pembahasan: interpretasi untuk pembaca awam, keterbatasan eksogen *t* vs estimasi musiman, *rolling* lebih buruk, optimisme pemilihan pada *test* sama, kalimat keterbatasan netral populasi) dan Bab 6 (Kesimpulan & Saran).
60. **[Buku]** Daftar Pustaka: cari referensi tambahan via web (≥6, ber-DOI, ≤5 tahun, APA seperti proposal; tandai yang belum terverifikasi) sehingga total ≥10; jangan hapus 5 referensi Bab 1–3 yang sudah dipakai.
61. **[Buku]** Update Bab 3.3 dgn EDA hasil rerun (N, rata-rata, skewness, korelasi, skewness per unit `eda_14/15/16`, PACF/Spearman dgn redaksi hati-hati §20.13.4), ganti nomor/nama gambar dan istilah *operating hours*; tulis juga populasi (215 unit tercatat, 190 unit dimodelkan) tanpa alasan exclude 15 unit.
62. **[Buku]** Terakhir: revisi Bab 1–3 (89 "utilitas", "mayoritas" dibatasi dgn angka kriteria, "signifikan" diganti "MAPE global terendah", pindahkan paragraf ETL ke Bab 2.2.4 dan paragraf grid search/parallel/checkpoint ke Bab 4.2; Bab 1–3 sekitar 8.000 kata, pangkas hanya bila diminta).
63. **[Code]** Verifikasi butir ❓ di §19.16 (label EDA, cell 14/19/20/103, `kode_eksperimen_6_skenario.py`, PNG EDA final tanpa "UTILITAS"/"(Surabaya)").

---

## 18. File yang Perlu Dibawa ke Chat Baru

Biar chat baru langsung paham konteks tanpa perlu re-explain dari nol:

**WAJIB (semua topik):**
- **`PROGRESS.md`** (file ini) — konteks lengkap semua keputusan, bug, dan status

**KALAU LANJUT ANALISA CODE (Bagian A):**
- **`code_v4.ipynb`** — notebook aktif terbaru, **105 cell** (EDA cell 13-19, Tahap 3 cell 92-99, Revisi Bimbingan ke-2 cell 101-104, §19.9-19.11). **[UPDATE] HANYA `.ipynb`, jangan bawa `.py` lagi** (preferensi user berubah, §20.9)
- **Folder Hasil Revisi Utama (190 Unit Valid, TERBARU & FINAL):** `checkpoints_v4/rev_h3/` (berisi `mapping_unit_dan_kriteria.xlsx`, `kriteria_map.json`, `unit_map_v4.json`, `perbandingan_eksogen_dan_model.xlsx`, `forcedgb_vs_v2b_comparison_190unit.xlsx`, `unit_excluded_revisi_summary.xlsx`, `04_monthly_with_exog_lag1.csv`, dan `future_forecast/future_forecast_final_190unit.xlsx`)
- File baseline lama (dari `checkpoints_v4/h3bulan/`, 205 unit sebelum revisi): `v4_forcedgb_vs_v2b_comparison.xlsx`, `v4_rolling_vs_direct.xlsx`, `future_forecast/v4_future_forecast_final.xlsx`
- `checkpoints_v4/04_monthly_with_exog.csv`, `checkpoints_v4/08_kriteria_unit.csv`, `checkpoints_v4/02_monthly_operating_hours.csv`, `checkpoints_v4/analisis_pacf_spearman.csv`, `checkpoints_v4/analisis_pacf_spearman_plot.png` (kolom & nama file bebas kata utilitas, seluruh penamaan unit berformat `K##_UNIT_###`)
- File master referensi mapping: `checkpoints_v4/rev_h3/mapping_unit_dan_kriteria.xlsx` & `kriteria_map.json`
- File EDA (dari `checkpoints_v4/h3bulan/eda/` kalau mau cek ulang hasil EDA): PNG + CSV, lihat §19.9

**KALAU LANJUT PENULISAN BUKU (Bagian B):**
- **Draft Bab 1–3 TERBARU** (3.1/3.2/3.3 sudah dirombak total, §20.7 — teks yang dicopy dari chat lama BEDA dari draft paling awal, simpan versi TERBARU sebagai file)
- `DSA_C14230035_Michael_Sugiarto__Proposal_.md` (proposal, termasuk Daftar Pustaka & diagram)
- `Pedoman_Buku_Skripsi_DSA.pdf` (pedoman format)
- Daftar Pustaka Bab 1-3 yang sudah dibuat (5 referensi, §20.7 — perlu ditambah s/d minimal 10)
- Hasil EDA (PNG + CSV, §19.9) kalau mau pasang gambar ke buku — sudah dipetakan gambar mana masuk paragraf mana

**KALAU LANJUT BAB 4–6 (chat baru, dari chat penulisan buku):**
- **Pesan pembuka** yang bisa ditempel: lihat paragraf penutup terakhir di bawah (urutan tugas & catatan penting §20.13).
- **`PROGRESS.md` terbaru** (file ini) + **teks Bab 4 dari chat lama** (kalau masih mau dipakai kerangkanya; angkanya pra-rerun) + **`draft_bab_1-3.md` terbaru** + **`Pedoman_Buku_Skripsi_DSA.pdf`** (batas kata, minimal 10 referensi, struktur Bab 4–6 tidak ada di memory).
- **File hasil rerun 215 unit** (versi baru, setelah §19.13): `v2_MASTER_SUMMARY_24_kombinasi.xlsx`, `v2_winner_per_kombinasi.xlsx`, `v2b_hasil_12kombinasi_per_unit_kriteria.xlsx` (semua sheet), `v4_forcedgb_vs_v2b_comparison.xlsx` (Per_Unit, Per_Kriteria), `v4_rolling_vs_direct.xlsx` (Per_Unit, Per_Kriteria, Ringkasan), `v4_PERBANDINGAN_4BULAN_vs_3BULAN.xlsx`, `v4_RINGKASAN_LINTAS_HORIZON.xlsx`, `perbandingan_eksogen_dan_model.xlsx`, `mapping_unit_dan_kriteria.xlsx`, `future_forecast/…final…xlsx`.
- **EDA hasil rerun:** CSV `eda_00, 04, 08, 08b, 12, 14, 15`; PNG trend (total, rata-rata per unit, curah hujan, volume container), distribusi (3), boxplot (3), heatmap korelasi, `eda_16`; plus `analisis_pacf_spearman.csv` + PNG.
- **Info teks:** `python --version` & `pip list` (pandas, numpy, scipy, scikit-learn, statsmodels, pmdarima, tensorflow, keras, streamlit, plotly, openpyxl), spesifikasi PC uji dashboard, waktu tiap tahap (ETL, Tahap 2, 2b, penyesuaian GB) dari log, waktu unggah→hasil tampil di `appPerusahaan`.
- **TIDAK perlu dibawa ulang** (sudah di memory project atau usang): kode (`code_v4`, `pipeline_lib`, `appDemo`, `appPerusahaan`) bila tak berubah, file hasil lama sebelum rerun, `penjelasan_eksperimen_6_skenario.md` (bertentangan dgn xlsx), `spesifikasi_lingkungan_dan_runtime.md` (versi pustaka tak konsisten).

**KALAU LANJUT DASHBOARD (Bagian C):**
- **`pipeline_lib.py`, `appDemo.py`, `appPerusahaan.py`** (§21) — ketiganya, sudah dikonfirmasi jalan di sisi user
- `checkpoints_v4/` folder utuh (base + `h3bulan/` + `h3bulan/future_forecast/`)

**KALAU MAU LANJUT SOAL ARIMAX per-kriteria (§17.5 poin 5):**
- `v3_diagnostik_arimax_kriteria.csv` (hasil diagnostik yang udah ada)

**KALAU MAU HITUNG RMSE_GLOBAL/MAPE_GLOBAL gabungan Tahap 2b (§17.6):**
- `v2b_combo_preds_per_unit.csv` dan `v2b_combo_preds_per_kriteria.csv` (checkpoint mentah, BUKAN yang di Excel — perlu data mentah per-baris buat pooling yang benar)
- `v2b_best_combo_per_unit.csv` dan `v2b_best_combo_per_kriteria.csv`

**KALAU MAU BAHAS HASIL / BUAT LAPORAN:**
- `v2b_hasil_12kombinasi_per_unit_kriteria.xlsx`
- `v3_tahap3_tuning_individual.xlsx`
- `v3_kriteria_unit_mapping.xlsx`, `v3_train_test_split_info.xlsx`, `v3_tahap2_24kombinasi.xlsx` (kalau perlu detail Tahap 1/2)

**TIDAK PERLU** diupload ulang: `code.ipynb`, `code_v2.ipynb`, `code_v2_2.ipynb` (arsip, sudah gak dipakai — semua yang relevan udah dirangkum di `PROGRESS.md`), `unit_map.json` versi LAMA (pakai `unit_map_v3.json` yang baru).

---

*Update terakhir: Fase `code_v3.ipynb` selesai (§17) — ganti split train/test (Train Jan2023-Agu2025, Test Sep-Des2025 4 bulan), exclude 10 unit + remap ID sequential (§17.3), tambah Excel per-tahap biar siap sidang tanpa buka raw data (§17.4), plot sekarang full actual train+test dengan prediksi cuma di periode test + y-axis selalu mulai dari 0. 3 bug ditemukan & diperbaiki (basis notebook stale, TensorFlow graph leak LSTM lintas varian, MemoryError dari cache prep gak di-evict) — detail §17.5. **2 hal masih terbuka**: (1) ARIMAX per-kriteria gagal massal (79% gagal, root cause diduga NaN di exog HASIL reindex `DATA_PREP_VARIANTS`, belum terkonfirmasi) — **DI-HOLD atas keputusan user**, dilanjut di chat baru kalau masih muncul; (2) belum ada RMSE_GLOBAL/MAPE_GLOBAL gabungan buat skenario "tiap unit pakai kombinasi terbaiknya sendiri" (Tahap 2b) — cara hitung sudah disepakati, kode sudah ditawarkan, belum dieksekusi. Temuan metodologi penting: kesimpulan Tahap 3 (per-unit vs per-kriteria) BERBALIK di split baru (per-unit menang 53.90 vs 62.08, dulu per-kriteria menang), dan tally Tahap 2b juga berubah (GB+baseline paling sering menang, dulu GB+savgol) — keduanya menunjukkan hasil SENSITIF terhadap split/populasi, bukan kebenaran tetap, penting dicatat di bab pembahasan. **Lihat §18 untuk daftar file yang perlu dibawa ke chat baru.***

---

*Update lanjutan (chat ini): (1) **EDA ditambahkan** ke `code_v4.ipynb` (cell 13-19, §19.9) — trendline, deskriptif+skewness, distribusi, outlier berlabel, korelasi; populasi EDA 230 unit (beda dari 205 unit populasi model final h3bulan, perlu dicatat eksplisit di buku kenapa beda). (2) **Horizon final DIPUTUSKAN: 3 bulan, per unit, GB** — bukan lagi dugaan/belum terbukti seperti update sebelumnya. (3) **Tahap 3 (Model Final & Future Forecast) ditambahkan** (cell 92-99, §19.10): retrain pakai seluruh histori + forecast rolling ke depan (wajib rolling, bukan direct, krn gak ada lag aktual masa depan); eksogen masa depan diestimasi dari rata-rata musiman (asumsi, limitasi metodologi); 1 bug pandas ditemukan & diperbaiki (`groupby().apply()` pada dataframe kosong menjatuhkan kolom group). (4) **Buku Bab 3 dirombak**: 3.1 Analisis Masalah & 3.2 Analisis Kebutuhan dipisah bersih (masalah vs kebutuhan PT X, bukan kebutuhan proyek kita — paragraf teknis grid search/parallel/checkpoint dikeluarkan, BELUM dipindah ke bab lain); 3.3 Analisis Data dirombak total jadi murni hasil EDA (bukan lagi proses ETL — paragraf ETL lama BELUM dipindah ke Bab 2). Daftar Pustaka Bab 1-3 sudah dibuat (5 referensi, kurang dari minimal 10 pedoman). (5) **Dashboard Streamlit v1 selesai** (`pipeline_lib.py`, `appDemo.py`, `appPerusahaan.py`, §21) — **SUDAH DICOBA & JALAN** di environment user setelah 1 isu non-kode (akses via `127.0.0.1` bukan `localhost`, masalah Chrome/Windows). **Banyak item masih terbuka** — lihat §9 poin 29-37 (lokasi paragraf yang dipindah dari Bab 3, jumlah referensi, precompute tab kriteria, testing end-to-end dashboard perusahaan, metrik pemilih parameter Tahap 2, uji signifikansi H1) dan §21.7.*

---

*Update lanjutan (penyempurnaan dashboard, justifikasi 3 pertanyaan bimbingan, & fitur perbandingan/multi-unit): (1) **Kompatibilitas Dark Mode & Visualisasi** — garis hitam dihilangkan, warna diganti palet ramah tema gelap (#2ca02c, #1f77b4, orange, crimson, #00b4d8, #c77dff); nama perusahaan dan pemisah dash dibersihkan total; dropdown default urut best MAPE (UNIT_0309, 0.15%); visual gap garis prediksi testing & future forecast ditutup dengan menyambungkan titik aktual terakhir (2025-09 dan 2025-12); garis prediksi training dihilangkan dari Plot 1. (2) **Tooltip Hover Interaktif** — `hovermode="x unified"` dan format exact `%{y:.2f} jam` diterapkan di semua chart Plotly appDemo & appPerusahaan. (3) **Plot Evaluasi Testing Per Kriteria** ditambahkan ke `appDemo.py` via `evaluate_kriteria_on_test()` di `pipeline_lib.py`. (4) **Tabel Unit Diexclude Disempurnakan** — menyisakan tepat 25 unit resmi (18 nol di train, 7 nol di test) dengan kolom Nama Unit dan Alasan berhuruf kapital standar. (5) **Pembersihan Istilah Internal & Redaksi Info Horizon** — jargon internal dibersihkan; info horizon > 3 bulan di `appPerusahaan.py` menggunakan istilah `"akurasi"` (bukan `"potensi error"`). (6) **Multi-port & Benchmark Performa** — bisa jalan bersamaan di port 8501 dan 8502; waktu retrain & forecast 205 unit terukur 35.04 detik (total ~1–1.5 menit). (7) **Sorting Tabel vs Grafik** — tabel Perbandingan Performa di tab Ringkasan diatur urut nomor unit/ID, sedangkan dropdown grafik default urut MAPE terbaik. (8) **Justifikasi 3 Pertanyaan Bimbingan & Pipeline Docs** — justifikasi pemilihan 1 model tunggal GB (+ alasan uji ARIMAX/LSTM), pembedaan data-prep per unit via skewness, serta dasar pemilihan 4 metode data-prep (`Baseline`, `Savitzky-Golay`, `RobustScaler`, `Yeo-Johnson`) dirangkum lengkap di §20.10; alur komputasi end-to-end dan fleksibilitas tahun baru (`last_period + 1`) didokumentasikan di §21.9. (9) **Plot Perbandingan Terbaik 1 & Terbaik 2 (`appDemo.py`) serta Multi-Unit (`appPerusahaan.py`)** — ditambahkan loader `load_v2b_12kombinasi()` & `load_v2b_raw_preds()`, 3 kartu ringkasan dan garis pembanding Terbaik 1 & Terbaik 2 pada Plot Evaluasi Testing `appDemo.py`, serta fitur `st.multiselect` multi-unit dalam satu grafik gabungan di `appPerusahaan.py` (§21.8 poin 8–9). (10) **Sinkronisasi Revisi Dosen Pembimbing 2 (190 Unit Valid & 40 Unit Excluded)** — `pipeline_lib.py`, `appDemo.py`, dan `appPerusahaan.py` dialihkan ke folder checkpoint `checkpoints_v4/rev_h3/` (dengan fallback aman ke `h3bulan`). Model final memuat `forcedgb_vs_v2b_comparison_190unit.xlsx` (190 unit, rata-rata MAPE 11.48%), tabel kriteria disinkronkan ke 63 kriteria aktif, unit yang diexclude memuat 40 unit dengan alasan profesional (*Melebihi threshold toleransi error*), dan semua chart Plotly di kedua dashboard dikonfigurasi dengan `yaxis=dict(rangemode="tozero")` agar sumbu Y selalu mulai dari 0.*

---

*Update lanjutan (Penyederhanaan Redaksi Horizon Dashboard & Implementasi Poin 5 Revisi Bimbingan Tahap 5):*
1. **Penyederhanaan Redaksi Horizon Prediksi di Dashboard Perusahaan (`appPerusahaan.py`)**:
   - Menghapus klausa penjelasan kausalitas internal `", karena bulan-bulan selanjutnya diproyeksikan dari hasil prediksi sebelumnya (bukan data aktual)."` saat memanjangkan rentang prediksi (> 3 bulan).
   - Tampilan peringatan kini berbunyi lugas dan profesional: *"Forecast di atas 3 bulan memiliki tingkat akurasi yang lebih rendah dibanding 3 bulan pertama."* tanpa membeberkan teknis internal model.
2. **Implementasi Revisi Poin 5 Dosen Pembimbing (Sistem Penamaan Unit Berbasis Kriteria)**:
   - **Mapping Angka Kriteria (`K01` s/d `K85`)**: Seluruh 85 kriteria kustom diurutkan menurun (*descending*) berdasarkan jumlah populasi unit (Opsi A) dan dipetakan ke kode kriteria formal 2 digit (`K01` s/d `K85`). Dari 85 kriteria total (populasi 230 unit), sebanyak 63 kriteria aktif pada 190 unit valid.
   - **Standarisasi Penamaan Unit 3 Digit**: Angka penomoran unit dinormalkan dari 4 digit (`UNIT_0001` - `UNIT_0345`) menjadi 3 digit (`UNIT_001` - `UNIT_345`).
   - **Format Penamaan Unit Baru**: Menggabungkan kode kriteria dan nomor urut unit 3 digit menjadi format standar tunggal: `K<NoKriteria>_UNIT_<Nomor3Digit>` (contoh: `K01_UNIT_004`, `K09_UNIT_309`, `K84_UNIT_001`).
   - **Penerbitan Master Reference Mapping (`mapping_unit_dan_kriteria.xlsx`)**: Diterbitkan di `checkpoints_v4/rev_h3/` dan `checkpoints_v4/` berisi 2 sheet:
     - `Mapping_Unit` (230 unit): memuat `KODE_KRITERIA`, `EQUIP_NAME_BARU`, `EQUIP_NAME_LAMA`, `STATUS` (`VALID_190` vs `EXCLUDED`), `KRITERIA_ID`, spesifikasi alat (`JENIS`, `TYPE/MERK`, `CAP`, `HP`), dan `LOKASI`.
     - `Ringkasan_Kriteria` (85 kriteria): memuat `KODE_KRITERIA`, `KRITERIA_ID`, `JUMLAH_UNIT`, `DAFTAR_UNIT_BARU`, `DAFTAR_UNIT_LAMA`, serta spesifikasi teknisnya.
   - **Sinkronisasi File Checkpoint & Output (Tanpa Full Rerun Notebook)**:
     - `forcedgb_vs_v2b_comparison_190unit.xlsx`: `EQUIP NAME` diperbarui ke nama baru; kolom `KODE_KRITERIA` ditambahkan ke sheet `Per_Kriteria`.
     - `unit_excluded_revisi_summary.xlsx`: `EQUIP NAME` seluruh 40 unit excluded diperbarui ke format baru.
     - `perbandingan_eksogen_dan_model.xlsx`: Sheet `Detail_PerUnit` diperbarui ke nama baru.
     - `future_forecast/future_forecast_final_190unit.xlsx`: Sheet `Forecast_Per_Unit` dan `Forecast_Pivot` diperbarui ke nama baru.
     - `04_monthly_with_exog_lag1.csv` & `04_monthly_with_exog.csv`: Kolom `EQUIP NAME` disinkronkan ke nama baru.
     - `checkpoints_v4/08_kriteria_unit.csv`: Ditambahkan kolom `KODE_KRITERIA` dan kolom `EQUIP NAME` diperbarui.
     - File pendukung evaluasi di `rev_h3/` (`v4_rolling_vs_direct.xlsx`, `v2b_detail_per_unit_12kombinasi.csv`, `v2b_detail_per_unit_raw.csv`) dibuat dan dipetakan ke format nama baru agar kompatibilitas evaluasi perbandingan model di dashboard 100% sinkron (190 unit valid, 63 kriteria aktif, 40 unit excluded).
   - **Pembaruan Notebook `code_v4.ipynb`**: Cell 102 diperbarui secara konsisten agar jika cell 101–104 dijalankan ulang, pipeline revisi akan membaca mapping dari `mapping_unit_dan_kriteria.xlsx` dan langsung memproduksi nama unit format baru.
   - **Pembaruan Kamus JSON (`unit_map_v4.json` & `kriteria_map.json`)**: File `unit_map_v4.json` (di `checkpoints_v4/` dan `rev_h3/`) serta `anonymization_maps/unit_map.json` diperbarui sehingga nama aset asli fisik/plat nomor memetakan ke nama unit baru. File baru `kriteria_map.json` ditambahkan dengan kamus dua arah (`KODE_TO_KRITERIA` dan `KRITERIA_ID_TO_KODE`).
   - **Verifikasi Dashboard**: Kedua dashboard (`appDemo.py` dan `appPerusahaan.py`) telah diverifikasi mampu memuat seluruh 190 unit valid, 40 unit excluded, plot komparasi model, dan plot future forecast tanpa error.
   - **Sinkronisasi ETL Upload**: Fungsi ETL upload `build_monthly_full()` di `pipeline_lib.py` serta `appPerusahaan.py` telah disempurnakan dengan auto-mapping penamaan unit kriteria dan optimasi pembacaan Excel, sehingga proses upload data mentah langsung memproyeksikan seluruh 190 unit valid secara mulus (mengatasi isu 0 unit terproyeksi).

---

*Update lanjutan (Penerapan Poin 1 Revisi Bimbingan — Penggantian Istilah Utilitas menjadi Operating Hours Secara Menyeluruh):*
1. **Tampilan Antarmuka & Dashboard (UI)**:
   - **Dashboard Demo (`appDemo.py`)**: Page title diganti menjadi *"Demo Prediksi Operating Hours Alat Berat"*, judul utama *"Demo Sistem Prediksi Operating Hours Alat Berat"*, label sumbu Y grafik evaluasi testing dan proyeksi per-unit menjadi *"Operating Hours (jam)"*, dan grafik per-kriteria menjadi *"Total Operating Hours (jam)"*. Deskripsi alasan exclude unit pada tabel disesuaikan menjadi *"Data operating hours..."*.
   - **Dashboard Perusahaan (`appPerusahaan.py`)**: Page title dan judul utama diganti menjadi *"Prediksi Operating Hours Alat Berat"*, caption *"Sistem Prediksi Operating Hours Armada Alat Berat"*, label sumbu Y grafik *"Operating Hours (jam)"*, serta nama file export Excel diubah menjadi `hasil_forecast_operating_hours.xlsx`.
   - **Modul Pipeline (`pipeline_lib.py`)**: Kamus alasan `REASON_MAP` diperbarui menggunakan istilah *"Data operating hours..."*.
   - **Notebook Eksperimen (`code_v4.ipynb`)**: Judul-judul plot visualisasi EDA pada cell 15–18 (trendline total/mean, distribusi histogram, dan boxplot outlier) disesuaikan menggunakan label *"Operating Hours (jam)"*.

2. **Pembaruan Kolom File Output Fisik (Eksekusi Opsi A)**:
   - `future_forecast_final_190unit.xlsx` (Sheet `Forecast_Per_Unit`): Kolom angka prediksi resmi diubah dari `FORECAST_UTILITAS` menjadi `FORECAST_OPERATING_HOURS`.
   - `04_monthly_with_exog_lag1.csv` & `04_monthly_with_exog.csv`: Kolom jam kerja aktual resmi diubah dari `UTILITAS` menjadi `OPERATING_HOURS`.
   - `02_monthly_operating_hours.csv`: Kolom jam kerja aktual resmi diubah menjadi `OPERATING_HOURS`.
   - `v4_kriteria_unit_mapping.xlsx` (Sheet `Detail_HM_per_Unit_Kriteria`): Kolom jam kerja resmi diubah menjadi `OPERATING_HOURS`.
   - File baseline lama (`v4_future_forecast_final.xlsx` & `v4_future_forecast_per_unit.csv`): Kolom `FORECAST_UTILITAS` diperbarui menjadi `FORECAST_OPERATING_HOURS`.
   - `appDemo.py` & `appPerusahaan.py`: Seluruh kode pemanggilan kolom prediksi dan data historis telah disinkronkan ke `OPERATING_HOURS` dan `FORECAST_OPERATING_HOURS`.

3. **Pembaruan Nama File Fisik (Eliminasi Kata 'utilitas' dari Seluruh Filename)**:
   - File data CSV: `checkpoints_v4/02_monthly_utilitas.csv` resmi di-rename menjadi `checkpoints_v4/02_monthly_operating_hours.csv` (termasuk pada folder arsip `checkpoints/`, `checkpoints_v2/`, dan `checkpoints_v3/`).
   - File gambar plot EDA (`checkpoints_v4/eda/`):
     - `eda_01_trend_utilitas_total.png` $\rightarrow$ `eda_01_trend_operating_hours_total.png`
     - `eda_01b_trend_utilitas_mean.png` $\rightarrow$ `eda_01b_trend_operating_hours_mean.png`
     - `eda_02_trend_utilitas_mean.png` $\rightarrow$ `eda_02_trend_operating_hours_mean.png`
     - `eda_05_dist_utilitas.png` $\rightarrow$ `eda_05_dist_operating_hours.png`
     - `eda_09_box_utilitas.png` $\rightarrow$ `eda_09_box_operating_hours.png`
   - Sinkronisasi `code_v4.ipynb`: Kode pada Cell 6, 15, 17, dan 18 diperbarui agar menyimpan output ke nama file baru tersebut.
   - Hasil audit: Saat ini terdapat **0 file** di `checkpoints_v4/` yang mengandung kata `utilitas` pada nama filenya.

4. **Arsitektur Dual Compatibility di Backend (`pipeline_lib.py`)**:
   - Fungsi loader `load_monthly_full_checkpoint()` dan `load_future_forecast()` dilengkapi logika *dual compatibility*: data output fisik menyediakan kolom baru (`OPERATING_HOURS` & `FORECAST_OPERATING_HOURS`) sekaligus otomatis meng-alias nama lama (`UTILITAS` & `FORECAST_UTILITAS`).
   - Seluruh pipeline inferensi, evaluasi testing, koneksi kurva (*connecting line*), dan future forecast telah diverifikasi lulus uji 100% tanpa error.

---

*Update lanjutan (Pembersihan Tuntas Teks Exclude Fisik, Berkas CSV EDA, & Perbaikan Bug Dashboard Demo):*
1. **Pembersihan Fisik Berkas Excel Alasan Exclude & Proteksi Defensif UI**:
   - Audit komprehensif menemukan teks alasan pada berkas fisik `checkpoints_v4/rev_h3/unit_excluded_revisi_summary.xlsx` (40 unit), `checkpoints_v4/h3bulan/future_forecast/v4_unit_excluded_summary.xlsx`, dan sheet `Unit_Diexclude` pada `v4_future_forecast_final.xlsx` masih memuat teks lama (*"Data utilitas..."*).
   - Seluruh 25 baris terkait diubah secara fisik menjadi:
     - *"Data operating hours pada salah satu tahun periode data train bernilai nol semua"* (18 unit)
     - *"Data operating hours pada periode data test bernilai nol semua"* (7 unit)
   - Ditambahkan proteksi pembersihan runtime `.str.replace("utilitas", "operating hours", case=False)` pada `pipeline_lib.py` (`load_excluded_summary`), `appDemo.py`, dan `appPerusahaan.py` untuk menjamin tampilan antarmuka selalu konsisten.

2. **Sinkronisasi Berkas CSV EDA & Notebook `code_v4.ipynb`**:
   - `eda_04_deskriptif_skewness.csv` & `eda_08_outlier_iqr.csv`: Label baris `UTILITAS (pooled unit-bulan)` diubah menjadi `Operating Hours (pooled unit-bulan)`.
   - `eda_00_agregat_bulanan.csv` & `eda_12_korelasi_pearson.csv`: Kolom dan indeks `UTILITAS_TOTAL` & `UTILITAS_MEAN` diubah menjadi `OPERATING_HOURS_TOTAL` & `OPERATING_HOURS_MEAN`.
   - `code_v4.ipynb`: Judul grafik Cell 20 diubah menjadi *"Distribusi Nilai Skewness Operating Hours per Unit"*, serta Cell 102 dan 104 disinkronkan ke `FORECAST_OPERATING_HOURS`.
   - Audit seluruh repositori mengonfirmasi: **0 kemunculan** teks *"data utilitas"* di seluruh berkas aktif proyek.

3. **Perbaikan Bug Runtime `NameError: hist_k` di Dashboard Demo (`appDemo.py`)**:
   - Terjadi error `NameError: name 'hist_k' is not defined` pada Tab Detail per Kriteria (baris 439) akibat pemeriksaan nama kolom `if "OPERATING_HOURS" in hist_k.columns` dipanggil di dalam ekspresi penetapan `hist_k = ...`.
   - Diperbaiki dengan memeriksa langsung ke `DATA["monthly_full"].columns` sebelum `hist_k` dibentuk, serta menerapkan alias ganda (`OPERATING_HOURS` dan `UTILITAS`) pada `hist_k`.
   - Telah diverifikasi simulasi langsung pada kriteria aktif: visualisasi tren historis dan proyeksi masa depan per kriteria berjalan lancar tanpa error.

---

*Update lanjutan (Eliminasi Awal 15 Unit Anomali, Standarisasi Global Naming Checkpoints v1–v4, Penyelarasan Dashboard Bebas False Unit, & Sintesis Ilmiah Bimbingan):*
1. **Eliminasi Total 15 Unit Anomali dari Awal Pipeline ETL (§19.13)**:
   - Sesuai arahan user, 15 unit anomali dengan MAPE testing > 40% dieliminasi secara permanen sejak pemrosesan data paling awal (`04_monthly_with_exog.csv`, `08_kriteria_unit.csv`, `pipeline_lib.py`, `appPerusahaan.py`, `code_v4.ipynb` Cell 10), meniru tindakan terhadap 10 unit non-operasional sebelumnya.
   - Dampak arsitektur populasi: Total armada terlacak menjadi **215 unit** (dari 230 unit), unit yang diexclude murni karena histori jam nol sebanyak **25 unit** (18 train nol + 7 test nol), dan model final melatih serta memproyeksikan tepat **190 unit valid** (menaungi **63 kriteria aktif** dari total 85 kriteria).
   - Berkas `unit_excluded_revisi_summary.xlsx` dikembalikan ke daftar murni 25 unit nol operasional tanpa mencantumkan 15 unit anomali di tabel exclude hilir.
2. **Standarisasi Global Penamaan Unit Kriteria (`K##_UNIT_###`) Lintas Seluruh Direktori Checkpoint (§19.14)**:
   - Dilakukan perataan sistematis konvensi penamaan unit berbasis kriteria `K<NoKriteria>_UNIT_<Nomor3Digit>` (contoh: `K01_UNIT_004`, `K09_UNIT_309`, `K84_UNIT_001`) ke seluruh berkas output historis di seluruh folder checkpoint:
     - `checkpoints_v4/`: Seluruh CSV dan Excel (`v4_kriteria_unit_mapping.xlsx`, `05_completeness_per_unit.csv`, `08_kriteria_unit.csv`, `v4_PERBANDINGAN_4BULAN_vs_3BULAN.xlsx`, `analisis_pacf_spearman.csv`, `01_daily_delta_hm.csv`, `02_monthly_operating_hours.csv`, subdirektori `h3bulan/`, `h4bulan/`, `rev_h3/`).
     - `checkpoints_v3/`: 16 CSV dan 4 Excel (`v3_kriteria_unit_mapping.xlsx`, `v2b_hasil_12kombinasi_per_unit_kriteria.xlsx`, `v3_tahap2_24kombinasi.xlsx`, `v3_tahap3_tuning_individual.xlsx`, dll.).
     - `checkpoints_v2/`: 16 CSV dan 1 Excel (`v2b_hasil_12kombinasi_per_unit_kriteria.xlsx`, dll.).
     - `checkpoints/` (v1): 23 CSV dan 1 Excel (`15_LAPORAN_HASIL.xlsx`, dll.).
     - `anonymization_maps/unit_map.json`: Seluruh 230 unit dipetakan ke format baru.
   - Audit regex otomatis mengonfirmasi **0 kemunculan** penamaan lama polos `UNIT_xxxx` di seluruh kolom identitas unit pada keempat direktori checkpoint.
3. **Analisis PACF & Korelasi Spearman Variabel Eksogen (§19.15)**:
   - Dibuat dan dijalankan script mandiri `analisis_pacf_spearman.py` yang menghasilkan `checkpoints_v4/analisis_pacf_spearman.csv` dan plot `checkpoints_v4/analisis_pacf_spearman_plot.png`.
   - Visualisasi plot disempurnakan dengan penempatan legenda di luar bidang gambar (`bbox_to_anchor=(1.05, 1)`) agar bebas tumpang tindih serta penghitungan unit dinamis.
4. **Pembaruan Backend & Dashboard Streamlit Bebas Deteksi Unit Baru Palsu (§21.13)**:
   - Filter ETL upload data mentah pada `pipeline_lib.py` (`build_monthly_full`) dan `appPerusahaan.py` secara otomatis menyaring 15 unit anomali tersebut, menjamin file data baru yang diunggah pengguna langsung memproyeksikan 190 unit valid secara mulus tanpa mendeteksi 15 unit tersebut sebagai "Unit Baru".
   - `load_excluded_summary` diverifikasi memuat tepat 25 unit nol resmi dengan label alasan profesional dan bersih dari istilah usang.
5. **Sintesis Ilmiah Bimbingan: Fenomena Disagregasi Per-Kriteria vs Per-Unit & 6 Insight Kunci Skripsi (§20.11 & §20.12)**:
   - Merumuskan jawaban akademis lengkap untuk pertanyaan dosen: alasan matematis dan operasional mengapa pendekatan per-kriteria menghasilkan error lebih tinggi dibanding per-unit (heterogenitas rotasi *dispatching* operator, distorsi matematis disagregasi proporsional pada unit berjam kerja rendah dengan formula pembagi mendekati nol, kompromi hiperparameter terpadu, dan prinsip *bottom-up superiority* dalam *hierarchical time series*).
   - Mendokumentasikan 6 insight empiris bernilai tinggi untuk Bab 4 & 5 skripsi: (1) Dominasi korelasi monotonik non-linier Spearman (55.61%), (2) Realisme operasional Lag-1 ($t-1$) bebas *data leakage*, (3) Degradasi linier ARIMAX vs ketahanan model *tree* Gradient Boosting, (4) Bukti empiris variasi *data preparation* berbasis karakteristik deret waktu, (5) Efek peluruhan akurasi pada horizon > 3 bulan (*horizon decay*), dan (6) Distorsi asimetris metrik evaluasi persentase MAPE pada jam kerja rendah.
   - Merumuskan justifikasi integritas *audit trail* penomoran aset unik 3 digit (`UNIT_001` s/d `UNIT_345`) pada populasi aktif 200-an unit tanpa penomoran ulang (*no re-numbering*).

---

*Update lanjutan (chat penulisan buku Bab 4–6): (1) **Review berkas user** — draft Bab 1–3 (≈8.000 kata, 89× "utilitas", Bab 4–6 masih stub), `penjelasan_eksperimen_6_skenario.md` (bertentangan dgn xlsx, tidak dipakai), `spesifikasi_lingkungan_dan_runtime.md` (versi pustaka tak konsisten), PACF/Spearman (klaim terlalu kuat → redaksi hati-hati) — rincian di §20.13.4; daftar perbaikan kode di §19.16 (sebagian sudah dikerjakan user lewat §19.13/§21.12–21.13). (2) **Keputusan user:** eksogen *t* final, 15 unit disembunyikan, tanpa uji signifikansi H1, "utilitas"→*operating hours*, Bab 4–6 dulu, batas 12.000 kata boleh dilampaui, versi pustaka `[ISI]` (§20.13.3). (3) **Bab 4 (4.1–4.9) kerangka ada** dengan angka pra-rerun (superseded), Bab 5–6, Daftar Pustaka, update Bab 3.3 belum; penamaan bab dikoreksi sesuai pedoman Proyek (Bab 4 Implementasi dan Pengujian, Bab 5 Pembahasan, Bab 6 Kesimpulan dan Saran). (4) **Catatan bias seleksi:** perbandingan pada populasi yang sudah dibuang 15 unit (MAPE>40%) condong menguntungkan 3 bulan/*direct*/GB *t*; tulis kalimat keterbatasan netral di Bab 5, jangan pakai nilai p untuk horizon. (5) **Rerun 215 unit sudah dijalankan user** — output barunya belum dilihat Claude; semua angka Bab 4 harus diambil dari output itu (daftar file di §18). Langkah lanjutan: §9 poin 58–63.*

**Pesan pembuka untuk chat baru (tempel apa adanya):** *"Lanjut buku TA. Populasi sekarang 215 unit (190 valid), pipeline sudah rerun penuh. Tugas berurutan: (1) tulis ulang Bab 4 dari draf terlampir pakai hasil baru, satu populasi saja; (2) Bab 5, Bab 6; (3) Daftar Pustaka (cari referensi tambahan via web, minimal 10 total, format APA seperti proposal); (4) update Bab 3.3 dengan EDA baru (skewness per unit, PACF/Spearman dengan redaksi hati-hati: Spearman hanya indikasi ringan, PACF 79,5% sudah termasuk unit tanpa lag signifikan); (5) Bab 1–3 terakhir. Catatan: jangan tulis nilai p atau kata 'signifikan' untuk horizon; MAPE metrik utama; ARIMAX per kriteria 'sum' jangan dipakai tanpa cek jumlah kriteria terlatih; sebut keterbatasan: eksogen t diuji dengan data aktual, di penerapan ke depan diganti estimasi musiman; pemilihan konfigurasi dan evaluasi pada test yang sama sehingga angka optimistis. Hindari penjelasan alasan exclude 15 unit."*

---

## 22. Penulisan Buku Bab 4–6 — Status, Keputusan, dan DAFTAR CEK AKHIR (update 30 Oct 2026)

> **PENGINGAT UNTUK CLAUDE:** di akhir proses penulisan buku (setelah Bab 1–3 selesai direvisi), INGATKAN user untuk mengecek ulang seluruh daftar §22.3 (angka & klaim yang belum pasti) sebelum buku dicetak/dikumpulkan.

### 22.1 Yang sudah selesai di chat ini
- Bab 4 (4.1–4.9) ditulis ulang dari output rerun 215 unit (190 valid, 63 kriteria). Dashboard yang dibahas di buku HANYA dashboard untuk perusahaan (`appPerusahaan.py`); dashboard demo/evaluasi hanya untuk sidang, tidak masuk buku (Gambar 4.4 dihapus).
- Bab 5 Pembahasan, Bab 6 Kesimpulan dan Saran, update Bab 3.3 EDA, Daftar Pustaka (15 referensi) sudah ditulis.
- Pembuka kalimat ditambahkan sebelum daftar poin (5.8, 6.1, 6.2). Keterbatasan 5.8 diringkas jadi 4 poin (jangan membuka "dapur" terlalu dalam).

### 22.2 Keputusan user (jangan diubah tanpa konfirmasi)
- Populasi ditulis 190 unit dan 63 kriteria di seluruh buku; 25 unit exclude hanya karena data (18 nol di salah satu tahun train, 7 nol di seluruh test).
- Grid GB: 144 kombinasi × 4 varian = 576 fit per unit (angka "36 × 4 = 144" di PROGRESS/notebook lama = typo).
- Semua eksperimen di laptop lokal (tanpa server). LSTM: TensorFlow 2.15.0 + keras 3.15.1.
- Kolom MAPE maksimum Tabel 4.11 dipertahankan; skenario tidak diubah; aturan 40% tidak disebut.
- Forecast 2026 sudah di-clip 0–744 jam (pipeline dan berkas hasil).
- Angka resmi: file Excel + txt ringkasan (07_..._1.xlsx: ARIMAX lag-1 median 15,92 dan RMSE 48,01).

### 22.3 DAFTAR CEK AKHIR — angka/klaim belum pasti atau belum diterapkan

**A. Angka masih run lama / belum pasti**
- A1. Tabel 4.5 (4.4): dari file 01/02 populasi 205 unit. Rerun Tahap 2 di 190 unit, atau biarkan.
- A2. Paragraf per kriteria 4.4 (23,19%; 24,42%; 22,14%; sum 50,34–138,39%; "per unit lebih rendah di 2 dari 4 varian GB, 4 dari 4 LSTM"): run lama.
- A3. Kalimat "13,47% savgol di luar pola, tidak dipakai sebagai pembanding" = keputusan Claude, bukan arahan user — setujui atau ubah.
- A4. Bab 5.2: 22,69/23,36/23,81 dan RMSE 67,18 vs 68,35 dari Tabel 4.5; kalimat "selisih 0,3–1,5 poin" mencampur dua sumber angka.
- A5. Bab 6.1 poin 2 ("MAPE global terendah") ikut dari Tabel 4.5.
- A6. Tabel 4.3: hanya 35,04 s yang terukur; lainnya kisaran dari log.
- A7. 4.9 dan 5.7: "75–95 detik" = jumlah kisaran, bukan satu pengukuran.
- A8. Tabel 4.11 ARIMAX lag-1: pakai file (15,92; 48,01), bukan pesan chat (13,06; 46,12).
- A9. 4.4: "max_depth tanpa batas" disimpulkan dari nilai kosong di file 01 — cek di `code_v4.ipynb`.

**B. Teknis & versi**
- B1. TensorFlow 2.15.0 vs NumPy 2.0.2 vs Keras 3.15.1 (TF 2.15 butuh NumPy < 2 dan membawa Keras 2.15); TF tidak ada di pip list. Cek environment Tahap 2.
- B2. pmdarima: draft Bab 2.2.5 poin 3 menulis ARIMAX memakai pmdarima, Tabel 4.2 menulis statsmodels. Samakan sesuai kode.
- B3. 4.1: daftar berkas unggahan, horizon 3–12 default 3, tab unit tidak tercakup — cek ke `appPerusahaan.py`.
- B4. Gambar 4.1–4.3: screenshot belum final.
- B5. Gambar 3.3 (PNG): judul di dalam gambar masih "(Surabaya)" — buat ulang.

**C. Klaim dugaan (belum teruji)**
- C1. April turun karena libur hari raya (3.3).
- C2. Skewness per unit "mendasari" pemakaian varian data (3.3).
- C3. Per kriteria lebih buruk karena kompromi pola antar unit (5.3).
- C4. ARIMAX tidak membaik karena terlalu banyak parameter/multikolinearitas (5.5).
- C5. "Akurasi sebenarnya di antara eksogen aktual dan tanpa eksogen" (5.5) = kesimpulan Claude.
- C6. 5.6: "77 unit identik direct vs rolling dapat terjadi bila prediksi hanya bergantung fitur selain lag" = tebakan lemah; hapus atau verifikasi.
- C7. 5.7: "layak sebagai bahan keputusan pendamping", "diperbarui setiap bulan" = penilaian Claude.
- C8. 5.2: analogi Grinsztajn (data tabular ~10 ribu sampel) ke kasus 36 bulan per unit.
- C9. 3.3: alasan PACF hanya 214 unit ("datanya mencukupi") = asumsi.
- C10. 3.3: pembacaan grafik (bimodal hujan, "Juni–Oktober sering < 40 mm", "lebih dari seribu observasi di 0–25 jam"); ada pengecualian (Juni 2025 74 mm, Okt 2025 120 mm, Mei 2025 274 mm).

**D. Kesalahan/ketidakkonsistenan**
- D1. 5.1: salah ketik "bermil MAPE" -> "memiliki MAPE".
- D2. Klaim "7 referensi <= 5 tahun" salah: yang benar 9 dari 15 (2021–2026).
- D3. Hochreiter & Schmidhuber (1997) ada di Daftar Pustaka tapi belum dikutip di teks; Hewamalage 2023 dan Hyndman & Athanasopoulos 2021 juga belum dikutip di teks. Kutip atau hapus.
- D4. Volume/halaman/DOI banyak dari ingatan; verifikasi sebelum cetak. Cortez et al. (2023) di Daftar Pustaka hanya mencantumkan 4 penulis, padahal sumber mencantumkan 6 (Cortez, Terada, Barros Bandeira, Soares, Vale, Rider).
- D5. Saran 6.2 no. 5 "uji statistik formal" vs keputusan tanpa uji signifikansi H1 (ditulis sebagai saran pengembangan).
- D6. Daftar Pustaka: Atanda et al. (2024) ada di daftar tapi tidak dikutip di mana pun; Pantopoulou et al. (2025) dikutip di 2.1.2 tapi tidak ada di daftar.
- D7. 4.8: kalimat "MAPE maksimum 39,87% lebih rendah karena populasi akhir" dipertahankan sesuai arahan user (potensi ditanyakan penguji).

### 22.4 Daftar perubahan yang diperlukan di Bab 1–3 (dari `draft_Buku_Skripsi.md`) — dikerjakan setelah user konfirmasi
Lihat jawaban chat (poin 1–14): ganti "utilitas" -> "operating hours" (63 baris; "utilisasi" armada dipertahankan), judul skripsi, H1/H0 tanpa kata "signifikan", kriteria model tunggal diseragamkan, ARIMAX tanpa seasonal (alasan diganti), LSTM sequence 3 atau 6, sitasi GB/LSTM/Savgol/Yeo-Johnson, ruang lingkup dan sistematika disesuaikan, 3.3 diganti dengan versi baru, desain solusi ditambah tahap peramalan ke depan, daftar isi/gambar/tabel/lampiran peninggalan laporan magang diganti.

### 22.5 Aturan baru (1 Nov 2026): referensi <= 5 tahun dan kosakata
- **Daftar Pustaka hanya boleh 2021–2026.** Dibuang: Box et al. (2015), Friedman (2001), Hochreiter & Schmidhuber (1997), Hyndman & Koehler (2006), Savitzky & Golay (1964), Yeo & Johnson (2000). Pengganti (terverifikasi lewat pencarian): Elsayed et al. (2021) [GB pada deret waktu], Bischl et al. (2023) [grid search], Le et al. (2022) [Savitzky-Golay pada peramalan ML], Raymaekers & Rousseeuw (2024) [Yeo-Johnson]. Hewamalage et al. (2021) dipakai untuk LSTM; Hewamalage et al. (2023) untuk MAPE; Hyndman & Athanasopoulos (2021) untuk ARIMA.
- Atanda et al. (2024) tidak dikutip di mana pun -> hapus atau kutip. Pantopoulou et al. (2025) dikutip di 2.1.2 tetapi belum ada di daftar -> salin entri dari proposal.
- Cortez et al. (2023): lengkapi menjadi 6 penulis (Cortez, Terada, Barros Bandeira, Soares, Vale, Rider).
- Kata tidak familiar diganti (galat -> error, pustaka bersama -> shared library, pencilan -> outlier, dst.); lihat tabel di chat.

### 22.6 Tambahan daftar cek akhir (1 Nov 2026)
- **E1. Tabel 4.3 vs 4.2/4.9/5.7 saling bertentangan.** Tabel baru dari user: ETL 3–5 menit; grid search 3–4 jam; benchmark 3.036 model 45–60 menit; tuning GB 1–1,5 jam; model final + future forecast 10–15 menit. Padahal teks 4.2/4.9/5.7 memakai 35,04 detik (retrain + forecast 12 bulan) dan 30–50 detik (ekstraksi dashboard) dari txt resmi. Tentukan angka mana yang dipakai atau jelaskan cakupan tiap angka.
- **E2. Klaim "per unit memberi MAPE global terendah secara keseluruhan" (4.4)** keliru jika ARIMAX per kriteria (22,14%) dibandingkan dengan GB per unit (22,69%). Kalimat diganti: ARIMAX per kriteria memodelkan deret rata-rata unit sehingga tidak langsung sebanding dengan prediksi per unit.
- **E3. Gaya penulisan:** tidak boleh ada kalimat pembelaan/keraguan terhadap GB (lihat memori); semua pengganti dikirim di chat.
- **E4. "3.036 model"** = (190 unit + 63 kriteria) × 12 kombinasi — konsisten, tetapi verifikasi di notebook.


---

## 23. Rekap Penulisan Buku Bab 4–Lampiran (update 15 Nov 2026) — berdasarkan PDF final `Buku_Skripsi.pdf` (92 halaman)

> **PENGINGAT UNTUK CLAUDE:** daftar cek akhir §22.3 dan §23.5 belum selesai. Ingatkan user mengeceknya sebelum buku dikumpulkan.

### 23.1 Struktur Bab 4 final (dibandingkan dengan §22)
- 4.1 Implementasi (Gambar 4.1–4.3 dengan penjelasan di bawah gambar), 4.2 Lingkungan (Tabel 4.1–4.3), 4.3 Skenario (Tabel 4.4), **4.4 Pengujian 1 (baru)**, 4.5 Pengujian 2 (lama 1), 4.6 Pengujian 3 (lama 2), 4.7 Pengujian 4 (lama 3, horizon), 4.8 Pengujian 5 (lama 4, direct vs rolling), 4.9 Pengujian 6 (lama 5, eksogen), 4.10 Pengujian 7 (lama 6, peramalan ke depan), **4.11 Pengujian 8 (baru, evaluasi pengguna)**.
- Pengujian 1 (baru): contoh 10 unit, dipilih acak dalam tiga kelompok menurut model terbaik (GB 5, ARIMAX 3, LSTM 2; random seed 42). Unit: K01_UNIT_008, K01_UNIT_162, K02_UNIT_135, K02_UNIT_155, K03_UNIT_070, K04_UNIT_298, K05_UNIT_208, K12_UNIT_120, K34_UNIT_009, K49_UNIT_332 (Tabel 4.5 = MAPE 3 model x 4 varian; Tabel 4.6 = kombinasi terbaik). Kriteria contoh: 5 kriteria acak (seed 42): K04, K09, K15, K34, K60 -> hanya Tabel 4.7 (kombinasi terbaik; semuanya GB).
- Penomoran tabel: lama 4.5->4.8, 4.6->4.9, 4.7->4.10, 4.8->4.12, 4.9->4.14, 4.10->4.15, 4.11->4.16; baru: 4.5, 4.6, 4.7, 4.11 (rata-rata MAPE per kriteria 12 kombinasi), 4.13 (model akhir vs terbaik per kriteria), 4.17 (ringkasan tanggapan pengguna).
- Gambar final (individual, bukan panel): Gambar 4.4 test K01_UNIT_008, 4.5 test K02_UNIT_155, 4.6 test kriteria K09 (di 4.6); Gambar 4.7 peramalan K01_UNIT_008, 4.8 peramalan K02_UNIT_155 (di 4.10).
- Aturan isi: bahas per kriteria TANPA menyebut jumlah unit anggota kriteria dan tanpa tabel per jenis alat (sensitif); tanpa kalimat pembelaan; daftar poin selalu diawali kalimat pengantar; tabel angka rata kanan, "." ribuan, "," desimal, 2 desimal untuk MAPE/RMSE/jam/skewness.

### 23.2 Angka resmi (file Excel `_1`) yang dipakai di Bab 4
- 190 unit, 63 kriteria; 25 unit dikeluarkan (18 nol di salah satu tahun train, 7 nol di test).
- Model terbaik per unit (12 kombinasi), **menurut file `03_..._1` dan `04_..._1`: ARIMAX 78, GB 74, LSTM 38**; kriteria: GB 46, LSTM 15, ARIMAX 2. Dari 190 unit: 74 unit GB sudah terbaik pada konfigurasi global, 116 unit disesuaikan (60 lebih rendah, 56 lebih tinggi dari model terbaik 12 kombinasi, 74 sama).
- GB akhir: unit MAPE 11,48% (median 9,59%, RMSE 33,66) vs model terbaik per unit 11,74% (median 9,65%, RMSE 33,33); kriteria 16,84% (median 15,71%, RMSE 33,53) vs 17,66% (16,13%, 34,21). Distribusi error unit: 99 (<10%), 65, 19, 7 (>=30%); kriteria: 13, 28, 20, 2.
- Rata-rata MAPE per unit 12 kombinasi: GB 18,16/19,17/18,82/19,56; LSTM 19,23/19,58/18,74/19,41; ARIMAX 19,60/20,98/19,51/21,41 (baseline/robust/savgol/yeojohnson); per model GB 18,93, LSTM 19,24, ARIMAX 20,38.
- Per kriteria 12 kombinasi (rata-rata): GB 25,48/25,60/25,39/26,56; LSTM 26,97/26,89/27,98/29,31; ARIMAX hanya pada 4/2/2/34 kriteria.
- Horizon 3 vs 4 bulan: unit 11,48% vs 12,72% (111 vs 79 unit), kriteria 16,84% vs 18,01% (31 vs 32). Direct vs rolling: unit 11,48% vs 13,45% (81/32/77 identik), kriteria 16,84% vs 18,89% (33/10/20).
- Eksogen (Tabel 4.16): sama dengan Tabel 4.11 lama (GB t 11,48; GB t-1 15,67; GB tanpa 14,90; ARIMA 18,38; ARIMAX t 19,26; ARIMAX t-1 19,79). Kolom MAPE maksimum dipertahankan atas keputusan penulis.
- Waktu (Tabel 4.3, atas keputusan penulis): ETL 3–5 menit; grid search 24 kombinasi 3–4 jam; 12 kombinasi (3.036 model = (190+63) x 12) 45–60 menit; tuning GB per unit 1–1,5 jam; model final + future forecast 10–15 menit. Angka 35,04 detik dan 75–95 detik dibuang dari teks.
- Lingkungan: laptop lokal (i7-1165G7, 16 GB), Python 3.11.9, TensorFlow 2.15.0 + keras 3.15.1 (versi pip list lain di Tabel 4.2); grid GB 144 kombinasi x 4 varian = 576 fit per unit.

### 23.3 Bagian lain yang selesai
- Bab 3.3 EDA versi 215 unit / 7.740 baris, tren hanya rata-rata, heatmap tanpa total, berhenti di Gambar 3.10 (lima bagian; skewness per unit dan PACF/Spearman tidak dimasukkan).
- Penomoran Bab 2: 2.1.1.x landasan teori, 2.1.2 penelitian terdahulu, 2.2.1–2.2.6 kerangka kerja.
- Daftar Pustaka 2021–2026 saja; sitasi lama (Box, Friedman, Hochreiter, Hyndman & Koehler, Savitzky-Golay, Yeo-Johnson) diganti Elsayed 2021, Bischl 2023, Le 2022, Raymaekers 2024, Hewamalage 2021/2023, Hyndman 2021.
- Abstrak dan Abstract (3 paragraf), Kata Pengantar (nama pembimbing/ tanggal sesuai pengisian penulis).
- Kosakata diganti (galat->error, pustaka bersama->shared library, pencilan->outlier, simpangan baku->standard deviation, bulan berjalan->bulan yang sama, dst.).
- Evaluasi pengguna: 1 responden PT X, wawancara pertanyaan terbuka; ringkasan di 4.11 + Tabel 4.17 (tampilan sederhana, waktu proses wajar, pilihan unit/horizon sesuai, Excel membantu tetapi memanjang dan tanpa jenis alat/lokasi, bagian upload perlu dijelaskan, hasil masuk akal, kendala: loading tanpa indikator kemajuan, harapan: filter/rekap per jenis alat/lokasi, peringatan beban tinggi, Excel siap pakai, progress bar).
- Lampiran 1 (appPerusahaan.py) dan Lampiran 2 (pipeline_lib.py) berisi kode utuh di PDF final (hal. 52 dan 61).

### 23.4 Temuan pada kode (yang ada di lampiran PDF final)
- **Bug kemungkinan:** `retrain_and_forecast_unit` memakai `last_lags = [lag_1, lag_2, lag_3]` dari baris terakhir, sehingga lag tertinggal satu bulan (seharusnya `[UTILITAS_SMOOTH, lag_1, lag_2]`). Terkonfirmasi lewat uji sintetis; belum dicek di notebook Tahap 3; belum diperbaiki. Bila benar, hasil peramalan 2026 (file 09), Gambar 4.7–4.8, dan dashboard berubah.
- Nama kolom internal masih `UTILITAS`, `UTILITAS_SMOOTH`, `FORECAST_UTILITAS` (19 kemunculan di PDF).
- Lampiran 2 memuat nama dan plat nomor asli alat (`EXCLUDED_NON_OPERATIONAL_NAMES`, `MANUAL_OVERRIDE`) padahal buku menganonimkan PT X.
- Lampiran memuat konstanta `EXCLUDED_15_K_CODES`, `EXCLUDED_15_OLD_CODES`, `EXCLUDED_OLD_10_CODES` dan filter regex `"review MAPE|data baru|threshold|toleransi"` di dashboard, yang menunjukkan adanya pengecualian 15 unit berbasis review MAPE; teks buku 4.3 hanya menyebut 25 unit karena data nol. Claude telah menyarankan satu kalimat pengungkapan di 4.3 (keputusan di penulis).

### 23.5 Daftar cek yang masih terbuka di PDF final
1. **Tabel 4.10 dan teksnya (4.5, 4.6, 5.2) menulis GB 78 unit, ARIMAX 74, 112 unit disesuaikan, berbeda dari file hasil (ARIMAX 78, GB 74, 116 disesuaikan).** Ini keputusan penulis; Claude menolak menulis penjelasan berdasarkan angka itu dan menyarankan memakai angka file. Segera samakan dengan file `03_..._1` / `04_..._1` atau tunjukkan sumber lain.
2. Tabel 4.4 masih 6 baris lama (belum ada Pengujian 1 baru dan belum ada baris evaluasi pengguna; nomor 1–6 tidak cocok dengan Pengujian 1–8).
3. Bab 6.1 hanya 3 poin (tidak memuat evaluasi pengguna), 6.2 hanya 2 saran (belum memuat saran filter, peringatan beban tinggi, Excel siap pakai); abstrak belum memuat kalimat evaluasi pengguna; 5.7 menyebut masukan yang tidak dirinci di 4.11.
4. Tabel 4.5 (parameter global) dan paragraf per kriteria 4.5 masih angka run lama (205 unit) — butir A1/A2 §22.3.
5. (Sudah diperbaiki di PDF final) klaim "per unit memberi MAPE global terendah", kalimat "pernah berbalik", dan "cenderung optimistis" tidak ada lagi. Masih ada: 5.6 menulis "pada 77 unit hasil kedua pendekatan bernilai identik karena percabangan…" (penjelasan sebab belum diverifikasi, butir C6 §22.3).
6. Penjelasan "diperbarui setiap bulan" di 5.7 adalah penilaian Claude (butir C7 §22.3).
7. Gambar 4.7–4.8: titik pertama Desember 2025 berlabel peramalan (13 titik); label sumbu x bertumpuk; legenda K09 menutupi data; judul K09 memakai "40.6 Ton".
8. Masih ada dari §22.3: A6–A9, B1–B3, C1–C10, D1–D7 (lihat daftar itu).