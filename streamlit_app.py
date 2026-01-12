"""
Aplikasi Web Simulasi Biaya Pakan untuk Memaksimalkan Margin Keuntungan Usaha Ternak Ayam Kampung
Menggunakan Streamlit untuk interface web yang dapat diakses melalui browser Chrome.
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
from openpyxl.utils import get_column_letter
from calculations import PakanCalculator
from simulation import ScenarioSimulator
from optimization import ProfitOptimizer
from visualization import Visualizer
from feed_mix import (
    feed_mix_db,
    simulasi_mix_sederhana,
    simulasi_mix_estimasi,
    hitung_kebutuhan_bulanan_kg,
)

# Konfigurasi halaman
st.set_page_config(
    page_title="Simulasi Biaya Pakan Ayam Kampung",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS untuk styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .positive {
        color: #28a745;
        font-weight: bold;
    }
    .negative {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


def format_rupiah(nominal):
    """Format nominal menjadi format Rupiah."""
    return f"Rp {nominal:,.0f}".replace(",", ".")


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
    
    return csv_path, excel_path


def main():
    """Fungsi utama aplikasi Streamlit."""
    
    # Header
    st.markdown('<div class="main-header">🐔 Simulasi Biaya Pakan Ayam Kampung</div>', 
                unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar untuk input parameter
    with st.sidebar:
        st.header("📋 Parameter Input")
        st.markdown("---")
        
        jumlah_ayam = st.number_input(
            "Jumlah Ayam (ekor)",
            min_value=1,
            value=100,
            step=1,
            help="Jumlah ayam yang akan dipelihara. Default 100 ekor, step 1 (ubah dengan tombol +/-)."
        )
        
        harga_pakan_per_kg = st.number_input(
            "Harga Pakan per kg (Rp)",
            min_value=0.0,
            value=12000.0,
            step=1000.0,
            help="Harga pakan per kilogram. Default 12.000, step 1.000."
        )
        
        konsumsi_pakan_per_ekor_hari = st.number_input(
            "Konsumsi Pakan per ekor/hari (gram)",
            min_value=0.0,
            value=100.0,
            step=10.0,
            help="Rata-rata konsumsi pakan per ekor per hari. Default 100 gram, step 10 gram."
        )
        
        periode_pemeliharaan = st.number_input(
            "Periode Pemeliharaan (hari)",
            min_value=1,
            value=90,
            step=1,
            help="Lama periode pemeliharaan dalam hari. Default 90, step 1."
        )
        
        harga_jual_per_kg = st.number_input(
            "Harga Jual per kg (Rp)",
            min_value=0.0,
            value=35000.0,
            step=1000.0,
            help="Harga jual ayam per kilogram. Default 35.000, step 1.000."
        )
        
        bobot_akhir_rata_rata = st.number_input(
            "Bobot Akhir Rata-rata (kg)",
            min_value=0.0,
            value=1.5,
            step=0.1,
            help="Bobot akhir rata-rata per ekor. Default 1,5 kg, step 0,1 kg."
        )
        
        biaya_operasional_lain = st.number_input(
            "Biaya Operasional Lain (Rp)",
            min_value=0.0,
            value=500000.0,
            step=100000.0,
            help="Biaya operasional selain pakan. Default 500.000, step 100.000."
        )
        
        st.markdown("---")
        st.markdown("### 💡 Tips")
        st.info("""
        - Pastikan semua parameter diisi dengan benar
        - Gunakan nilai realistis berdasarkan pengalaman
        - Simulasi dapat membantu memahami risiko perubahan harga
        """)
    
    # Buat kalkulator
    calculator = PakanCalculator(
        jumlah_ayam=int(jumlah_ayam),
        harga_pakan_per_kg=harga_pakan_per_kg,
        konsumsi_pakan_per_ekor_hari=konsumsi_pakan_per_ekor_hari,
        periode_pemeliharaan=int(periode_pemeliharaan),
        harga_jual_per_kg=harga_jual_per_kg,
        bobot_akhir_rata_rata=bobot_akhir_rata_rata,
        biaya_operasional_lain=biaya_operasional_lain
    )
    
    # Tab untuk berbagai fitur
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Ringkasan",
        "📈 Simulasi",
        "🎯 Optimasi",
        "💡 Rekomendasi",
        "🥣 Mix Pakan",   # Tab 5: Mix Pakan
        "📥 Export",      # Tab 6: Export
    ])
    
    # TAB 1: Ringkasan Perhitungan
    with tab1:
        st.header("Ringkasan Hasil Perhitungan")
        st.markdown("---")
        
        summary = calculator.get_summary()
        
        # Metrik utama
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            keuntungan = summary['Keuntungan (Rp)']
            color_class = "positive" if keuntungan > 0 else "negative"
            st.metric(
                "Keuntungan",
                format_rupiah(keuntungan),
                delta=f"{summary['Margin Keuntungan (%)']:.2f}%"
            )
        
        with col2:
            st.metric(
                "Total Pendapatan",
                format_rupiah(summary['Total Pendapatan (Rp)'])
            )
        
        with col3:
            st.metric(
                "Total Biaya",
                format_rupiah(summary['Total Biaya (Rp)'])
            )
        
        with col4:
            st.metric(
                "ROI",
                f"{summary['ROI (%)']:.2f}%"
            )
        
        st.markdown("---")
        
        # Detail perhitungan
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Parameter Input")
            df_input = pd.DataFrame({
                'Parameter': [
                    'Jumlah Ayam',
                    'Harga Pakan per kg',
                    'Konsumsi Pakan per ekor/hari',
                    'Periode Pemeliharaan',
                    'Harga Jual per kg',
                    'Bobot Akhir Rata-rata',
                    'Biaya Operasional Lain'
                ],
                'Nilai': [
                    f"{summary['Jumlah Ayam (ekor)']:,} ekor",
                    format_rupiah(summary['Harga Pakan per kg (Rp)']),
                    f"{summary['Konsumsi Pakan per ekor/hari (gram)']} gram",
                    f"{summary['Periode Pemeliharaan (hari)']} hari",
                    format_rupiah(summary['Harga Jual per kg (Rp)']),
                    f"{summary['Bobot Akhir Rata-rata (kg)']} kg",
                    format_rupiah(summary['Biaya Operasional Lain (Rp)'])
                ]
            })
            st.dataframe(df_input, use_container_width=True, hide_index=True)
        
        with col2:
            st.subheader("Hasil Perhitungan")
            df_output = pd.DataFrame({
                'Metrik': [
                    'Total Konsumsi Pakan',
                    'Total Biaya Pakan',
                    'Total Biaya',
                    'Total Pendapatan',
                    'Keuntungan',
                    'Margin Keuntungan',
                    'Break Even Point (BEP)',
                    'Return on Investment (ROI)'
                ],
                'Nilai': [
                    f"{summary['Total Konsumsi Pakan (kg)']:.2f} kg",
                    format_rupiah(summary['Total Biaya Pakan (Rp)']),
                    format_rupiah(summary['Total Biaya (Rp)']),
                    format_rupiah(summary['Total Pendapatan (Rp)']),
                    format_rupiah(summary['Keuntungan (Rp)']),
                    f"{summary['Margin Keuntungan (%)']:.2f}%",
                    f"{summary['Break Even Point (ekor)']:.2f} ekor",
                    f"{summary['ROI (%)']:.2f}%"
                ]
            })
            st.dataframe(df_output, use_container_width=True, hide_index=True)
        
        # Status profitabilitas
        st.markdown("---")
        if keuntungan > 0:
            st.success(f"✅ Usaha MENGUNTUNGKAN dengan margin {summary['Margin Keuntungan (%)']:.2f}%")
        elif keuntungan == 0:
            st.warning("⚠️ Usaha BREAK EVEN (tidak untung tidak rugi)")
        else:
            st.error(f"❌ Usaha RUGI sebesar {format_rupiah(abs(keuntungan))}")
    
    # TAB 2: Simulasi
    with tab2:
        st.header("Simulasi Skenario")
        st.markdown("---")
        
        simulasi_type = st.radio(
            "Pilih Jenis Simulasi",
            ["Perubahan Harga Pakan", "Perubahan Harga Jual", "Kombinasi Harga Pakan & Jual"],
            horizontal=True,
            help="Pilih skenario simulasi yang ingin dianalisis"
        )
        
        if st.button("🚀 Jalankan Simulasi", type="primary"):
            simulator = ScenarioSimulator(calculator)
            visualizer = Visualizer()
            
            with st.spinner("Menjalankan simulasi..."):
                if simulasi_type == "Perubahan Harga Pakan":
                    df_simulasi = simulator.simulasi_perubahan_harga_pakan([-20, -10, 0, 10, 20])
                    
                    st.subheader("Hasil Simulasi Perubahan Harga Pakan")
                    st.dataframe(
                        df_simulasi[['Perubahan Harga Pakan (%)', 'Harga Pakan Baru (Rp)', 
                                   'Total Biaya (Rp)', 'Total Pendapatan (Rp)', 
                                   'Keuntungan (Rp)', 'Margin Keuntungan (%)', 'ROI (%)']],
                        use_container_width=True
                    )
                    
                    # Visualisasi
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_dir = "output"
                    save_path = os.path.join(output_dir, f"simulasi_harga_pakan_{timestamp}.png")
                    visualizer.plot_skenario_harga_pakan(df_simulasi, save_path)
                    st.image(save_path, use_container_width=True)
                    
                    # Export
                    csv_path, excel_path = export_dataframe(df_simulasi, "simulasi_harga_pakan", output_dir)
                    col1, col2 = st.columns(2)
                    with col1:
                        with open(csv_path, 'rb') as f:
                            st.download_button("📥 Download CSV", f.read(), 
                                             file_name=os.path.basename(csv_path), 
                                             mime="text/csv")
                    with col2:
                        with open(excel_path, 'rb') as f:
                            st.download_button("📥 Download Excel", f.read(), 
                                             file_name=os.path.basename(excel_path), 
                                             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                
                elif simulasi_type == "Perubahan Harga Jual":
                    df_simulasi = simulator.simulasi_perubahan_harga_jual([-20, -10, 0, 10, 20])
                    
                    st.subheader("Hasil Simulasi Perubahan Harga Jual")
                    st.dataframe(
                        df_simulasi[['Perubahan Harga Jual (%)', 'Harga Jual Baru (Rp)', 
                                   'Total Biaya (Rp)', 'Total Pendapatan (Rp)', 
                                   'Keuntungan (Rp)', 'Margin Keuntungan (%)', 'ROI (%)']],
                        use_container_width=True
                    )
                    
                    # Visualisasi
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_dir = "output"
                    save_path = os.path.join(output_dir, f"simulasi_harga_jual_{timestamp}.png")
                    visualizer.plot_skenario_harga_jual(df_simulasi, save_path)
                    st.image(save_path, use_container_width=True)
                    
                    # Export
                    csv_path, excel_path = export_dataframe(df_simulasi, "simulasi_harga_jual", output_dir)
                    col1, col2 = st.columns(2)
                    with col1:
                        with open(csv_path, 'rb') as f:
                            st.download_button("📥 Download CSV", f.read(), 
                                             file_name=os.path.basename(csv_path), 
                                             mime="text/csv")
                    with col2:
                        with open(excel_path, 'rb') as f:
                            st.download_button("📥 Download Excel", f.read(), 
                                             file_name=os.path.basename(excel_path), 
                                             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                
                else:  # Kombinasi
                    df_simulasi = simulator.simulasi_kombinasi([-20, -10, 0, 10, 20], [-20, -10, 0, 10, 20])
                    
                    st.subheader("Hasil Simulasi Kombinasi")
                    st.dataframe(
                        df_simulasi[['Perubahan Harga Pakan (%)', 'Perubahan Harga Jual (%)',
                                   'Keuntungan (Rp)', 'Margin Keuntungan (%)', 'ROI (%)']],
                        use_container_width=True
                    )
                    
                    # Visualisasi
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_dir = "output"
                    save_path = os.path.join(output_dir, f"simulasi_kombinasi_{timestamp}.png")
                    visualizer.plot_heatmap_kombinasi(df_simulasi, save_path)
                    st.image(save_path, use_container_width=True)
                    
                    # Export
                    csv_path, excel_path = export_dataframe(df_simulasi, "simulasi_kombinasi", output_dir)
                    col1, col2 = st.columns(2)
                    with col1:
                        with open(csv_path, 'rb') as f:
                            st.download_button("📥 Download CSV", f.read(), 
                                             file_name=os.path.basename(csv_path), 
                                             mime="text/csv")
                    with col2:
                        with open(excel_path, 'rb') as f:
                            st.download_button("📥 Download Excel", f.read(), 
                                             file_name=os.path.basename(excel_path), 
                                             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    # TAB 3: Optimasi
    with tab3:
        st.header("Optimasi Jumlah Ayam")
        st.markdown("---")
        
        optimasi_type = st.radio(
            "Pilih Jenis Optimasi",
            ["Hitung Jumlah Ayam untuk Target Profit", 
             "Analisis Sensitivitas Jumlah Ayam", 
             "Cari Jumlah Ayam Optimal"],
            horizontal=False,
            help="Pilih jenis analisis optimasi yang ingin dijalankan"
        )
        
        optimizer = ProfitOptimizer(calculator)
        
        if optimasi_type == "Hitung Jumlah Ayam untuk Target Profit":
            target_profit = st.number_input(
                "Target Profit (Rp)",
                min_value=0.0,
                value=5000000.0,
                step=1000000.0,
                help="Berapa profit yang ingin dicapai dalam Rupiah. Default 5.000.000, step 1.000.000."
            )
            
            if st.button("🔍 Hitung", type="primary"):
                jumlah_ayam_diperlukan = optimizer.hitung_jumlah_ayam_untuk_profit(target_profit)
                
                if jumlah_ayam_diperlukan == float('inf'):
                    st.error("⚠️ Tidak mungkin mencapai target profit dengan parameter saat ini.")
                    st.info("💡 Saran: Perlu menurunkan biaya atau meningkatkan harga jual.")
                else:
                    st.success(f"✅ Untuk mencapai target profit {format_rupiah(target_profit)}:")
                    st.metric("Jumlah Ayam yang Diperlukan", f"{jumlah_ayam_diperlukan:,.0f} ekor")
                    
                    # Verifikasi
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
                    st.info(f"Profit aktual: {format_rupiah(profit_aktual)}")
        
        elif optimasi_type == "Analisis Sensitivitas Jumlah Ayam":
            col1, col2, col3 = st.columns(3)
            with col1:
                min_ayam = st.number_input(
                    "Jumlah Ayam Minimum",
                    min_value=1,
                    value=1,
                    step=10,
                    help="Batas bawah jumlah ayam untuk analisis sensitivitas"
                )
            with col2:
                max_ayam = st.number_input(
                    "Jumlah Ayam Maksimum",
                    min_value=1,
                    value=1000,
                    step=50,
                    help="Batas atas jumlah ayam untuk analisis sensitivitas"
                )
            with col3:
                step = st.number_input(
                    "Step Increment",
                    min_value=1,
                    value=50,
                    step=10,
                    help="Jarak antar skenario jumlah ayam (semakin kecil, semakin detail)"
                )
            
            if st.button("📊 Analisis", type="primary"):
                range_ayam = range(min_ayam, max_ayam + 1, step)
                
                with st.spinner(f"Menganalisis {len(range_ayam)} skenario..."):
                    data_sensitivitas = optimizer.analisis_sensitivitas_jumlah_ayam(range_ayam)
                    df_sensitivitas = pd.DataFrame(data_sensitivitas)
                    
                    st.subheader("Hasil Analisis Sensitivitas")
                    st.dataframe(df_sensitivitas, use_container_width=True)
                    
                    # Visualisasi
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_dir = "output"
                    save_path = os.path.join(output_dir, f"sensitivitas_jumlah_ayam_{timestamp}.png")
                    visualizer = Visualizer()
                    visualizer.plot_sensitivitas_jumlah_ayam(data_sensitivitas, save_path)
                    st.image(save_path, use_container_width=True)
                    
                    # Export
                    csv_path, excel_path = export_dataframe(df_sensitivitas, "sensitivitas_jumlah_ayam", output_dir)
                    col1, col2 = st.columns(2)
                    with col1:
                        with open(csv_path, 'rb') as f:
                            st.download_button("📥 Download CSV", f.read(), 
                                             file_name=os.path.basename(csv_path), 
                                             mime="text/csv")
                    with col2:
                        with open(excel_path, 'rb') as f:
                            st.download_button("📥 Download Excel", f.read(), 
                                             file_name=os.path.basename(excel_path), 
                                             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        
        else:  # Cari Jumlah Ayam Optimal
            col1, col2, col3 = st.columns(3)
            with col1:
                min_ayam = st.number_input(
                    "Min Ayam",
                    min_value=1,
                    value=1,
                    step=10,
                    key="opt_min",
                    help="Batas bawah jumlah ayam yang akan dicari optimum-nya"
                )
            with col2:
                max_ayam = st.number_input(
                    "Max Ayam",
                    min_value=1,
                    value=10000,
                    step=100,
                    key="opt_max",
                    help="Batas atas jumlah ayam yang akan dicari optimum-nya"
                )
            with col3:
                step = st.number_input(
                    "Step",
                    min_value=1,
                    value=10,
                    step=5,
                    key="opt_step",
                    help="Jarak antar skenario pada pencarian optimum (semakin kecil, semakin detail)"
                )
            
            if st.button("🎯 Cari Optimal", type="primary"):
                with st.spinner("Mencari jumlah ayam optimal..."):
                    hasil_optimasi = optimizer.cari_jumlah_ayam_optimal(min_ayam, max_ayam, step)
                    
                    st.success("✅ Hasil Optimasi:")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Jumlah Ayam Optimal", f"{hasil_optimasi['Jumlah Ayam Optimal']:,} ekor")
                    with col2:
                        st.metric("Profit Maksimum", format_rupiah(hasil_optimasi['Profit Maksimum (Rp)']))
    
    # TAB 4: Rekomendasi
    with tab4:
        st.header("Rekomendasi Strategi")
        st.markdown("---")
        
        summary = calculator.get_summary()
        keuntungan = summary['Keuntungan (Rp)']
        margin = summary['Margin Keuntungan (%)']
        roi = summary['ROI (%)']
        bep = summary['Break Even Point (ekor)']
        
        # Analisis profitabilitas
        st.subheader("📊 Analisis Profitabilitas")
        bep_label = "tak terhingga (pendapatan per ekor <= biaya per ekor)" if bep == float("inf") else f"{bep:.0f} ekor"
        if keuntungan <= 0:
            st.error("⚠️ Usaha saat ini tidak menguntungkan. Perlu evaluasi menyeluruh.")
            st.markdown("""
            **Rekomendasi:**
            - Pertimbangkan untuk menurunkan biaya pakan atau mencari supplier lebih murah
            - Evaluasi harga jual, apakah bisa ditingkatkan
            - Minimal perlu **{}** untuk mencapai BEP
            """.format(bep_label))
        else:
            st.success("✅ Usaha menguntungkan dengan parameter saat ini")
        
        st.markdown("---")
        
        # Analisis margin
        st.subheader("💰 Analisis Margin")
        if margin < 10:
            st.warning("⚠️ Margin keuntungan rendah (<10%). Risiko tinggi terhadap fluktuasi harga.")
            st.markdown("""
            **Rekomendasi:**
            - Fokus pada efisiensi operasional
            - Pertimbangkan skala ekonomi dengan meningkatkan jumlah ayam
            """)
        elif margin < 20:
            st.info("✅ Margin keuntungan sedang (10-20%). Usaha cukup sehat.")
            st.markdown("- Pertimbangkan ekspansi dengan hati-hati")
        else:
            st.success("✅ Margin keuntungan tinggi (>20%). Usaha sangat sehat.")
            st.markdown("- Pertimbangkan ekspansi untuk meningkatkan total profit")
        
        st.markdown("---")
        
        # Analisis ROI
        st.subheader("📈 Analisis ROI")
        if roi < 10:
            st.warning("⚠️ ROI rendah. Pertimbangkan alternatif investasi lain.")
        elif roi < 20:
            st.info("✅ ROI baik. Investasi cukup menarik.")
        else:
            st.success("✅ ROI sangat baik. Investasi sangat menarik.")
        
        st.markdown("---")
        
        # Analisis per ekor
        st.subheader("🐔 Analisis per Ekor")
        konsumsi_per_ekor_kg = (calculator.konsumsi_pakan_per_ekor_hari * calculator.periode_pemeliharaan) / 1000
        biaya_pakan_per_ekor = konsumsi_per_ekor_kg * calculator.harga_pakan_per_kg
        pendapatan_per_ekor = calculator.bobot_akhir_rata_rata * calculator.harga_jual_per_kg
        profit_per_ekor = pendapatan_per_ekor - biaya_pakan_per_ekor
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Biaya Pakan per Ekor", format_rupiah(biaya_pakan_per_ekor))
        with col2:
            st.metric("Pendapatan per Ekor", format_rupiah(pendapatan_per_ekor))
        with col3:
            color = "normal" if profit_per_ekor > 0 else "inverse"
            st.metric("Profit per Ekor", format_rupiah(profit_per_ekor))
        
        st.markdown("---")
        
        # Saran optimasi
        st.subheader("💡 Saran Optimasi")
        st.markdown("""
        1. **Lakukan simulasi perubahan harga** untuk memahami sensitivitas
        2. **Gunakan analisis sensitivitas jumlah ayam** untuk menentukan skala optimal
        3. **Monitor harga pakan dan harga jual** secara berkala
        4. **Pertimbangkan negosiasi harga** dengan supplier pakan
        5. **Evaluasi efisiensi konsumsi pakan** (apakah bisa dikurangi tanpa mengurangi bobot)
        """)
    
    # TAB 5: Mix Pakan (Racikan Pakan)
    with tab5:
        st.header("Simulasi Mix Pakan (Racikan Pakan)")
        st.markdown("---")

        st.markdown(
            "Fitur ini membantu menghitung **biaya** dan (opsional) "
            "**estimasi nutrisi kasar** dari racikan pakan campuran."
        )

        col_mode, col_info = st.columns([2, 1])
        with col_mode:
            mode_mix = st.radio(
                "Pilih Mode Mix Pakan",
                ["Sederhana (Biaya saja)", "Estimasi (Biaya + Nutrisi Kasar)"],
                help=(
                    "Mode Sederhana: hanya hitung biaya dan harga per kg.\n"
                    "Mode Estimasi: tambah estimasi protein & energi berdasarkan standar generik."
                ),
            )

        st.markdown("### 1. Komposisi Bahan")
        st.caption(
            "Silakan ubah persentase (%) dan harga per kg sesuai kondisi aktual. "
            "Total persentase sebaiknya mendekati 100%."
        )

        df_default = feed_mix_db.get_formula_contoh_df()
        if df_default.empty:
            df_default = feed_mix_db.get_bahan_df()
            df_default["Persen (%)"] = 0.0

        edited_df = st.data_editor(
            df_default,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
        )

        total_persen = edited_df.get("Persen (%)", pd.Series([], dtype=float)).sum()
        st.write(f"Total komposisi: **{total_persen:.2f}%**")
        if abs(total_persen - 100) > 1:
            st.warning(
                "Total komposisi tidak sama dengan 100%. "
                "Perhitungan tetap bisa jalan, tapi sebaiknya disesuaikan."
            )

        st.markdown("### 2. Parameter Simulasi")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            total_kg_mix = st.number_input(
                "Target produksi pakan (kg)",
                min_value=1.0,
                value=100.0,
                step=10.0,
                help="Berapa kg pakan campuran yang ingin dibuat."
            )
        with col_b:
            harga_komersial = st.number_input(
                "Harga pakan komersial pembanding (Rp/kg)",
                min_value=0.0,
                value=12000.0,
                step=500.0,
                help="Harga pakan pabrikan (BR1/komersial) untuk dibandingkan."
            )
        with col_c:
            st.caption("Opsional: proyeksi bulanan")
            jml_ayam_mix = st.number_input(
                "Jumlah ayam (opsional)",
                min_value=0,
                value=0,
                step=10,
                help="Isi jika ingin estimasi kebutuhan pakan per bulan."
            )
            konsumsi_mix = st.number_input(
                "Konsumsi/ekor/hari (gram, opsional)",
                min_value=0.0,
                value=0.0,
                step=10.0,
                help="Rata-rata konsumsi pakan per ekor per hari untuk proyeksi bulanan."
            )

        kebutuhan_bulanan_kg = 0.0
        if jml_ayam_mix > 0 and konsumsi_mix > 0:
            kebutuhan_bulanan_kg = hitung_kebutuhan_bulanan_kg(
                jumlah_ayam=jml_ayam_mix,
                konsumsi_gram_per_ekor_per_hari=konsumsi_mix,
                hari_per_bulan=30,
            )

        if kebutuhan_bulanan_kg > 0:
            st.caption(
                f"Perkiraan kebutuhan pakan per bulan: **{kebutuhan_bulanan_kg:.1f} kg** "
                "(berdasarkan jumlah ayam & konsumsi harian)."
            )

        st.markdown("### 3. Jalankan Simulasi")
        if st.button("🥣 Hitung Mix Pakan", type="primary", help="Klik untuk menghitung biaya dan (jika dipilih) nutrisi mix pakan."):
            try:
                if mode_mix.startswith("Sederhana"):
                    hasil = simulasi_mix_sederhana(
                        df_komposisi=edited_df,
                        total_kg=total_kg_mix,
                        harga_komersial_per_kg=harga_komersial,
                        kebutuhan_bulanan_kg=kebutuhan_bulanan_kg or None,
                    )
                else:
                    hasil = simulasi_mix_estimasi(
                        df_komposisi=edited_df,
                        total_kg=total_kg_mix,
                        harga_komersial_per_kg=harga_komersial,
                        kebutuhan_bulanan_kg=kebutuhan_bulanan_kg or None,
                    )
            except Exception as e:
                st.error(f"Terjadi error saat simulasi: {e}")
            else:
                st.subheader("Ringkasan Biaya Mix Pakan")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Biaya Bahan", format_rupiah(hasil["total_biaya"]))
                with col2:
                    st.metric("Harga Mix per kg", format_rupiah(hasil["harga_mix_per_kg"]))
                with col3:
                    st.metric("Harga Pakan Komersial", format_rupiah(hasil["harga_komersial_per_kg"]))

                selisih = hasil["selisih_per_kg"]
                if selisih > 0:
                    st.success(
                        f"Mix pakan **LEBIH MURAH** {format_rupiah(selisih)} per kg "
                        "dibanding pakan komersial."
                    )
                elif selisih < 0:
                    st.warning(
                        f"Mix pakan **LEBIH MAHAL** {format_rupiah(abs(selisih))} per kg "
                        "dibanding pakan komersial."
                    )
                else:
                    st.info("Harga mix pakan sama dengan pakan komersial.")

                if hasil.get("penghematan_bulanan") is not None:
                    if hasil["penghematan_bulanan"] > 0:
                        st.info(
                            f"Estimasi penghematan per bulan: "
                            f"**{format_rupiah(hasil['penghematan_bulanan'])}**"
                        )

                st.markdown("### Daftar Belanja Bahan")
                df_belanja = hasil["tabel_belanja"].copy()
                df_belanja["Kg per Bahan"] = df_belanja["Kg per Bahan"].round(2)
                df_belanja["Biaya per Bahan (Rp)"] = df_belanja["Biaya per Bahan (Rp)"].round(0)
                st.dataframe(df_belanja, use_container_width=True)

                # Pie chart komposisi
                st.markdown("### Visualisasi Komposisi & Biaya")
                col_pie, col_bar = st.columns(2)
                with col_pie:
                    st.caption("Komposisi berat (%) per bahan")
                    st.bar_chart(
                        df_belanja.set_index("Nama Bahan")["Persen (%)"],
                        use_container_width=True,
                    )
                with col_bar:
                    st.caption("Biaya per bahan (Rp)")
                    st.bar_chart(
                        df_belanja.set_index("Nama Bahan")["Biaya per Bahan (Rp)"],
                        use_container_width=True,
                    )

                if mode_mix.startswith("Estimasi"):
                    st.markdown("### Estimasi Nutrisi (Mode Estimasi)")
                    st.info(
                        "Nilai nutrisi berikut **menggunakan estimasi standar** "
                        "dan hanya sebagai gambaran kasar."
                    )
                    col_p, col_e = st.columns(2)
                    with col_p:
                        st.metric(
                            "Protein Kasar (rata-rata)",
                            f"{hasil['protein_rata']:.2f} %",
                            help="Estimasi protein campuran berdasarkan standar bahan (% dari total berat).",
                        )
                        st.caption(
                            f"Range estimasi protein: {hasil['protein_min']:.2f} – {hasil['protein_max']:.2f} %"
                        )
                    with col_e:
                        st.metric(
                            "Energi Metabolis (rata-rata)",
                            f"{hasil['energi_rata']:.0f} kkal/kg",
                            help="Estimasi energi metabolis campuran (kkal/kg).",
                        )
                        st.caption(
                            f"Range estimasi energi: {hasil['energi_min']:.0f} – {hasil['energi_max']:.0f} kkal/kg"
                        )

    # TAB 6: Export
    with tab6:
        st.header("Export Data")
        st.markdown("---")

        summary = calculator.get_summary()
        df_summary = pd.DataFrame([summary])

        st.subheader("Export Ringkasan Perhitungan")
        st.dataframe(df_summary, use_container_width=True)

        col1, col2 = st.columns(2)

        # Export CSV & Excel (menggunakan helper yang sama)
        csv_path, excel_path = export_dataframe(df_summary, "ringkasan_perhitungan", "output")

        with col1:
            with open(csv_path, 'rb') as f:
                st.download_button(
                    "📥 Download Ringkasan (CSV)",
                    f.read(),
                    file_name=os.path.basename(csv_path),
                    mime="text/csv",
                    use_container_width=True
                )

        with col2:
            with open(excel_path, 'rb') as f:
                st.download_button(
                    "📥 Download Ringkasan (Excel)",
                    f.read(),
                    file_name=os.path.basename(excel_path),
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )


if __name__ == "__main__":
    main()
