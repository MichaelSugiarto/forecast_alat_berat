# Bank Potensi Pertanyaan & Jawaban Sidang Skripsi
**Topik:** Peramalan Jam Kerja Operasional (*Operating Hours*) Alat Berat PT SPIL  
**Dokumentasi:** Penjelasan Konsep, Justifikasi Metodologi, dan Contekan Jawaban Sidang

---

## Daftar Isi
1. [Pertanyaan 1: Konversi Balik Satuan Jam pada Varian Robust dan Yeo-Johnson (Inverse Transformation)](#pertanyaan-1-konversi-balik-satuan-jam-pada-varian-robust-dan-yeo-johnson-inverse-transformation)
2. [Pertanyaan 2: Mengapa Tahap 3 (Final) Sangat Cepat (35 Detik), Padahal Tahap 2b Butuh 20–30 Menit?](#pertanyaan-2-mengapa-tahap-3-final-sangat-cepat-35-detik-padahal-tahap-2b-butuh-2030-menit)
3. [Pertanyaan 3: Mengapa Tertulis Peramalan 12 Bulan, Padahal Horizon Evaluasi Resmi Skripsi Adalah 3 Bulan?](#pertanyaan-3-mengapa-tertulis-peramalan-12-bulan-padahal-horizon-evaluasi-resmi-skripsi-adalah-3-bulan)
4. [Pertanyaan 4: Mengapa Jam Kerja Prediksi Dibatasi (Clipping) ke Rentang 0 s/d 744 Jam?](#pertanyaan-4-mengapa-jam-kerja-prediksi-dibatasi-clipping-ke-rentang-0-sd-744-jam)
5. [Pertanyaan 5: Apa Makna Kolom "MAPE Maksimum" pada Tabel 4.11 dan Mengapa Gradient Boosting Unggul Jauh dari ARIMA?](#pertanyaan-5-apa-makna-kolom-mape-maksimum-pada-tabel-411-dan-mengapa-gradient-boosting-unggul-jauh-dari-arima)

---

## Pertanyaan 1: Konversi Balik Satuan Jam pada Varian Robust dan Yeo-Johnson (Inverse Transformation)

### Kutipan Kalimat Buku Skripsi (Bab 3 / Bab 4):
> *"Keempat varian ini dilatih dan dievaluasi secara terpisah pada ketiga model (ARIMAX, Gradient Boosting, LSTM). Prediksi pada varian robust dan yeojohnson terlebih dahulu dikonversi kembali ke satuan jam sebelum RMSE dan MAPE dihitung, sehingga keempat varian dapat dibandingkan dengan ukuran yang sama."*

### Pertanyaan Dosen Penguji yang Mungkin Muncul:
> *"Apa maksud kalimat ini? Mengapa hasil prediksi model Robust dan Yeo-Johnson harus dikonversi balik ke satuan jam terlebih dahulu sebelum dihitung nilai error-nya? Kenapa tidak langsung dihitung saja?"*

### Penjelasan Konsep & Alasan Ilmiah:
Tujuan utama langkah ini adalah menerapkan prinsip **perbandingan yang adil dan setara (*fair / apple-to-apple comparison*)**.

1. **Karakteristik 4 Varian Pra-pemrosesan Data:**
   * **`baseline`**: Menggunakan data jam kerja asli (misal: 200 jam).
   * **`savgol`** (*Savitzky-Golay*): Menghaluskan noise lonjakan sesaat, namun satuannya **tetap jam** (misal: 198 jam).
   * **`robust`** (*RobustScaler*): Mengubah skala data menggunakan median dan IQR agar kebal outlier. Nilai jam kerja berubah menjadi **angka desimal kecil tanpa satuan**, misalnya **`0,45`**.
   * **`yeojohnson`** (*Power Transformation*): Mengubah distribusi data agar mendekati kurva normal (Gaussian). Nilai jam kerja berubah menjadi skala rumus logaritmik, misalnya **`4,82`**.

2. **Apa Masalahnya Jika Langsung Dihitung Tanpa Konversi Balik?**
   Misalkan jam kerja aktual di lapangan adalah **200 jam**:
   * Model `baseline` menebak **190 jam** $\rightarrow$ Selisih error: $|200 - 190| = 10\text{ jam}$ (MAPE sekitar $5\%$).
   * Model `robust` menebak **`0,45`** (karena dia dilatih pada skala desimal). Jika langsung dihitung terhadap data asli:
     $$|200 - 0,45| = 199,55\text{ jam} \quad \rightarrow \quad \text{MAPE} = 99,78\% \text{ (Salah Fatal!)}$$
   Kesalahan ini terjadi bukan karena modelnya bodoh, melainkan karena membandingkan **satuan Jam** dengan **satuan Desimal RobustScaler** (seperti membandingkan 200 Rupiah dengan 0,45 Dollar tanpa kurs).

3. **Solusi: *Inverse Transformation* (Pembalikan Rumus):**
   Sebelum rumus MAPE dan RMSE dijalankan:
   * Angka `0,45` (Robust) dikembalikan ke jam aslinya via rumus invers RobustScaler $\rightarrow$ menjadi **190 jam**.
   * Angka `4,82` (Yeo-Johnson) dikembalikan ke jam aslinya via rumus invers eksponensial $\rightarrow$ menjadi **192 jam**.

4. **Hasil Akhir:**
   Seluruh hasil tebakan dari ke-4 varian sudah sama-sama berwujud **JAM**. Dengan demikian:
   * **RMSE** semuanya murni mengukur selisih jam kerja fisik.
   * **MAPE** semuanya murni mengukur persentase meleset terhadap jam kerja sebenarnya.
   * Kita bisa menilai secara objektif apakah manipulasi matematika (Robust/Yeo-Johnson) benar-benar membantu algoritma menebak jam operasional lebih akurat daripada data mentah (Baseline).

> [!TIP]
> ### Contekan Jawaban Langsung untuk Sidang:
> *"Varian RobustScaler dan Yeo-Johnson mengubah skala data menjadi nilai non-jam untuk mempermudah algoritma belajar. Namun, sebelum performa model diuji, seluruh hasil prediksinya wajib di-inverse transform (dikonversi balik) ke skala jam kerja fisik aslinya. Hal ini memastikan bahwa metrik evaluasi MAPE dan RMSE pada Tabel 4 dihitung secara adil dan setara pada satuan fisik yang sama, yaitu jam kerja operasional lapangan."*

---

## Pertanyaan 2: Mengapa Tahap 3 (Final) Sangat Cepat (35 Detik), Padahal Tahap 2b Butuh 20–30 Menit?

### Pertanyaan Dosen Penguji:
> *"Di bab pengujian tertulis Tahap 2b butuh waktu 20–30 menit, sedangkan Tahap 3 peramalan seluruh unit selesai hanya dalam 35 detik. Padahal keduanya sama-sama memproses seluruh armada. Kenapa bisa berbeda sangat jauh?"*

### Penjelasan Teknis:

| Aspek Komputasi | Tahap 2b (Benchmark Komparatif 12 Kombinasi) | Tahap 3 (Eksekusi Model Final Terpilih) |
|---|---|---|
| **Fase / Tujuan** | **Eksplorasi Benchmark** (Mencari model juara) | **Produksi / Deployment** (Mengeksekusi 1 model juara) |
| **Model per Unit** | **12 kombinasi** per unit dan per kriteria | **Hanya 1 model** (Gradient Boosting terpilih) |
| **Model Deep Learning** | **YA** (Melatih 760 model LSTM neural network) | **TIDAK ADA** (LSTM sudah tereliminasi) |
| **Model Statistik** | **YA** (Melatih 760 model ARIMAX Kalman filter) | **TIDAK ADA** (ARIMAX sudah tereliminasi) |
| **Total Kali Fitting** | **3.036 kali fitting model** | **Hanya 190 kali fitting model** (Turun 94%) |
| **Durasi Komputasi** | **~20 – 30 menit** | **35,04 detik** |

1. **Beban Jumlah Fitting Berkurang 94%:**  
   Pada Tahap 2b, sistem harus mencoba 12 kombinasi model satu per satu pada 190 unit dan 63 kriteria ($3.036\text{ kali fit}$). Pada Tahap 3, sistem tidak lagi bereksperimen, melainkan langsung melatih 1 model pemenang per unit ($190\text{ kali fit}$).
2. **Tidak Ada Beban Iterasi Deep Learning:**  
   Sekitar 90% waktu Tahap 2b habis untuk melatih ratusan jaringan saraf tiruan LSTM (banyak epoch) dan konvergensi MLE ARIMAX. Pada Tahap 3, kedua model tersebut sudah tidak dipakai.
3. **Kecepatan Mesin `HistGradientBoostingRegressor`:**  
   Algoritma Gradient Boosting Scikit-Learn berbasis bahasa C/Cython yang sangat optimal. Melatih 1 model pohon pada 36 baris data bulanan hanya membutuhkan waktu **~0,058 detik (58 milidetik) per unit**. Mengulang proses ini untuk 190 unit hanya butuh ~11–28 detik komputasi murni.

> [!TIP]
> ### Contekan Jawaban Langsung untuk Sidang:
> *"Tahap 2b membutuhkan waktu sekitar 20–30 menit karena sistem melakukan benchmark massal sebanyak 3.036 fitting model, termasuk pelatihan ratusan model deep learning LSTM dan ARIMAX. Sebaliknya, pada Tahap 3 (deployment operasional), sistem hanya mengeksekusi 190 model Gradient Boosting terpilih yang sangat ringan dan efisien secara komputasi tanpa beban iterasi neural network, sehingga seluruh armada selesai diproses dalam 35,04 detik."*

---

## Pertanyaan 3: Mengapa Tertulis Peramalan 12 Bulan, Padahal Horizon Evaluasi Resmi Skripsi Adalah 3 Bulan?

### Pertanyaan Dosen Penguji:
> *"Di Bab 4 disimpulkan bahwa horizon peramalan terbaik adalah 3 bulan. Tetapi kenapa pada spesifikasi sistem dan file proyeksi masa depan tertulis 12 bulan (Januari–Desember 2026)?"*

### Penjelasan Akademis vs Kebutuhan Industri:
Ada perbedaan fokus antara **ketelitian akademis** dan **kebutuhan operasional perusahaan**:

1. **Secara Akademis Skripsi (Fokus Utama: 3 Bulan):**
   * Berdasarkan Tabel 4.9, evaluasi empiris membuktikan horizon 3 bulan menghasilkan error paling rendah (MAPE 11,48%) dibandingkan horizon yang lebih panjang.
   * Di dashboard sidang ([`appDemo.py`](file:///d:/SPIL%20Michael/Folder%20TA/t%20a/appDemo.py)), slider disetel default ke **3 bulan** (Januari–Maret 2026) dengan peringatan ilmiah: *"Semakin panjang horizon, potensi akumulasi error semakin besar"*.
2. **Secara Kebutuhan Industri PT SPIL (Kebutuhan Tahunan: 12 Bulan):**
   * Pihak manajemen PT SPIL membutuhkan estimasi kasar jam kerja armada untuk penyusunan anggaran biaya operasional dan pemeliharaan (*budgeting*) **1 tahun kalender penuh (12 bulan)**.
   * Oleh karena itu, arsitektur pipeline dirancang fleksibel dengan slider 3 s/d 12 bulan.
3. **Durasi Waktu Run 35,04 Detik:**
   * Angka 35,04 detik adalah hasil uji performa pada **skenario maksimal 12 bulan**. Jika hanya memproyeksikan 3 bulan, waktunya bahkan lebih cepat (~25–30 detik).

> [!TIP]
> ### Contekan Jawaban Langsung untuk Sidang:
> *"Skenario evaluasi resmi skripsi tetap berpegang teguh pada horizon 3 bulan karena terbukti paling akurat secara statistik. Namun, sistem pipeline dan dashboard dirancang fleksibel mampu melakukan peramalan rolling hingga 12 bulan untuk mengakomodasi kebutuhan manajemen PT SPIL dalam menyusun estimasi anggaran operasional tahunan armada."*

---

## Pertanyaan 4: Mengapa Jam Kerja Prediksi Dibatasi (Clipping) ke Rentang 0 s/d 744 Jam?

### Pertanyaan Dosen Penguji:
> *"Mengapa pada fungsi peramalan masa depan ditambahkan pemotongan nilai (clipping) antara 0 dan 744 jam? Apakah ini manipulasi data?"*

### Penjelasan Batasan Fisik (*Domain Knowledge Constraints*):
Penambahan batas tersebut **bukan manipulasi**, melainkan **penerapan batasan fisik dunia nyata (*physical reality constraints*)**:
1. **Batas Bawah (0 Jam):**  
   Alat berat tidak mungkin beroperasi dengan jam kerja bernilai negatif. Jika model pohon regresi mengekstrapolasikan tren penurunan tajam hingga bernilai minus (misal $-3,61$ jam), nilai tersebut secara fisik berarti alat sedang dalam kondisi **mati total / menganggur (*idle*)**, sehingga dibulatkan secara logis ke **0,00 jam**.
2. **Batas Atas (744 Jam):**  
   Secara kalender, jumlah jam maksimal dalam 1 bulan (31 hari) adalah:
   $$31 \text{ hari} \times 24 \text{ jam/hari} = 744 \text{ jam}$$
   Alat berat yang beroperasi tanpa henti 24/7 sekalipun tidak akan pernah melampaui 744 jam sebulan. Prediksi regresi yang melebihi 744 jam dipotong ke batas fisik maksimumnya, yaitu **744,00 jam**.

> [!TIP]
> ### Contekan Jawaban Langsung untuk Sidang:
> *"Pemotongan rentang 0 hingga 744 jam merupakan post-processing wajib untuk menjamin validitas fisik operasional. Jam kerja tidak mungkin bernilai negatif (dibatasi 0 jam sebagai kondisi idle) dan tidak mungkin melampaui kapasitas kalender fisik 24 jam x 31 hari = 744 jam per bulan. Hal ini mencegah dashboard menampilkan angka yang mustahil secara operasional."*

---

## Pertanyaan 5: Apa Makna Kolom "MAPE Maksimum" pada Tabel 4.11 dan Mengapa Gradient Boosting Unggul Jauh dari ARIMA?

### Pertanyaan Dosen Penguji:
> *"Pada Tabel 4.11 perbandingan model, untuk apa ditampilkan kolom 'MAPE Maksimum'? Apa interpretasi perbandingannya antara Gradient Boosting dengan ARIMA?"*

### Penjelasan Empiris:
* **Definisi:** Dari 190 unit yang dievaluasi, selain menghitung rata-rata (*Mean*) dan nilai tengah (*Median*), metrik **Max MAPE** mencatat **persentase error paling buruk yang terjadi pada 1 unit terburuk** di model tersebut.
* **Perbandingan Angka Nyata Tabel 4.11:**
  * **Gradient Boosting (Eksogen $t$):** Mean MAPE = **11,48%**, Max MAPE = **39,87%**
  * **ARIMA Murni:** Mean MAPE = **18,38%**, Max MAPE = **126,99%**
  * **ARIMAX (Lag-1):** Mean MAPE = **19,79%**, Max MAPE = **96,92%**
* **Interpretasi Bisnis & Operasional:**
  * Model ARIMA memiliki risiko operasional tinggi karena pada unit tertentu tebakannya meleset liar hingga **126,99%** (salah lebih dari 2 kali lipat).
  * Sebaliknya, Gradient Boosting terbukti **sangat stabil dan aman bagi perusahaan**, karena pada unit yang paling meleset sekalipun, error-nya **hanya 39,87%** (tidak pernah menghasilkan prediksi ekstrem).

> [!TIP]
> ### Contekan Jawaban Langsung untuk Sidang:
> *"Kolom MAPE Maksimum disajikan untuk mengevaluasi parameter risiko terburuk (worst-case scenario) dari model peramalan. Hasil evaluasi membuktikan model Gradient Boosting jauh lebih stabil dan andal untuk operasional perusahaan dengan error unit terburuk hanya 39,87%, dibandingkan ARIMA murni yang pada unit tertentu menghasilkan error ekstrem hingga 126,99%."*
