# -*- coding: utf-8 -*-
"""
generate_prediction_figures.py
==============================
Skrip lengkap untuk menghasilkan gambar statis (PNG 300 DPI) dan data plot (CSV)
hasil evaluasi testing (Direct vs Rolling) dan peramalan 2026 (12 bulan)
untuk keperluan buku skripsi.

Model: Gradient Boosting (HistGradientBoostingRegressor)
Pembagian data: Train Jan 2023 - Sep 2025, Test Okt 2025 - Des 2025
Eksogen: CURAH_HUJAN dan VOLUME_CONTAINER aktual (t)

Semua figur dan file CSV disimpan di folder: ./output_figures/
"""

import argparse
import os
import sys
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error

# Import pustaka pipeline proyek
BASE_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path(".")
sys.path.insert(0, str(BASE_DIR))
import pipeline_lib as pl

warnings.filterwarnings("ignore")

# ============================================================================
# KONFIGURASI GLOBAL & TAMPILAN
# ============================================================================
OUTPUT_DIR = BASE_DIR / "output_figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Konfigurasi Font & Matplotlib (Font minimal 11 pt, 300 DPI)
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans", "Helvetica"],
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "xtick.labelsize": 10.5,
    "ytick.labelsize": 10.5,
    "legend.fontsize": 10.5,
    "figure.titlesize": 13,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})

# Palet warna ramah buta warna (Colorblind-friendly)
COLOR_TRAIN = "#4D4D4D"      # Dark charcoal / abu gelap
COLOR_TEST = "#0072B2"       # Blue / biru tua
COLOR_DIRECT = "#D55E00"     # Vermilion / oranye kemerahan
COLOR_ROLLING = "#7570B3"    # Purple / ungu
COLOR_FORECAST = "#C00000"   # Crimson / merah tua

# Nama bulan dalam Bahasa Indonesia
MONTH_NAMES_INDO = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "Mei", 6: "Jun",
    7: "Jul", 8: "Agu", 9: "Sep", 10: "Okt", 11: "Nov", 12: "Des"
}

# 10 Unit target
ALL_TARGET_UNITS = [
    "K01_UNIT_008", "K01_UNIT_162", "K02_UNIT_135", "K02_UNIT_155", "K03_UNIT_070",
    "K04_UNIT_298", "K05_UNIT_208", "K12_UNIT_120", "K34_UNIT_009", "K49_UNIT_332"
]

# 5 Kriteria target
ALL_TARGET_KRITERIA = ["K04", "K09", "K15", "K34", "K60"]

# Target validasi acuan (toleransi 0,01)
REFERENCE_UNITS = {
    "K01_UNIT_008": {"mape_direct": 2.96, "mape_rolling": 2.96, "varian": "yeojohnson"},
    "K01_UNIT_162": {"mape_direct": 6.56, "mape_rolling": 5.82, "varian": "baseline"},
    "K02_UNIT_135": {"mape_direct": 11.56, "mape_rolling": 16.24, "varian": "baseline"},
    "K02_UNIT_155": {"mape_direct": 2.35, "mape_rolling": 2.35, "varian": "robust"},
    "K03_UNIT_070": {"mape_direct": 35.11, "mape_rolling": 35.11, "varian": "yeojohnson"},
    "K04_UNIT_298": {"mape_direct": 5.07, "mape_rolling": 6.49, "varian": "robust"},
    "K05_UNIT_208": {"mape_direct": 11.54, "mape_rolling": 13.61, "varian": "baseline"},
    "K12_UNIT_120": {"mape_direct": 10.26, "mape_rolling": 9.49, "varian": "yeojohnson"},
    "K34_UNIT_009": {"mape_direct": 18.40, "mape_rolling": 34.85, "varian": "robust"},
    "K49_UNIT_332": {"mape_direct": 23.68, "mape_rolling": 30.30, "varian": "savgol"},
}

REFERENCE_KRITERIA = {
    "K04": {"mape_direct": 16.64, "mape_rolling": 19.26, "varian": "baseline"},
    "K09": {"mape_direct": 5.31, "mape_rolling": 5.39, "varian": "robust"},
    "K15": {"mape_direct": 16.10, "mape_rolling": 18.09, "varian": "robust"},
    "K34": {"mape_direct": 26.53, "mape_rolling": 26.53, "varian": "robust"},
    "K60": {"mape_direct": 9.95, "mape_rolling": 9.95, "varian": "yeojohnson"},
}


# ============================================================================
# FUNGSI UTILITAS & FORMATTING
# ============================================================================
def safe_savefig(fig, path, **kwargs):
    """Menyimpan figur dengan mekanisme retry untuk mencegah OSError transien pada Windows."""
    import time
    for attempt in range(5):
        try:
            fig.savefig(str(path), **kwargs)
            return
        except OSError as e:
            if attempt < 4:
                time.sleep(0.6)
            else:
                raise e


def format_indo_number(val, decimals=2):
    """Format angka Indonesia: titik untuk ribuan, koma untuk desimal."""
    if pd.isna(val) or val is None:
        return "-"
    formatted = f"{float(val):,.{decimals}f}"
    parts = formatted.split(".")
    whole = parts[0].replace(",", ".")
    dec = parts[1] if len(parts) > 1 else ""
    return f"{whole},{dec}" if dec else whole


def format_indo_month(period_or_str):
    """Format bulan menjadi 'Okt 2025'."""
    if isinstance(period_or_str, pd.Period):
        m = period_or_str.month
        y = period_or_str.year
    else:
        parts = str(period_or_str).split("-")
        y = int(parts[0])
        m = int(parts[1])
    return f"{MONTH_NAMES_INDO[m]} {y}"


def format_kriteria_title(kode, jenis, merk, cap, hp):
    """Format judul kriteria: tanpa kata 'Ton' dan desimal kapasitas memakai koma."""
    if isinstance(cap, (int, float)):
        cap_val = format_indo_number(cap, 1 if cap % 1 != 0 else 0)
    else:
        cap_val = str(cap).replace(".", ",")
    hp_val = format_indo_number(hp, 0)
    return f"Aktual vs Prediksi Operating Hours — {kode} ({jenis}, {merk}, kapasitas {cap_val}, {hp_val} HP)"


def eval_metrics(actual, pred):
    """Menghitung MAPE (%) dan RMSE (jam)."""
    if pred is None:
        return np.nan, np.nan
    actual = np.asarray(actual, dtype=float)
    pred = np.asarray(pred, dtype=float)
    mask = ~pd.isna(actual) & ~pd.isna(pred)
    if mask.sum() == 0:
        return np.nan, np.nan
    a, p = actual[mask], pred[mask]
    a_safe = np.where(a == 0, np.nan, a)
    mape = np.nanmean(np.abs((a_safe - p) / a_safe)) * 100
    rmse = np.sqrt(mean_squared_error(a, p))
    return mape, rmse


