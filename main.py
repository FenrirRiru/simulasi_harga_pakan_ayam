"""
Aplikasi Simulasi Biaya Pakan untuk Memaksimalkan Margin Keuntungan Usaha Ternak Ayam Kampung

Aplikasi ini membantu peternak ayam kampung untuk:
- Menghitung biaya, pendapatan, dan profitabilitas
- Menganalisis skenario perubahan harga
- Mengoptimalkan jumlah ayam untuk target profit
- Memvisualisasikan hasil analisis
"""

import pandas as pd
import os
from datetime import datetime
from openpyxl.utils import get_column_letter
from calculations import PakanCalculator
from simulation import ScenarioSimulator
from optimization import ProfitOptimizer
from visualization import Visualizer


def format_rupiah(nominal):
    """Format nominal menjadi format Rupiah."""
    return f"Rp {nominal:,.0f}".replace(",", ".")


def input_float(prompt, default=None):
    """Input float dengan validasi dan default value."""
    while True:
        try:
            if default is not None:
                user_input = input(f"{prompt} (default: {default}): ").strip()
                if user_input == "":
                    return default
                return float(user_input)
            else:
                user_input = input(f"{prompt}: ").strip()
                return float(user_input)
        except ValueError:
            print("Input tidak valid. Silakan masukkan angka.")


def input_int(prompt, default=None):
    """Input integer dengan validasi dan default value."""
    while True:
        try:
            if default is not None:
                user_input = input(f"{prompt} (default: {default}): ").strip()
                if user_input == "":
                    return default
                return int(user_input)
            else:
                user_input = input(f"{prompt}: ").strip()
                return int(user_input)
        except ValueError:
            print("Input tidak valid. Silakan masukkan bilangan bulat.")


def input_parameter():
    """Input parameter dari user."""
    print("\n" + "="*70)
    print("INPUT PARAMETER USAHA TERNAK AYAM KAMPUNG")
    print("="*70)
    
    jumlah_ayam = input_int("Jumlah ayam (ekor)", default=100)
    harga_pakan_per_kg = input_float("Harga pakan per kg (Rp)", default=12000)
    konsumsi_pakan_per_ekor_hari = input_float("Konsumsi pakan per ekor per hari (gram)", default=100)
    periode_pemeliharaan = input_int("Periode pemeliharaan (hari)", default=90)
    harga_jual_per_kg = input_float("Harga jual ayam per kg (Rp)", default=35000)
    bobot_akhir_rata_rata = input_float("Bobot akhir rata-rata per ekor (kg)", default=1.5)
    biaya_operasional_lain = input_float("Biaya operasional lain (Rp)", default=500000)
    
    return {
        'jumlah_ayam': jumlah_ayam,
        'harga_pakan_per_kg': harga_pakan_per_kg,
        'konsumsi_pakan_per_ekor_hari': konsumsi_pakan_per_ekor_hari,
        'periode_pemeliharaan': periode_pemeliharaan,
        'harga_jual_per_kg': harga_jual_per_kg,
        'bobot_akhir_rata_rata': bobot_akhir_rata_rata,
        'biaya_operasional_lain': biaya_operasional_lain
    }


