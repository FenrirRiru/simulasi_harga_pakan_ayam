"""
Modul untuk optimasi jumlah ayam berdasarkan target profit.
"""

import numpy as np
from calculations import PakanCalculator


class ProfitOptimizer:
    """
    Kelas untuk optimasi jumlah ayam berdasarkan target profit.
    """
    
    def __init__(self, base_calculator):
        """
        Inisialisasi dengan kalkulator dasar.
        
        Parameters:
        -----------
        base_calculator : PakanCalculator
            Kalkulator dengan parameter dasar
        """
        self.base_calculator = base_calculator
    
    def hitung_jumlah_ayam_untuk_profit(self, target_profit):
        """
        Menghitung jumlah ayam yang diperlukan untuk mencapai target profit.
        
        Parameters:
        -----------
        target_profit : float
            Target profit dalam Rupiah
        
        Returns:
        --------
        float : Jumlah ayam yang diperlukan
        """
        # Biaya per ekor
        konsumsi_per_ekor_kg = (self.base_calculator.konsumsi_pakan_per_ekor_hari * 
                                self.base_calculator.periode_pemeliharaan) / 1000
        biaya_pakan_per_ekor = konsumsi_per_ekor_kg * self.base_calculator.harga_pakan_per_kg
        pendapatan_per_ekor = (self.base_calculator.bobot_akhir_rata_rata * 
                              self.base_calculator.harga_jual_per_kg)
        
        # Profit per ekor
        profit_per_ekor = pendapatan_per_ekor - biaya_pakan_per_ekor
        
        # Jika profit per ekor <= 0, tidak mungkin mencapai target profit
        if profit_per_ekor <= 0:
            return np.inf
        
        # Jumlah ayam = (target profit + biaya operasional) / profit per ekor
        jumlah_ayam = (target_profit + self.base_calculator.biaya_operasional_lain) / profit_per_ekor
        return max(0, jumlah_ayam)
    
    def analisis_sensitivitas_jumlah_ayam(self, range_jumlah_ayam):
        """
        Analisis sensitivitas profit terhadap perubahan jumlah ayam.
        
        Parameters:
        -----------
        range_jumlah_ayam : list atau numpy array
            Range jumlah ayam untuk dianalisis
        
        Returns:
        --------
        dict : Dictionary berisi hasil analisis
        """
        results = {
            'Jumlah Ayam': [],
            'Total Biaya (Rp)': [],
            'Total Pendapatan (Rp)': [],
            'Keuntungan (Rp)': [],
            'Margin Keuntungan (%)': [],
            'ROI (%)': []
        }
        
        for jumlah in range_jumlah_ayam:
            calculator = PakanCalculator(
                jumlah_ayam=int(jumlah),
                harga_pakan_per_kg=self.base_calculator.harga_pakan_per_kg,
                konsumsi_pakan_per_ekor_hari=self.base_calculator.konsumsi_pakan_per_ekor_hari,
                periode_pemeliharaan=self.base_calculator.periode_pemeliharaan,
                harga_jual_per_kg=self.base_calculator.harga_jual_per_kg,
                bobot_akhir_rata_rata=self.base_calculator.bobot_akhir_rata_rata,
                biaya_operasional_lain=self.base_calculator.biaya_operasional_lain
            )
            
            results['Jumlah Ayam'].append(int(jumlah))
            results['Total Biaya (Rp)'].append(round(calculator.hitung_total_biaya(), 2))
            results['Total Pendapatan (Rp)'].append(round(calculator.hitung_total_pendapatan(), 2))
            results['Keuntungan (Rp)'].append(round(calculator.hitung_keuntungan(), 2))
            results['Margin Keuntungan (%)'].append(round(calculator.hitung_margin_keuntungan_persen(), 2))
            results['ROI (%)'].append(round(calculator.hitung_roi(), 2))
        
        return results
    
    def cari_jumlah_ayam_optimal(self, min_ayam=1, max_ayam=10000, step=10):
        """
        Mencari jumlah ayam optimal yang memberikan profit maksimum.
        
        Parameters:
        -----------
        min_ayam : int
            Jumlah ayam minimum
        max_ayam : int
            Jumlah ayam maksimum
        step : int
            Langkah increment untuk pencarian
        
        Returns:
        --------
        dict : Dictionary berisi jumlah ayam optimal dan profit maksimum
        """
        max_profit = float('-inf')
        optimal_jumlah = min_ayam
        
        for jumlah in range(min_ayam, max_ayam + 1, step):
            calculator = PakanCalculator(
                jumlah_ayam=jumlah,
                harga_pakan_per_kg=self.base_calculator.harga_pakan_per_kg,
                konsumsi_pakan_per_ekor_hari=self.base_calculator.konsumsi_pakan_per_ekor_hari,
                periode_pemeliharaan=self.base_calculator.periode_pemeliharaan,
                harga_jual_per_kg=self.base_calculator.harga_jual_per_kg,
                bobot_akhir_rata_rata=self.base_calculator.bobot_akhir_rata_rata,
                biaya_operasional_lain=self.base_calculator.biaya_operasional_lain
            )
            
            profit = calculator.hitung_keuntungan()
            if profit > max_profit:
                max_profit = profit
                optimal_jumlah = jumlah
        
        return {
            'Jumlah Ayam Optimal': optimal_jumlah,
            'Profit Maksimum (Rp)': round(max_profit, 2)
        }