def get_safe_y_limit(arrays, is_k09=False):
    """Menghitung batas atas sumbu Y:
    - Untuk K09: nilai maksimum data x 1,08 (jangan dibatasi 744 dan jangan terpotong).
    - Untuk unit/kriteria lain: mulai 0, maksimum tidak melebihi 744 jam.
    """
    max_val = 0.0
    for arr in arrays:
        if arr is not None and len(arr) > 0:
            valid = np.asarray(arr)[~pd.isna(arr)]
            if len(valid) > 0:
                max_val = max(max_val, float(np.max(valid)))
    if is_k09:
        top = max_val * 1.08
    else:
        top = min(744.0, max_val * 1.15)
    if top <= 0:
        top = 100.0
    return 0.0, top


# ============================================================================
# PARSING ARGUMEN CLI
# ============================================================================
parser = argparse.ArgumentParser(description="Generate prediction and forecast figures.")
parser.add_argument("--all", action="store_true", help="Generate all 10 units, 5 criteria, and panels.")
parser.add_argument("--units", nargs="*", default=None, help="Specific units to generate figures for.")
parser.add_argument("--kriteria", nargs="*", default=None, help="Specific criteria to generate figures for.")
args = parser.parse_args()

if args.all:
    target_units_to_plot = ALL_TARGET_UNITS
    target_kriteria_to_plot = ALL_TARGET_KRITERIA
    generate_panels = True
else:
    # Default revisi: fig_test_K01_UNIT_008, fig_test_K02_UNIT_155, fig_test_kriteria_K09,
    # fig_forecast_K01_UNIT_008, fig_forecast_K02_UNIT_155
    target_units_to_plot = args.units if args.units is not None else ["K01_UNIT_008", "K02_UNIT_155"]
    target_kriteria_to_plot = args.kriteria if args.kriteria is not None else ["K09"]
    generate_panels = False

print(f"Target unit yang diplot: {target_units_to_plot}")
print(f"Target kriteria yang diplot: {target_kriteria_to_plot}")
print(f"Generate panels: {generate_panels}")


# ============================================================================
# PEMUATAN DATA & PERSIAPAN PREPROSESING
# ============================================================================
print("=" * 70)
print("MEMUAT DATASET & KONFIGURASI CHECKPOINT...")
print("=" * 70)

ckpt_dir = BASE_DIR / "checkpoints_v4"
rev_h3_dir = ckpt_dir / "rev_h3"
if not rev_h3_dir.exists():
    rev_h3_dir = ckpt_dir / "h3bulan"

monthly_full_raw = pl.load_monthly_full_checkpoint(ckpt_dir)
kriteria_raw = pl.load_kriteria_checkpoint(ckpt_dir)

# Mapping unit dan kriteria revisi 190 unit
map_path = rev_h3_dir / "mapping_unit_dan_kriteria.xlsx"
df_map_u = pd.read_excel(map_path, sheet_name="Mapping_Unit")
df_map_k = pd.read_excel(map_path, sheet_name="Ringkasan_Kriteria")

valid_190_units = set(df_map_u[df_map_u["STATUS"] == "VALID_190"]["EQUIP_NAME_BARU"])
print(f"Total armada valid: {len(valid_190_units)} unit (termasuk 25 unit excluded yang disaring).")

# Filter monthly_full dan kriteria ke 190 unit valid
monthly_full = monthly_full_raw[monthly_full_raw["EQUIP NAME"].isin(valid_190_units)].copy()
kriteria = kriteria_raw[kriteria_raw["EQUIP NAME"].isin(valid_190_units)].copy()

# Metadata kamus unit
unit_meta = {}
for _, r in df_map_u[df_map_u["EQUIP_NAME_BARU"].isin(valid_190_units)].iterrows():
    u = r["EQUIP_NAME_BARU"]
    unit_meta[u] = {
        "KODE_KRITERIA": r.get("KODE_KRITERIA", ""),
        "JENIS": r.get("JENIS", ""),
        "TYPE/MERK": r.get("TYPE/MERK", ""),
        "CAP": r.get("CAP", ""),
        "HP": r.get("HP", ""),
    }

# Metadata kamus kriteria
kriteria_meta = {}
for _, r in df_map_k.iterrows():
    k = r["KODE_KRITERIA"]
    kriteria_meta[k] = {
        "KRITERIA_ID": r["KRITERIA_ID"],
        "JENIS": r.get("JENIS", ""),
        "TYPE/MERK": r.get("TYPE/MERK", ""),
        "CAP": r.get("CAP", ""),
        "HP": r.get("HP", ""),
    }

# Konfigurasi GB akhir
final_cfg_u = pl.load_final_config(rev_h3_dir, level="unit")
final_cfg_k = pl.load_final_config(rev_h3_dir, level="kriteria")

# Future forecast 2026 (12 bulan)
df_forecast_raw = pl.load_future_forecast(rev_h3_dir)

# Split train dan test
train_raw = monthly_full[monthly_full["TAHUN_BULAN"] <= pl.TRAIN_END].copy()
test_raw = monthly_full[(monthly_full["TAHUN_BULAN"] >= pl.TEST_START) & (monthly_full["TAHUN_BULAN"] <= pl.TEST_END)].copy()

# Preprosesing untuk setiap varian (baseline, savgol, robust, yeojohnson)
prepped_data = {}
for variant in pl.DATA_PREP_VARIANTS:
    tr_p, te_p, transformers = pl.DATA_PREP_VARIANTS[variant](train_raw, test_raw)
    tr_full = tr_p.merge(kriteria[["EQUIP NAME", "KRITERIA_ID"]], on="EQUIP NAME", how="left")
    te_full = te_p.merge(kriteria[["EQUIP NAME", "KRITERIA_ID"]], on="EQUIP NAME", how="left")
    
    full_lag = pl.make_lag_features(pd.concat([tr_full, te_full], ignore_index=True))
    tr_lag = full_lag[full_lag["TAHUN_BULAN"] <= pl.TRAIN_END].copy()
    te_lag = full_lag[(full_lag["TAHUN_BULAN"] >= pl.TEST_START) & (full_lag["TAHUN_BULAN"] <= pl.TEST_END)].copy()
    
    prepped_data[variant] = {
        "train_lag": tr_lag,
        "test_lag": te_lag,
        "transformers": transformers,
    }


# ============================================================================
# EVALUASI & VALIDASI WAJIB (10 UNIT & 5 KRITERIA)
# ============================================================================
print("\n" + "=" * 70)
print("EVALUASI MODEL & VALIDASI WAJIB...")
print("=" * 70)

unit_results = {}
unit_validation_passed = {}

