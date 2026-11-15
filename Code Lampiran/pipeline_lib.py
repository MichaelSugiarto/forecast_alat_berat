# -*- coding: utf-8 -*-
# pipeline_lib.py
# Modul ETL, persiapan data, dan peramalan rolling Gradient Boosting per unit.

import json
import re
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.preprocessing import PowerTransformer, RobustScaler

warnings.filterwarnings("ignore")

# Konfigurasi fitur dan daftar pengecualian unit non-operasional
N_LAGS = 3
FEAT_COLS = [f"lag_{i}" for i in range(1, N_LAGS + 1)] + ["CURAH_HUJAN", "VOLUME_CONTAINER"]
GB_KEYS = ["learning_rate", "max_iter", "max_depth", "min_samples_leaf"]

EXCLUDED_NON_OPERATIONAL_NAMES = {
    "RANDU", "TRONTON PK 215", "KALMAR 31", "L 8153 UO EX.L 9378 UN",
    "L 8435 US / S80", "L 8514 UK (EX.L 9635 US)", "KANTIL", "GAJAH TUNGGAL",
    "TOP LOADER BOSS", "KASUARI",
    "B 9220 BL", "L 8251 UO", "L 9067 UN", "L 8810 UQ", "KALMAR 22",
    "BERNARD BEAR", "WINDU", "KALMAR 7", "L 8985 UQ", "L 8796 UO (EX.L 9025 US)",
    "KALMAR 23", "ULIN", "CRANE LB 80T/LUCKY DOLPHIN", "PERKUTUT", "CENDET",
}

EXCLUDED_15_K_CODES = {
    "K01_UNIT_006", "K01_UNIT_142", "K01_UNIT_220", "K02_UNIT_187", "K03_UNIT_080",
    "K13_UNIT_021", "K19_UNIT_344", "K20_UNIT_091", "K21_UNIT_197", "K41_UNIT_185",
    "K52_UNIT_081", "K63_UNIT_339", "K66_UNIT_027", "K76_UNIT_301", "K78_UNIT_024",
}

EXCLUDED_15_OLD_CODES = {
    "UNIT_0006", "UNIT_0142", "UNIT_0220", "UNIT_0187", "UNIT_0080",
    "UNIT_0021", "UNIT_0344", "UNIT_0091", "UNIT_0197", "UNIT_0185",
    "UNIT_0081", "UNIT_0339", "UNIT_0027", "UNIT_0301", "UNIT_0024",
}

EXCLUDED_OLD_10_CODES = {
    "UNIT_0306", "UNIT_0336", "UNIT_0088", "UNIT_0134", "UNIT_0159",
    "UNIT_0166", "UNIT_0095", "UNIT_0037", "UNIT_0330", "UNIT_0096",
}

EXCLUDED_NON_OPERATIONAL_UNITS = EXCLUDED_OLD_10_CODES | EXCLUDED_15_OLD_CODES | EXCLUDED_15_K_CODES
EXCLUDED_OLD_CODES = EXCLUDED_OLD_10_CODES

MONTH_MAP = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
}
TARGET_CURRSTATE = {"FXD", "FAC", "STR", "MAS", "MTB", "FOB", "MXD", "MOB"}
PREFERRED_PREV = {
    "FXD": "All", "FAC": "All", "STR": "All", "MAS": "All",
    "MTB": "All", "FOB": "All", "MXD": "All", "MOB": "MTL",
}
VALID_CONTAINER_TYPES = {
    "10 CO", "10 DC", "20 CO", "20 DC", "20 FT", "20 HC", "20 IT", "20 OT", "20 RF", "20 RH", "20 RM",
    "21 DC", "40 CO", "40 DC", "40 FT", "40 HC", "40 IT", "40 OT", "40 RF", "40 RH", "40 RM", "41 DC", "45 HC",
}
MANUAL_OVERRIDE = {
    "TOP LOADER KALMAR 35 T/TOBATI": "TOBATI (EX.FL KALMAR 32T)",
    "L 9902 UR / S75": "L 8477 UUC (EX.L 9902 UR)",
    "TOP LOADER BOSS": "WIND RIVER (EX.TL BOSS 42T)",
}