def tampilkan_ringkasan(calculator):
    """Menampilkan ringkasan hasil perhitungan."""
    print("\n" + "="*70)
    print("RINGKASAN HASIL PERHITUNGAN")
    print("="*70)
    
    summary = calculator.get_summary()
    
    print(f"\n{'Parameter Input':<40} {'Nilai':>30}")
    print("-" * 70)
    print(f"{'Jumlah Ayam':<40} {summary['Jumlah Ayam (ekor)']:>30,} ekor")
    print(f"{'Harga Pakan per kg':<40} {format_rupiah(summary['Harga Pakan per kg (Rp)']):>30}")
    print(f"{'Konsumsi Pakan per ekor/hari':<40} {summary['Konsumsi Pakan per ekor/hari (gram)']:>30} gram")
    print(f"{'Periode Pemeliharaan':<40} {summary['Periode Pemeliharaan (hari)']:>30} hari")
    print(f"{'Harga Jual per kg':<40} {format_rupiah(summary['Harga Jual per kg (Rp)']):>30}")
    print(f"{'Bobot Akhir Rata-rata':<40} {summary['Bobot Akhir Rata-rata (kg)']:>30} kg")
    print(f"{'Biaya Operasional Lain':<40} {format_rupiah(summary['Biaya Operasional Lain (Rp)']):>30}")
    
    print(f"\n{'Hasil Perhitungan':<40} {'Nilai':>30}")
    print("-" * 70)
    print(f"{'Total Konsumsi Pakan':<40} {summary['Total Konsumsi Pakan (kg)']:>30,.2f} kg")
    print(f"{'Total Biaya Pakan':<40} {format_rupiah(summary['Total Biaya Pakan (Rp)']):>30}")
    print(f"{'Total Biaya':<40} {format_rupiah(summary['Total Biaya (Rp)']):>30}")
    print(f"{'Total Pendapatan':<40} {format_rupiah(summary['Total Pendapatan (Rp)']):>30}")
    print(f"{'Keuntungan':<40} {format_rupiah(summary['Keuntungan (Rp)']):>30}")
    print(f"{'Margin Keuntungan':<40} {summary['Margin Keuntungan (%)']:>30,.2f} %")
    print(f"{'Break Even Point (BEP)':<40} {summary['Break Even Point (ekor)']:>30,.2f} ekor")
    print(f"{'Return on Investment (ROI)':<40} {summary['ROI (%)']:>30,.2f} %")
    
    # Analisis profitabilitas
    print(f"\n{'Analisis Profitabilitas':<40}")
    print("-" * 70)
    if summary['Keuntungan (Rp)'] > 0:
        print("✓ Usaha MENGUNTUNGKAN")
    elif summary['Keuntungan (Rp)'] == 0:
        print("⚠ Usaha BREAK EVEN (tidak untung tidak rugi)")
    else:
        print("✗ Usaha RUGI")
    
    if summary['ROI (%)'] > 20:
        print("✓ ROI sangat baik (>20%)")
    elif summary['ROI (%)'] > 10:
        print("✓ ROI baik (10-20%)")
    elif summary['ROI (%)'] > 0:
        print("⚠ ROI rendah (0-10%)")
    else:
        print("✗ ROI negatif (rugi)")


def menu_simulasi(calculator):
    """Menu untuk simulasi skenario."""
    print("\n" + "="*70)
    print("MENU SIMULASI SKENARIO")
    print("="*70)
    print("1. Simulasi Perubahan Harga Pakan (±10%, ±20%)")
    print("2. Simulasi Perubahan Harga Jual (±10%, ±20%)")
    print("3. Simulasi Kombinasi Harga Pakan dan Harga Jual")
    print("4. Kembali ke Menu Utama")
    
    pilihan = input("\nPilih menu (1-4): ").strip()
    
    simulator = ScenarioSimulator(calculator)
    visualizer = Visualizer()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    if pilihan == "1":
        print("\nMenjalankan simulasi perubahan harga pakan...")
        df_simulasi = simulator.simulasi_perubahan_harga_pakan([-20, -10, 0, 10, 20])
        
        print("\nHasil Simulasi Perubahan Harga Pakan:")
        print(df_simulasi[['Perubahan Harga Pakan (%)', 'Harga Pakan Baru (Rp)', 
                           'Total Biaya (Rp)', 'Total Pendapatan (Rp)', 
                           'Keuntungan (Rp)', 'Margin Keuntungan (%)', 'ROI (%)']].to_string(index=False))
        
        # Visualisasi
        save_path = os.path.join(output_dir, f"simulasi_harga_pakan_{timestamp}.png")
        visualizer.plot_skenario_harga_pakan(df_simulasi, save_path)
        print(f"\nGrafik disimpan di: {save_path}")
        
        # Export CSV dan Excel
        export_dataframe(df_simulasi, "simulasi_harga_pakan", output_dir)
        
    elif pilihan == "2":
        print("\nMenjalankan simulasi perubahan harga jual...")
        df_simulasi = simulator.simulasi_perubahan_harga_jual([-20, -10, 0, 10, 20])
        
        print("\nHasil Simulasi Perubahan Harga Jual:")
        print(df_simulasi[['Perubahan Harga Jual (%)', 'Harga Jual Baru (Rp)', 
                           'Total Biaya (Rp)', 'Total Pendapatan (Rp)', 
                           'Keuntungan (Rp)', 'Margin Keuntungan (%)', 'ROI (%)']].to_string(index=False))
        
        # Visualisasi
        save_path = os.path.join(output_dir, f"simulasi_harga_jual_{timestamp}.png")
        visualizer.plot_skenario_harga_jual(df_simulasi, save_path)
        print(f"\nGrafik disimpan di: {save_path}")
        
        # Export CSV dan Excel
        export_dataframe(df_simulasi, "simulasi_harga_jual", output_dir)
        
    elif pilihan == "3":
        print("\nMenjalankan simulasi kombinasi...")
        df_simulasi = simulator.simulasi_kombinasi([-20, -10, 0, 10, 20], [-20, -10, 0, 10, 20])
        
        print("\nHasil Simulasi Kombinasi (sample 5 baris pertama):")
        print(df_simulasi[['Perubahan Harga Pakan (%)', 'Perubahan Harga Jual (%)',
                           'Keuntungan (Rp)', 'Margin Keuntungan (%)', 'ROI (%)']].head().to_string(index=False))
        
        # Visualisasi heatmap
        save_path = os.path.join(output_dir, f"simulasi_kombinasi_{timestamp}.png")
        visualizer.plot_heatmap_kombinasi(df_simulasi, save_path)
        print(f"\nGrafik disimpan di: {save_path}")
        
        # Export CSV dan Excel
        export_dataframe(df_simulasi, "simulasi_kombinasi", output_dir)
    
    return pilihan != "4"