for unit in ALL_TARGET_UNITS:
    ref = REFERENCE_UNITS[unit]
    row = final_cfg_u[final_cfg_u["EQUIP NAME"] == unit]
    if row.empty:
        print(f"PERINGATAN: Konfigurasi unit {unit} tidak ditemukan!")
        unit_validation_passed[unit] = False
        continue
    row = row.iloc[0]
    variant = row["V4_GB_VARIAN"]
    params = pl.clean_gb_params(row)
    
    prep = prepped_data[variant]
    g_train = prep["train_lag"][prep["train_lag"]["EQUIP NAME"] == unit].dropna(subset=pl.FEAT_COLS + ["UTILITAS_SMOOTH"])
    g_test = prep["test_lag"][prep["test_lag"]["EQUIP NAME"] == unit].dropna(subset=pl.FEAT_COLS)
    tf = prep["transformers"]
    
    model = HistGradientBoostingRegressor(random_state=42, **params)
    model.fit(g_train[pl.FEAT_COLS], g_train["UTILITAS_SMOOTH"])
    
    # Direct Prediction
    pred_direct_raw = model.predict(g_test[pl.FEAT_COLS])
    pred_direct = pl.inverse_transform_pred(pred_direct_raw, unit, tf)
    pred_direct = np.clip(pred_direct, 0.0, 744.0).round(2)
    
    # Rolling Prediction
    g_test_sorted = g_test.sort_values("TAHUN_BULAN").reset_index(drop=True)
    init_lags = [g_test_sorted.loc[0, "lag_1"], g_test_sorted.loc[0, "lag_2"], g_test_sorted.loc[0, "lag_3"]]
    exog_future = g_test_sorted[["CURAH_HUJAN", "VOLUME_CONTAINER"]].values
    pred_rolling_raw = pl.forecast_gb_rolling(model, init_lags, exog_future)
    pred_rolling = pl.inverse_transform_pred(pred_rolling_raw, unit, tf)
    pred_rolling = np.clip(pred_rolling, 0.0, 744.0).round(2)
    
    actual_test = g_test_sorted["UTILITAS"].values
    mape_d, rmse_d = eval_metrics(actual_test, pred_direct)
    mape_r, rmse_r = eval_metrics(actual_test, pred_rolling)
    
    # Validasi terhadap target referensi (toleransi 0.01)
    diff_d = abs(mape_d - ref["mape_direct"])
    diff_r = abs(mape_r - ref["mape_rolling"])
    passed = (diff_d <= 0.01) and (diff_r <= 0.01)
    
    if passed:
        print(f"[PASS] {unit}: Direct={mape_d:.2f}% (ref {ref['mape_direct']:.2f}%), Rolling={mape_r:.2f}% (ref {ref['mape_rolling']:.2f}%)")
    else:
        print(f"[FAIL] {unit}: Direct={mape_d:.4f}% vs ref={ref['mape_direct']}%, Rolling={mape_r:.4f}% vs ref={ref['mape_rolling']}%")
        print(f"       Penyebab yang dicurigai: ketidaksesuaian varian atau filtering unit.")
        
    unit_validation_passed[unit] = passed
    
    # Data training historis
    g_hist_train = monthly_full[(monthly_full["EQUIP NAME"] == unit) & (monthly_full["TAHUN_BULAN"] <= pl.TRAIN_END)].sort_values("TAHUN_BULAN")
    
    unit_results[unit] = {
        "variant": variant,
        "params": params,
        "mape_direct": mape_d,
        "rmse_direct": rmse_d,
        "mape_rolling": mape_r,
        "rmse_rolling": rmse_r,
        "train_periods": g_hist_train["TAHUN_BULAN"].tolist(),
        "train_actual": g_hist_train["UTILITAS"].tolist(),
        "test_periods": g_test_sorted["TAHUN_BULAN"].tolist(),
        "test_actual": actual_test.tolist(),
        "pred_direct": pred_direct.tolist(),
        "pred_rolling": pred_rolling.tolist(),
    }

# Evaluasi 5 Kriteria
kriteria_results = {}
kriteria_validation_passed = {}

for kode in ALL_TARGET_KRITERIA:
    ref = REFERENCE_KRITERIA[kode]
    k_meta = kriteria_meta[kode]
    krit_id = k_meta["KRITERIA_ID"]
    
    row = final_cfg_k[final_cfg_k["KRITERIA_ID"] == krit_id]
    if row.empty:
        print(f"PERINGATAN: Konfigurasi kriteria {kode} ({krit_id}) tidak ditemukan!")
        kriteria_validation_passed[kode] = False
        continue
    row = row.iloc[0]
    variant = row["V4_GB_VARIAN"]
    params = pl.clean_gb_params(row)
    
    prep = prepped_data[variant]
    g_train = prep["train_lag"][prep["train_lag"]["KRITERIA_ID"] == krit_id].dropna(subset=pl.FEAT_COLS + ["UTILITAS_SMOOTH"])
    g_test = prep["test_lag"][prep["test_lag"]["KRITERIA_ID"] == krit_id].dropna(subset=pl.FEAT_COLS)
    tf = prep["transformers"]
    
    model = HistGradientBoostingRegressor(random_state=42, **params)
    model.fit(g_train[pl.FEAT_COLS], g_train["UTILITAS_SMOOTH"])
    
    pred_direct_all = model.predict(g_test[pl.FEAT_COLS])
    
    actual_all, pred_direct_all_list, pred_rolling_all_list = [], [], []
    unit_members_test = {}
    
    for u, g_u in g_test.groupby("EQUIP NAME"):
        mask = (g_test["EQUIP NAME"] == u).values
        u_pred_d = pl.inverse_transform_pred(pred_direct_all[mask], u, tf)
        u_pred_d = np.clip(u_pred_d, 0.0, 744.0).round(2)
        u_act = g_u.sort_values("TAHUN_BULAN")["UTILITAS"].values
        
        g_u_sorted = g_u.sort_values("TAHUN_BULAN").reset_index(drop=True)
        init_lags = [g_u_sorted.loc[0, "lag_1"], g_u_sorted.loc[0, "lag_2"], g_u_sorted.loc[0, "lag_3"]]
        exog_future = g_u_sorted[["CURAH_HUJAN", "VOLUME_CONTAINER"]].values
        u_pred_r = pl.inverse_transform_pred(pl.forecast_gb_rolling(model, init_lags, exog_future), u, tf)
        u_pred_r = np.clip(u_pred_r, 0.0, 744.0).round(2)
        
        actual_all.extend(u_act)
        pred_direct_all_list.extend(u_pred_d)
        pred_rolling_all_list.extend(u_pred_r)
        
        unit_members_test[u] = {
            "periods": g_u_sorted["TAHUN_BULAN"].tolist(),
            "actual": u_act,
            "pred_direct": u_pred_d,
            "pred_rolling": u_pred_r,
        }
        
    actual_all = np.array(actual_all)
    pred_direct_all_list = np.array(pred_direct_all_list)
    pred_rolling_all_list = np.array(pred_rolling_all_list)
    
    mape_d, rmse_d = eval_metrics(actual_all, pred_direct_all_list)
    mape_r, rmse_r = eval_metrics(actual_all, pred_rolling_all_list)
    
    diff_d = abs(mape_d - ref["mape_direct"])
    diff_r = abs(mape_r - ref["mape_rolling"])
    passed = (diff_d <= 0.01) and (diff_r <= 0.01)
    
    if passed:
        print(f"[PASS] {kode}: Direct={mape_d:.2f}% (ref {ref['mape_direct']:.2f}%), Rolling={mape_r:.2f}% (ref {ref['mape_rolling']:.2f}%)")
    else:
        print(f"[FAIL] {kode}: Direct={mape_d:.4f}% vs ref={ref['mape_direct']}%, Rolling={mape_r:.4f}% vs ref={ref['mape_rolling']}%")
        print(f"       Penyebab yang dicurigai: ketidaksesuaian varian atau unit yang dimasukkan.")
        
    kriteria_validation_passed[kode] = passed
    
    # Rata-rata per unit anggota (jam) untuk plotting
    g_hist_k = monthly_full[(monthly_full["EQUIP NAME"].isin(unit_members_test.keys())) & (monthly_full["TAHUN_BULAN"] <= pl.TRAIN_END)]
    train_mean_s = g_hist_k.groupby("TAHUN_BULAN")["UTILITAS"].mean().sort_index()
    
    test_periods_list = sorted(list(set(g_test["TAHUN_BULAN"])))
    test_act_mean = []
    test_pred_d_mean = []
    test_pred_r_mean = []
    for p in test_periods_list:
        p_acts = [unit_members_test[u]["actual"][idx] for u in unit_members_test for idx, pr in enumerate(unit_members_test[u]["periods"]) if pr == p]
        p_preds_d = [unit_members_test[u]["pred_direct"][idx] for u in unit_members_test for idx, pr in enumerate(unit_members_test[u]["periods"]) if pr == p]
        p_preds_r = [unit_members_test[u]["pred_rolling"][idx] for u in unit_members_test for idx, pr in enumerate(unit_members_test[u]["periods"]) if pr == p]
        test_act_mean.append(float(np.mean(p_acts)))
        test_pred_d_mean.append(float(np.mean(p_preds_d)))
        test_pred_r_mean.append(float(np.mean(p_preds_r)))
        
    kriteria_results[kode] = {
        "variant": variant,
        "mape_direct": mape_d,
        "rmse_direct": rmse_d,
        "mape_rolling": mape_r,
        "rmse_rolling": rmse_r,
        "train_periods": train_mean_s.index.tolist(),
        "train_actual_mean": train_mean_s.values.tolist(),
        "test_periods": test_periods_list,
        "test_actual_mean": test_act_mean,
        "test_pred_d_mean": test_pred_d_mean,
        "test_pred_r_mean": test_pred_r_mean,
    }