# 1. ETL data mentah Excel (BBM, Container, Detail Alat Berat, Curah Hujan)
def _scan_bbm_unit_names(bbm_files):
    units = set()
    for yr, path in bbm_files.items():
        xls = pd.ExcelFile(path)
        for sh in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sh, header=[0, 1, 2], nrows=1)
            if df.empty:
                continue
            level0 = df.columns.get_level_values(0)
            for l0 in set(level0):
                if l0 == "EQUIP NAME":
                    continue
                subcols = set(df.columns[level0 == l0].get_level_values(2))
                if "HM" in subcols and "LITER" in subcols:
                    units.add(l0)
    return units


def _scan_container_branch_codes(container_files):
    branches = set()
    for yr, path in container_files.items():
        df = pd.read_excel(path, sheet_name=0, header=None)
        col0 = df.iloc[:, 0]
        starts = col0[col0 == "CURRSTATE"].index.tolist()
        for i, s in enumerate(starts):
            end = starts[i + 1] if i + 1 < len(starts) else len(df)
            data_start = s + 9
            block_col0 = df.iloc[data_start:end, 0]
            gt_idx = block_col0[block_col0 == "Grand Total"].index
            data_end = gt_idx[0] if len(gt_idx) > 0 else end
            branches.update(df.iloc[data_start:data_end, 0].dropna().unique().tolist())
    return branches


def _scan_cost_file_names_and_lokasi(cost_file):
    df = pd.read_excel(cost_file, sheet_name="Sheet2", header=1)
    names = set(df["NAMA ALAT BERAT"].dropna().unique().tolist())
    lokasi_col = [c for c in df.columns if str(c).strip().upper().startswith("DES")]
    lokasi_col = lokasi_col[-1] if lokasi_col else "DES 2025"
    lokasi = set(df[lokasi_col].dropna().unique().tolist())
    return names, lokasi, lokasi_col


def _process_bbm_sheet(excel_source, sheet, unit_map):
    df = pd.read_excel(excel_source, sheet_name=sheet, header=[0, 1, 2])
    if df.empty or df.shape[1] == 0:
        return None
    cols = df.columns
    level0 = cols.get_level_values(0)
    tgl_col = next((c for c in cols if c[2] == "TANGGAL"), None)
    if tgl_col is None:
        return None
    unit_cols = []
    for l0 in set(level0):
        if l0 == "EQUIP NAME":
            continue
        subcols = set(cols[level0 == l0].get_level_values(2))
        if "HM" in subcols and "LITER" in subcols:
            for c in cols[level0 == l0]:
                if c[2] in ("HM", "LITER"):
                    unit_cols.append(c)
    if not unit_cols:
        return None
    sub = df[[tgl_col] + unit_cols].copy()
    sub.columns = pd.MultiIndex.from_tuples([("__TANGGAL__", "", "")] + list(sub.columns[1:]))
    tgl_raw = sub[("__TANGGAL__", "", "")].astype(str)
    sub = sub[~tgl_raw.isin(["AVG", "TOTAL LTR/UTL", "nan"])]
    sub = sub.set_index(("__TANGGAL__", "", ""))
    sub.index.name = "TANGGAL"
    sub.columns = pd.MultiIndex.from_tuples([(c[0], c[2]) for c in sub.columns])
    long_df = sub.stack(level=0, future_stack=True).reset_index()
    long_df = long_df.rename(columns={"level_1": "EQUIP NAME"})
    long_df["EQUIP NAME"] = long_df["EQUIP NAME"].map(unit_map)
    return long_df


