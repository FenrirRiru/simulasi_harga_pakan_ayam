"""
Modul untuk visualisasi data dan grafik.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Set style untuk grafik yang lebih menarik
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


class Visualizer:
    """
    Kelas untuk membuat berbagai visualisasi grafik.
    """
    
    def __init__(self):
        """Inisialisasi visualizer."""
        pass
    
    def plot_skenario_harga_pakan(self, df_simulasi, save_path=None):
        """
        Membuat grafik simulasi perubahan harga pakan.
        
        Parameters:
        -----------
        df_simulasi : pd.DataFrame
            DataFrame hasil simulasi perubahan harga pakan
        save_path : str, optional
            Path untuk menyimpan grafik
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Analisis Sensitivitas Perubahan Harga Pakan', fontsize=16, fontweight='bold')
        
        # Grafik 1: Keuntungan vs Perubahan Harga Pakan
        axes[0, 0].plot(df_simulasi['Perubahan Harga Pakan (%)'], 
                       df_simulasi['Keuntungan (Rp)'], 
                       marker='o', linewidth=2, markersize=8, color='#2ecc71')
        axes[0, 0].axhline(y=0, color='r', linestyle='--', alpha=0.5)
        axes[0, 0].set_xlabel('Perubahan Harga Pakan (%)')
        axes[0, 0].set_ylabel('Keuntungan (Rp)')
        axes[0, 0].set_title('Keuntungan vs Perubahan Harga Pakan')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Grafik 2: Margin Keuntungan vs Perubahan Harga Pakan
        axes[0, 1].plot(df_simulasi['Perubahan Harga Pakan (%)'], 
                       df_simulasi['Margin Keuntungan (%)'], 
                       marker='s', linewidth=2, markersize=8, color='#3498db')
        axes[0, 1].axhline(y=0, color='r', linestyle='--', alpha=0.5)
        axes[0, 1].set_xlabel('Perubahan Harga Pakan (%)')
        axes[0, 1].set_ylabel('Margin Keuntungan (%)')
        axes[0, 1].set_title('Margin Keuntungan vs Perubahan Harga Pakan')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Grafik 3: ROI vs Perubahan Harga Pakan
        axes[1, 0].plot(df_simulasi['Perubahan Harga Pakan (%)'], 
                       df_simulasi['ROI (%)'], 
                       marker='^', linewidth=2, markersize=8, color='#e74c3c')
        axes[1, 0].axhline(y=0, color='r', linestyle='--', alpha=0.5)
        axes[1, 0].set_xlabel('Perubahan Harga Pakan (%)')
        axes[1, 0].set_ylabel('ROI (%)')
        axes[1, 0].set_title('ROI vs Perubahan Harga Pakan')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Grafik 4: Total Biaya vs Total Pendapatan
        axes[1, 1].bar(df_simulasi['Perubahan Harga Pakan (%)'].astype(str) + '%',
                      df_simulasi['Total Biaya (Rp)'], 
                      alpha=0.7, label='Total Biaya', color='#e67e22')
        axes[1, 1].bar(df_simulasi['Perubahan Harga Pakan (%)'].astype(str) + '%',
                      df_simulasi['Total Pendapatan (Rp)'], 
                      alpha=0.7, label='Total Pendapatan', color='#27ae60')
        axes[1, 1].set_xlabel('Perubahan Harga Pakan (%)')
        axes[1, 1].set_ylabel('Jumlah (Rp)')
        axes[1, 1].set_title('Total Biaya vs Total Pendapatan')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        
        plt.close()
    
    def plot_skenario_harga_jual(self, df_simulasi, save_path=None):
        """
        Membuat grafik simulasi perubahan harga jual.
        
        Parameters:
        -----------
        df_simulasi : pd.DataFrame
            DataFrame hasil simulasi perubahan harga jual
        save_path : str, optional
            Path untuk menyimpan grafik
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Analisis Sensitivitas Perubahan Harga Jual', fontsize=16, fontweight='bold')
        
        # Grafik 1: Keuntungan vs Perubahan Harga Jual
        axes[0, 0].plot(df_simulasi['Perubahan Harga Jual (%)'], 
                       df_simulasi['Keuntungan (Rp)'], 
                       marker='o', linewidth=2, markersize=8, color='#2ecc71')
        axes[0, 0].axhline(y=0, color='r', linestyle='--', alpha=0.5)
        axes[0, 0].set_xlabel('Perubahan Harga Jual (%)')
        axes[0, 0].set_ylabel('Keuntungan (Rp)')
        axes[0, 0].set_title('Keuntungan vs Perubahan Harga Jual')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Grafik 2: Margin Keuntungan vs Perubahan Harga Jual
        axes[0, 1].plot(df_simulasi['Perubahan Harga Jual (%)'], 
                       df_simulasi['Margin Keuntungan (%)'], 
                       marker='s', linewidth=2, markersize=8, color='#3498db')
        axes[0, 1].axhline(y=0, color='r', linestyle='--', alpha=0.5)
        axes[0, 1].set_xlabel('Perubahan Harga Jual (%)')
        axes[0, 1].set_ylabel('Margin Keuntungan (%)')
        axes[0, 1].set_title('Margin Keuntungan vs Perubahan Harga Jual')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Grafik 3: ROI vs Perubahan Harga Jual
        axes[1, 0].plot(df_simulasi['Perubahan Harga Jual (%)'], 
                       df_simulasi['ROI (%)'], 
                       marker='^', linewidth=2, markersize=8, color='#e74c3c')
        axes[1, 0].axhline(y=0, color='r', linestyle='--', alpha=0.5)
        axes[1, 0].set_xlabel('Perubahan Harga Jual (%)')
        axes[1, 0].set_ylabel('ROI (%)')
        axes[1, 0].set_title('ROI vs Perubahan Harga Jual')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Grafik 4: Total Biaya vs Total Pendapatan
        axes[1, 1].bar(df_simulasi['Perubahan Harga Jual (%)'].astype(str) + '%',
                      df_simulasi['Total Biaya (Rp)'], 
                      alpha=0.7, label='Total Biaya', color='#e67e22')
        axes[1, 1].bar(df_simulasi['Perubahan Harga Jual (%)'].astype(str) + '%',
                      df_simulasi['Total Pendapatan (Rp)'], 
                      alpha=0.7, label='Total Pendapatan', color='#27ae60')
        axes[1, 1].set_xlabel('Perubahan Harga Jual (%)')
        axes[1, 1].set_ylabel('Jumlah (Rp)')
        axes[1, 1].set_title('Total Biaya vs Total Pendapatan')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        
        plt.close()
    
    def plot_sensitivitas_jumlah_ayam(self, data_sensitivitas, save_path=None):
        """
        Membuat grafik analisis sensitivitas jumlah ayam.
        
        Parameters:
        -----------
        data_sensitivitas : dict
            Dictionary hasil analisis sensitivitas jumlah ayam
        save_path : str, optional
            Path untuk menyimpan grafik
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Analisis Sensitivitas Jumlah Ayam', fontsize=16, fontweight='bold')
        
        jumlah_ayam = data_sensitivitas['Jumlah Ayam']
        
        # Grafik 1: Keuntungan vs Jumlah Ayam
        axes[0, 0].plot(jumlah_ayam, data_sensitivitas['Keuntungan (Rp)'], 
                       marker='o', linewidth=2, markersize=6, color='#2ecc71')
        axes[0, 0].axhline(y=0, color='r', linestyle='--', alpha=0.5)
        axes[0, 0].set_xlabel('Jumlah Ayam (ekor)')
        axes[0, 0].set_ylabel('Keuntungan (Rp)')
        axes[0, 0].set_title('Keuntungan vs Jumlah Ayam')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Grafik 2: Margin Keuntungan vs Jumlah Ayam
        axes[0, 1].plot(jumlah_ayam, data_sensitivitas['Margin Keuntungan (%)'], 
                       marker='s', linewidth=2, markersize=6, color='#3498db')
        axes[0, 1].axhline(y=0, color='r', linestyle='--', alpha=0.5)
        axes[0, 1].set_xlabel('Jumlah Ayam (ekor)')
        axes[0, 1].set_ylabel('Margin Keuntungan (%)')
        axes[0, 1].set_title('Margin Keuntungan vs Jumlah Ayam')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Grafik 3: ROI vs Jumlah Ayam
        axes[1, 0].plot(jumlah_ayam, data_sensitivitas['ROI (%)'], 
                       marker='^', linewidth=2, markersize=6, color='#e74c3c')
        axes[1, 0].axhline(y=0, color='r', linestyle='--', alpha=0.5)
        axes[1, 0].set_xlabel('Jumlah Ayam (ekor)')
        axes[1, 0].set_ylabel('ROI (%)')
        axes[1, 0].set_title('ROI vs Jumlah Ayam')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Grafik 4: Total Biaya vs Total Pendapatan
        axes[1, 1].plot(jumlah_ayam, data_sensitivitas['Total Biaya (Rp)'], 
                       marker='o', linewidth=2, markersize=6, label='Total Biaya', color='#e67e22')
        axes[1, 1].plot(jumlah_ayam, data_sensitivitas['Total Pendapatan (Rp)'], 
                       marker='s', linewidth=2, markersize=6, label='Total Pendapatan', color='#27ae60')
        axes[1, 1].set_xlabel('Jumlah Ayam (ekor)')
        axes[1, 1].set_ylabel('Jumlah (Rp)')
        axes[1, 1].set_title('Total Biaya vs Total Pendapatan')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        
        plt.close()
    
    def plot_heatmap_kombinasi(self, df_kombinasi, save_path=None):
        """
        Membuat heatmap untuk simulasi kombinasi harga pakan dan harga jual.
        
        Parameters:
        -----------
        df_kombinasi : pd.DataFrame
            DataFrame hasil simulasi kombinasi
        save_path : str, optional
            Path untuk menyimpan grafik
        """
        # Pivot table untuk heatmap
        pivot_keuntungan = df_kombinasi.pivot_table(
            values='Keuntungan (Rp)',
            index='Perubahan Harga Pakan (%)',
            columns='Perubahan Harga Jual (%)'
        )
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        fig.suptitle('Heatmap Analisis Kombinasi Harga Pakan dan Harga Jual', 
                     fontsize=16, fontweight='bold')
        
        # Heatmap Keuntungan
        sns.heatmap(pivot_keuntungan, annot=True, fmt='.0f', cmap='RdYlGn', 
                   center=0, ax=axes[0], cbar_kws={'label': 'Keuntungan (Rp)'})
        axes[0].set_title('Keuntungan (Rp)')
        axes[0].set_xlabel('Perubahan Harga Jual (%)')
        axes[0].set_ylabel('Perubahan Harga Pakan (%)')
        
        # Heatmap ROI
        pivot_roi = df_kombinasi.pivot_table(
            values='ROI (%)',
            index='Perubahan Harga Pakan (%)',
            columns='Perubahan Harga Jual (%)'
        )
        
        sns.heatmap(pivot_roi, annot=True, fmt='.1f', cmap='RdYlGn', 
                   center=0, ax=axes[1], cbar_kws={'label': 'ROI (%)'})
        axes[1].set_title('ROI (%)')
        axes[1].set_xlabel('Perubahan Harga Jual (%)')
        axes[1].set_ylabel('Perubahan Harga Pakan (%)')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        
        plt.close()
