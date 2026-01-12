"""
Modul untuk simulasi skenario perubahan harga pakan dan harga jual.
"""

import pandas as pd
import numpy as np
from calculations import PakanCalculator


class ScenarioSimulator:
    """
    Kelas untuk melakukan simulasi berbagai skenario perubahan harga.
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
    
    def simulasi_perubahan_harga_pakan(self, persentase_perubahan=[-20, -10, 0, 10, 20]):
        """
        Simulasi perubahan harga pakan dengan berbagai persentase.
        
        Parameters:
        -----------
        persentase_perubahan : list
            List persentase perubahan harga pakan (misalnya [-20, -10, 0, 10, 20])
        
        Returns:
        --------
        pd.DataFrame : DataFrame berisi hasil simulasi
        """
        results = []
        
        for persen in persentase_perubahan:
            harga_pakan_baru = self.base_calculator.harga_pakan_per_kg * (1 + persen / 100)
            
            calculator = PakanCalculator(
                jumlah_ayam=self.base_calculator.jumlah_ayam,
                harga_pakan_per_kg=harga_pakan_baru,
                konsumsi_pakan_per_ekor_hari=self.base_calculator.konsumsi_pakan_per_ekor_hari,
                periode_pemeliharaan=self.base_calculator.periode_pemeliharaan,
                harga_jual_per_kg=self.base_calculator.harga_jual_per_kg,
                bobot_akhir_rata_rata=self.base_calculator.bobot_akhir_rata_rata,
                biaya_operasional_lain=self.base_calculator.biaya_operasional_lain
            )
            
            summary = calculator.get_summary()
            summary['Perubahan Harga Pakan (%)'] = persen
            summary['Harga Pakan Baru (Rp)'] = round(harga_pakan_baru, 2)
            results.append(summary)
        
        df = pd.DataFrame(results)
        return df
    
    def simulasi_perubahan_harga_jual(self, persentase_perubahan=[-20, -10, 0, 10, 20]):
        """
        Simulasi perubahan harga jual dengan berbagai persentase.
        
        Parameters:
        -----------
        persentase_perubahan : list
            List persentase perubahan harga jual (misalnya [-20, -10, 0, 10, 20])
        
        Returns:
        --------
        pd.DataFrame : DataFrame berisi hasil simulasi
        """
        results = []
        
        for persen in persentase_perubahan:
            harga_jual_baru = self.base_calculator.harga_jual_per_kg * (1 + persen / 100)
            
            calculator = PakanCalculator(
                jumlah_ayam=self.base_calculator.jumlah_ayam,
                harga_pakan_per_kg=self.base_calculator.harga_pakan_per_kg,
                konsumsi_pakan_per_ekor_hari=self.base_calculator.konsumsi_pakan_per_ekor_hari,
                periode_pemeliharaan=self.base_calculator.periode_pemeliharaan,
                harga_jual_per_kg=harga_jual_baru,
                bobot_akhir_rata_rata=self.base_calculator.bobot_akhir_rata_rata,
                biaya_operasional_lain=self.base_calculator.biaya_operasional_lain
            )
            
            summary = calculator.get_summary()
            summary['Perubahan Harga Jual (%)'] = persen
            summary['Harga Jual Baru (Rp)'] = round(harga_jual_baru, 2)
            results.append(summary)
        
        df = pd.DataFrame(results)
        return df
    
    def simulasi_kombinasi(self, persentase_pakan=[-20, -10, 0, 10, 20],
                          persentase_jual=[-20, -10, 0, 10, 20]):
        """
        Simulasi kombinasi perubahan harga pakan dan harga jual.
        
        Parameters:
        -----------
        persentase_pakan : list
            List persentase perubahan harga pakan
        persentase_jual : list
            List persentase perubahan harga jual
        
        Returns:
        --------
        pd.DataFrame : DataFrame berisi hasil simulasi kombinasi
        """
        results = []
        
        for persen_pakan in persentase_pakan:
            for persen_jual in persentase_jual:
                harga_pakan_baru = self.base_calculator.harga_pakan_per_kg * (1 + persen_pakan / 100)
                harga_jual_baru = self.base_calculator.harga_jual_per_kg * (1 + persen_jual / 100)
                
                calculator = PakanCalculator(
                    jumlah_ayam=self.base_calculator.jumlah_ayam,
                    harga_pakan_per_kg=harga_pakan_baru,
                    konsumsi_pakan_per_ekor_hari=self.base_calculator.konsumsi_pakan_per_ekor_hari,
                    periode_pemeliharaan=self.base_calculator.periode_pemeliharaan,
                    harga_jual_per_kg=harga_jual_baru,
                    bobot_akhir_rata_rata=self.base_calculator.bobot_akhir_rata_rata,
                    biaya_operasional_lain=self.base_calculator.biaya_operasional_lain
                )
                
                summary = calculator.get_summary()
                summary['Perubahan Harga Pakan (%)'] = persen_pakan
                summary['Perubahan Harga Jual (%)'] = persen_jual
                summary['Harga Pakan Baru (Rp)'] = round(harga_pakan_baru, 2)
                summary['Harga Jual Baru (Rp)'] = round(harga_jual_baru, 2)
                results.append(summary)
        
        df = pd.DataFrame(results)
        return df