def _parse_container_file(path, branch_map):
    df = pd.read_excel(path, sheet_name=0, header=None)
    col0 = df.iloc[:, 0]
    starts = col0[col0 == "CURRSTATE"].index.tolist()
    monthly_totals = {m: 0.0 for m in range(1, 13)}
    for i, s in enumerate(starts):
        curr = df.iloc[s, 1]
        prev = df.iloc[s + 1, 1]
        if curr not in TARGET_CURRSTATE or prev != PREFERRED_PREV.get(curr):
            continue
        end = starts[i + 1] if i + 1 < len(starts) else len(df)
        month_row = df.iloc[s + 7, :].copy()
        type_row = df.iloc[s + 8, :]
        month_row.iloc[1:] = month_row.iloc[1:].ffill()
        data_start = s + 9
        block_col0 = df.iloc[data_start:end, 0]
        gt_idx = block_col0[block_col0 == "Grand Total"].index
        data_end = gt_idx[0] if len(gt_idx) > 0 else end
        branch_rows = df.iloc[data_start:data_end]
        for col_idx in range(1, df.shape[1]):
            mon = month_row.iloc[col_idx]
            typ = type_row.iloc[col_idx]
            if pd.isna(mon) or mon not in MONTH_MAP or typ not in VALID_CONTAINER_TYPES:
                continue
            vals = pd.to_numeric(branch_rows.iloc[:, col_idx], errors="coerce").fillna(0)
            monthly_totals[MONTH_MAP[mon]] += vals.sum()
    return monthly_totals


def _extract_after_ex(name):
    m = re.search(r"EX\.\s*([^)]+)\)", str(name), re.IGNORECASE)
    return m.group(1).strip() if m else None


def _extract_before_paren(name):
    name = str(name)
    return name.split("(")[0].strip() if "(" in name else None


