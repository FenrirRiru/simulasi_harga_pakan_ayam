# Aplikasi Simulasi Biaya Pakan untuk Memaksimalkan Margin Keuntungan Usaha Ternak Ayam Kampung

Aplikasi Python untuk membantu peternak ayam kampung dalam menganalisis dan mengoptimalkan profitabilitas usaha ternak mereka melalui simulasi berbagai skenario bisnis.

## Fitur Utama

### 1. Perhitungan Keuangan
- **Total Biaya Pakan**: Menghitung total konsumsi dan biaya pakan
- **Total Pendapatan**: Menghitung pendapatan dari penjualan ayam
- **Margin Keuntungan**: Menghitung keuntungan absolut dan persentase
- **Break Even Point (BEP)**: Menentukan jumlah ayam minimum untuk tidak rugi
- **Return on Investment (ROI)**: Menghitung tingkat pengembalian investasi

### 2. Simulasi Skenario
- **Simulasi Perubahan Harga Pakan**: Analisis sensitivitas terhadap perubahan harga pakan (±10%, ±20%)
- **Simulasi Perubahan Harga Jual**: Analisis sensitivitas terhadap perubahan harga jual (±10%, ±20%)
- **Simulasi Kombinasi**: Analisis kombinasi perubahan harga pakan dan harga jual

### 3. Optimasi
- **Hitung Jumlah Ayam untuk Target Profit**: Menentukan jumlah ayam yang diperlukan untuk mencapai target profit tertentu
- **Analisis Sensitivitas Jumlah Ayam**: Menganalisis pengaruh perubahan jumlah ayam terhadap profitabilitas
- **Cari Jumlah Ayam Optimal**: Mencari jumlah ayam yang memberikan profit maksimum

### 4. Visualisasi
- Grafik keuntungan, margin, dan ROI vs perubahan harga
- Grafik analisis sensitivitas jumlah ayam
- Heatmap kombinasi harga pakan dan harga jual

### 5. Export Data
- Export hasil perhitungan ke CSV dan Excel (.xlsx)
- Simpan grafik visualisasi sebagai gambar PNG
- Format Excel dengan auto-adjust column widths untuk kemudahan membaca

### 6. Web Interface (Streamlit)
- Interface web modern yang dapat diakses melalui browser Chrome
- Input parameter melalui sidebar yang user-friendly
- Visualisasi grafik langsung di browser
- Download hasil dengan satu klik
- Real-time update saat parameter berubah

## Requirements

- Python 3.7 atau lebih tinggi
- pandas >= 2.0.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- numpy >= 1.24.0
- openpyxl >= 3.1.0 (untuk export Excel)
- streamlit >= 1.28.0 (untuk web UI)

## Instalasi

1. Clone atau download repository ini
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Cara Penggunaan

### Opsi 1: Web Interface (Recommended)

Aplikasi dapat dijalankan melalui browser Chrome dengan interface web yang modern dan user-friendly:

**Windows:**
```bash
run_web.bat
```

**Linux/Mac:**
```bash
chmod +x run_web.sh
./run_web.sh
```

**Atau langsung dengan Streamlit:**
```bash
venv\Scripts\activate
```
```bash
streamlit run streamlit_app.py
```

Aplikasi akan otomatis membuka di browser default Anda (Chrome). Jika tidak terbuka otomatis, buka browser dan akses:
- **URL**: `http://localhost:8501`

**Fitur Web Interface:**
- ✅ Interface modern dan responsif
- ✅ Input parameter melalui sidebar
- ✅ Visualisasi grafik langsung di browser
- ✅ Download hasil ke CSV/Excel dengan satu klik
- ✅ Tab terorganisir untuk berbagai fitur
- ✅ Real-time update saat parameter berubah
- ✅ Tampilan metrik yang informatif dengan warna indikator

### Opsi 2: Command Line Interface (CLI)

Untuk penggunaan melalui terminal/command prompt:

```bash
python main.py
```

### Input Parameter

Saat pertama kali menjalankan aplikasi, Anda akan diminta untuk memasukkan parameter berikut:

1. **Jumlah ayam (ekor)**: Jumlah ayam yang akan dipelihara
2. **Harga pakan per kg (Rp)**: Harga pakan per kilogram
3. **Konsumsi pakan per ekor per hari (gram)**: Rata-rata konsumsi pakan per ekor per hari
4. **Periode pemeliharaan (hari)**: Lama periode pemeliharaan
5. **Harga jual ayam per kg (Rp)**: Harga jual ayam per kilogram
6. **Bobot akhir rata-rata (kg)**: Bobot akhir rata-rata per ekor
7. **Biaya operasional lain (Rp)**: Biaya operasional selain pakan (listrik, air, dll)

**Catatan**: Setiap parameter memiliki nilai default yang bisa digunakan dengan menekan Enter.

### Menu Utama

Setelah memasukkan parameter, Anda akan melihat menu utama dengan opsi berikut:

1. **Tampilkan Ringkasan Perhitungan**: Menampilkan semua hasil perhitungan dalam format tabel
2. **Simulasi Skenario**: Menjalankan berbagai simulasi perubahan harga
3. **Optimasi**: Fitur optimasi untuk memaksimalkan profit
4. **Recomendasi Strategi**: Mendapatkan rekomendasi strategi untuk memaksimalkan profit
5. **Export Ringkasan ke CSV/Excel**: Menyimpan hasil perhitungan ke file CSV dan Excel
6. **Ubah Parameter Input**: Mengubah parameter input yang telah dimasukkan
7. **Keluar**: Keluar dari aplikasi

