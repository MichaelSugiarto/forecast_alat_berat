# DOKUMENTASI METODOLOGI EKSPERIMEN 6 SKENARIO EKSOGEN & MODEL

Dokumen ini menjelaskan rancangan komputasi, metodologi, dan konfigurasi eksperimen 6 skenario perbandingan model dan variabel eksogen (ARIMA vs ARIMAX vs Gradient Boosting; eksogen $t$, eksogen $t-1$ / *lag-1*, dan tanpa eksogen) sebagaimana dirujuk dalam Cell 103 `code_v4.ipynb` serta lembar kerja `perbandingan_eksogen_dan_model.xlsx`.

---

## 1. Latar Belakang & Tujuan Eksperimen 6 Skenario
Pengujian komparatif ini dirancang untuk menjawab pertanyaan metodologis pemodelan deret waktu:
1. Apakah penambahan variabel eksogen (curah hujan dan volume kontainer) memberikan peningkatan akurasi peramalan yang signifikan dibandingkan model univariat murni tanpa eksogen?
2. Apakah penggunaan data eksogen pada periode berjalan ($t$) menimbulkan risiko asumsi masa depan (*data leakage*) saat diimplementasikan secara operasional?
3. Apakah penggunaan eksogen yang dimundurkan satu bulan (*lag-1* atau $t-1$) mampu menghasilkan estimasi yang realistis secara operasional sekaligus mempertahankan akurasi model?
4. Bagaimana dampak variasi eksogen tersebut pada model statistik linier (ARIMA/ARIMAX) dibandingkan pada model pohon pembelajaran mesin (*Gradient Boosting*)?

---

## 2. Struktur 6 Skenario yang Diuji

| No | Skenario Model & Eksogen | Fitur Input yang Digunakan | Penjelasan Metodologis |
|:---|:---|:---|:---|
| 1 | **ARIMA Murni** (Tanpa Eksogen) | Deret target $Y_t$ saja | Model deret waktu univariat klasik berbasis autokorelasi linier internal. |
| 2 | **ARIMAX Eksogen $t$** | Deret $Y_t$ + Curah Hujan ($t$) + Container ($t$) | Model statistik linier multivariat dengan eksogen periode berjalan. |
| 3 | **ARIMAX Eksogen $t-1$ (*Lag-1*)** | Deret $Y_t$ + Curah Hujan ($t-1$) + Container ($t-1$) | Model statistik linier multivariat dengan eksogen yang dimundurkan 1 bulan ke belakang (bebas *leakage*). |
| 4 | **Gradient Boosting Murni** (Tanpa Eksogen) | `lag_1`, `lag_2`, `lag_3` dari $Y_t$ (3 fitur) | Model pohon regresi berbasis kelambatan waktu historis murni tanpa bantuan faktor eksternal. |
| 5 | **Gradient Boosting Eksogen $t$** | `lag_1..3` + Curah Hujan ($t$) + Container ($t$) (5 fitur) | Model regresi pohon dengan fitur eksogen periode berjalan. |
| 6 | **Gradient Boosting Eksogen $t-1$ (*Lag-1*)** | `lag_1..3` + Curah Hujan ($t-1$) + Container ($t-1$) (5 fitur) | Model produksi final: eksogen diketahui secara riil dari bulan sebelumnya ($t-1$), realistis operasional, bebas *leakage*. |

---

## 3. Rincian Konfigurasi Teknis Eksperimen

### 3.1 Pembagian Data Train dan Test (*Time-Based Split*)
- **Training Set**: Periode **Januari 2023 s/d September 2025** (33 bulan data historis, `TAHUN_BULAN <= '2025-09'`).
- **Test Set**: Periode **Oktober 2025 s/d Desember 2025** (3 bulan data evaluasi *out-of-sample*, `TEST_START = '2025-10'` dan `TEST_END = '2025-12'`).
- Pemisahan dilakukan secara kronologis ketat tanpa pengacakan waktu (*no shuffle*) untuk mencerminkan kondisi peramalan dunia nyata.