def build_monthly_full(bbm_files, container_files, cost_file, rainfall_file, out_dir=None):
    # Menjalankan ETL penuh dari file Excel mentah menjadi data bulanan teragregasi per unit.
    out_dir = Path(out_dir) if out_dir else None

    bbm_units = _scan_bbm_unit_names(bbm_files)
    branch_codes = _scan_container_branch_codes(container_files)
    cost_names, cost_lokasi, lokasi_col = _scan_cost_file_names_and_lokasi(cost_file)

    all_unit_names = sorted(bbm_units | cost_names)
    unit_map = {name: f"UNIT_{i + 1:04d}" for i, name in enumerate(all_unit_names)}
    branch_map = {name: f"BRANCH_{i + 1:03d}" for i, name in enumerate(sorted(branch_codes))}
    lokasi_map = {name: f"LOC_{i + 1:03d}" for i, name in enumerate(sorted(cost_lokasi))}

    frames = []
    for yr, path in bbm_files.items():
        xls = pd.ExcelFile(path)
        for sh in xls.sheet_names:
            r = _process_bbm_sheet(xls, sh, unit_map)
            if r is not None:
                frames.append(r)
    raw_bbm = pd.concat(frames, ignore_index=True)

    raw_bbm["TANGGAL"] = pd.to_datetime(raw_bbm["TANGGAL"], format="%d-%m-%Y", errors="coerce")
    raw_bbm = raw_bbm.dropna(subset=["TANGGAL"])
    raw_bbm["HM_Clean"] = pd.to_numeric(raw_bbm["HM"], errors="coerce")
    raw_bbm["HM_Clean"] = raw_bbm["HM_Clean"].replace(0, np.nan)
    raw_bbm["HM_Clean"] = raw_bbm.groupby("EQUIP NAME")["HM_Clean"].ffill()
    raw_bbm["HM_Clean"] = raw_bbm["HM_Clean"].fillna(0)
    raw_bbm["DELTA_HM"] = raw_bbm.groupby("EQUIP NAME")["HM_Clean"].diff().fillna(0)
    raw_bbm.loc[raw_bbm["DELTA_HM"] < 0, "DELTA_HM"] = 0
    raw_bbm.loc[raw_bbm["DELTA_HM"] > 24, "DELTA_HM"] = 24
    raw_bbm["TAHUN_BULAN"] = raw_bbm["TANGGAL"].dt.to_period("M")
    monthly_hm = (
        raw_bbm.groupby(["EQUIP NAME", "TAHUN_BULAN"])["DELTA_HM"]
        .sum().round(1).reset_index().rename(columns={"DELTA_HM": "UTILITAS"})
    )

    container_monthly_frames = []
    for yr, path in container_files.items():
        totals = _parse_container_file(path, branch_map)
        for m, v in totals.items():
            container_monthly_frames.append({
                "TAHUN_BULAN": pd.Period(f"{yr}-{m:02d}", freq="M"),
                "VOLUME_CONTAINER": v,
            })
    monthly_container = pd.DataFrame(container_monthly_frames).sort_values("TAHUN_BULAN").reset_index(drop=True)

    rain = pd.read_excel(rainfall_file, header=3)
    rain = rain.rename(columns={"precipitation_sum (mm)": "precipitation_sum"})
    rain["time"] = pd.to_datetime(rain["time"])
    rain["TAHUN_BULAN"] = rain["time"].dt.to_period("M")
    monthly_rain = (
        rain.groupby("TAHUN_BULAN")["precipitation_sum"]
        .sum().round(1).reset_index().rename(columns={"precipitation_sum": "CURAH_HUJAN"})
    )

    monthly_full = monthly_hm.merge(monthly_rain, on="TAHUN_BULAN", how="left")
    monthly_full = monthly_full.merge(monthly_container, on="TAHUN_BULAN", how="left")

    # Populasi unit resmi berdasarkan data spesifikasi cost & bbm
    cost_df = pd.read_excel(cost_file, sheet_name="Sheet2", header=1)
    kriteria_raw = cost_df[["NAMA ALAT BERAT", lokasi_col, "ALAT BERAT", "TYPE/MERK", "CAP", "HP"]].copy()
    kriteria_raw = kriteria_raw.rename(columns={lokasi_col: "LOKASI_RAW", "ALAT BERAT": "JENIS"})

    unit_ids_with_data = set(monthly_hm["EQUIP NAME"].unique())
    alias_after_ex, alias_before_paren = {}, {}
    for full_name, uid in unit_map.items():
        if uid not in unit_ids_with_data:
            continue
        after = _extract_after_ex(full_name)
        if after:
            alias_after_ex.setdefault(after.upper(), full_name)
        before = _extract_before_paren(full_name)
        if before:
            alias_before_paren.setdefault(before.upper(), full_name)

    def resolve_to_data_bearing_unit(nama_cost):
        nama_cost = str(nama_cost).strip()
        uid = unit_map.get(nama_cost)
        if uid and uid in unit_ids_with_data:
            return nama_cost
        if nama_cost in MANUAL_OVERRIDE and unit_map.get(MANUAL_OVERRIDE[nama_cost]) in unit_ids_with_data:
            return MANUAL_OVERRIDE[nama_cost]
        upper = nama_cost.upper()
        if upper in alias_after_ex:
            return alias_after_ex[upper]
        if upper in alias_before_paren:
            return alias_before_paren[upper]
        return None

    kriteria_raw["NAMA_RESOLVED"] = kriteria_raw["NAMA ALAT BERAT"].apply(resolve_to_data_bearing_unit)
    kriteria_raw["EQUIP NAME"] = kriteria_raw["NAMA_RESOLVED"].map(unit_map)
    kriteria_raw["LOKASI"] = kriteria_raw["LOKASI_RAW"].map(lokasi_map)
    kriteria_raw = kriteria_raw.drop(columns=["NAMA ALAT BERAT", "LOKASI_RAW", "NAMA_RESOLVED"])
    kriteria_raw["KRITERIA_ID"] = kriteria_raw[["JENIS", "TYPE/MERK", "CAP", "HP"]].astype(str).agg("|".join, axis=1)
    kriteria = (
        kriteria_raw.dropna(subset=["EQUIP NAME"])
        .drop_duplicates(subset=["EQUIP NAME"]).reset_index(drop=True)
    )

    unit_resmi = set(kriteria["EQUIP NAME"])
    semua_unit_bbm = set(monthly_full["EQUIP NAME"].unique())
    inv_unit_map = {v: k for k, v in unit_map.items()}
    unit_dikecualikan = semua_unit_bbm - unit_resmi
    excluded_summary0 = pd.DataFrame([
        {"EQUIP NAME": u, "NAMA_ASLI": inv_unit_map.get(u, u)} for u in unit_dikecualikan
    ]).sort_values("NAMA_ASLI") if unit_dikecualikan else pd.DataFrame(columns=["EQUIP NAME", "NAMA_ASLI"])

    monthly_full = monthly_full[monthly_full["EQUIP NAME"].isin(unit_resmi)].reset_index(drop=True)

    # Filter unit non-operasional awal dan standardisasi penomoran ID unit
    old_codes_sorted = sorted(set(unit_map.values()), key=lambda c: int(c.split("_")[1]))
    remaining_old_codes = [c for c in old_codes_sorted if c not in EXCLUDED_OLD_CODES]
    remap_old_to_new = {old: f"UNIT_{i + 1:04d}" for i, old in enumerate(remaining_old_codes)}

    monthly_full = monthly_full[~monthly_full["EQUIP NAME"].isin(EXCLUDED_OLD_CODES)].copy()
    monthly_full["EQUIP NAME"] = monthly_full["EQUIP NAME"].map(remap_old_to_new)
    kriteria = kriteria[~kriteria["EQUIP NAME"].isin(EXCLUDED_OLD_CODES)].copy()
    kriteria["EQUIP NAME"] = kriteria["EQUIP NAME"].map(remap_old_to_new)
    unit_map_final = {name: remap_old_to_new[code] for name, code in unit_map.items() if code in remap_old_to_new}

    # Remap ke penamaan berbasis kriteria jika file mapping referensi tersedia
    ref_candidates = [
        Path("./checkpoints_v4/rev_h3/mapping_unit_dan_kriteria.xlsx"),
        Path("./checkpoints_v4/mapping_unit_dan_kriteria.xlsx"),
    ]
    ref_path = next((p for p in ref_candidates if p.exists()), None)
    if ref_path is not None:
        try:
            df_ref = pd.read_excel(ref_path, sheet_name="Mapping_Unit")
            old_to_k_unit = dict(zip(df_ref["EQUIP_NAME_LAMA"], df_ref["EQUIP_NAME_BARU"]))
            kriteria_code_map = dict(zip(df_ref["KRITERIA_ID"], df_ref["KODE_KRITERIA"]))
            monthly_full["EQUIP NAME"] = monthly_full["EQUIP NAME"].map(lambda u: old_to_k_unit.get(u, u))
            kriteria["EQUIP NAME"] = kriteria["EQUIP NAME"].map(lambda u: old_to_k_unit.get(u, u))
            if "KODE_KRITERIA" not in kriteria.columns:
                kriteria["KODE_KRITERIA"] = kriteria["KRITERIA_ID"].map(kriteria_code_map)
            unit_map_final = {name: old_to_k_unit.get(code, code) for name, code in unit_map_final.items()}
        except Exception:
            pass

    # Eliminasi 15 unit non-operasional tambahan dari seluruh keluaran ETL
    drop_mask_extra = (
        monthly_full["EQUIP NAME"].isin(EXCLUDED_15_K_CODES)
        | monthly_full["EQUIP NAME"].isin(EXCLUDED_15_OLD_CODES)
        | monthly_full["EQUIP NAME"].isin(EXCLUDED_NON_OPERATIONAL_NAMES)
    )
    monthly_full = monthly_full[~drop_mask_extra].reset_index(drop=True)
    drop_krit_extra = (
        kriteria["EQUIP NAME"].isin(EXCLUDED_15_K_CODES)
        | kriteria["EQUIP NAME"].isin(EXCLUDED_15_OLD_CODES)
        | kriteria["EQUIP NAME"].isin(EXCLUDED_NON_OPERATIONAL_NAMES)
    )
    kriteria = kriteria[~drop_krit_extra].reset_index(drop=True)
    unit_map_final = {
        name: code for name, code in unit_map_final.items()
        if code not in EXCLUDED_15_K_CODES and code not in EXCLUDED_15_OLD_CODES and name not in EXCLUDED_NON_OPERATIONAL_NAMES
    }

    if out_dir is not None:
        out_dir.mkdir(parents=True, exist_ok=True)
        monthly_full.to_csv(out_dir / "04_monthly_with_exog.csv", index=False)
        kriteria.to_csv(out_dir / "08_kriteria_unit.csv", index=False)
        with open(out_dir / "unit_map_v4.json", "w") as f:
            json.dump(unit_map_final, f, indent=2)

    return {
        "monthly_full": monthly_full,
        "kriteria": kriteria,
        "unit_map": unit_map_final,
        "excluded_cost_mismatch": excluded_summary0,
        "n_unit_bbm": len(semua_unit_bbm),
        "n_unit_resmi": len(unit_resmi),
    }