### Menu Simulasi Skenario

1. **Simulasi Perubahan Harga Pakan**: Menganalisis dampak perubahan harga pakan (-20%, -10%, 0%, +10%, +20%)
2. **Simulasi Perubahan Harga Jual**: Menganalisis dampak perubahan harga jual (-20%, -10%, 0%, +10%, +20%)
3. **Simulasi Kombinasi**: Menganalisis kombinasi perubahan harga pakan dan harga jual

Setiap simulasi akan menghasilkan:
- Tabel hasil perhitungan
- Grafik visualisasi (disimpan di folder `output/`)
- File CSV dan Excel dengan data lengkap (disimpan di folder `output/`)

### Menu Optimasi

1. **Hitung Jumlah Ayam untuk Target Profit**: Menghitung jumlah ayam yang diperlukan untuk mencapai target profit tertentu
2. **Analisis Sensitivitas Jumlah Ayam**: Menganalisis profitabilitas untuk berbagai jumlah ayam
3. **Cari Jumlah Ayam Optimal**: Mencari jumlah ayam yang memberikan profit maksimum

## Struktur Proyek

```
simulasi_harga_pakan/
│
├── main.py                 # File utama dengan CLI interface
├── streamlit_app.py        # File aplikasi web dengan Streamlit UI (untuk browser Chrome)
├── run_web.bat            # Script untuk menjalankan web app di Windows
├── run_web.sh             # Script untuk menjalankan web app di Linux/Mac
├── calculations.py          # Modul perhitungan keuangan
├── simulation.py           # Modul simulasi skenario
├── optimization.py         # Modul optimasi
├── visualization.py        # Modul visualisasi grafik
├── requirements.txt        # Dependencies Python
├── README.md              # Dokumentasi
└── output/                # Folder output (dibuat otomatis)
    ├── *.csv              # File CSV hasil perhitungan
    ├── *.xlsx             # File Excel hasil perhitungan
    └── *.png              # File gambar grafik
```

## Contoh Penggunaan

### Contoh 1: Perhitungan Dasar

```
Jumlah ayam: 100 ekor
Harga pakan: Rp 12.000/kg
Konsumsi pakan: 100 gram/ekor/hari
Periode: 90 hari
Harga jual: Rp 35.000/kg
Bobot akhir: 1.5 kg/ekor
Biaya operasional: Rp 500.000
```

Aplikasi akan menghitung:
- Total konsumsi pakan: 900 kg
- Total biaya pakan: Rp 10.800.000
- Total pendapatan: Rp 5.250.000
- Keuntungan: Rp -5.550.000 (rugi)
- Margin: -105.71%
- BEP: 75 ekor

### Contoh 2: Simulasi Perubahan Harga

Dengan simulasi perubahan harga pakan, Anda dapat melihat bagaimana perubahan harga pakan mempengaruhi profitabilitas. Misalnya, jika harga pakan naik 20%, profit akan turun sebesar X%.

### Contoh 3: Optimasi Jumlah Ayam

Jika target profit adalah Rp 5.000.000, aplikasi akan menghitung bahwa diperlukan sekitar 200 ekor ayam (tergantung parameter lainnya).

## Output

Semua output (grafik dan CSV) akan disimpan di folder `output/` dengan nama file yang mencakup timestamp untuk menghindari overwrite.

Format nama file:
- `ringkasan_perhitungan_YYYYMMDD_HHMMSS.csv` dan `.xlsx`
- `simulasi_harga_pakan_YYYYMMDD_HHMMSS.png`, `.csv`, dan `.xlsx`
- `simulasi_harga_jual_YYYYMMDD_HHMMSS.png`, `.csv`, dan `.xlsx`
- `simulasi_kombinasi_YYYYMMDD_HHMMSS.png`, `.csv`, dan `.xlsx`
- `sensitivitas_jumlah_ayam_YYYYMMDD_HHMMSS.png`, `.csv`, dan `.xlsx`
- dll.

## Catatan Penting

1. **Akurasi Data**: Pastikan parameter input yang dimasukkan akurat untuk mendapatkan hasil yang reliable
2. **Asumsi**: Aplikasi ini menggunakan asumsi bahwa semua ayam bertahan hidup hingga akhir periode
3. **Biaya Lain**: Pastikan semua biaya operasional sudah termasuk dalam "Biaya operasional lain"
4. **Harga Pasar**: Harga pakan dan harga jual dapat berfluktuasi, gunakan simulasi untuk memahami risiko

## Pengembangan

Aplikasi ini dikembangkan dengan struktur modular untuk memudahkan pengembangan lebih lanjut:

- `calculations.py`: Logika perhitungan bisnis
- `simulation.py`: Logika simulasi skenario
- `optimization.py`: Logika optimasi
- `visualization.py`: Logika visualisasi
- `main.py`: Interface pengguna

## Lisensi

Aplikasi ini dibuat untuk keperluan akademis dan dapat digunakan secara bebas.

## Kontribusi

Kontribusi untuk meningkatkan aplikasi ini sangat diterima. Silakan buat issue atau pull request.

## Penulis

Dikembangkan untuk membantu peternak ayam kampung dalam mengoptimalkan profitabilitas usaha mereka.

---

**Selamat menggunakan aplikasi Simulasi Biaya Pakan!**