def menu_optimasi(calculator):
    """Menu untuk optimasi."""
    print("\n" + "="*70)
    print("MENU OPTIMASI")
    print("="*70)
    print("1. Hitung Jumlah Ayam untuk Target Profit")
    print("2. Analisis Sensitivitas Jumlah Ayam")
    print("3. Cari Jumlah Ayam Optimal")
    print("4. Kembali ke Menu Utama")
    
    pilihan = input("\nPilih menu (1-4): ").strip()
    
    optimizer = ProfitOptimizer(calculator)
    visualizer = Visualizer()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    if pilihan == "1":
        target_profit = input_float("Masukkan target profit (Rp)", default=5000000)
        jumlah_ayam_diperlukan = optimizer.hitung_jumlah_ayam_untuk_profit(target_profit)
        
        if jumlah_ayam_diperlukan == float('inf'):
            print("\n⚠ Tidak mungkin mencapai target profit dengan parameter saat ini.")
            print("   Perlu menurunkan biaya atau meningkatkan harga jual.")
        else:
            print(f"\nUntuk mencapai target profit {format_rupiah(target_profit)}:")
            print(f"Jumlah ayam yang diperlukan: {jumlah_ayam_diperlukan:,.0f} ekor")
            
            # Verifikasi dengan kalkulator
            calculator_verifikasi = PakanCalculator(
                jumlah_ayam=int(jumlah_ayam_diperlukan),
                harga_pakan_per_kg=calculator.harga_pakan_per_kg,
                konsumsi_pakan_per_ekor_hari=calculator.konsumsi_pakan_per_ekor_hari,
                periode_pemeliharaan=calculator.periode_pemeliharaan,
                harga_jual_per_kg=calculator.harga_jual_per_kg,
                bobot_akhir_rata_rata=calculator.bobot_akhir_rata_rata,
                biaya_operasional_lain=calculator.biaya_operasional_lain
            )
            profit_aktual = calculator_verifikasi.hitung_keuntungan()
            print(f"Profit aktual: {format_rupiah(profit_aktual)}")
    
    elif pilihan == "2":
        min_ayam = input_int("Jumlah ayam minimum", default=1)
        max_ayam = input_int("Jumlah ayam maksimum", default=1000)
        step = input_int("Step increment", default=50)
        
        range_ayam = range(min_ayam, max_ayam + 1, step)
        print(f"\nMenganalisis {len(range_ayam)} skenario...")
        
        data_sensitivitas = optimizer.analisis_sensitivitas_jumlah_ayam(range_ayam)
        df_sensitivitas = pd.DataFrame(data_sensitivitas)
        
        print("\nHasil Analisis Sensitivitas (sample 10 baris pertama):")
        print(df_sensitivitas.head(10).to_string(index=False))
        
        # Visualisasi
        save_path = os.path.join(output_dir, f"sensitivitas_jumlah_ayam_{timestamp}.png")
        visualizer.plot_sensitivitas_jumlah_ayam(data_sensitivitas, save_path)
        print(f"\nGrafik disimpan di: {save_path}")
        
        # Export CSV dan Excel
        export_dataframe(df_sensitivitas, "sensitivitas_jumlah_ayam", output_dir)
    
    elif pilihan == "3":
        min_ayam = input_int("Jumlah ayam minimum", default=1)
        max_ayam = input_int("Jumlah ayam maksimum", default=10000)
        step = input_int("Step increment", default=10)
        
        print("\nMencari jumlah ayam optimal...")
        hasil_optimasi = optimizer.cari_jumlah_ayam_optimal(min_ayam, max_ayam, step)
        
        print("\nHasil Optimasi:")
        print(f"Jumlah Ayam Optimal: {hasil_optimasi['Jumlah Ayam Optimal']:,} ekor")
        print(f"Profit Maksimum: {format_rupiah(hasil_optimasi['Profit Maksimum (Rp)'])}")
    
    return pilihan != "4"