# 2. Varian pra-pemrosesan data
def _cap_smooth(df, value_col="UTILITAS", group_col="EQUIP NAME", upper_q=0.95, window=2):
    df = df.sort_values([group_col, "TAHUN_BULAN"]).copy()
    caps = df.groupby(group_col)[value_col].transform(lambda s: s.quantile(upper_q))
    df[value_col + "_CAPPED"] = df[value_col].clip(upper=caps).round(2)
    df[value_col + "_SMOOTH"] = (
        df.groupby(group_col)[value_col + "_CAPPED"]
        .transform(lambda s: s.rolling(window, min_periods=1).mean())
        .round(2)
    )
    return df


def prep_baseline(train_df, test_df, value_col="UTILITAS", group_col="EQUIP NAME",
                  upper_q=0.95, window=2):
    return (
        _cap_smooth(train_df, value_col, group_col, upper_q, window),
        _cap_smooth(test_df, value_col, group_col, upper_q, window),
        {},
    )


def prep_savgol(train_df, test_df, value_col="UTILITAS", group_col="EQUIP NAME",
                window=5, polyorder=2):
    def _smooth(df):
        df = df.sort_values([group_col, "TAHUN_BULAN"]).copy()

        def _calc_sg(series):
            y = series.values.astype(float)
            n = len(y)
            wl = min(window, n if n % 2 == 1 else n - 1)
            if wl < polyorder + 2 or wl < 3:
                return y
            return np.round(savgol_filter(y, window_length=wl, polyorder=polyorder), 2)

        df[value_col + "_SMOOTH"] = df.groupby(group_col)[value_col].transform(_calc_sg)
        return df

    return _smooth(train_df), _smooth(test_df), {}