# ============================================================================
# PEMBUATAN GAMBAR & DATA CSV
# ============================================================================
print("\n" + "=" * 70)
print("MEMBUAT GAMBAR HASIL EVALUASI & PERAMALAN...")
print("=" * 70)

# Daftar periode tick sumbu X 36 bulan: tiap 4 bulan + Okt 2025 dan Des 2025 saja
TICK_PERIODS_36 = [
    pd.Period("2023-01", "M"), pd.Period("2023-05", "M"), pd.Period("2023-09", "M"),
    pd.Period("2024-01", "M"), pd.Period("2024-05", "M"), pd.Period("2024-09", "M"),
    pd.Period("2025-01", "M"), pd.Period("2025-05", "M"), pd.Period("2025-09", "M"),
    pd.Period("2025-10", "M"), pd.Period("2025-12", "M")
]

# Daftar periode tick sumbu X 48 bulan (peramalan 2026): tiap 4 bulan + Okt 2025, Des 2025, dan 2026
TICK_PERIODS_48 = [
    pd.Period("2023-01", "M"), pd.Period("2023-05", "M"), pd.Period("2023-09", "M"),
    pd.Period("2024-01", "M"), pd.Period("2024-05", "M"), pd.Period("2024-09", "M"),
    pd.Period("2025-01", "M"), pd.Period("2025-05", "M"), pd.Period("2025-09", "M"),
    pd.Period("2025-10", "M"), pd.Period("2025-12", "M"),
    pd.Period("2026-04", "M"), pd.Period("2026-08", "M"), pd.Period("2026-12", "M")
]


# ----------------------------------------------------------------------------
# 1) INDIVIDUAL TEST PLOTS
# ----------------------------------------------------------------------------
print(f"\n--- 1) Menghasilkan fig_test_<UNIT>.png & plot_data_test_<UNIT>.csv ---")
for unit in target_units_to_plot:
    if not unit_validation_passed.get(unit, False):
        print(f"[SKIP] {unit} dilewati karena validasi gagal.")
        continue
        
    res = unit_results[unit]
    meta = unit_meta[unit]
    jenis = meta["JENIS"]
    variant = res["variant"]
    
    # Persiapan data deret waktu
    tr_periods = res["train_periods"]
    tr_actual = res["train_actual"]
    te_periods = res["test_periods"]
    te_actual = res["test_actual"]
    pred_d = res["pred_direct"]
    pred_r = res["pred_rolling"]
    
    # Sambungkan titik terakhir training (2025-09) ke awal testing agar kurva kontinu
    conn_periods = [tr_periods[-1]] + te_periods
    conn_actual = [tr_actual[-1]] + te_actual
    conn_pred_d = [tr_actual[-1]] + pred_d
    conn_pred_r = [tr_actual[-1]] + pred_r
    
    all_periods = tr_periods + te_periods
    x_indices = {p: i for i, p in enumerate(all_periods)}
    
    x_tr = [x_indices[p] for p in tr_periods]
    x_conn = [x_indices[p] for p in conn_periods]
    
    fig, ax = plt.subplots(figsize=(10, 4.2))
    
    # Plot kurva
    ax.plot(x_tr, tr_actual, color=COLOR_TRAIN, linestyle="-", marker="o", markersize=4,
            linewidth=1.5, label="Aktual (training)")
    ax.plot(x_conn, conn_actual, color=COLOR_TEST, linestyle="-", marker="o", markersize=5,
            linewidth=1.8, label="Aktual (test)")
    ax.plot(x_conn, conn_pred_d, color=COLOR_DIRECT, linestyle="-", marker="s", markersize=5,
            linewidth=1.8, label="Prediksi direct")
    ax.plot(x_conn, conn_pred_r, color=COLOR_ROLLING, linestyle="--", marker="^", markersize=5,
            linewidth=1.8, label="Prediksi rolling")
    
    # Konfigurasi sumbu & judul
    title_text = f"Aktual vs Prediksi Operating Hours — {unit} ({jenis})"
    sub_text = (
        f"Varian: {variant} | "
        f"Direct: MAPE = {format_indo_number(res['mape_direct'])}%, RMSE = {format_indo_number(res['rmse_direct'])} jam | "
        f"Rolling: MAPE = {format_indo_number(res['mape_rolling'])}%, RMSE = {format_indo_number(res['rmse_rolling'])} jam"
    )
    ax.set_title(f"{title_text}\n{sub_text}", fontsize=11, pad=10)
    
    ax.set_xlabel("Bulan", fontsize=11, labelpad=10)
    ax.set_ylabel("Operating Hours (jam)", fontsize=11)
    
    y_min, y_max = get_safe_y_limit([tr_actual, te_actual, pred_d, pred_r])
    ax.set_ylim(bottom=0.0, top=y_max)
    
    # Ticks sumbu X: tiap 4 bulan + Okt 2025 & Des 2025 saja, rotasi 45 derajat
    tick_locs = [x_indices[p] for p in TICK_PERIODS_36 if p in x_indices]
    tick_labels = [format_indo_month(p) for p in TICK_PERIODS_36 if p in x_indices]
    ax.set_xticks(tick_locs)
    ax.set_xticklabels(tick_labels, rotation=45, ha="right", fontsize=10)
    
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)
    
    # Legenda di luar area plot: di bawah, di tengah, 4 kolom
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.32), ncol=4,
              frameon=True, framealpha=0.9, edgecolor="#cccccc", fontsize=10.5)
    
    fig_path = OUTPUT_DIR / f"fig_test_{unit}.png"
    safe_savefig(fig, fig_path, bbox_inches="tight")
    plt.close(fig)
    print(f"  [OK] Disimpan: {fig_path.name}")
    
    # Simpan CSV plot data
    csv_rows = []
    for p, act in zip(tr_periods, tr_actual):
        csv_rows.append({
            "TAHUN_BULAN": str(p),
            "BULAN_LABEL": format_indo_month(p),
            "SET": "train",
            "AKTUAL": round(act, 2),
            "PRED_DIRECT": np.nan,
            "PRED_ROLLING": np.nan
        })
    for p, act, pd_val, pr_val in zip(te_periods, te_actual, pred_d, pred_r):
        csv_rows.append({
            "TAHUN_BULAN": str(p),
            "BULAN_LABEL": format_indo_month(p),
            "SET": "test",
            "AKTUAL": round(act, 2),
            "PRED_DIRECT": round(pd_val, 2),
            "PRED_ROLLING": round(pr_val, 2)
        })
    df_csv = pd.DataFrame(csv_rows)
    csv_path = OUTPUT_DIR / f"plot_data_test_{unit}.csv"
    df_csv.to_csv(csv_path, index=False)