def rekomendasi_strategi(calculator):
    """Memberikan rekomendasi strategi untuk memaksimalkan profit."""
    print("\n" + "="*70)
    print("REKOMENDASI STRATEGI MEMAKSIMALKAN PROFIT")
    print("="*70)
    
    summary = calculator.get_summary()
    keuntungan = summary['Keuntungan (Rp)']
    margin = summary['Margin Keuntungan (%)']
    roi = summary['ROI (%)']
    bep = summary['Break Even Point (ekor)']
    
    rekomendasi = []
    
    # Analisis profitabilitas
    if keuntungan <= 0:
        rekomendasi.append("⚠ Usaha saat ini tidak menguntungkan. Perlu evaluasi menyeluruh.")
        rekomendasi.append("   - Pertimbangkan untuk menurunkan biaya pakan atau mencari supplier lebih murah")
        rekomendasi.append("   - Evaluasi harga jual, apakah bisa ditingkatkan")
        rekomendasi.append(f"   - Minimal perlu {bep:.0f} ekor ayam untuk mencapai BEP")
    else:
        rekomendasi.append("✓ Usaha menguntungkan dengan parameter saat ini")
    
    # Analisis margin
    if margin < 10:
        rekomendasi.append("⚠ Margin keuntungan rendah (<10%). Risiko tinggi terhadap fluktuasi harga.")
        rekomendasi.append("   - Fokus pada efisiensi operasional")
        rekomendasi.append("   - Pertimbangkan skala ekonomi dengan meningkatkan jumlah ayam")
    elif margin < 20:
        rekomendasi.append("✓ Margin keuntungan sedang (10-20%). Usaha cukup sehat.")
        rekomendasi.append("   - Pertimbangkan ekspansi dengan hati-hati")
    else:
        rekomendasi.append("✓ Margin keuntungan tinggi (>20%). Usaha sangat sehat.")
        rekomendasi.append("   - Pertimbangkan ekspansi untuk meningkatkan total profit")
    
    # Analisis ROI
    if roi < 10:
        rekomendasi.append("⚠ ROI rendah. Pertimbangkan alternatif investasi lain.")
    elif roi < 20:
        rekomendasi.append("✓ ROI baik. Investasi cukup menarik.")
    else:
        rekomendasi.append("✓ ROI sangat baik. Investasi sangat menarik.")
    
    # Rekomendasi spesifik
    konsumsi_per_ekor_kg = (calculator.konsumsi_pakan_per_ekor_hari * calculator.periode_pemeliharaan) / 1000
    biaya_pakan_per_ekor = konsumsi_per_ekor_kg * calculator.harga_pakan_per_kg
    pendapatan_per_ekor = calculator.bobot_akhir_rata_rata * calculator.harga_jual_per_kg
    profit_per_ekor = pendapatan_per_ekor - biaya_pakan_per_ekor
    
    rekomendasi.append(f"\nAnalisis per Ekor:")
    rekomendasi.append(f"   - Biaya pakan per ekor: {format_rupiah(biaya_pakan_per_ekor)}")
    rekomendasi.append(f"   - Pendapatan per ekor: {format_rupiah(pendapatan_per_ekor)}")
    rekomendasi.append(f"   - Profit per ekor: {format_rupiah(profit_per_ekor)}")
    
    if profit_per_ekor > 0:
        rekomendasi.append(f"   - Setiap ekor ayam memberikan profit {format_rupiah(profit_per_ekor)}")
        rekomendasi.append(f"   - Untuk meningkatkan total profit, pertimbangkan menambah jumlah ayam")
    
    # Saran optimasi
    rekomendasi.append(f"\nSaran Optimasi:")
    rekomendasi.append("   1. Lakukan simulasi perubahan harga untuk memahami sensitivitas")
    rekomendasi.append("   2. Gunakan analisis sensitivitas jumlah ayam untuk menentukan skala optimal")
    rekomendasi.append("   3. Monitor harga pakan dan harga jual secara berkala")
    rekomendasi.append("   4. Pertimbangkan negosiasi harga dengan supplier pakan")
    rekomendasi.append("   5. Evaluasi efisiensi konsumsi pakan (apakah bisa dikurangi tanpa mengurangi bobot)")
    
    for rec in rekomendasi:
        print(rec)