def _prep_scaler_generic(train_df, test_df, scaler_cls, value_col="UTILITAS", group_col="EQUIP NAME"):
    tr = train_df.sort_values([group_col, "TAHUN_BULAN"]).copy()
    te = test_df.sort_values([group_col, "TAHUN_BULAN"]).copy()
    tr[value_col + "_SMOOTH"] = np.nan
    te[value_col + "_SMOOTH"] = np.nan
    transformers = {}
    for unit in tr[group_col].unique():
        tr_mask = tr[group_col] == unit
        te_mask = te[group_col] == unit
        vals = tr.loc[tr_mask, value_col].values.reshape(-1, 1)
        if len(vals) < 2 or np.std(vals) == 0:
            tr.loc[tr_mask, value_col + "_SMOOTH"] = tr.loc[tr_mask, value_col]
            te.loc[te_mask, value_col + "_SMOOTH"] = te.loc[te_mask, value_col]
            continue
        scaler = scaler_cls()
        tr_scaled = scaler.fit_transform(vals).flatten()
        tr.loc[tr_mask, value_col + "_SMOOTH"] = tr_scaled
        transformers[unit] = scaler
        if te_mask.any():
            te_vals = te.loc[te_mask, value_col].values.reshape(-1, 1)
            te.loc[te_mask, value_col + "_SMOOTH"] = scaler.transform(te_vals).flatten()
    return tr, te, transformers


def prep_robust(train_df, test_df, value_col="UTILITAS", group_col="EQUIP NAME"):
    return _prep_scaler_generic(train_df, test_df, RobustScaler, value_col, group_col)


def prep_yeojohnson(train_df, test_df, value_col="UTILITAS", group_col="EQUIP NAME"):
    def _pt():
        return PowerTransformer(method="yeo-johnson")

    return _prep_scaler_generic(train_df, test_df, _pt, value_col, group_col)


DATA_PREP_VARIANTS = {
    "baseline": prep_baseline,
    "savgol": prep_savgol,
    "robust": prep_robust,
    "yeojohnson": prep_yeojohnson,
}


def inverse_transform_pred(pred_array, unit, transformers):
    if not transformers or unit not in transformers:
        return np.asarray(pred_array, dtype=float)
    scaler = transformers[unit]
    return scaler.inverse_transform(np.asarray(pred_array, dtype=float).reshape(-1, 1)).flatten()