# ----------------------------------------------------------------------------
# 3) INDIVIDUAL KRITERIA TEST PLOTS
# ----------------------------------------------------------------------------
print(f"\n--- 3) Menghasilkan fig_test_kriteria_<KODE>.png & plot_data_test_kriteria_<KODE>.csv ---")
for kode in target_kriteria_to_plot:
    if not kriteria_validation_passed.get(kode, False):
        print(f"[SKIP] Kriteria {kode} dilewati karena validasi gagal.")
        continue
        
    res = kriteria_results[kode]
    meta = kriteria_meta[kode]
    jenis = meta["JENIS"]
    merk = meta["TYPE/MERK"]
    cap = meta["CAP"]
    hp = meta["HP"]
    variant = res["variant"]
    
    tr_periods = res["train_periods"]
    tr_actual = res["train_actual_mean"]
    te_periods = res["test_periods"]
    te_actual = res["test_actual_mean"]
    pred_d = res["test_pred_d_mean"]
    pred_r = res["test_pred_r_mean"]
    
    conn_periods = [tr_periods[-1]] + te_periods
    conn_actual = [tr_actual[-1]] + te_actual
    conn_pred_d = [tr_actual[-1]] + pred_d
    
    all_periods = tr_periods + te_periods
    x_indices = {p: i for i, p in enumerate(all_periods)}
    
    x_tr = [x_indices[p] for p in tr_periods]
    x_conn = [x_indices[p] for p in conn_periods]
    
    fig, ax = plt.subplots(figsize=(10, 4.2))
    
    ax.plot(x_tr, tr_actual, color=COLOR_TRAIN, linestyle="-", marker="o", markersize=4,
            linewidth=1.5, label="Aktual (training)")
    ax.plot(x_conn, conn_actual, color=COLOR_TEST, linestyle="-", marker="o", markersize=5,
            linewidth=1.8, label="Aktual (test)")
    ax.plot(x_conn, conn_pred_d, color=COLOR_DIRECT, linestyle="-", marker="s", markersize=5,
            linewidth=1.8, label="Prediksi direct")
    
    # Judul kriteria: tanpa kata 'Ton' dan desimal pakai koma, contoh 'kapasitas 40,6'
    title_text = format_kriteria_title(kode, jenis, merk, cap, hp)
    sub_text = (
        f"Varian: {variant} | "
        f"MAPE = {format_indo_number(res['mape_direct'])}% | "
        f"RMSE = {format_indo_number(res['rmse_direct'])} jam"
    )
    ax.set_title(f"{title_text}\n{sub_text}", fontsize=11, pad=10)
    
    ax.set_xlabel("Bulan", fontsize=11, labelpad=10)
    ax.set_ylabel("Operating Hours (jam)", fontsize=11)
    
    # Untuk K09: batas atas sumbu y = nilai maksimum data x 1,08 (jangan dibatasi 744 dan jangan terpotong)
    is_k09 = (kode == "K09")
    y_min, y_max = get_safe_y_limit([tr_actual, te_actual, pred_d], is_k09=is_k09)
    ax.set_ylim(bottom=0.0, top=y_max)
    
    # Ticks sumbu X: tiap 4 bulan + Okt 2025 & Des 2025 saja, rotasi 45 derajat
    tick_locs = [x_indices[p] for p in TICK_PERIODS_36 if p in x_indices]
    tick_labels = [format_indo_month(p) for p in TICK_PERIODS_36 if p in x_indices]
    ax.set_xticks(tick_locs)
    ax.set_xticklabels(tick_labels, rotation=45, ha="right", fontsize=10)
    
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)
    
    # Legenda di luar area plot: di bawah, di tengah, 4 kolom
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.32), ncol=4,
              frameon=True, framealpha=0.9, edgecolor="#cccccc", fontsize=10.5)
    
    fig_path = OUTPUT_DIR / f"fig_test_kriteria_{kode}.png"
    safe_savefig(fig, fig_path, bbox_inches="tight")
    plt.close(fig)
    print(f"  [OK] Disimpan: {fig_path.name}")
    
    # CSV data plot kriteria
    csv_rows = []
    for p, act in zip(tr_periods, tr_actual):
        csv_rows.append({
            "TAHUN_BULAN": str(p),
            "BULAN_LABEL": format_indo_month(p),
            "SET": "train",
            "AKTUAL_RATA_RATA": round(act, 2),
            "PRED_DIRECT_RATA_RATA": np.nan,
            "PRED_ROLLING_RATA_RATA": np.nan
        })
    for p, act, pd_val, pr_val in zip(te_periods, te_actual, pred_d, pred_r):
        csv_rows.append({
            "TAHUN_BULAN": str(p),
            "BULAN_LABEL": format_indo_month(p),
            "SET": "test",
            "AKTUAL_RATA_RATA": round(act, 2),
            "PRED_DIRECT_RATA_RATA": round(pd_val, 2),
            "PRED_ROLLING_RATA_RATA": round(pr_val, 2)
        })
    df_csv = pd.DataFrame(csv_rows)
    csv_path = OUTPUT_DIR / f"plot_data_test_kriteria_{kode}.csv"
    df_csv.to_csv(csv_path, index=False)


