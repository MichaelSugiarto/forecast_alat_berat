# PENJELASAN KODE & TEMUAN PACF SERTA SPEARMAN (§20.10)

Dokumen ini melengkapi ketiadaan kode eksplisit PACF dan Spearman di notebook utama (`code_v4.ipynb`) untuk mendukung sitasi metodologi pada Subbab 3.3 dan Subbab 20.10.

---

## 1. Bukti Empiris Spearman Lebih Kuat daripada Pearson (55.6%)
- **Tujuan Analisis**: Membuktikan apakah hubungan antara *operating hours* alat berat dengan variabel eksogen (volume kontainer) bersifat linier murni (Pearson) atau non-linier monotonik (Spearman).
- **Hasil Komputasi (N = 214 Unit Alat Berat)**:
  - Pada **119 unit (55.61%)**, nilai absolut korelasi peringkat Spearman ($|r_s|$) terbukti lebih besar daripada nilai korelasi Pearson ($|r_p|$).
  - Pada **95 unit (44.39%)**, korelasi Pearson lebih besar.
- **Kesimpulan Metodologis**: Hubungan non-linier mendominasi di mayoritas armada alat berat PT X. Kondisi ini menjelaskan secara empiris mengapa model *Gradient Boosting* (yang mempartisi data berbasis ambang batas pohon keputusan non-linier) menghasilkan prediksi yang jauh lebih akurat dibanding model linier ARIMAX.

---

## 2. Bukti Empiris Keterputusan PACF pada Lag 1 s/d Lag 3 (79.9%)
- **Tujuan Analisis**: Mengidentifikasi dependensi memori temporal deret waktu *operating hours* pada masing-masing unit dengan fungsi autokorelasi parsial (PACF). Ambang batas signifikansi statistik dihitung dengan rumus:
  $$\text{Threshold} = \frac{1.96}{\sqrt{N}}$$
- **Distribusi Lag Signifikan Terakhir**:
  - **Lag 0** (tidak ada lag yang signifikan di atas ambang batas): 62 unit
  - **Lag 1**: 80 unit
  - **Lag 2**: 14 unit
  - **Lag 3**: 15 unit
  - **Lag 4**: 15 unit
  - **Lag 5**: 9 unit
  - **Lag 6**: 19 unit
- **Temuan Kunci**:
  - Sebanyak **171 dari 214 unit (79.91%)** memiliki dependensi autokorelasi parsial yang **terputus tajam pada Lag $\le 3$**.
  - Hanya sebagian kecil (~20%) yang memiliki autokorelasi parsial melampaui lag 3.
- **Kesimpulan Metodologis**:
  1. Data operasional PT X bersifat *short-memory* (memori jangka pendek 1 hingga 3 bulan), sehingga penyertaan 3 fitur kelambatan waktu (`lag_1`, `lag_2`, `lag_3`) pada *Gradient Boosting* sudah sangat optimal menangkap seluruh sinyal temporal tanpa menimbulkan *overfitting*.
  2. Ketiadaan dependensi temporal multi-tahunan menjelaskan mengapa arsitektur LSTM (*deep learning cell state*) tidak mampu mengungguli *Gradient Boosting* pada data ini.

---

## 3. Berkas Pendukung di Folder Ini:
- `analisis_pacf_spearman.py`: Skrip mandiri Python untuk menjalankan ulang perhitungan kapan saja.
- `analisis_pacf_dan_spearman.png`: Grafik visualisasi publikasi (diagram batang sebaran PACF dan diagram lingkaran proporsi Spearman).
- `analisis_pacf_spearman.csv`: Tabel detail nilai koefisien Pearson, Spearman, dan lag PACF per unit.