# 3. Pembentukan fitur lag dan peramalan rolling
def make_lag_features(df, value_col="UTILITAS_SMOOTH", n_lags=N_LAGS):
    df = df.sort_values(["EQUIP NAME", "TAHUN_BULAN"]).copy()
    for lag in range(1, n_lags + 1):
        df[f"lag_{lag}"] = df.groupby("EQUIP NAME")[value_col].shift(lag)
    return df


def clean_gb_params(row, prefix="V4_GB_"):
    # Mengambil dan membersihkan hyperparameter Gradient Boosting dari satu baris konfigurasi.
    params = {}
    for k in GB_KEYS:
        v = row.get(f"{prefix}{k}")
        if v is None or (isinstance(v, float) and np.isnan(v)):
            params[k] = None
            continue
        if k == "max_depth" and (v == "None" or pd.isna(v)):
            params[k] = None
            continue
        if isinstance(v, str):
            v = None if v == "None" else float(v)
        if v is not None and k in ("max_iter", "min_samples_leaf"):
            v = int(v)
        if v is not None and k == "max_depth":
            v = int(v)
        params[k] = v
    return params


def forecast_gb_rolling(model, last_lags, exog_future):
    # Melakukan peramalan rolling/rekursif menggunakan prediksi bulan sebelumnya sebagai lag bulan berikutnya.
    lags = list(last_lags)
    preds = []
    for row_exog in exog_future:
        feat = np.array([lags[0], lags[1], lags[2], row_exog[0], row_exog[1]]).reshape(1, -1)
        pred = model.predict(feat)[0]
        preds.append(pred)
        lags = [pred, lags[0], lags[1]]
    return np.array(preds)


# 4. Retrain penuh dan peramalan ke depan
def estimate_future_exog(monthly_full, horizon=12):
    # Estimasi CURAH_HUJAN dan VOLUME_CONTAINER ke depan menggunakan rata-rata musiman per bulan kalender.
    exog_monthly = monthly_full.groupby("TAHUN_BULAN")[["CURAH_HUJAN", "VOLUME_CONTAINER"]].first()
    exog_monthly_bulan = exog_monthly.copy()
    exog_monthly_bulan["BULAN_KALENDER"] = exog_monthly_bulan.index.map(lambda p: p.month)
    exog_seasonal_avg = exog_monthly_bulan.groupby("BULAN_KALENDER")[["CURAH_HUJAN", "VOLUME_CONTAINER"]].mean()

    last_period = monthly_full["TAHUN_BULAN"].max()
    future_periods = pd.period_range(last_period + 1, periods=horizon, freq="M")
    exog_future_df = pd.DataFrame({
        "TAHUN_BULAN": future_periods,
        "BULAN_KALENDER": [p.month for p in future_periods],
    }).merge(exog_seasonal_avg.reset_index(), on="BULAN_KALENDER", how="left")
    return exog_future_df[["TAHUN_BULAN", "CURAH_HUJAN", "VOLUME_CONTAINER"]]


def _fit_gb_on_full_history(g_full, variant, params):
    # Melatih ulang model Gradient Boosting pada seluruh histori satu unit.
    if len(g_full) < 6:
        return None, None
    prep_fn = DATA_PREP_VARIANTS[variant]
    # Kirim g_full sebagai placeholder test_df agar kolom grup tidak hilang pada operasi groupby
    g_prepped, _, transformers = prep_fn(g_full, g_full)
    g_lag = make_lag_features(g_prepped)
    g_lag_valid = g_lag.dropna(subset=FEAT_COLS + ["UTILITAS_SMOOTH"])
    if len(g_lag_valid) < 6:
        return None, None
    model = HistGradientBoostingRegressor(random_state=42, **params)
    model.fit(g_lag_valid[FEAT_COLS], g_lag_valid["UTILITAS_SMOOTH"])
    return model, (g_lag, transformers)