# ----------------------------------------------------------------------------
# 4) FORECAST 2026 PLOTS
# ----------------------------------------------------------------------------
print(f"\n--- 4) Menghasilkan fig_forecast_<UNIT>.png & plot_data_forecast_<UNIT>.csv ---")
for unit in target_units_to_plot:
    if not unit_validation_passed.get(unit, False):
        print(f"[SKIP] {unit} dilewati karena validasi gagal.")
        continue
        
    meta = unit_meta[unit]
    jenis = meta["JENIS"]
    variant = unit_results[unit]["variant"]
    
    # Ambil seluruh histori (train + test: Jan 2023 - Des 2025)
    hist_u = monthly_full[monthly_full["EQUIP NAME"] == unit].sort_values("TAHUN_BULAN")
    hist_periods = hist_u["TAHUN_BULAN"].tolist()
    hist_vals = hist_u["UTILITAS"].tolist()
    
    # Ambil peramalan 2026
    sub_fc = df_forecast_raw[df_forecast_raw["EQUIP NAME"] == unit].sort_values("TAHUN_BULAN")
    fc_periods = [pd.Period(str(p), "M") for p in sub_fc["TAHUN_BULAN"]]
    fc_col = "FORECAST_OPERATING_HOURS" if "FORECAST_OPERATING_HOURS" in sub_fc.columns else "FORECAST_UTILITAS"
    fc_vals = sub_fc[fc_col].tolist()
    
    # Pisahkan training (Jan 2023 - Sep 2025) dan test aktual (Okt - Des 2025)
    tr_p_list = [p for p in hist_periods if p <= pl.TRAIN_END]
    tr_v_list = [hist_vals[i] for i, p in enumerate(hist_periods) if p <= pl.TRAIN_END]
    
    # Sambungkan test aktual dari Sep 2025 ke Des 2025
    te_conn_p = [p for p in hist_periods if p >= pl.TRAIN_END]
    te_conn_v = [hist_vals[i] for i, p in enumerate(hist_periods) if p >= pl.TRAIN_END]
    
    # Titik jangkar Desember 2025 untuk garis peramalan
    fc_conn_p = [hist_periods[-1]] + fc_periods
    fc_conn_v = [hist_vals[-1]] + fc_vals
    
    all_p = hist_periods + fc_periods
    x_idx = {p: i for i, p in enumerate(all_p)}
    
    x_tr = [x_idx[p] for p in tr_p_list]
    x_te = [x_idx[p] for p in te_conn_p]
    x_fc = [x_idx[p] for p in fc_conn_p]
    
    fig, ax = plt.subplots(figsize=(10, 4.2))
    
    # 1) Aktual training: Jan 2023 s/d Sep 2025
    ax.plot(x_tr, tr_v_list, color=COLOR_TRAIN, linestyle="-", marker="o", markersize=4,
            linewidth=1.4, label="Aktual (training)")
    
    # 2) Aktual test: Sep 2025 s/d Des 2025 (titik jangkar Des 2025 digambar sebagai aktual test warna biru)
    ax.plot(x_te, te_conn_v, color=COLOR_TEST, linestyle="-", marker="o", markersize=5,
            linewidth=1.7, label="Aktual (test)")
    
    # 3) Peramalan 2026: garis putus-putus merah tersambung dari Des 2025 ke Jan 2026,
    #    tetapi penanda diamond hanya di 12 bulan peramalan (Jan 2026 s/d Des 2026)
    markevery_12m = list(range(1, len(x_fc)))
    ax.plot(x_fc, fc_conn_v, color=COLOR_FORECAST, linestyle="--", marker="D", markersize=5,
            markevery=markevery_12m, linewidth=1.8, label="Peramalan 2026")
    
    title_text = f"Peramalan Operating Hours 2026 — {unit} ({jenis})"
    sub_text = f"Varian Model: {variant} | Horizon: 12 Bulan (Jan 2026 – Des 2026)"
    ax.set_title(f"{title_text}\n{sub_text}", fontsize=11, pad=10)
    
    ax.set_xlabel("Bulan", fontsize=11, labelpad=10)
    ax.set_ylabel("Operating Hours (jam)", fontsize=11)
    
    y_min, y_max = get_safe_y_limit([hist_vals, fc_vals])
    ax.set_ylim(bottom=0.0, top=y_max)
    
    # Ticks sumbu X: tiap 4 bulan + Okt 2025 & Des 2025 + 2026, rotasi 45 derajat
    tick_locs = [x_idx[p] for p in TICK_PERIODS_48 if p in x_idx]
    tick_labels = [format_indo_month(p) for p in TICK_PERIODS_48 if p in x_idx]
    ax.set_xticks(tick_locs)
    ax.set_xticklabels(tick_labels, rotation=45, ha="right", fontsize=10)
    
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)
    
    # Legenda di luar area plot: di bawah, di tengah, 4 kolom
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.32), ncol=4,
              frameon=True, framealpha=0.9, edgecolor="#cccccc", fontsize=10.5)
    
    fig_path = OUTPUT_DIR / f"fig_forecast_{unit}.png"
    safe_savefig(fig, fig_path, bbox_inches="tight")
    plt.close(fig)
    print(f"  [OK] Disimpan: {fig_path.name}")
    
    # CSV plot data
    csv_rows = []
    for p, act in zip(hist_periods, hist_vals):
        set_name = "train" if p <= pl.TRAIN_END else "test"
        csv_rows.append({
            "TAHUN_BULAN": str(p),
            "BULAN_LABEL": format_indo_month(p),
            "PERIODE": set_name,
            "AKTUAL": round(act, 2),
            "PERAMALAN_2026": np.nan
        })
    for p, fc_v in zip(fc_periods, fc_vals):
        csv_rows.append({
            "TAHUN_BULAN": str(p),
            "BULAN_LABEL": format_indo_month(p),
            "PERIODE": "peramalan_2026",
            "AKTUAL": np.nan,
            "PERAMALAN_2026": round(fc_v, 2)
        })
    df_csv = pd.DataFrame(csv_rows)
    csv_path = OUTPUT_DIR / f"plot_data_forecast_{unit}.csv"
    df_csv.to_csv(csv_path, index=False)


