"""
Modul untuk perhitungan biaya, pendapatan, dan profitabilitas usaha ternak ayam kampung.
"""

import numpy as np


class PakanCalculator:
    """
    Kelas untuk menghitung berbagai metrik keuangan usaha ternak ayam kampung.
    """
    
    def __init__(self, jumlah_ayam, harga_pakan_per_kg, konsumsi_pakan_per_ekor_hari,
                 periode_pemeliharaan, harga_jual_per_kg, bobot_akhir_rata_rata,
                 biaya_operasional_lain):
        """
        Inisialisasi parameter input.
        
        Parameters:
        -----------
        jumlah_ayam : int
            Jumlah ayam dalam ekor
        harga_pakan_per_kg : float
            Harga pakan per kilogram dalam Rupiah
        konsumsi_pakan_per_ekor_hari : float
            Konsumsi pakan per ekor per hari dalam gram
        periode_pemeliharaan : int
            Periode pemeliharaan dalam hari
        harga_jual_per_kg : float
            Harga jual ayam per kilogram dalam Rupiah
        bobot_akhir_rata_rata : float
            Bobot akhir rata-rata per ekor dalam kilogram
        biaya_operasional_lain : float
            Biaya operasional lain-lain dalam Rupiah
        """
        self.jumlah_ayam = jumlah_ayam
        self.harga_pakan_per_kg = harga_pakan_per_kg
        self.konsumsi_pakan_per_ekor_hari = konsumsi_pakan_per_ekor_hari
        self.periode_pemeliharaan = periode_pemeliharaan
        self.harga_jual_per_kg = harga_jual_per_kg
        self.bobot_akhir_rata_rata = bobot_akhir_rata_rata
        self.biaya_operasional_lain = biaya_operasional_lain
    
    def hitung_total_konsumsi_pakan(self):
        """
        Menghitung total konsumsi pakan dalam kilogram.
        
        Returns:
        --------
        float : Total konsumsi pakan dalam kg
        """
        konsumsi_per_ekor_kg = (self.konsumsi_pakan_per_ekor_hari * self.periode_pemeliharaan) / 1000
        total_konsumsi_kg = konsumsi_per_ekor_kg * self.jumlah_ayam
        return total_konsumsi_kg
    
    def hitung_total_biaya_pakan(self):
        """
        Menghitung total biaya pakan.
        
        Returns:
        --------
        float : Total biaya pakan dalam Rupiah
        """
        total_konsumsi_kg = self.hitung_total_konsumsi_pakan()
        total_biaya_pakan = total_konsumsi_kg * self.harga_pakan_per_kg
        return total_biaya_pakan
    
    def hitung_total_biaya(self):
        """
        Menghitung total biaya (pakan + operasional).
        
        Returns:
        --------
        float : Total biaya dalam Rupiah
        """
        total_biaya_pakan = self.hitung_total_biaya_pakan()
        total_biaya = total_biaya_pakan + self.biaya_operasional_lain
        return total_biaya
    
    def hitung_total_pendapatan(self):
        """
        Menghitung total pendapatan dari penjualan ayam.
        
        Returns:
        --------
        float : Total pendapatan dalam Rupiah
        """
        total_bobot_kg = self.jumlah_ayam * self.bobot_akhir_rata_rata
        total_pendapatan = total_bobot_kg * self.harga_jual_per_kg
        return total_pendapatan
    
    def hitung_keuntungan(self):
        """
        Menghitung keuntungan absolut.
        
        Returns:
        --------
        float : Keuntungan dalam Rupiah
        """
        total_pendapatan = self.hitung_total_pendapatan()
        total_biaya = self.hitung_total_biaya()
        keuntungan = total_pendapatan - total_biaya
        return keuntungan
    
    def hitung_margin_keuntungan_persen(self):
        """
        Menghitung margin keuntungan dalam persentase.
        
        Returns:
        --------
        float : Margin keuntungan dalam persen
        """
        total_pendapatan = self.hitung_total_pendapatan()
        if total_pendapatan == 0:
            return 0
        keuntungan = self.hitung_keuntungan()
        margin_persen = (keuntungan / total_pendapatan) * 100
        return margin_persen
    
    def hitung_break_even_point(self):
        """
        Menghitung Break Even Point (BEP) dalam jumlah ekor ayam.
        BEP adalah jumlah ayam minimum yang harus dipelihara agar tidak rugi.
        
        Returns:
        --------
        float : Jumlah ayam untuk BEP
        """
        # Biaya per ekor
        konsumsi_per_ekor_kg = (self.konsumsi_pakan_per_ekor_hari * self.periode_pemeliharaan) / 1000
        biaya_pakan_per_ekor = konsumsi_per_ekor_kg * self.harga_pakan_per_kg
        pendapatan_per_ekor = self.bobot_akhir_rata_rata * self.harga_jual_per_kg
        
        # Jika pendapatan per ekor <= biaya per ekor, tidak ada BEP
        if pendapatan_per_ekor <= biaya_pakan_per_ekor:
            return np.inf
        
        # BEP = biaya operasional / (pendapatan per ekor - biaya pakan per ekor)
        bep = self.biaya_operasional_lain / (pendapatan_per_ekor - biaya_pakan_per_ekor)
        return max(0, bep)
    
    def hitung_roi(self):
        """
        Menghitung Return on Investment (ROI) dalam persentase.
        
        Returns:
        --------
        float : ROI dalam persen
        """
        total_biaya = self.hitung_total_biaya()
        if total_biaya == 0:
            return 0
        keuntungan = self.hitung_keuntungan()
        roi = (keuntungan / total_biaya) * 100
        return roi
    
    def get_summary(self):
        """
        Mengembalikan ringkasan semua perhitungan dalam bentuk dictionary.
        
        Returns:
        --------
        dict : Dictionary berisi semua hasil perhitungan
        """
        return {
            'Jumlah Ayam (ekor)': self.jumlah_ayam,
            'Harga Pakan per kg (Rp)': self.harga_pakan_per_kg,
            'Konsumsi Pakan per ekor/hari (gram)': self.konsumsi_pakan_per_ekor_hari,
            'Periode Pemeliharaan (hari)': self.periode_pemeliharaan,
            'Harga Jual per kg (Rp)': self.harga_jual_per_kg,
            'Bobot Akhir Rata-rata (kg)': self.bobot_akhir_rata_rata,
            'Biaya Operasional Lain (Rp)': self.biaya_operasional_lain,
            'Total Konsumsi Pakan (kg)': round(self.hitung_total_konsumsi_pakan(), 2),
            'Total Biaya Pakan (Rp)': round(self.hitung_total_biaya_pakan(), 2),
            'Total Biaya (Rp)': round(self.hitung_total_biaya(), 2),
            'Total Pendapatan (Rp)': round(self.hitung_total_pendapatan(), 2),
            'Keuntungan (Rp)': round(self.hitung_keuntungan(), 2),
            'Margin Keuntungan (%)': round(self.hitung_margin_keuntungan_persen(), 2),
            'Break Even Point (ekor)': round(self.hitung_break_even_point(), 2),
            'ROI (%)': round(self.hitung_roi(), 2)
        }
