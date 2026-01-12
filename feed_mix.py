"""
Modul Mix Pakan (Racikan Pakan) untuk simulasi biaya dan estimasi nutrisi.

Catatan:
- Untuk kesederhanaan, "database" disimulasikan dengan struktur data in-memory
  (dictionary dan pandas.DataFrame), bukan database SQL sungguhan.
- Struktur tabel mengikuti spesifikasi:
  - bahan_pakan
  - standar_nutrisi_bahan
  - formula_mix_pakan (disederhanakan sebagai kumpulan komposisi).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional, Tuple

import numpy as np
import pandas as pd


# =========================
#  Data Class & "Tabel"    #
# =========================


@dataclass
class BahanPakan:
    """Representasi satu baris pada tabel `bahan_pakan` (disederhanakan)."""

    id_bahan: int
    nama_bahan: str
    kategori_bahan: str
    harga_per_kg: float
    supplier: str
    protein_content: Optional[float] = None  # persen
    energi_metabolis: Optional[float] = None  # kkal/kg
    is_estimasi_nutrisi: bool = True
    catatan_kualitas: str = ""
    stok_tersedia: float = 0.0  # kg
    tanggal_update: datetime = field(default_factory=datetime.now)


@dataclass
class StandarNutrisiBahan:
    """Representasi satu baris pada tabel `standar_nutrisi_bahan`."""

    id_standar: int
    nama_bahan_generik: str
    protein_min: float
    protein_max: float
    energi_min: float
    energi_max: float
    protein_rata: float
    energi_rata: float
    sumber_referensi: str


@dataclass
class FormulaMixItem:
    """Satu baris komposisi bahan di dalam formula mix pakan."""

    id_bahan: int
    persen_komposisi: float  # persen dari total berat


@dataclass
class FormulaMixPakan:
    """Representasi sederhana tabel `formula_mix_pakan`."""

    id_formula: int
    nama_formula: str
    kategori_umur: str  # Starter/Grower/Finisher
    mode_nutrisi: str  # 'detail'/'estimasi'/'sederhana'
    target_protein: Optional[float] = None
    target_energi: Optional[float] = None
    keterangan: str = ""
    created_date: datetime = field(default_factory=datetime.now)
    status_aktif: bool = True
    items: List[FormulaMixItem] = field(default_factory=list)


class FeedMixDB:
    """
    "Database" sederhana untuk menyimpan bahan pakan, standar nutrisi, dan formula mix.
    """

    def __init__(self) -> None:
        self.bahan_pakan: Dict[int, BahanPakan] = {}
        self.standar_nutrisi: Dict[str, StandarNutrisiBahan] = {}
        self.formula_mix: Dict[int, FormulaMixPakan] = {}
        self._auto_id_bahan = 1
        self._auto_id_standar = 1
        self._auto_id_formula = 1
        self._seed_standar()
        self._seed_bahan_dasar()
        self._seed_formula_contoh()

    # ---------- Seeder ----------

    def _seed_standar(self) -> None:
        """Seed data standar nutrisi sesuai spesifikasi (disederhanakan)."""

        def add_standar(
            nama: str,
            p_min: float,
            p_max: float,
            e_min: float,
            e_max: float,
            p_rata: float,
            e_rata: float,
            sumber: str,
        ) -> None:
            self.standar_nutrisi[nama.lower()] = StandarNutrisiBahan(
                id_standar=self._auto_id_standar,
                nama_bahan_generik=nama,
                protein_min=p_min,
                protein_max=p_max,
                energi_min=e_min,
                energi_max=e_max,
                protein_rata=p_rata,
                energi_rata=e_rata,
                sumber_referensi=sumber,
            )
            self._auto_id_standar += 1

        # Sumber Energi
        add_standar("Jagung kuning", 8, 10, 3200, 3400, 9, 3300, "Literatur umum")
        add_standar("Jagung lokal", 7, 9, 3000, 3200, 8, 3100, "Literatur umum")
        add_standar("Bekatul halus", 11, 13, 2700, 2900, 12, 2800, "Literatur umum")
        add_standar("Bekatul kasar", 9, 11, 2500, 2700, 10, 2600, "Literatur umum")
        add_standar("Dedak padi", 8, 10, 2400, 2600, 9, 2500, "Literatur umum")

        # Sumber Protein
        add_standar("Konsentrat lokal", 30, 40, 2800, 3000, 35, 2900, "Literatur umum")
        add_standar("Tepung ikan lokal", 45, 60, 2700, 2900, 52, 2800, "Literatur umum")
        add_standar("Bungkil kedelai", 40, 48, 2200, 2400, 44, 2300, "Literatur umum")
        add_standar("Ampas tahu", 20, 25, 1800, 2000, 22, 1900, "Literatur umum")

    def _seed_bahan_dasar(self) -> None:
        """Seed beberapa bahan pakan dengan harga lokal estimasi."""

        def add_bahan(
            nama: str,
            kategori: str,
            harga: float,
            supplier: str,
            stok: float = 0.0,
            use_standar: bool = True,
        ) -> None:
            key = nama.lower()
            standar = self.standar_nutrisi.get(key)
            protein = standar.protein_rata if (use_standar and standar) else None
            energi = standar.energi_rata if (use_standar and standar) else None
            is_estimasi = bool(use_standar and standar)

            self.bahan_pakan[self._auto_id_bahan] = BahanPakan(
                id_bahan=self._auto_id_bahan,
                nama_bahan=nama,
                kategori_bahan=kategori,
                harga_per_kg=harga,
                supplier=supplier,
                protein_content=protein,
                energi_metabolis=energi,
                is_estimasi_nutrisi=is_estimasi,
                stok_tersedia=stok,
            )
            self._auto_id_bahan += 1

        add_bahan("Jagung kuning", "Sumber Energi", 6500, "Pasar lokal")
        add_bahan("Bekatul halus", "Sumber Energi", 3500, "Penggilingan padi")
        add_bahan("Dedak padi", "Sumber Energi", 3000, "Penggilingan padi")
        add_bahan("Konsentrat lokal", "Sumber Protein", 11000, "Toko pakan UMKM")
        add_bahan("Tepung ikan lokal", "Sumber Protein", 16000, "Supplier ikan")
        add_bahan("Bungkil kedelai", "Sumber Protein", 12500, "Toko pakan UMKM")
        add_bahan("Ampas tahu", "Sumber Protein", 2500, "Produsen tahu")

    def _seed_formula_contoh(self) -> None:
        """Formula contoh: Starter Mix Ekonomis."""

        def find_id(nama: str) -> int:
            for b in self.bahan_pakan.values():
                if b.nama_bahan.lower() == nama.lower():
                    return b.id_bahan
            raise KeyError(nama)

        formula = FormulaMixPakan(
            id_formula=self._auto_id_formula,
            nama_formula="Starter Mix Ekonomis",
            kategori_umur="Starter",
            mode_nutrisi="estimasi",
            keterangan="Formula contoh untuk DOC/starter dengan biaya ekonomis.",
        )
        self._auto_id_formula += 1
        formula.items = [
            FormulaMixItem(find_id("Jagung kuning"), 50.0),
            FormulaMixItem(find_id("Konsentrat lokal"), 25.0),
            FormulaMixItem(find_id("Bekatul halus"), 20.0),
            FormulaMixItem(find_id("Tepung ikan lokal"), 4.0),
            FormulaMixItem(find_id("Dedak padi"), 1.0),
        ]
        self.formula_mix[formula.id_formula] = formula

    # ---------- Helper akses data ----------

    def get_bahan_df(self) -> pd.DataFrame:
        """Mengembalikan daftar bahan dalam bentuk DataFrame (untuk UI)."""
        rows = []
        for b in self.bahan_pakan.values():
            rows.append(
                {
                    "id_bahan": b.id_bahan,
                    "Nama Bahan": b.nama_bahan,
                    "Kategori": b.kategori_bahan,
                    "Harga per kg (Rp)": b.harga_per_kg,
                    "Supplier": b.supplier,
                    "Protein (%)": b.protein_content,
                    "Energi (kkal/kg)": b.energi_metabolis,
                }
            )
        return pd.DataFrame(rows)

    def get_formula_contoh_df(self) -> pd.DataFrame:
        """
        Mengembalikan komposisi default untuk satu formula contoh
        sebagai DataFrame yang bisa diedit di UI.
        """
        # Ambil formula pertama
        if not self.formula_mix:
            return pd.DataFrame(
                columns=[
                    "id_bahan",
                    "Nama Bahan",
                    "Kategori",
                    "Harga per kg (Rp)",
                    "Persen (%)",
                    "Protein (%)",
                    "Energi (kkal/kg)",
                ]
            )
        formula = next(iter(self.formula_mix.values()))
        rows = []
        for item in formula.items:
            b = self.bahan_pakan[item.id_bahan]
            rows.append(
                {
                    "id_bahan": b.id_bahan,
                    "Nama Bahan": b.nama_bahan,
                    "Kategori": b.kategori_bahan,
                    "Harga per kg (Rp)": b.harga_per_kg,
                    "Persen (%)": item.persen_komposisi,
                    "Protein (%)": b.protein_content,
                    "Energi (kkal/kg)": b.energi_metabolis,
                }
            )
        return pd.DataFrame(rows)

    def get_standar_for_bahan(self, nama_bahan: str) -> Optional[StandarNutrisiBahan]:
        return self.standar_nutrisi.get(nama_bahan.lower())


# Satu instance global yang dapat digunakan oleh UI
feed_mix_db = FeedMixDB()


# =========================
#  Fungsi Simulasi         #
# =========================


def _normalise_komposisi(df: pd.DataFrame) -> pd.DataFrame:
    """Pastikan kolom 'Persen (%)' ada dan digunakan untuk bobot."""
    df = df.copy()
    if "Persen (%)" not in df.columns:
        raise ValueError("Data komposisi harus memiliki kolom 'Persen (%)'.")
    total = df["Persen (%)"].sum()
    if total <= 0:
        raise ValueError("Total persentase komposisi harus > 0.")
    df["Bobot Fraksi"] = df["Persen (%)"] / total
    return df


def simulasi_mix_sederhana(
    df_komposisi: pd.DataFrame,
    total_kg: float,
    harga_komersial_per_kg: float,
    kebutuhan_bulanan_kg: Optional[float] = None,
) -> Dict[str, object]:
    """
    Mode A - SEDERHANA: hanya fokus biaya.

    Parameters
    ----------
    df_komposisi : pd.DataFrame
        Kolom wajib: 'Nama Bahan', 'Harga per kg (Rp)', 'Persen (%)'
    total_kg : float
        Target berat pakan yang akan dibuat (kg).
    harga_komersial_per_kg : float
        Harga pakan komersial pembanding (Rp/kg).
    kebutuhan_bulanan_kg : float, optional
        Jika diisi, akan dihitung estimasi penghematan per bulan.
    """
    df = _normalise_komposisi(df_komposisi)

    # Hitung kebutuhan kg tiap bahan
    df["Kg per Bahan"] = df["Bobot Fraksi"] * total_kg
    df["Biaya per Bahan (Rp)"] = df["Kg per Bahan"] * df["Harga per kg (Rp)"]

    total_biaya = df["Biaya per Bahan (Rp)"].sum()
    harga_mix_per_kg = total_biaya / total_kg if total_kg > 0 else 0

    # Perbandingan vs pakan komersial
    biaya_komersial_total = harga_komersial_per_kg * total_kg
    selisih_per_kg = harga_komersial_per_kg - harga_mix_per_kg

    penghematan_bulanan = None
    if kebutuhan_bulanan_kg and kebutuhan_bulanan_kg > 0:
        penghematan_bulanan = selisih_per_kg * kebutuhan_bulanan_kg

    hasil = {
        "total_biaya": float(total_biaya),
        "harga_mix_per_kg": float(harga_mix_per_kg),
        "harga_komersial_per_kg": float(harga_komersial_per_kg),
        "selisih_per_kg": float(selisih_per_kg),
        "penghematan_bulanan": float(penghematan_bulanan) if penghematan_bulanan is not None else None,
        "tabel_belanja": df[
            ["Nama Bahan", "Kategori", "Harga per kg (Rp)", "Persen (%)", "Kg per Bahan", "Biaya per Bahan (Rp)"]
        ],
    }
    return hasil


def simulasi_mix_estimasi(
    df_komposisi: pd.DataFrame,
    total_kg: float,
    harga_komersial_per_kg: float,
    kebutuhan_bulanan_kg: Optional[float] = None,
) -> Dict[str, object]:
    """
    Mode B - ESTIMASI: biaya + estimasi nutrisi (protein & energi).
    Menggunakan standar_nutrisi_bahan (nilai min, max, rata).
    """
    hasil_biaya = simulasi_mix_sederhana(
        df_komposisi=df_komposisi,
        total_kg=total_kg,
        harga_komersial_per_kg=harga_komersial_per_kg,
        kebutuhan_bulanan_kg=kebutuhan_bulanan_kg,
    )

    df = _normalise_komposisi(df_komposisi)

    # Estimasi protein & energi campuran (berbasis fraksi bobot)
    protein_min_list = []
    protein_max_list = []
    energi_min_list = []
    energi_max_list = []

    for _, row in df.iterrows():
        f = row["Bobot Fraksi"]

        # Jika user mengisi kolom Protein/Energi manual di komposisi, gunakan itu sebagai nilai rata.
        manual_protein = None
        manual_energi = None
        if "Protein (%)" in df.columns and pd.notna(row.get("Protein (%)")):
            manual_protein = float(row["Protein (%)"])
        if "Energi (kkal/kg)" in df.columns and pd.notna(row.get("Energi (kkal/kg)")):
            manual_energi = float(row["Energi (kkal/kg)"])

        standar = feed_mix_db.get_standar_for_bahan(row["Nama Bahan"])

        if manual_protein is not None:
            p_min = p_max = manual_protein
        elif standar:
            p_min = standar.protein_min
            p_max = standar.protein_max
        else:
            p_min = p_max = 0.0

        if manual_energi is not None:
            e_min = e_max = manual_energi
        elif standar:
            e_min = standar.energi_min
            e_max = standar.energi_max
        else:
            e_min = e_max = 0.0

        protein_min_list.append(f * p_min)
        protein_max_list.append(f * p_max)
        energi_min_list.append(f * e_min)
        energi_max_list.append(f * e_max)

    total_protein_min = float(np.sum(protein_min_list))
    total_protein_max = float(np.sum(protein_max_list))
    total_protein_rata = (total_protein_min + total_protein_max) / 2 if (total_protein_min or total_protein_max) else 0

    total_energi_min = float(np.sum(energi_min_list))
    total_energi_max = float(np.sum(energi_max_list))
    total_energi_rata = (total_energi_min + total_energi_max) / 2 if (total_energi_min or total_energi_max) else 0

    hasil_biaya.update(
        {
            "protein_min": total_protein_min,
            "protein_max": total_protein_max,
            "protein_rata": total_protein_rata,
            "energi_min": total_energi_min,
            "energi_max": total_energi_max,
            "energi_rata": total_energi_rata,
        }
    )
    return hasil_biaya


def hitung_kebutuhan_bulanan_kg(
    jumlah_ayam: int,
    konsumsi_gram_per_ekor_per_hari: float,
    hari_per_bulan: int = 30,
) -> float:
    """Hitung estimasi kebutuhan pakan (kg/bulan) berdasarkan konsumsi harian."""
    if jumlah_ayam <= 0 or konsumsi_gram_per_ekor_per_hari <= 0 or hari_per_bulan <= 0:
        return 0.0
    return float(jumlah_ayam * konsumsi_gram_per_ekor_per_hari / 1000.0 * hari_per_bulan)


# Fungsi CRUD sederhana yang diminta di prompt (implementasi minimal)


def tambah_bahan_sederhana(nama: str, kategori: str, harga: float, supplier: str) -> BahanPakan:
    """Tambah bahan pakan baru tanpa data nutrisi (mode sederhana)."""
    global feed_mix_db
    b = BahanPakan(
        id_bahan=feed_mix_db._auto_id_bahan,
        nama_bahan=nama,
        kategori_bahan=kategori,
        harga_per_kg=harga,
        supplier=supplier,
        is_estimasi_nutrisi=False,
    )
    feed_mix_db.bahan_pakan[b.id_bahan] = b
    feed_mix_db._auto_id_bahan += 1
    return b


def tambah_bahan_lengkap(nama: str, harga: float, protein: float, energi: float, supplier: str) -> BahanPakan:
    """Tambah bahan pakan dengan data nutrisi lengkap (mode detail)."""
    global feed_mix_db
    b = BahanPakan(
        id_bahan=feed_mix_db._auto_id_bahan,
        nama_bahan=nama,
        kategori_bahan="Custom",
        harga_per_kg=harga,
        supplier=supplier,
        protein_content=protein,
        energi_metabolis=energi,
        is_estimasi_nutrisi=False,
    )
    feed_mix_db.bahan_pakan[b.id_bahan] = b
    feed_mix_db._auto_id_bahan += 1
    return b


def auto_estimasi_nutrisi(id_bahan: int) -> Optional[BahanPakan]:
    """Update nutrisi bahan berdasarkan standar_nutrisi_bahan jika tersedia."""
    global feed_mix_db
    b = feed_mix_db.bahan_pakan.get(id_bahan)
    if not b:
        return None
    standar = feed_mix_db.get_standar_for_bahan(b.nama_bahan)
    if not standar:
        return b
    b.protein_content = standar.protein_rata
    b.energi_metabolis = standar.energi_rata
    b.is_estimasi_nutrisi = True
    b.tanggal_update = datetime.now()
    return b


def get_bahan_by_supplier(nama_supplier: str) -> List[BahanPakan]:
    """Ambil daftar bahan berdasarkan nama supplier."""
    global feed_mix_db
    return [b for b in feed_mix_db.bahan_pakan.values() if b.supplier.lower() == nama_supplier.lower()]


def catat_kualitas_bahan(id_bahan: int, catatan: str) -> Optional[BahanPakan]:
    """Tambahkan/catatan kualitas visual/empiris pada bahan."""
    global feed_mix_db
    b = feed_mix_db.bahan_pakan.get(id_bahan)
    if not b:
        return None
    if b.catatan_kualitas:
        b.catatan_kualitas += "\n" + catatan
    else:
        b.catatan_kualitas = catatan
    b.tanggal_update = datetime.now()
    return b