def export_dataframe(df, filename_base, output_dir="output"):
    """
    Export DataFrame ke CSV dan Excel.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame yang akan diexport
    filename_base : str
        Nama file dasar (tanpa ekstensi)
    output_dir : str
        Direktori output
    """
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Export CSV
    csv_path = os.path.join(output_dir, f"{filename_base}_{timestamp}.csv")
    df.to_csv(csv_path, index=False)
    print(f"Data CSV disimpan di: {csv_path}")
    
    # Export Excel
    excel_path = os.path.join(output_dir, f"{filename_base}_{timestamp}.xlsx")
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Data', index=False)
        
        # Auto-adjust column widths
        worksheet = writer.sheets['Data']
        for idx, col in enumerate(df.columns, start=1):
            max_length = max(
                df[col].astype(str).map(len).max(),
                len(str(col))
            )
            col_letter = get_column_letter(idx)
            worksheet.column_dimensions[col_letter].width = min(max_length + 2, 50)
    
    print(f"Data Excel disimpan di: {excel_path}")


def export_ringkasan(calculator):
    """Export ringkasan ke CSV dan Excel."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    summary = calculator.get_summary()
    df = pd.DataFrame([summary])
    
    # Export menggunakan fungsi helper
    export_dataframe(df, "ringkasan_perhitungan", output_dir)


def main():
    """Fungsi utama aplikasi."""
    print("\n" + "="*70)
    print("APLIKASI SIMULASI BIAYA PAKAN")
    print("Memaksimalkan Margin Keuntungan Usaha Ternak Ayam Kampung")
    print("="*70)
    
    # Input parameter
    params = input_parameter()
    calculator = PakanCalculator(**params)
    
    while True:
        print("\n" + "="*70)
        print("MENU UTAMA")
        print("="*70)
        print("1. Tampilkan Ringkasan Perhitungan")
        print("2. Simulasi Skenario")
        print("3. Optimasi")
        print("4. Rekomendasi Strategi")
        print("5. Export Ringkasan ke CSV/Excel")
        print("6. Ubah Parameter Input")
        print("7. Keluar")
        
        pilihan = input("\nPilih menu (1-7): ").strip()
        
        if pilihan == "1":
            tampilkan_ringkasan(calculator)
            input("\nTekan Enter untuk kembali ke menu utama...")
        
        elif pilihan == "2":
            while menu_simulasi(calculator):
                pass
        
        elif pilihan == "3":
            while menu_optimasi(calculator):
                pass
        
        elif pilihan == "4":
            rekomendasi_strategi(calculator)
            input("\nTekan Enter untuk kembali ke menu utama...")
        
        elif pilihan == "5":
            export_ringkasan(calculator)
            input("\nTekan Enter untuk kembali ke menu utama...")
        
        elif pilihan == "6":
            params = input_parameter()
            calculator = PakanCalculator(**params)
            print("\nParameter telah diupdate!")
        
        elif pilihan == "7":
            print("\nTerima kasih telah menggunakan aplikasi!")
            break
        
        else:
            print("\nPilihan tidak valid. Silakan pilih menu 1-7.")


if __name__ == "__main__":
    main()