def retrain_and_forecast_unit(monthly_full, row, exog_future_df, horizon=12):
    # Retrain Gradient Boosting dengan histori penuh satu unit lalu hasilkan forecast rolling ke depan.
    unit = row["EQUIP NAME"]
    variant = row["V4_GB_VARIAN"]
    if pd.isna(variant):
        return None
    params = clean_gb_params(row)
    g_full = monthly_full[monthly_full["EQUIP NAME"] == unit].sort_values("TAHUN_BULAN").copy()

    model, extra = _fit_gb_on_full_history(g_full, variant, params)
    if model is None:
        return None
    g_lag, transformers = extra

    last_row = g_lag.iloc[-1]
    last_lags = [last_row["lag_1"], last_row["lag_2"], last_row["lag_3"]]
    if any(pd.isna(last_lags)):
        return None

    exog_h = exog_future_df.head(horizon)[["CURAH_HUJAN", "VOLUME_CONTAINER"]].values
    pred_smooth = forecast_gb_rolling(model, last_lags, exog_h)
    pred_real = inverse_transform_pred(pred_smooth, unit, transformers)
    pred_real = np.clip(pred_real, 0.0, 744.0).round(2)

    return pd.DataFrame({
        "EQUIP NAME": unit,
        "TAHUN_BULAN": exog_future_df.head(horizon)["TAHUN_BULAN"].values,
        "HORIZON_BULAN_KE": range(1, horizon + 1),
        "FORECAST_OPERATING_HOURS": pred_real,
        "FORECAST_UTILITAS": pred_real,
        "VARIAN": variant,
    })


# 5. Loader konfigurasi model final dan daftar pengecualian unit
def load_final_config(checkpoint_dir, level="unit"):
    # Memuat konfigurasi varian dan hyperparameter Gradient Boosting final dari checkpoint.
    sheet = "Per_Unit" if level == "unit" else "Per_Kriteria"
    chk = Path(checkpoint_dir)
    p_revisi = chk / "forcedgb_vs_v2b_comparison_190unit.xlsx"
    if p_revisi.exists():
        return pd.read_excel(p_revisi, sheet_name=sheet)
    path = chk / "v4_forcedgb_vs_v2b_comparison.xlsx"
    if not path.exists() and (chk.parent / "h3bulan" / path.name).exists():
        path = chk.parent / "h3bulan" / path.name
    return pd.read_excel(path, sheet_name=sheet)


REASON_MAP = {
    "nol total di salah satu tahun train": "Data operating hours pada salah satu tahun periode data train bernilai nol semua",
    "Nol total di salah satu tahun train": "Data operating hours pada salah satu tahun periode data train bernilai nol semua",
    "test bernilai nol seluruhnya": "Data operating hours pada periode data test bernilai nol semua",
    "Test bernilai nol seluruhnya": "Data operating hours pada periode data test bernilai nol semua",
}


def load_excluded_summary(checkpoint_dir):
    # Memuat daftar unit yang dikecualikan karena ketidaklayakan data historis.
    chk = Path(checkpoint_dir)
    p_revisi = chk / "unit_excluded_revisi_summary.xlsx"
    if p_revisi.exists():
        df = pd.read_excel(p_revisi)
        if "ALASAN" in df.columns:
            df = df[~df["ALASAN"].astype(str).str.contains("review MAPE|data baru|threshold|toleransi", case=False, na=False)].reset_index(drop=True)
            df["ALASAN"] = (
                df["ALASAN"].astype(str).str.strip()
                .map(lambda s: REASON_MAP.get(s, s))
                .str.replace("utilitas", "operating hours", case=False)
            )
        return df[["EQUIP NAME", "ALASAN"]]

    path = chk / "future_forecast" / "v4_unit_excluded_summary.xlsx"
    if not path.exists() and (chk.parent / "h3bulan" / "future_forecast" / path.name).exists():
        path = chk.parent / "h3bulan" / "future_forecast" / path.name
    if path.exists():
        df = pd.read_excel(path)
        df = df[~df["ALASAN"].astype(str).str.contains("review MAPE|data baru|threshold|toleransi", case=False, na=False)].reset_index(drop=True)
        df["ALASAN"] = (
            df["ALASAN"].astype(str).str.strip()
            .map(lambda s: REASON_MAP.get(s, s[0].upper() + s[1:] if len(s) > 0 else s))
            .str.replace("utilitas", "operating hours", case=False)
        )
        return df[["EQUIP NAME", "ALASAN"]]
    return pd.DataFrame(columns=["EQUIP NAME", "ALASAN"])