### 3.2 Penentuan Orde $(p, d, q)$ pada ARIMA / ARIMAX (Tetap per Varian)
- Orde ARIMA dan ARIMAX ditetapkan **tetap per varian penyesuaian data**, diambil langsung dari konfigurasi terbaik Tahap 2 (`v2_winner_per_kombinasi.xlsx`):
  - Varian `baseline`: Orde $(2, 1, 0)$
  - Varian `robust`: Orde $(2, 0, 0)$
  - Varian `savgol`: Orde $(1, 0, 0)$
  - Varian `yeojohnson`: Orde $(2, 0, 0)$
- Pemilihan orde tetap ini menjamin perbandingan *apple-to-apple* antar skenario eksogen tanpa distorsi konvergensi estimasi numerik pada deret bulanan.

### 3.3 Penentuan Parameter Gradient Boosting (Individual per Unit)
- Hiperparameter *Gradient Boosting* bersifat **individual per unit**, diambil langsung dari konfigurasi optimal hasil penyesuaian individual (`forcedgb_vs_v2b_comparison_190unit.xlsx`):
  - `learning_rate`: [0.01, 0.05, 0.1]
  - `max_iter`: [50, 100, 150]
  - `max_depth`: [3, 5, None]
  - `min_samples_leaf`: [2, 5, 10]
  - `l2_regularization`: [0.0, 1.0]
- Setiap unit menggunakan parameter terbaiknya masing-masing secara konsisten di ketiga skenario GB.

### 3.4 Cara Pembentukan Eksogen *Lag-1* di Training dan Testing
- Variabel eksogen bulanan (`CURAH_HUJAN` dan `VOLUME_CONTAINER`) digeser satu periode ke belakang menggunakan operasi *shift*:
  ```python
  exog['CH_LAG1'] = exog['CURAH_HUJAN'].shift(1).bfill()
  exog['VC_LAG1'] = exog['VOLUME_CONTAINER'].shift(1).bfill()
  ```
- Nilai awal pertama (Januari 2023) diisi menggunakan *backward fill* (`bfill()`) agar tidak terjadi kehilangan baris data (*no NaN*).
- **Pada periode uji (Test Set: Oktober, November, Desember 2025)**:
  - Bulan Oktober 2025 menggunakan data curah hujan & kontainer **September 2025**.
  - Bulan November 2025 menggunakan data curah hujan & kontainer **Oktober 2025**.
  - Bulan Desember 2025 menggunakan data curah hujan & kontainer **November 2025**.
- Karena nilai $t-1$ merupakan realisasi masa lalu yang sudah tercatat saat peramalan dilakukan, skenario ini secara metodologi **bebas dari risiko data leakage**.

### 3.5 Populasi Unit yang Dievaluasi
- Evaluasi komparatif difokuskan pada **190 unit armada alat berat valid** yang memenuhi kriteria kelayakan operasional penuh sepanjang periode observasi.

### 3.6 Random State / Seed
- `random_state = 42` diterapkan pada inisialisasi `HistGradientBoostingRegressor(random_state=42, **params)` untuk menjamin keterulangan (*reproducibility*) penuh hasil eksperimen.

---

## 4. Ringkasan Temuan Hasil Eksperimen (190 Unit Analisis)

Berdasarkan lembar kerja `perbandingan_eksogen_dan_model.xlsx`:
1. **Gradient Boosting Mengungguli ARIMA/ARIMAX di Seluruh Skenario**:
   - Rata-rata MAPE GB berada pada kisaran **11.48% – 12.01%**, jauh lebih unggul dibandingkan ARIMA/ARIMAX yang memiliki rata-rata MAPE **16.63% – 19.49%**.
2. **Kelebihan Eksogen Lag-1 ($t-1$) pada Gradient Boosting**:
   - Model **Gradient Boosting Lag-1** menghasilkan performa terbaik dan paling stabil dengan rata-rata MAPE **11.48%** dan median **8.51%**.
   - Model ini membuktikan bahwa efek aktivitas pelabuhan dan cuaca memiliki dampak tertunda (*time-lag effect*) terhadap beban kerja mesin di lapangan, sekaligus menyelesaikan kekhawatiran asumsi masa depan (*data leakage*).