# ----------------------------------------------------------------------------
# 2, 6, 7) PANEL PLOTS (HANYA JIKA DIMINTA SECARA EKSPLISIT DENGAN --all)
# ----------------------------------------------------------------------------
if generate_panels:
    print("\n--- 2) Menghasilkan fig_test_panel_10unit.png & plot_data_test_panel_10unit.csv ---")
    fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(12, 14), sharex=False, sharey=False)
    axes_flat = axes.flatten()
    panel_unit_csv_rows = []

    for idx, unit in enumerate(ALL_TARGET_UNITS):
        ax = axes_flat[idx]
        if not unit_validation_passed.get(unit, False):
            ax.text(0.5, 0.5, f"{unit}\nValidasi Gagal", ha="center", va="center")
            continue
            
        res = unit_results[unit]
        meta = unit_meta[unit]
        jenis = meta["JENIS"]
        variant = res["variant"]
        
        tr_periods = res["train_periods"]
        tr_actual = res["train_actual"]
        te_periods = res["test_periods"]
        te_actual = res["test_actual"]
        pred_d = res["pred_direct"]
        pred_r = res["pred_rolling"]
        
        conn_periods = [tr_periods[-1]] + te_periods
        conn_actual = [tr_actual[-1]] + te_actual
        conn_pred_d = [tr_actual[-1]] + pred_d
        conn_pred_r = [tr_actual[-1]] + pred_r
        
        all_periods = tr_periods + te_periods
        x_indices = {p: i for i, p in enumerate(all_periods)}
        
        x_tr = [x_indices[p] for p in tr_periods]
        x_conn = [x_indices[p] for p in conn_periods]
        
        line1, = ax.plot(x_tr, tr_actual, color=COLOR_TRAIN, linestyle="-", marker="o", markersize=3,
                         linewidth=1.2, label="Aktual (training)")
        line2, = ax.plot(x_conn, conn_actual, color=COLOR_TEST, linestyle="-", marker="o", markersize=3.5,
                         linewidth=1.4, label="Aktual (test)")
        line3, = ax.plot(x_conn, conn_pred_d, color=COLOR_DIRECT, linestyle="-", marker="s", markersize=3.5,
                         linewidth=1.4, label="Prediksi direct")
        line4, = ax.plot(x_conn, conn_pred_r, color=COLOR_ROLLING, linestyle="--", marker="^", markersize=3.5,
                         linewidth=1.4, label="Prediksi rolling")
        
        p_title = f"{unit} ({jenis})"
        p_sub = f"Varian: {variant} | Dir: {format_indo_number(res['mape_direct'])}% | Roll: {format_indo_number(res['mape_rolling'])}%"
        ax.set_title(f"{p_title} — {p_sub}", fontsize=10.5, pad=5)
        
        ax.set_xlabel("Bulan", fontsize=10)
        ax.set_ylabel("Operating Hours (jam)", fontsize=10)
        
        y_min, y_max = get_safe_y_limit([tr_actual, te_actual, pred_d, pred_r])
        ax.set_ylim(bottom=0.0, top=y_max)
        
        tick_locs = [x_indices[p] for p in TICK_PERIODS_36 if p in x_indices]
        tick_labels = [format_indo_month(p) for p in TICK_PERIODS_36 if p in x_indices]
        ax.set_xticks(tick_locs)
        ax.set_xticklabels(tick_labels, rotation=45, ha="right", fontsize=9.5)
        ax.tick_params(axis="y", labelsize=9.5)
        ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)
        
        for p, act in zip(tr_periods, tr_actual):
            panel_unit_csv_rows.append({
                "EQUIP_NAME": unit, "JENIS": jenis, "TAHUN_BULAN": str(p),
                "BULAN_LABEL": format_indo_month(p), "SET": "train",
                "AKTUAL": round(act, 2), "PRED_DIRECT": np.nan, "PRED_ROLLING": np.nan
            })
        for p, act, pd_val, pr_val in zip(te_periods, te_actual, pred_d, pred_r):
            panel_unit_csv_rows.append({
                "EQUIP_NAME": unit, "JENIS": jenis, "TAHUN_BULAN": str(p),
                "BULAN_LABEL": format_indo_month(p), "SET": "test",
                "AKTUAL": round(act, 2), "PRED_DIRECT": round(pd_val, 2), "PRED_ROLLING": round(pr_val, 2)
            })

    fig.legend(
        [line1, line2, line3, line4],
        ["Aktual (training)", "Aktual (test)", "Prediksi direct", "Prediksi rolling"],
        loc="upper center", ncol=4, bbox_to_anchor=(0.5, 0.995), framealpha=0.9, fontsize=11
    )
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    panel_path = OUTPUT_DIR / "fig_test_panel_10unit.png"
    safe_savefig(fig, panel_path, bbox_inches="tight")
    plt.close(fig)
    print(f"  [OK] Disimpan: {panel_path.name}")
    df_panel_u = pd.DataFrame(panel_unit_csv_rows)
    df_panel_u.to_csv(OUTPUT_DIR / "plot_data_test_panel_10unit.csv", index=False)

    print("\n--- 6) Menghasilkan fig_test_panel_5kriteria.png & plot_data_test_panel_5kriteria.csv ---")
    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(12, 14), sharex=False, sharey=False)
    axes_flat = axes.flatten()
    panel_krit_csv_rows = []

    for idx, kode in enumerate(ALL_TARGET_KRITERIA):
        ax = axes_flat[idx]
        if not kriteria_validation_passed.get(kode, False):
            ax.text(0.5, 0.5, f"Kriteria {kode}\nValidasi Gagal", ha="center", va="center")
            continue
            
        res = kriteria_results[kode]
        meta = kriteria_meta[kode]
        jenis = meta["JENIS"]
        merk = meta["TYPE/MERK"]
        cap = meta["CAP"]
        hp = meta["HP"]
        variant = res["variant"]
        
        tr_periods = res["train_periods"]
        tr_actual = res["train_actual_mean"]
        te_periods = res["test_periods"]
        te_actual = res["test_actual_mean"]
        pred_d = res["test_pred_d_mean"]
        pred_r = res["test_pred_r_mean"]
        
        conn_periods = [tr_periods[-1]] + te_periods
        conn_actual = [tr_actual[-1]] + te_actual
        conn_pred_d = [tr_actual[-1]] + pred_d
        
        all_periods = tr_periods + te_periods
        x_indices = {p: i for i, p in enumerate(all_periods)}
        
        x_tr = [x_indices[p] for p in tr_periods]
        x_conn = [x_indices[p] for p in conn_periods]
        
        line1, = ax.plot(x_tr, tr_actual, color=COLOR_TRAIN, linestyle="-", marker="o", markersize=3,
                         linewidth=1.2, label="Aktual (training)")
        line2, = ax.plot(x_conn, conn_actual, color=COLOR_TEST, linestyle="-", marker="o", markersize=3.5,
                         linewidth=1.4, label="Aktual (test)")
        line3, = ax.plot(x_conn, conn_pred_d, color=COLOR_DIRECT, linestyle="-", marker="s", markersize=3.5,
                         linewidth=1.4, label="Prediksi direct")
        
        p_title = format_kriteria_title(kode, jenis, merk, cap, hp).replace("Aktual vs Prediksi Operating Hours — ", "")
        p_sub = f"Varian: {variant} | MAPE = {format_indo_number(res['mape_direct'])}% | RMSE = {format_indo_number(res['rmse_direct'])} jam"
        ax.set_title(f"{p_title}\n{p_sub}", fontsize=10.5, pad=6)
        
        ax.set_xlabel("Bulan", fontsize=10)
        ax.set_ylabel("Operating Hours (jam)", fontsize=10)
        
        is_k09 = (kode == "K09")
        y_min, y_max = get_safe_y_limit([tr_actual, te_actual, pred_d], is_k09=is_k09)
        ax.set_ylim(bottom=0.0, top=y_max)
        
        tick_locs = [x_indices[p] for p in TICK_PERIODS_36 if p in x_indices]
        tick_labels = [format_indo_month(p) for p in TICK_PERIODS_36 if p in x_indices]
        ax.set_xticks(tick_locs)
        ax.set_xticklabels(tick_labels, rotation=45, ha="right", fontsize=9.5)
        ax.tick_params(axis="y", labelsize=9.5)
        ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)
        
        for p, act in zip(tr_periods, tr_actual):
            panel_krit_csv_rows.append({
                "KODE_KRITERIA": kode, "JENIS": jenis, "TYPE/MERK": merk,
                "CAP": cap, "HP": hp, "TAHUN_BULAN": str(p),
                "BULAN_LABEL": format_indo_month(p), "SET": "train",
                "AKTUAL_RATA_RATA": round(act, 2), "PRED_DIRECT_RATA_RATA": np.nan, "PRED_ROLLING_RATA_RATA": np.nan
            })
        for p, act, pd_val, pr_val in zip(te_periods, te_actual, pred_d, pred_r):
            panel_krit_csv_rows.append({
                "KODE_KRITERIA": kode, "JENIS": jenis, "TYPE/MERK": merk,
                "CAP": cap, "HP": hp, "TAHUN_BULAN": str(p),
                "BULAN_LABEL": format_indo_month(p), "SET": "test",
                "AKTUAL_RATA_RATA": round(act, 2), "PRED_DIRECT_RATA_RATA": round(pd_val, 2), "PRED_ROLLING_RATA_RATA": round(pr_val, 2)
            })

    axes_flat[5].set_visible(False)
    fig.legend(
        [line1, line2, line3],
        ["Aktual (training)", "Aktual (test)", "Prediksi direct"],
        loc="upper center", ncol=3, bbox_to_anchor=(0.5, 0.995), framealpha=0.9, fontsize=11
    )
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    panel_path = OUTPUT_DIR / "fig_test_panel_5kriteria.png"
    safe_savefig(fig, panel_path, bbox_inches="tight")
    plt.close(fig)
    print(f"  [OK] Disimpan: {panel_path.name}")
    df_panel_k = pd.DataFrame(panel_krit_csv_rows)
    df_panel_k.to_csv(OUTPUT_DIR / "plot_data_test_panel_5kriteria.csv", index=False)

    print("\n--- 7) Menghasilkan fig_forecast_panel_10unit.png & plot_data_forecast_panel_10unit.csv ---")
    fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(12, 14), sharex=False, sharey=False)
    axes_flat = axes.flatten()
    panel_fc_csv_rows = []

    for idx, unit in enumerate(ALL_TARGET_UNITS):
        ax = axes_flat[idx]
        if not unit_validation_passed.get(unit, False):
            ax.text(0.5, 0.5, f"{unit}\nValidasi Gagal", ha="center", va="center")
            continue
            
        meta = unit_meta[unit]
        jenis = meta["JENIS"]
        variant = unit_results[unit]["variant"]
        
        hist_u = monthly_full[monthly_full["EQUIP NAME"] == unit].sort_values("TAHUN_BULAN")
        hist_periods = hist_u["TAHUN_BULAN"].tolist()
        hist_vals = hist_u["UTILITAS"].tolist()
        
        sub_fc = df_forecast_raw[df_forecast_raw["EQUIP NAME"] == unit].sort_values("TAHUN_BULAN")
        fc_periods = [pd.Period(str(p), "M") for p in sub_fc["TAHUN_BULAN"]]
        fc_col = "FORECAST_OPERATING_HOURS" if "FORECAST_OPERATING_HOURS" in sub_fc.columns else "FORECAST_UTILITAS"
        fc_vals = sub_fc[fc_col].tolist()
        
        tr_p_list = [p for p in hist_periods if p <= pl.TRAIN_END]
        tr_v_list = [hist_vals[i] for i, p in enumerate(hist_periods) if p <= pl.TRAIN_END]
        
        te_conn_p = [p for p in hist_periods if p >= pl.TRAIN_END]
        te_conn_v = [hist_vals[i] for i, p in enumerate(hist_periods) if p >= pl.TRAIN_END]
        
        fc_conn_p = [hist_periods[-1]] + fc_periods
        fc_conn_v = [hist_vals[-1]] + fc_vals
        
        all_p = hist_periods + fc_periods
        x_idx = {p: i for i, p in enumerate(all_p)}
        
        x_tr = [x_idx[p] for p in tr_p_list]
        x_te = [x_idx[p] for p in te_conn_p]
        x_fc = [x_idx[p] for p in fc_conn_p]
        
        line1, = ax.plot(x_tr, tr_v_list, color=COLOR_TRAIN, linestyle="-", marker="o", markersize=2.5,
                         linewidth=1.2, label="Aktual (training)")
        line2, = ax.plot(x_te, te_conn_v, color=COLOR_TEST, linestyle="-", marker="o", markersize=3.5,
                         linewidth=1.4, label="Aktual (test)")
        markevery_12m = list(range(1, len(x_fc)))
        line3, = ax.plot(x_fc, fc_conn_v, color=COLOR_FORECAST, linestyle="--", marker="D", markersize=3.5,
                         markevery=markevery_12m, linewidth=1.4, label="Peramalan 2026")
        
        p_title = f"{unit} ({jenis})"
        p_sub = f"Varian: {variant} | Horizon: 12 Bulan"
        ax.set_title(f"{p_title} — {p_sub}", fontsize=10.5, pad=5)
        
        ax.set_xlabel("Bulan", fontsize=10)
        ax.set_ylabel("Operating Hours (jam)", fontsize=10)
        
        y_min, y_max = get_safe_y_limit([hist_vals, fc_vals])
        ax.set_ylim(bottom=0.0, top=y_max)
        
        tick_locs = [x_idx[p] for p in TICK_PERIODS_48 if p in x_idx]
        tick_labels = [format_indo_month(p) for p in TICK_PERIODS_48 if p in x_idx]
        ax.set_xticks(tick_locs)
        ax.set_xticklabels(tick_labels, rotation=45, ha="right", fontsize=9.5)
        ax.tick_params(axis="y", labelsize=9.5)
        ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)
        
        for p, act in zip(hist_periods, hist_vals):
            set_name = "train" if p <= pl.TRAIN_END else "test"
            panel_fc_csv_rows.append({
                "EQUIP_NAME": unit, "JENIS": jenis, "TAHUN_BULAN": str(p),
                "BULAN_LABEL": format_indo_month(p), "PERIODE": set_name,
                "AKTUAL": round(act, 2), "PERAMALAN_2026": np.nan
            })
        for p, fc_v in zip(fc_periods, fc_vals):
            panel_fc_csv_rows.append({
                "EQUIP_NAME": unit, "JENIS": jenis, "TAHUN_BULAN": str(p),
                "BULAN_LABEL": format_indo_month(p), "PERIODE": "peramalan_2026",
                "AKTUAL": np.nan, "PERAMALAN_2026": round(fc_v, 2)
            })

    fig.legend(
        [line1, line2, line3],
        ["Aktual (training)", "Aktual (test)", "Peramalan 2026"],
        loc="upper center", ncol=3, bbox_to_anchor=(0.5, 0.995), framealpha=0.9, fontsize=11
    )
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    panel_path = OUTPUT_DIR / "fig_forecast_panel_10unit.png"
    safe_savefig(fig, panel_path, bbox_inches="tight")
    plt.close(fig)
    print(f"  [OK] Disimpan: {panel_path.name}")
    df_panel_fc = pd.DataFrame(panel_fc_csv_rows)
    df_panel_fc.to_csv(OUTPUT_DIR / "plot_data_forecast_panel_10unit.csv", index=False)


# ============================================================================
# RINGKASAN AKHIR
# ============================================================================
print("\n" + "=" * 70)
print("SELURUH PROSES SELESAI DENGAN SUKSES!")
print("=" * 70)
